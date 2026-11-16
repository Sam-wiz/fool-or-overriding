"""Build an arXiv-style preprint PDF from the same source as the Apart-template report (report/content.py).
usage: python src/build_arxiv.py   ->  report/out/Fooled_or_Overriding_preprint.pdf  (needs Google Chrome; markdown)"""
import importlib.util, os, re, subprocess, sys

spec = importlib.util.spec_from_file_location("content", "report/content.py"); C = importlib.util.module_from_spec(spec); spec.loader.exec_module(C)
SUBS = {"STEER_TITLE": getattr(C, "ST2", {}).get("title", ""), "STEER_TEXT": getattr(C, "ST2", {}).get("text", ""),
        "PER_MODEL_EXTRA": getattr(C, "EXTRA_TEXT", ""), "GITHUB_URL": getattr(C, "GITHUB_URL", "")}
def sub(x):
    for k, v in SUBS.items(): x = x.replace(k, v)
    return x.replace("<", "&lt;").replace(">", "&gt;")
def cap(c, kind):
    m = re.match(rf"({kind} \d+)\.\s*(.*)", c, re.S)
    if not m: return f"*{sub(c)}*"
    return f"**{m.group(1)}:** {sub(m.group(2))}" if kind == "Figure" else f"**{m.group(1)}: {sub(m.group(2))}**"

md = [f"# {sub(C.TITLE)}", "", "  ·  ".join(f"**{n}** ({a})" for n, a in C.AUTHORS), "",
      "*Apart Research AI x Epistemics Sprint, Track 1 · November 2026 · " + sub(C.GITHUB_URL) + "*", "", "## Abstract", "", sub(C.ABSTRACT), ""]
for blk in C.BODY:
    k = blk[0]
    if k == "h2": md += [f"## {sub(blk[1])}", ""]
    elif k == "h3": md += [f"### {sub(blk[1])}", ""]
    elif k in ("p", "small"): md += [sub(blk[1]), ""]
    elif k == "bullets": md += [f"- {sub(b)}" for b in blk[1]] + [""]
    elif k == "num": md += [f"{i + 1}. {sub(b)}" for i, b in enumerate(blk[1])] + [""]
    elif k == "fig": md += [f"![]({os.path.abspath(blk[1])})", "", cap(blk[3], "Figure"), ""]
    elif k == "table":
        header, rows, c = blk[1], blk[2], blk[3]
        md += [cap(c, "Table"), "", "| " + " | ".join(sub(h) for h in header) + " |", "|" + "---|" * len(header)]
        md += ["| " + " | ".join(sub(str(v)).replace("|", "/") for v in r) + " |" for r in rows] + [""]
    elif k == "refs": md += [f"{i + 1}. {sub(r)}" for i, r in enumerate(C.REFS)] + [""]
    elif k == "pagebreak": md += ['<div style="break-before: page"></div>', ""]
os.makedirs("report/out", exist_ok=True)
open("report/out/preprint.md", "w").write("\n".join(md))
out = "report/out/Fooled_or_Overriding_preprint.pdf"
subprocess.run([sys.executable, "src/arxiv_pdf.py", "report/out/preprint.md", out], check=True)
