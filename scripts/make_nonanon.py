#!/usr/bin/env python3
"""
Generate multivac_paper_nonanon.tex from multivac_paper.tex by applying ONLY the
non-anonymous transformations (preamble option, author block, title, links, judge
prompt). The body is copied verbatim, so the two versions can never diverge.

Run after any edit to multivac_paper.tex, then rebuild both PDFs.
"""
import os
HERE = os.path.dirname(__file__)
SRC = os.path.join(HERE, "..", "multivac_paper.tex")
DST = os.path.join(HERE, "..", "multivac_paper_nonanon.tex")

# (anon substring, non-anon replacement). Each MUST match exactly once.
SUBS = [
    (r"""% TMLR double-blind submission: compiling tmlr.sty WITHOUT the `accepted`
% or `preprint` option renders the anonymized title block
% ("Anonymous authors / Paper under double-blind review") and the
% "Under review as submission to TMLR" running head automatically.
\usepackage{tmlr}""",
     r"""% Non-anonymous preprint build (generated from multivac_paper.tex by make_nonanon.py):
% the `preprint` option renders the author block and drops the "Under review" head.
\usepackage[preprint]{tmlr}"""),

    (r"""% TMLR-style clickable links: colored (not boxed), long URLs breakable via xurl.
% pdfauthor is left empty so no identity leaks into PDF metadata under double-blind.
\usepackage[colorlinks=true,linkcolor={blue!45!black},citecolor={blue!45!black},%
            urlcolor={blue!55!black},pdfauthor={},%
            pdftitle={Blind Peer Matrix: Symmetric Multi-Judge Evaluation of Frontier Language Models}]{hyperref}""",
     r"""% TMLR-style clickable links: colored (not boxed), long URLs breakable via xurl.
\usepackage[colorlinks=true,linkcolor={blue!45!black},citecolor={blue!45!black},%
            urlcolor={blue!55!black},pdfauthor={Yash Darji},%
            pdftitle={The Multivac: Blind Peer Matrix Evaluation of Frontier Language Models}]{hyperref}"""),

    (r"""\title{Blind Peer Matrix: Symmetric Multi-Judge Evaluation\\of Frontier Language Models}

\begin{document}""",
     r"""\title{The Multivac: Blind Peer Matrix Evaluation\\of Frontier Language Models}

\author{
  Yash Darji \\
  Independent Researcher \\
  ORCID: \href{https://orcid.org/0009-0009-6895-842X}{0009-0009-6895-842X} \\
  \texttt{yashdarji2378@gmail.com}
}

\begin{document}"""),

    (r"\fbox{\parbox{0.92\textwidth}{\centering \textbf{Anonymized artifact} (code, dataset, and one-command reproduction pipeline):\\ \url{https://anonymous.4open.science/r/multivac-evaluation-6F8B/README.md}}}",
     r"\fbox{\parbox{0.92\textwidth}{\centering \textbf{Code, data, and reproduction pipeline:} \url{https://github.com/themultivac/multivac-evaluation}\\ Interactive platform: \url{https://app.themultivac.com}}}"),

    (r"are released under MIT license.\footnote{Code, dataset, and one-command reproduction pipeline (anonymized for review): \url{https://anonymous.4open.science/r/multivac-evaluation-6F8B/README.md}.}",
     r"are released under MIT license.\footnote{Code and dataset: \url{https://github.com/themultivac/multivac-evaluation}. Platform: \url{https://app.themultivac.com}.}"),

    (r"""The exact judge system prompt and user-prompt template are reproduced below (the product name in the system prompt is redacted for double-blind review).

\input{paper_tables/appendix_D_prompt}""",
     r"""The exact judge system prompt and user-prompt template are reproduced below.

\input{paper_tables/appendix_D_prompt_nonanon}"""),
]


def main():
    t = open(SRC).read()
    for anon, nonanon in SUBS:
        n = t.count(anon)
        if n != 1:
            raise SystemExit(f"ERROR: expected exactly 1 match, found {n} for:\n  {anon[:80]}...")
        t = t.replace(anon, nonanon)
    open(DST, "w").write(t)
    print(f"Wrote {DST} ({len(SUBS)} non-anon substitutions applied; body copied verbatim).")


if __name__ == "__main__":
    main()
