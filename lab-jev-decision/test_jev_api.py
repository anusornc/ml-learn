#!/usr/bin/env python3
"""
Test script for Jev Model (typesafe/jev-1.13) Decision API
Usage:
    export JEV_API_KEY="your_api_key_here"
    python test_jev_api.py
"""

import os
import sys
import json
import time
import urllib.request
import urllib.error

def run_test():
    api_key = os.environ.get("JEV_API_KEY")
    if not api_key:
        print("❌ Error: JEV_API_KEY environment variable not set.")
        print("Please run: export JEV_API_KEY=\"your_key_here\"")
        print("\nOr you can enter your key now:")
        try:
            api_key = input("Enter JEV_API_KEY: ").strip()
        except (KeyboardInterrupt, EOFError):
            sys.exit(1)
        if not api_key:
            print("No key provided. Exiting.")
            sys.exit(1)

    url = "https://www.jevai.org/api/v1/decisions"
    
    # Example payload: Customer support triage
    payload = {
        "model": "typesafe/jev-1.13",
        "state": "Customer: 'I was charged twice for invoice #INV-9821 on Sept 18. Please refund the extra $49 immediately!'",
        "questions": {
            "intent": {
                "type": "choice",
                "instructions": "Identify the primary customer intent.",
                "criteria": {
                    "refund": "Requesting money back due to double charge",
                    "inquiry": "General billing question",
                    "cancellation": "Wants to cancel subscription",
                    "other": "Other topics"
                }
            },
            "urgency": {
                "type": "score",
                "instructions": "Rate urgency level (0=low, 1=medium, 2=high).",
                "criteria": [
                    "Low: polite question",
                    "Medium: noticeable dissatisfaction",
                    "High: demanding immediate refund or threatening escalation"
                ]
            },
            "needs_human": {
                "type": "noul",
                "instructions": "Does this case require human agent intervention?",
                "criteria": {
                    "true": "Requires human approval or financial dispute handling",
                    "false": "Can be handled automatically by system"
                }
            }
        }
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    req_data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=req_data, headers=headers, method="POST")

    print(f"🚀 Sending request to {url} ...")
    start_time = time.time()

    try:
        with urllib.request.urlopen(req, timeout=15) as response:
            elapsed_time = (time.time() - start_time) * 1000
            status_code = response.getcode()
            res_body = response.read().decode("utf-8")
            data = json.loads(res_body)

            print(f"✅ Success! (HTTP {status_code}) - Elapsed: {elapsed_time:.1f} ms\n")
            print("=== Response Summary ===")
            answers = data.get("result", {}).get("answers", {})
            for q_id, ans in answers.items():
                if "choice" in ans:
                    print(f"• [Choice] {q_id}: {ans['choice']} (Confidence: {ans.get('confidence', 0)*100:.1f}%)")
                elif "score" in ans:
                    print(f"• [Score]  {q_id}: {ans['score']} (Legend: {ans.get('legend', '')})")
                elif "noul" in ans:
                    print(f"• [Noul]   {q_id}: {ans['noul']*100:.1f}% probability of YES")
            
            print("\n=== Full Raw JSON ===")
            print(json.dumps(data, indent=2, ensure_ascii=False))

    except urllib.error.HTTPError as e:
        err_content = e.read().decode("utf-8", errors="ignore")
        print(f"❌ HTTP Error {e.code}: {e.reason}")
        print(f"Details: {err_content}")
    except urllib.error.URLError as e:
        print(f"❌ Connection Error: {e.reason}")

if __name__ == "__main__":
    run_test()
