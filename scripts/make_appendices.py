#!/usr/bin/env python3
"""
Generate appendix content (Tables A / C / E) from the frozen peer-matrix data.
No API calls -- frozen data only. Emits LaTeX fragments to paper_tables/ and prints
diagnostics (distinct-family count, duplicate display names) used by the consistency read.
"""
import json, glob, os, re
from collections import defaultdict

HERE = os.path.dirname(__file__)
DATA = sorted(glob.glob(os.path.join(HERE, "..", "data", "peer_matrix", "EVAL-*")))
OUT = os.path.join(HERE, "..", "paper_tables")

FAMILY = [
    ("claude", "Anthropic"), ("gpt_oss", "OpenAI"), ("gpt_codex", "OpenAI"),
    ("gpt", "OpenAI"), ("judge_gpt", "OpenAI"), ("judge_claude", "Anthropic"),
    ("judge_gemini", "Google"),
    ("gemini", "Google"), ("gemma", "Google"), ("grok", "xAI"),
    ("deepseek", "DeepSeek"), ("mimo", "Xiaomi"), ("minimax", "MiniMax"),
    ("qwen", "Qwen/Alibaba"), ("devstral", "Mistral"), ("mistral", "Mistral"),
    ("seed", "ByteDance"), ("llama", "Meta"), ("kimi", "Moonshot"),
    ("phi", "Microsoft"), ("granite", "IBM"), ("olmo", "Ai2"),
    ("glm", "Zhipu"), ("nemotron", "NVIDIA"),
]
def fam(key):
    for pre, f in FAMILY:
        if key.startswith(pre):
            return f
    return "UNMAPPED"

def latex_escape(s):
    return s.replace("&", "\\&").replace("%", "\\%").replace("_", "\\_")

def main():
    evals_of = defaultdict(set)          # key -> set(eval ids) via models_used
    cats_of = defaultdict(set)           # key -> categories (as respondent participant)
    names = {}
    recv = defaultdict(lambda: {"s": 0.0, "n": 0})   # key -> incl-zeros mean of received
    given = defaultdict(int)             # key -> judgments given (as judge, non-self, no error)
    dims = defaultdict(lambda: defaultdict(list))    # key -> dim -> list (received, zeros incl)
    DIMS = ["correctness", "completeness", "clarity", "depth", "usefulness"]

    for p in DATA:
        ev = json.load(open(os.path.join(p, "results.json")))
        eid = os.path.basename(p); cat = ev.get("category", "?")
        for m in set(ev.get("models_used", [])):
            evals_of[m].add(eid); cats_of[m].add(cat)
        for j in ev.get("judgments", []):
            if j.get("respondent_name"):
                names[j["respondent_key"]] = j["respondent_name"]
            if j.get("judge_name"):
                names.setdefault(j["judge_key"], j["judge_name"])
            self_j = j.get("judge_key") == j.get("respondent_key")
            if j.get("error") is None and not self_j:
                given[j["judge_key"]] += 1
                rk = j["respondent_key"]; ws = float(j.get("weighted_score") or 0.0)
                recv[rk]["s"] += ws; recv[rk]["n"] += 1
                for d in DIMS:
                    if j.get(d) is not None:
                        dims[rk][d].append(float(j[d]))

    keys = sorted(evals_of, key=lambda k: (fam(k), -len(evals_of[k]), k))
    # ---- diagnostics ----
    fams = defaultdict(list)
    for k in keys:
        fams[fam(k)].append(k)
    dispnames = defaultdict(list)
    for k in keys:
        dispnames[names.get(k, k)].append(k)
    dupes = {n: ks for n, ks in dispnames.items() if len(ks) > 1}
    print(f"DIAGNOSTICS: {len(keys)} model keys in models_used; "
          f"{len(dispnames)} distinct display names; {len(fams)} distinct families.")
    print("Families:", ", ".join(f"{f}({len(v)})" for f, v in sorted(fams.items())))
    print("Duplicate display names (same name, >1 key):")
    for n, ks in dupes.items():
        print(f"   {n}: {ks}")
    if "UNMAPPED" in fams:
        print("UNMAPPED KEYS:", fams["UNMAPPED"])

    # ---- App A longtable ----
    a = [r"\footnotesize", r"\begin{longtable}{llrrrp{3.0cm}}", r"\caption{Complete model list (55 model configurations "
         r"from \texttt{models\_used}, 50 distinct by display name). Mean is the received composite score with genuine "
         r"zero-scores included; \emph{n/a} marks roster configurations that produced no parseable "
         r"judgment in the frozen data (issued and received none). Judg.\ given counts non-self judgments "
         r"a model issued as judge, zero-scores included, and can therefore exceed the scored-judgment "
         r"counts underlying the judge-leniency means in \S5.3 (e.g.\ Mistral Small Creative: 423 issued, "
         r"422 scored). Parameter counts are omitted: the repository records them only for the open "
         r"$\leq$32B pool, not for the proprietary majority.}\label{tab:models}\\",
         r"\toprule", r"Family & Model & Evals & Judg.\ given & Mean & Categories \\", r"\midrule",
         r"\endfirsthead", r"\toprule",
         r"Family & Model & Evals & Judg.\ given & Mean & Categories \\", r"\midrule",
         r"\endhead", r"\midrule", r"\endfoot", r"\bottomrule", r"\endlastfoot"]
    CATABBR = {"code": "code", "reasoning": "reas", "analysis": "anly", "communication": "comm",
               "meta_alignment": "meta", "meta-alignment": "meta", "edge_cases": "edge",
               "edge": "edge", "slm": "slm", "qwen": "qwen", "minimax": "mmax"}
    for k in keys:
        nm = names.get(k, k)
        mean_str = f"{recv[k]['s'] / recv[k]['n']:.2f}" if recv[k]["n"] else "n/a"
        cats = sorted({CATABBR.get(c, c) for c in cats_of[k]})
        a.append(f"{latex_escape(fam(k))} & {latex_escape(nm)} & {len(evals_of[k])} & "
                 f"{given.get(k,0)} & {mean_str} & {latex_escape(', '.join(cats))} \\\\")
    a.append(r"\end{longtable}")
    a.append(r"\normalsize")
    open(os.path.join(OUT, "appendix_A_models.tex"), "w").write("\n".join(a))

    # ---- App E per-model dimensions (n>=100 received judgments) ----
    e = [r"\begin{longtable}{lrrrrrr}",
         r"\caption{Per-model mean scores by dimension (zero-scores included), for all models "
         r"with $\geq 100$ received judgments. $\Delta$ is the clarity$-$depth gap.}"
         r"\label{tab:dims}\\", r"\toprule",
         r"Model & Corr. & Compl. & Clar. & Depth & Use. & $\Delta$(cl$-$dp) \\", r"\midrule",
         r"\endfirsthead", r"\toprule",
         r"Model & Corr. & Compl. & Clar. & Depth & Use. & $\Delta$(cl$-$dp) \\", r"\midrule",
         r"\endhead", r"\midrule", r"\endfoot", r"\bottomrule", r"\endlastfoot"]
    erows = []
    for k, dd in dims.items():
        if len(dd.get("clarity", [])) >= 100:
            mv = {d: (sum(dd[d]) / len(dd[d]) if dd.get(d) else 0.0) for d in DIMS}
            erows.append((names.get(k, k), mv, mv["clarity"] - mv["depth"]))
    for nm, mv, gap in sorted(erows, key=lambda x: -x[2]):
        e.append(f"{latex_escape(nm)} & {mv['correctness']:.2f} & {mv['completeness']:.2f} & "
                 f"{mv['clarity']:.2f} & {mv['depth']:.2f} & {mv['usefulness']:.2f} & {gap:.2f} \\\\")
    e.append(r"\end{longtable}")
    open(os.path.join(OUT, "appendix_E_dimensions.tex"), "w").write("\n".join(e))
    print(f"\nApp E: {len(erows)} models with >=100 received judgments.")

    # ---- App C score matrix for one evaluation ----
    EID = "EVAL-20260403-112809"
    ev = json.load(open(os.path.join(HERE, "..", "data", "peer_matrix", EID, "results.json")))
    order = list(ev.get("models_used", []))
    nm = {}
    cell = {}
    for j in ev.get("judgments", []):
        nm[j["judge_key"]] = j.get("judge_name", j["judge_key"])
        nm[j["respondent_key"]] = j.get("respondent_name", j["respondent_key"])
        cell[(j["respondent_key"], j["judge_key"])] = (None if j.get("error") else
                                                       float(j.get("weighted_score") or 0.0))
    short = [latex_escape(nm.get(k, k))[:10] for k in order]
    c = [r"\begin{table}[h]\centering\footnotesize",
         rf"\caption{{Complete score matrix for evaluation {EID} "
         rf"(category: {ev.get('category','?')}). Rows = respondents, columns = judges; "
         r"cell $S_{ij}$ is the weighted composite (0--10). Diagonal (self-judgment) excluded "
         r"($\bullet$); blank = judge failure.}\label{tab:matrix}",
         r"\setlength{\tabcolsep}{3pt}",
         r"\begin{tabular}{l" + "r" * len(order) + "}", r"\toprule",
         " & " + " & ".join(rf"\rotatebox{{90}}{{{s}}}" for s in short) + r" \\", r"\midrule"]
    for ri in order:
        row = [latex_escape(nm.get(ri, ri))[:16]]
        for ci in order:
            if ri == ci:
                row.append(r"$\bullet$")
            else:
                v = cell.get((ri, ci))
                row.append("" if v is None else f"{v:.1f}")
        c.append(" & ".join(row) + r" \\")
    c += [r"\bottomrule", r"\end{tabular}", r"\end{table}"]
    open(os.path.join(OUT, "appendix_C_matrix.tex"), "w").write("\n".join(c))
    print(f"App C: {len(order)} models in {EID} (category={ev.get('category')}).")
    print("\nWrote appendix_A_models.tex, appendix_E_dimensions.tex, appendix_C_matrix.tex")

if __name__ == "__main__":
    main()
