---
name: jev-decision-engine
description: >-
  Ultra-fast System 1 structured decision-making engine powered by Jev Model (typesafe/jev-1.13).
  Use this skill when you need sub-150ms type-safe decisions without verbose prose, including:
  (1) Pre-execution tool guardrails before running risky bash/database commands,
  (2) Fast intent routing and task classification,
  (3) Urgency/severity scoring,
  (4) Binary decision verification with calibrated probabilities (needs human approval, fraud detection, auto-rollback), or
  (5) Agent context pruning and history compaction.
---

# Jev Decision Engine (System 1 AI)

This skill equips the agent with a **System 1 Decision Engine** powered by `typesafe/jev-1.13`. It provides instant (~100ms), zero-prose, type-safe decision making across three primitives: **Choice**, **Score**, and **Noul**.

---

## When to Use This Skill

1. **Tool-Call Guardrails (Safety Check):** Before running destructive commands (`rm`, `drop`, `kill`, `git reset --hard`).
2. **Fast Intent Routing:** Categorizing user requests into workflows before calling heavy System 2 LLMs.
3. **Urgency & Severity Triage:** Rating tickets, alerts, or bugs on an ordinal scale.
4. **Binary Assertion & Approval:** Deciding if human confirmation is required (`noul >= 0.85`).
5. **Context Compaction:** Deciding whether to drop, summarize, or keep verbose tool outputs.

---

## Quick Start CLI Usage

The helper script is located at [evaluate.py](./scripts/evaluate.py).

### 1. Using Predefined Presets

Available presets: `guard`, `router`, `triage`, `moderation`, `pruning`.

```bash
# Evaluate risk of a terminal command
python3 .agents/skills/jev-decision-engine/scripts/evaluate.py \
  --preset guard \
  --state "Command: 'rm -rf /var/log/app/*' on production server"

# Classify customer support urgency
python3 .agents/skills/jev-decision-engine/scripts/evaluate.py \
  --preset triage \
  --state "Customer: 'Double charged $49 on invoice #9821, refund immediately!'"
```

### 2. Custom Multi-Primitive Evaluation

You can specify custom questions directly via flags:

```bash
python3 .agents/skills/jev-decision-engine/scripts/evaluate.py \
  --state "User request: 'Can you help me reset my account password?'" \
  --choice "category:auth=Authentication and login,billing=Invoices and payments,general=General inquiry" \
  --noul "needs_human=Does this require human agent verification?" \
  --score "urgency:Low,Medium,High"
```

### 3. Raw JSON Output for Scripting

Add `--raw` to get machine-readable JSON:

```bash
python3 .agents/skills/jev-decision-engine/scripts/evaluate.py \
  --preset guard \
  --state "Command: 'ls -la'" \
  --raw
```

---

## The 3 Typed Decision Primitives

For in-depth details on each primitive, see [primitives.md](./references/primitives.md).

| Primitive | Return Value | Typical Use Case |
| :--- | :--- | :--- |
| **`choice`** | Option key + probability distribution + confidence | Routing, multi-class categorization |
| **`score`** | Weighted float score (0 to N) + legend | Severity level, urgency, reversibility |
| **`noul`** | Calibrated probability of True/Yes (0.0 to 1.0) | Human-in-the-loop gate, risk check |

---

## Agent Decision Rule (Thresholds)

When interpreting `noul` probabilities from Jev:
- **`noul >= 0.85`:** **High Risk / Confirmation Required.** Stop and prompt the user for approval.
- **`0.40 <= noul < 0.85`:** **Ambiguous.** Fallback to standard reasoning or clarify with the user.
- **`noul < 0.40`:** **Safe.** Proceed with automatic unattended execution.
