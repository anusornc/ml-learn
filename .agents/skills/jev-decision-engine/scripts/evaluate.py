#!/usr/bin/env python3
"""
CLI tool for Jev Model (typesafe/jev-1.13) Decision Engine.
Supports live API execution as well as simulated mock mode.
"""

import os
import sys
import json
import time
import argparse
import urllib.request
import urllib.error

PRESETS = {
    "guard": {
        "description": "Evaluate safety, risk level, and human approval needed for tool/command execution.",
        "questions": {
            "risk_level": {
                "type": "choice",
                "instructions": "Evaluate the risk level of executing this action/command.",
                "criteria": {
                    "safe": "Read-only or harmless operation",
                    "medium": "Modifies temporary files or non-critical state",
                    "critical": "Irreversible deletion, service restart, or database modification"
                }
            },
            "requires_human_approval": {
                "type": "noul",
                "instructions": "Does this action strictly require human operator confirmation before running?",
                "criteria": {
                    "true": "High risk, production impact, or destructive action",
                    "false": "Can be executed automatically"
                }
            },
            "reversibility": {
                "type": "score",
                "instructions": "Rate reversibility of the action (0=Irreversible, 1=Partially reversible, 2=Fully reversible).",
                "criteria": [
                    "Irreversible (permanent data loss or downtime)",
                    "Partially reversible with significant manual effort",
                    "Fully reversible with no data loss"
                ]
            }
        }
    },
    "router": {
        "description": "Route intent and choose optimal model or execution pathway.",
        "questions": {
            "category": {
                "type": "choice",
                "instructions": "Classify the primary category of this task or query.",
                "criteria": {
                    "simple_qa": "Factual question or greeting requiring fast lightweight model",
                    "code_or_data": "Programming, database, or mathematical computation",
                    "deep_reasoning": "Complex architectural design, proof, or multi-step logic"
                }
            },
            "requires_tools": {
                "type": "noul",
                "instructions": "Does completing this task require external tools (filesystem, terminal, search)?"
            }
        }
    },
    "triage": {
        "description": "Triage customer support or incident tickets by urgency and intent.",
        "questions": {
            "intent": {
                "type": "choice",
                "instructions": "Identify the core customer intent.",
                "criteria": {
                    "refund": "Requesting money back or disputing charges",
                    "technical_bug": "Reporting broken feature or error",
                    "inquiry": "General product or pricing question",
                    "cancellation": "Requesting subscription termination"
                }
            },
            "urgency": {
                "type": "score",
                "instructions": "Rate urgency level (0=low, 1=medium, 2=critical/angry).",
                "criteria": [
                    "Low: polite question or general feedback",
                    "Medium: noticeable dissatisfaction or minor blockage",
                    "Critical: revenue loss, demanding immediate refund, or legal threat"
                ]
            },
            "needs_human": {
                "type": "noul",
                "instructions": "Does this case require human agent intervention?",
                "criteria": {
                    "true": "Requires manual financial or managerial discretion",
                    "false": "Can be automated by workflow"
                }
            }
        }
    },
    "moderation": {
        "description": "Detect prohibited content, counterfeit goods, or dangerous claims.",
        "questions": {
            "violation_type": {
                "type": "choice",
                "instructions": "Identify policy violation category.",
                "criteria": {
                    "medical_claims": "Unverified medical or miracle weight-loss claims without approval",
                    "counterfeit": "Fake or pirated branded goods",
                    "prohibited": "Weapons, narcotics, or illegal substances",
                    "clean": "Complies with standard guidelines"
                }
            },
            "auto_ban": {
                "type": "noul",
                "instructions": "Should this listing/content be immediately taken down?"
            }
        }
    },
    "pruning": {
        "description": "Decide whether to keep, summarize, or discard tool history blocks in agent context.",
        "questions": {
            "retention": {
                "type": "choice",
                "instructions": "How should this history block be handled for next prompt context?",
                "criteria": {
                    "drop": "Discard entirely, irrelevant redundant logs",
                    "summarize": "Drop repetitive tracebacks, keep only final result/status",
                    "keep_verbatim": "Keep entire verbatim output for exact reference"
                }
            }
        }
    }
}


def build_mock_response(questions, state="", elapsed_ms=110):
    state_lower = (state or "").lower()
    answers = {}

    for q_id, q_data in questions.items():
        q_type = q_data.get("type", "choice")
        if q_type == "choice":
            criteria = q_data.get("criteria", {})
            keys = list(criteria.keys()) if isinstance(criteria, dict) else ["opt_a", "opt_b"]
            
            # Content-aware choice selection
            chosen = keys[0] if keys else "default"
            if "risk" in q_id:
                if any(w in state_lower for w in ["rm ", "drop ", "restart", "delete", "kill", "format", "shutdown"]):
                    chosen = "critical" if "critical" in keys else keys[-1]
                else:
                    chosen = "safe" if "safe" in keys else keys[0]
            elif "intent" in q_id:
                if any(w in state_lower for w in ["refund", "money back", "คืนเงิน", "charged twice"]):
                    chosen = "refund" if "refund" in keys else keys[0]
                elif any(w in state_lower for w in ["cancel", "ยกเลิก"]):
                    chosen = "cancellation" if "cancellation" in keys else keys[0]
                elif any(w in state_lower for w in ["bug", "error", "fail", "พัง", "เสีย"]):
                    chosen = "technical_bug" if "technical_bug" in keys else keys[0]
            elif "category" in q_id or "model" in q_id or "tier" in q_id:
                if any(w in state_lower for w in ["hft", "memory pool", "lock-free", "concurrency", "c++", "low-level", "deep reasoning", "architecture", "frontier", "large"]):
                    chosen = "frontier_pro" if "frontier_pro" in keys else ("deep_reasoning" if "deep_reasoning" in keys else keys[-1])
                elif any(w in state_lower for w in ["rust", "python", "sql", "code", "database", "api"]):
                    chosen = "code_or_data" if "code_or_data" in keys else keys[0]
                else:
                    chosen = keys[0]
            elif "retention" in q_id:
                if any(w in state_lower for w in ["traceback", "failed", "repeat", "ขยะ", "log"]):
                    chosen = "summarize" if "summarize" in keys else keys[0]

            probs = {}
            for k in keys:
                probs[k] = 0.94 if k == chosen else round(0.06 / max(1, len(keys) - 1), 2)
            answers[q_id] = {
                "choice": chosen,
                "confidence": 0.94,
                "probabilities": probs
            }
        elif q_type == "score":
            criteria = q_data.get("criteria", [])
            count = len(criteria) if isinstance(criteria, list) else 3

            # Content-aware scoring
            score_val = 0.0
            if "complexity" in q_id or "difficulty" in q_id:
                if any(w in state_lower for w in ["hft", "memory pool", "lock-free", "concurrency", "c++", "kernel", "assembly"]):
                    score_val = float(count - 1)  # Maximum complexity
                elif any(w in state_lower for w in ["crud", "simple", "greeting", "format"]):
                    score_val = 0.0
                else:
                    score_val = 1.0
            elif "urgency" in q_id or "risk" in q_id:
                if any(w in state_lower for w in ["immediately", "now", "sue", "ด่วน", "วิกฤต", "crash", "oom", "500"]):
                    score_val = float(count - 1)
                elif any(w in state_lower for w in ["warn", "slow", "ช้า"]):
                    score_val = float(min(1, count - 1))
            elif "reversibility" in q_id:
                if any(w in state_lower for w in ["rm ", "drop ", "truncate"]):
                    score_val = 0.0  # Irreversible
                else:
                    score_val = float(count - 1)

            idx = min(int(round(score_val)), count - 1)
            probs = [0.88 if i == idx else round(0.12 / max(1, count - 1), 2) for i in range(count)]
            answers[q_id] = {
                "score": score_val,
                "confidence": 0.88,
                "probabilities": probs,
                "legend": criteria[idx] if isinstance(criteria, list) and idx < len(criteria) else f"Level {idx}"
            }
        elif q_type == "noul":
            prob = 0.50
            if any(w in state_lower for w in ["hft", "memory pool", "lock-free", "c++", "rm ", "drop ", "sue", "refund", "crash", "oom", "human", "danger", "urgent"]):
                prob = 0.97
            elif any(w in state_lower for w in ["ls", "cat", "hello", "greeting", "safe", "simple"]):
                prob = 0.03
            else:
                prob = 0.85
            answers[q_id] = {
                "noul": prob
            }

    return {
        "model": "typesafe/jev-1.13",
        "mock": True,
        "result": {
            "answers": answers
        },
        "elapsed_ms": elapsed_ms
    }


def parse_criteria_kv(raw_str):
    criteria = {}
    for item in raw_str.split(","):
        if "=" in item:
            k, v = item.split("=", 1)
            criteria[k.strip()] = v.strip()
        else:
            item = item.strip()
            if item:
                criteria[item] = item
    return criteria


def run_evaluation():
    parser = argparse.ArgumentParser(description="Jev Decision Engine CLI")
    parser.add_argument("--state", "-s", type=str, help="State context string or text to evaluate")
    parser.add_argument("--preset", "-p", choices=list(PRESETS.keys()), help="Use a predefined question preset")
    parser.add_argument("--choice", action="append", help="Define a choice question: 'id:opt1=desc,opt2=desc'")
    parser.add_argument("--score", action="append", help="Define a score question: 'id:level0_desc,level1_desc,level2_desc'")
    parser.add_argument("--noul", action="append", help="Define a noul question: 'id=instructions'")
    parser.add_argument("--json-input", "-j", type=str, help="Path to JSON file containing full payload or pass '-' for stdin")
    parser.add_argument("--api-key", type=str, default=os.environ.get("JEV_API_KEY"), help="Jev AI API Key")
    parser.add_argument("--endpoint", type=str, default=os.environ.get("JEV_API_ENDPOINT", "https://www.jevai.org/api/v1/decisions"), help="Jev Decision API URL")
    parser.add_argument("--mock", action="store_true", help="Force mock mode without network request")
    parser.add_argument("--raw", action="store_true", help="Output raw JSON response only")

    args = parser.parse_args()

    # Determine payload
    payload = None
    if args.json_input:
        if args.json_input == "-":
            payload = json.load(sys.stdin)
        else:
            with open(args.json_input, "r", encoding="utf-8") as f:
                payload = json.load(f)
    else:
        if not args.state:
            print("❌ Error: --state or --json-input is required.", file=sys.stderr)
            parser.print_help()
            sys.exit(1)

        questions = {}
        if args.preset:
            questions.update(PRESETS[args.preset]["questions"])

        if args.choice:
            for item in args.choice:
                if ":" in item:
                    q_id, raw_c = item.split(":", 1)
                    questions[q_id.strip()] = {
                        "type": "choice",
                        "instructions": f"Choose best option for {q_id.strip()}",
                        "criteria": parse_criteria_kv(raw_c)
                    }

        if args.score:
            for item in args.score:
                if ":" in item:
                    q_id, raw_c = item.split(":", 1)
                    crit_list = [c.strip() for c in raw_c.split(",") if c.strip()]
                    questions[q_id.strip()] = {
                        "type": "score",
                        "instructions": f"Score {q_id.strip()}",
                        "criteria": crit_list
                    }

        if args.noul:
            for item in args.noul:
                if "=" in item:
                    q_id, instr = item.split("=", 1)
                    questions[q_id.strip()] = {
                        "type": "noul",
                        "instructions": instr.strip()
                    }
                else:
                    questions[item.strip()] = {
                        "type": "noul",
                        "instructions": f"Is {item.strip()} true?"
                    }

        if not questions:
            print("❌ Error: At least one question (--preset, --choice, --score, --noul) is required.", file=sys.stderr)
            sys.exit(1)

        payload = {
            "model": "typesafe/jev-1.13",
            "state": args.state,
            "questions": questions
        }

    # Execute
    start_time = time.time()
    api_key = args.api_key

    if args.mock or not api_key:
        time.sleep(0.08)  # simulate ~80ms System 1 inference
        elapsed_ms = round((time.time() - start_time) * 1000)
        data = build_mock_response(payload.get("questions", {}), state=payload.get("state", ""), elapsed_ms=elapsed_ms)
    else:
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        req_data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(args.endpoint, data=req_data, headers=headers, method="POST")

        try:
            with urllib.request.urlopen(req, timeout=15) as response:
                elapsed_ms = round((time.time() - start_time) * 1000)
                res_body = response.read().decode("utf-8")
                data = json.loads(res_body)
                data["elapsed_ms"] = elapsed_ms
                data["mock"] = False
        except urllib.error.HTTPError as e:
            err_body = e.read().decode("utf-8", errors="ignore")
            print(f"❌ HTTP Error {e.code}: {err_body}", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f"❌ Connection Error: {e}", file=sys.stderr)
            sys.exit(1)

    # Output
    if args.raw:
        print(json.dumps(data, indent=2, ensure_ascii=False))
    else:
        answers = data.get("result", {}).get("answers", {})
        mode_str = "Mock Demo" if data.get("mock") else "Live API"
        print(f"\n⚡ [Jev Decision Engine] Latency: {data.get('elapsed_ms')} ms ({mode_str})")
        print("-" * 55)
        for q_id, ans in answers.items():
            if "choice" in ans:
                conf = ans.get("confidence", 0) * 100
                print(f"• [Choice] {q_id:20}: {ans['choice']} (Confidence: {conf:.1f}%)")
            elif "score" in ans:
                legend = f" - {ans.get('legend')}" if ans.get('legend') else ""
                print(f"• [Score]  {q_id:20}: {ans['score']}{legend}")
            elif "noul" in ans:
                prob = ans.get("noul", 0) * 100
                print(f"• [Noul]   {q_id:20}: {prob:.1f}% probability of YES")
        print("-" * 55)
        print("Raw JSON available with --raw flag.\n")


if __name__ == "__main__":
    run_evaluation()
