#!/usr/bin/env python3
"""
Reconcile the judgment-count claims (total / valid / self-excluded).

The paper (dataset_stats.json, DATASHEET.md, README.md) states 27,540 total, 22,254 valid,
"5,286 self-excluded". The parse-failure script counts 23,356 valid. This traces every number
to its exact filter so the paper's provenance table is correct.

Findings this reproduces:
  * 27,540 total slots                 = recount = SUM meta_analysis.total_judgments
  * 22,254 paper "valid"               = SUM meta_analysis.valid_judgments = usable score>0 (+2 pre-clamp)
  * 23,356 "parsed"                    = judgments with error is None (INCLUDES 1,104 valid 0-scores)
  * the 1,104 gap                      = judge parsed fine and scored a REFUSED/EMPTY response 0
  * "5,286 self-excluded" is FALSE     = real self-exclusions are 2,781; the rest are failures + 0-scores

No API calls -- pure re-analysis of the frozen dataset.
"""

import json
import glob
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from within_response_bias import MODEL_TO_FAMILY   # noqa: E402

DATA_GLOB = os.path.join(os.path.dirname(__file__), "..", "data", "peer_matrix", "EVAL-*")
API = ("Client error", "Server error", "name resolution", "disconnected",
       "peer closed connection", "incomplete chunked", "Temporary failure")


def main():
    b = dict(total=0, meta_total=0, meta_valid=0,
             err_none=0, valid_scored=0, zero_score=0, zero_score_justified=0,
             self_excl=0, api=0, empty=0, over10=0, parse=0, within_input=0)
    dates = []
    for p in sorted(glob.glob(DATA_GLOB)):
        ev = json.load(open(os.path.join(p, "results.json")))
        dates.append(ev.get("timestamp") or os.path.basename(p))
        m = ev.get("meta_analysis") or {}
        b["meta_total"] += m.get("total_judgments", 0)
        b["meta_valid"] += m.get("valid_judgments", 0)
        for j in ev.get("judgments", []):
            b["total"] += 1
            e, ws = j.get("error"), j.get("weighted_score")
            if e is None:
                b["err_none"] += 1
                if ws and ws > 0:
                    b["valid_scored"] += 1
                else:
                    b["zero_score"] += 1
                    if j.get("brief_justification"):
                        b["zero_score_justified"] += 1
            elif str(e).strip() == "":
                b["empty"] += 1
            elif e == "self_judgment_excluded":
                b["self_excl"] += 1
            elif any(x in str(e) for x in API):
                b["api"] += 1
            elif "over_10" in str(e) or "score_over" in str(e):
                b["over10"] += 1
            else:
                b["parse"] += 1
            if (j.get("judge_key") in MODEL_TO_FAMILY and j.get("respondent_key") in MODEL_TO_FAMILY
                    and j.get("judge_key") != j.get("respondent_key") and e is None and ws and ws > 0):
                b["within_input"] += 1

    genuine_fail = b["parse"] + b["empty"] + b["api"] + b["over10"]
    T = b["total"]
    print(f"evals: {len(dates)}   date range: {min(dates)[:10]} .. {max(dates)[:10]}  (freeze 2026-04-03)\n")
    print(f"total slots (recount)           = {b['total']}")
    print(f"SUM meta.total_judgments        = {b['meta_total']}   {'OK' if b['meta_total']==T else 'MISMATCH'}")
    print(f"SUM meta.valid_judgments        = {b['meta_valid']}   (= paper's 22,254)\n")

    print("--- full breakdown of the 27,540 slots ---")
    def line(label, n): print(f"  {label:44s} {n:6d}  ({100*n/T:5.1f}%)")
    line("valid, scored >0 (analysis input)", b["valid_scored"])
    line("valid, scored 0 (respondent refused/empty)", b["zero_score"])
    print(f"    -> of those 0-scores, with justification text: {b['zero_score_justified']}")
    line("  = parsed judge outputs (error is None)", b["err_none"])
    line("self-excluded (intentional diagonal)", b["self_excl"])
    line("parse failures (malformed / no JSON)", b["parse"])
    line("empty-error silent no-score", b["empty"])
    line("API / infra errors", b["api"])
    line("score>10 clamp (Phase 1)", b["over10"])
    s = b["valid_scored"]+b["zero_score"]+b["self_excl"]+b["parse"]+b["empty"]+b["api"]+b["over10"]
    print(f"  {'SUM check':44s} {s:6d}  ({'OK' if s==T else 'MISMATCH'})\n")

    print("--- verdicts ---")
    print(f"  parsed judgments (error None)     : {b['err_none']}   (the '23,356 valid' figure)")
    print(f"  usable scored (>0)                : {b['valid_scored']}   (paper 22,254 = this +{b['meta_valid']-b['valid_scored']} pre-clamp)")
    print(f"  genuine judge failures            : {genuine_fail}  ({100*genuine_fail/T:.1f}%)")
    print(f"  REAL self-exclusions              : {b['self_excl']}   (NOT 5,286)")
    print(f"  paper's '5,286 self-excluded'     : {T-b['meta_valid']}  = {b['self_excl']} self + {genuine_fail} fail + {b['zero_score']} zero-score  <-- MISLABELLED")
    print(f"  within-response analysis input    : {b['within_input']}   (score>0, non-self, both families known)")

    out = os.path.join(os.path.dirname(__file__), "..", "paper_tables", "count_reconciliation.json")
    b["genuine_failures"] = genuine_fail
    with open(out, "w") as f:
        json.dump(b, f, indent=2)
    print(f"\nWrote {out}")


if __name__ == "__main__":
    main()
