"""Build the workshop PDF from the six part files.

    python build_pdf.py

Combines _front.md + PART0..5 + _back.md into BOOK.md, substitutes glyphs
XeLaTeX cannot find, then runs pandoc.
"""
import pathlib
import re
import subprocess
import sys

HERE = pathlib.Path(__file__).parent
PARTS = ["_front.md", "PART0.md", "PART1.md", "PART2.md",
         "PART3.md", "PART4.md", "PART5.md", "_back.md"]
OUT = "Full-Stack_Deployment_Guide.pdf"

# Glyphs Cambria / Consolas do not carry -> safe equivalents
GLYPHS = {
    "\u25b6": ">", "\u25c0": "<", "\u2611": "[x]",
    "\u2192": "->", "\u2190": "<-", "\u2264": "<=",
    "\u2082": "2", "\u2026": "...", "\u2013": "-",
}

# LaTeX injected into the preamble: styled callout boxes and a real title page
HEADER = r"""
\usepackage{tcolorbox}
\tcbuselibrary{skins,breakable}
\usepackage{titlesec}
\usepackage{fancyhdr}

% --- callout boxes (markdown blockquotes) ---
\definecolor{calloutbg}{HTML}{F4F6F8}
\definecolor{calloutrule}{HTML}{00776A}
\renewenvironment{quote}
  {\begin{tcolorbox}[breakable, enhanced, colback=calloutbg,
     colframe=calloutrule, boxrule=0pt, leftrule=2.5pt,
     arc=1pt, left=8pt, right=8pt, top=6pt, bottom=6pt,
     before skip=8pt, after skip=8pt]}
  {\end{tcolorbox}}

% --- headings ---
\definecolor{headink}{HTML}{15181F}
\titleformat{\chapter}[display]
  {\normalfont\sffamily\huge\bfseries\color{headink}}
  {\normalfont\sffamily\normalsize\bfseries\color{calloutrule}\MakeUppercase{\chaptertitlename\ \thechapter}}
  {8pt}{\Huge}
\titlespacing*{\chapter}{0pt}{10pt}{24pt}

% --- running header / footer ---
\pagestyle{fancy}
\fancyhf{}
\fancyhead[L]{\footnotesize\sffamily\color{gray}Full-Stack App Deployment with AI APIs \& Cloud}
\fancyhead[R]{\footnotesize\sffamily\color{gray}\thepage}
\renewcommand{\headrulewidth}{0.4pt}
\fancyfoot{}
"""

TITLEPAGE = r"""
\begin{titlepage}
\thispagestyle{empty}
\vspace*{2.2cm}
{\sffamily\footnotesize\color{calloutrule}\textbf{PROJECT NEXUS 2026 \quad$\cdot$\quad AI INNOVATION CHALLENGE}}

\vspace{1.4cm}
{\sffamily\fontsize{32}{38}\selectfont\bfseries Full-Stack App\\[2pt] Deployment}

\vspace{0.5cm}
{\sffamily\fontsize{20}{24}\selectfont\color{calloutrule} with AI APIs \& Cloud}

\vspace{1.1cm}
\rule{\textwidth}{0.6pt}

\vspace{0.7cm}
{\large Build a web application from an empty folder, connect an AI API,\\
and put it on the internet.}

\vspace{0.5cm}
{\normalsize\color{gray} No prior experience of web development, servers, or deployment
is assumed.\\ Nothing in this guide costs money.}

\vfill
{\sffamily\small
\textbf{Workshop 4 of 10} \quad$\cdot$\quad 31 August 2026\\[6pt]
IEEE Multimedia University Student Branch\\
Co-organisers: E3S2 UTP, IEEE PES MMU SBC, EWB MMU, IEM MMU}

\vspace{0.8cm}
{\footnotesize\color{gray} Every command and every line of code in this guide was
executed and verified before publication.}
\end{titlepage}
"""


def combine() -> str:
    out = []
    for f in PARTS:
        text = (HERE / f).read_text(encoding="utf-8")
        if f.startswith("PART"):
            out.append("\\newpage\n")
        out.append(text.rstrip() + "\n")
    doc = "\n".join(out)

    for bad, good in GLYPHS.items():
        doc = doc.replace(bad, good)

    # Untagged fences render without a grey background. Tag the OPENING fence
    # only -- a naive regex also rewrites the closing fence, which turns every
    # code block inside out and produces very confusing LaTeX errors.
    lines, inside = [], False
    for line in doc.split("\n"):
        if line.startswith("```"):
            if not inside and line.strip() == "```":
                line = "```text"
            inside = not inside
        lines.append(line)
    return "\n".join(lines)


def main() -> int:
    doc = combine()
    (HERE / "BOOK.md").write_text(doc, encoding="utf-8")
    (HERE / "_header.tex").write_text(HEADER, encoding="utf-8")
    (HERE / "_titlepage.tex").write_text(TITLEPAGE, encoding="utf-8")
    print(f"BOOK.md: {len(doc.splitlines()):,} lines")

    cmd = [
        "pandoc", "BOOK.md", "-o", OUT,
        "--pdf-engine=xelatex",
        "--toc", "--toc-depth=2",
        "-V", "documentclass=report",
        "--syntax-highlighting=tango",
        "-H", "_header.tex",
        "-B", "_titlepage.tex",
        "-V", "titlepage=false",
    ]
    result = subprocess.run(cmd, cwd=HERE, capture_output=True, text=True)
    for line in (result.stdout + result.stderr).splitlines():
        if any(w in line.lower() for w in ("error", "missing char", "undefined")):
            print("  ", line)
    if result.returncode != 0:
        print("BUILD FAILED")
        print((result.stdout + result.stderr)[-2500:])
        return 1

    size = (HERE / OUT).stat().st_size
    print(f"{OUT}: {size/1024:.0f} KB")
    return 0


if __name__ == "__main__":
    sys.exit(main())
