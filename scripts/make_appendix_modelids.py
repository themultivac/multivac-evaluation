#!/usr/bin/env python3
"""
Appendix G: exact model identifiers for every registry entry in Table 4.

Pulled ENTIRELY from the frozen data (data/peer_matrix/*/model_metadata.json for the
API model string and routing provider; results.json timestamps for the call date range).
Nothing is reconstructed from display names: keys with no recorded model_metadata entry
are listed explicitly as "not recorded in the frozen data" rather than inferred.

No API calls -- frozen data only.
"""
import json
import glob
import os
from collections import defaultdict

HERE = os.path.dirname(__file__)
DATA = sorted(glob.glob(os.path.join(HERE, "..", "data", "peer_matrix", "EVAL-*")))
OUT = os.path.join(HERE, "..", "paper_tables", "appendix_G_modelids.tex")


def esc(s):
    return str(s).replace("_", r"\_").replace("&", r"\&").replace("%", r"\%")


def brk(s):
    """Escape, then allow line breaks after path/version separators so long API
    model strings wrap inside their column instead of overrunning the next one."""
    out = esc(s)
    for sep in ("/", "-", ":", "."):
        out = out.replace(sep, sep + r"\allowbreak ")
    return out


def main():
    meta = {}                       # key -> {model_id, provider}
    dates = defaultdict(list)       # key -> [YYYY-MM-DD]
    names = {}                      # key -> display name
    for d in DATA:
        rp = os.path.join(d, "results.json")
        if not os.path.exists(rp):
            continue
        ev = json.load(open(rp))
        day = (ev.get("timestamp") or "")[:10]
        for k in ev.get("models_used", []):
            if day:
                dates[k].append(day)
        for j in ev.get("judgments", []):
            if j.get("respondent_name"):
                names[j["respondent_key"]] = j["respondent_name"]
            if j.get("judge_name"):
                names.setdefault(j["judge_key"], j["judge_name"])
        mp = os.path.join(d, "model_metadata.json")
        if os.path.exists(mp):
            for k, v in json.load(open(mp)).items():
                if k not in meta and v.get("model_id"):
                    meta[k] = {"model_id": v.get("model_id"),
                               "provider": v.get("provider") or "not recorded"}

    keys = sorted(dates)
    have = [k for k in keys if k in meta]
    lack = [k for k in keys if k not in meta]

    L = []
    L.append(r"\begin{longtable}{>{\raggedright\arraybackslash}p{0.19\textwidth}>{\raggedright\arraybackslash}p{0.30\textwidth}>{\raggedright\arraybackslash}p{0.12\textwidth}>{\raggedright\arraybackslash}p{0.22\textwidth}}")
    L.append(r"\caption{Exact model identifiers for the registry entries of Table~\ref{tab:models}, "
             r"taken from the frozen data. \emph{API model string} and \emph{routing} are read from "
             r"\texttt{model\_metadata.json}; \emph{call dates} are the first and last peer-matrix "
             r"evaluation timestamps in which the key appears. Entries whose identifier was not "
             r"recorded in the frozen data are listed in the second block and are \emph{not} "
             r"reconstructed.}\label{tab:modelids}\\")
    L.append(r"\toprule")
    L.append(r"Registry key & API model string & Routing & Call dates \\")
    L.append(r"\midrule")
    L.append(r"\endfirsthead")
    L.append(r"\toprule Registry key & API model string & Routing & Call dates \\ \midrule \endhead")
    for k in have:
        ds = sorted(dates[k])
        span = ds[0] if ds[0] == ds[-1] else f"{ds[0]} to {ds[-1]}"
        L.append(f"\\texttt{{{brk(k)}}} & \\texttt{{{brk(meta[k]['model_id'])}}} & "
                 f"{esc(meta[k]['provider'])} & {span} \\\\")
    L.append(r"\bottomrule")
    L.append(r"\end{longtable}")

    L.append("")
    L.append(rf"\noindent\textbf{{Identifiers not recorded in the frozen data ({len(lack)} of "
             rf"{len(keys)} registry keys).}} The per-evaluation \texttt{{model\_metadata.json}} "
             r"file was added to the pipeline partway through the campaign and is present in "
             rf"{len([d for d in DATA if os.path.exists(os.path.join(d, 'model_metadata.json'))])} "
             rf"of {len(DATA)} peer-matrix evaluations. For the following keys no API model string "
             r"is recorded anywhere in the frozen dataset, and we do not reconstruct one; only the "
             r"display name and call dates are known:")
    L.append("")
    L.append(r"\begin{small}\begin{itemize}\setlength\itemsep{0pt}")
    for k in lack:
        ds = sorted(dates[k])
        span = ds[0] if ds[0] == ds[-1] else f"{ds[0]} to {ds[-1]}"
        L.append(f"  \\item \\texttt{{{esc(k)}}} ({esc(names.get(k, k))}) --- {span}")
    L.append(r"\end{itemize}\end{small}")

    open(OUT, "w").write("\n".join(L) + "\n")
    print(f"Wrote {OUT}: {len(have)} keys with recorded identifiers, {len(lack)} without.")


if __name__ == "__main__":
    main()
