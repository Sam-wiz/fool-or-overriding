# Build the sprint report into the official Apart template (.docx).  usage: python build_report.py
# Content lives in report/content.py as a list of blocks.
import copy, re, sys, os, importlib.util
import docx
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

spec = importlib.util.spec_from_file_location("content", "report/content.py"); C = importlib.util.module_from_spec(spec); spec.loader.exec_module(C)
d = docx.Document("report/template.docx")
from docx.oxml.ns import qn as _qn
from docx.oxml import OxmlElement as _OE
FONT = getattr(C, "FONT", "XCharter")
def _smart(t):
    """straight quotes -> typographic (apostrophes and single quotes), as in the authors' LaTeX preprint."""
    t = re.sub(r"(^|[\s(\[{/—–-])'", lambda m: m.group(1) + "\u2018", t)
    return t.replace("'", "\u2019")
def _style_font(st, size=None, bold=None, color=(0, 0, 0)):
    rpr = st.element.get_or_add_rPr()
    rf = rpr.find(_qn("w:rFonts"))
    if rf is None: rf = _OE("w:rFonts"); rpr.insert(0, rf)
    for k in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"): rf.set(_qn(k), FONT)
    for k in ("w:asciiTheme", "w:hAnsiTheme", "w:cstheme", "w:eastAsiaTheme"):
        if rf.get(_qn(k)) is not None: del rf.attrib[_qn(k)]
    if size: st.font.size = Pt(size)
    if bold is not None: st.font.bold = bold
    if color is not None: st.font.color.rgb = RGBColor(*color)
_style_font(d.styles["Normal"]); _style_font(d.styles["Title"], 16.5, True)
_style_font(d.styles["Heading 2"], 12.5, True); _style_font(d.styles["Heading 3"], 10.8, True)
for _h in ("Heading 2", "Heading 3"):
    pf = d.styles[_h].paragraph_format; pf.space_before = Pt(10 if _h == "Heading 2" else 6); pf.space_after = Pt(3); pf.keep_with_next = True
def _rule_below(p, sz=4, color="808080"):
    pPr = p._p.get_or_add_pPr(); b = _OE("w:pBdr"); e = _OE("w:bottom")
    e.set(_qn("w:val"), "single"); e.set(_qn("w:sz"), str(sz)); e.set(_qn("w:space"), "2"); e.set(_qn("w:color"), color); b.append(e); pPr.append(b)

# ---------------- title / authors / abstract block ----------------
t0 = d.tables[0]
title_p = [p for p in t0.rows[0].cells[0].paragraphs if p.style.name == "Title"][0]
for r in title_p.runs[1:]: r.text = ""
title_p.runs[0].text = C.TITLE.replace("'", "\u2019")
title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
for r in title_p.runs: r.font.name = FONT; r.font.size = Pt(16.5); r.bold = True; r.font.color.rgb = RGBColor(0, 0, 0)
# replace the nested author/abstract grid (renders badly outside Google Docs) with full-width paragraphs
t0._tbl.remove(t0.rows[1]._tr)
from docx.oxml.ns import qn
import copy as _copy
def _para_after(anchor_el, text, size=10, bold=False, italic=False, center=False, space_after=4):
    newp = d.add_paragraph(); r = newp.add_run(text); r.font.size = Pt(size); r.bold = bold; r.italic = italic
    if center: newp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    newp.paragraph_format.space_after = Pt(space_after); newp.paragraph_format.line_spacing = 1.0
    anchor_el.addnext(newp._p); return newp._p
el = t0._tbl
el = _para_after(el, "   ·   ".join(n for n, a in C.AUTHORS), size=11, bold=True, center=True, space_after=2)
el = _para_after(el, "Independent researchers", size=10, center=True, space_after=5)
el = _para_after(el, "Apart Research · AI x Epistemics Research Sprint, Track 1 · November 2026", size=9, italic=True, center=True, space_after=2)
el = _para_after(el, "Code, data and every cached model output: " + getattr(C, "GITHUB_URL", ""), size=9, italic=True, center=True, space_after=4)
_rp = d.add_paragraph(); _rp.paragraph_format.space_after = Pt(8); _rule_below(_rp, sz=6, color="000000"); el.addnext(_rp._p); el = _rp._p
_ab = d.add_paragraph(); _r = _ab.add_run("ABSTRACT"); _r.bold = True; _r.font.size = Pt(9.5); _r.font.small_caps = False
_ab.alignment = WD_ALIGN_PARAGRAPH.CENTER; _ab.paragraph_format.space_after = Pt(4); el.addnext(_ab._p); el = _ab._p
_ap = d.add_paragraph(); _r = _ap.add_run(_smart(C.ABSTRACT)); _r.font.size = Pt(9.5)
_ap.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY; _ap.paragraph_format.left_indent = Inches(0.45); _ap.paragraph_format.right_indent = Inches(0.45)
_ap.paragraph_format.line_spacing = 1.12; _ap.paragraph_format.space_after = Pt(10); el.addnext(_ap._p); el = _ap._p
# remove info-box table (table 1)
info = d.tables[1]._tbl; info.getparent().remove(info)

# ---------------- body ----------------
body = d.element.body
start = None
for i, p in enumerate(d.paragraphs):
    if p.text.strip().startswith("1. Introduction"): start = p; break
# delete everything from the first section heading onward (except sectPr)
el = start._p
while el is not None:
    nxt = el.getnext()
    if el.tag.endswith("sectPr"): break
    body.remove(el); el = nxt
sect = body[-1]


BODY_PT = getattr(C, "BODY_PT", 10)
def add_par(text, style="normal", bold=False, italic=False, size=None, align=None, space_after=4):
    p = d.add_paragraph(style=style)
    # inline **bold** and *italic*
    text = _smart(text)
    for tok in re.split(r"(\*\*[^*]+\*\*|\*[^*]+\*)", text):
        if not tok: continue
        if tok.startswith("**"): r = p.add_run(tok[2:-2]); r.bold = True
        elif tok.startswith("*"): r = p.add_run(tok[1:-1]); r.italic = True
        else: r = p.add_run(tok)
        if bold: r.bold = True
        if italic: r.italic = True
        if size: r.font.size = Pt(size)
    if align == "center": p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    elif style == "normal" and size is None: p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.space_after = Pt(space_after); p.paragraph_format.space_before = Pt(0)
    if style == "normal":
        p.paragraph_format.line_spacing = 1.07
        for r in p.runs:
            if r.font.size is None: r.font.size = Pt(BODY_PT)
    return p

from docx.oxml import OxmlElement
from docx.shared import RGBColor as _RGB
CAP_PT = 8.5
def add_caption(text, space_after=8, keep_next=False):
    """'Table 1. ...' / 'Figure 1. ...' -> bold label, grey justified caption text."""
    p = d.add_paragraph(style="normal")
    m = re.match(r"((?:Table|Figure) \d+\.)\s*(.*)", text, re.S)
    label, rest = (m.group(1), m.group(2)) if m else ("", text)
    if label:
        r = p.add_run(label + " "); r.bold = True; r.font.size = Pt(CAP_PT)
    rest = _smart(rest)
    for tok in re.split(r"(\*\*[^*]+\*\*|\*[^*]+\*)", rest):
        if not tok: continue
        if tok.startswith("**"): r = p.add_run(tok[2:-2]); r.bold = True
        elif tok.startswith("*"): r = p.add_run(tok[1:-1]); r.italic = True
        else: r = p.add_run(tok)
        r.font.size = Pt(CAP_PT); r.font.color.rgb = _RGB(0x33, 0x33, 0x33)
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.space_after = Pt(space_after); p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.line_spacing = 1.0; p.paragraph_format.keep_with_next = keep_next
    return p
def _border(parent, tag, val="single", sz=4, color="000000"):
    e = OxmlElement(f"w:{tag}"); e.set(qn("w:val"), val); e.set(qn("w:sz"), str(sz)); e.set(qn("w:space"), "0"); e.set(qn("w:color"), color)
    parent.append(e)
def style_table(tb, widths):
    """booktabs-like: heavy top/bottom rules, rule under header, light row separators, no verticals; fixed full width."""
    TEXT_W = 6.5
    n = len(tb.columns)
    widths = widths or [TEXT_W / n] * n
    scale = TEXT_W / sum(widths); widths = [w * scale for w in widths]
    tb.autofit = False
    tblPr = tb._tbl.tblPr
    for old in tblPr.findall(qn("w:tblBorders")): tblPr.remove(old)
    b = OxmlElement("w:tblBorders")
    _border(b, "top", sz=10); _border(b, "left", val="nil"); _border(b, "bottom", sz=10); _border(b, "right", val="nil")
    _border(b, "insideH", sz=2, color="BFBFBF"); _border(b, "insideV", val="nil")
    tblPr.append(b)
    lay = OxmlElement("w:tblLayout"); lay.set(qn("w:type"), "fixed"); tblPr.append(lay)
    tw = OxmlElement("w:tblW"); tw.set(qn("w:w"), str(int(TEXT_W * 1440))); tw.set(qn("w:type"), "dxa")
    for old in tblPr.findall(qn("w:tblW")): tblPr.remove(old)
    tblPr.append(tw)
    jc = OxmlElement("w:jc"); jc.set(qn("w:val"), "center"); tblPr.append(jc)
    grid = tb._tbl.tblGrid
    for gc, w in zip(grid.findall(qn("w:gridCol")), widths): gc.set(qn("w:w"), str(int(w * 1440)))
    for ri, row in enumerate(tb.rows):
        for j, c in enumerate(row.cells):
            c.width = Inches(widths[j])
            tcPr = c._tc.get_or_add_tcPr()
            va = OxmlElement("w:vAlign"); va.set(qn("w:val"), "center"); tcPr.append(va)
            mar = OxmlElement("w:tcMar")
            for side in ("top", "bottom"):
                m_ = OxmlElement(f"w:{side}"); m_.set(qn("w:w"), "28"); m_.set(qn("w:type"), "dxa"); mar.append(m_)
            for side in ("left", "right"):
                m_ = OxmlElement(f"w:{side}"); m_.set(qn("w:w"), "60"); m_.set(qn("w:type"), "dxa"); mar.append(m_)
            tcPr.append(mar)
            if ri == 0:
                shd = OxmlElement("w:shd"); shd.set(qn("w:val"), "clear"); shd.set(qn("w:color"), "auto"); shd.set(qn("w:fill"), "EDEDED"); tcPr.append(shd)
                tb_ = OxmlElement("w:tcBorders"); _border(tb_, "bottom", sz=6); tcPr.append(tb_)
            for pp in c.paragraphs:
                pp.alignment = WD_ALIGN_PARAGRAPH.LEFT if j == 0 else WD_ALIGN_PARAGRAPH.CENTER
                pp.paragraph_format.space_after = Pt(0); pp.paragraph_format.space_before = Pt(0); pp.paragraph_format.line_spacing = 1.0
    trPr = tb.rows[0]._tr.get_or_add_trPr(); h = OxmlElement("w:tblHeader"); trPr.append(h)

SUBS = {"STEER_TITLE": getattr(C, "ST2", {}).get("title", ""), "STEER_TEXT": getattr(C, "ST2", {}).get("text", "(pending)"),
        "PER_MODEL_EXTRA": getattr(C, "EXTRA_TEXT", ""), "GITHUB_URL": getattr(C, "GITHUB_URL", "https://github.com/<to-be-created>")}
def sub(x):
    if isinstance(x, str):
        for k, v in SUBS.items(): x = x.replace(k, v)
    return x
_PB_NEXT = False
for blk in C.BODY:
    blk = tuple(sub(b) if isinstance(b, str) else ([sub(z) for z in b] if isinstance(b, list) and b and isinstance(b[0], str) else b) for b in blk)
    kind = blk[0]
    if kind == "refs":
        for i, r in enumerate(C.REFS):
            p = add_par(f"[{i + 1}] {r}", size=8.5, space_after=1); p.paragraph_format.left_indent = Inches(0.25); p.paragraph_format.first_line_indent = Inches(-0.25)
        continue
    if kind == "h2":
        _hp = add_par(re.sub(r"^(\d+)\.\s+", r"\1   ", blk[1]), style="Heading 2"); _rule_below(_hp, sz=4, color="999999")
        if _PB_NEXT: _hp.paragraph_format.page_break_before = True; _PB_NEXT = False
    elif kind == "h3": add_par(re.sub(r"^(\d+\.\d+)\s+", r"\1   ", blk[1]), style="Heading 3")
    elif kind == "p": add_par(blk[1])
    elif kind == "bullets":
        for b in blk[1]:
            p = add_par("•  " + b); p.paragraph_format.left_indent = Inches(0.2)
    elif kind == "num":
        for i, b in enumerate(blk[1]):
            p = add_par(f"{i + 1}.  " + b); p.paragraph_format.left_indent = Inches(0.2)
    elif kind == "fig":
        path, width, cap = blk[1], blk[2], blk[3]
        p = d.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.add_run().add_picture(path, width=Inches(width)); p.paragraph_format.keep_with_next = True
        p.paragraph_format.space_before = Pt(4); p.paragraph_format.space_after = Pt(2)
        add_caption(cap, space_after=8)
    elif kind == "table":
        header, rows, cap, widths = blk[1], blk[2], blk[3], (blk[4] if len(blk) > 4 else None)
        capp = add_caption(cap, space_after=3, keep_next=True)
        tb = d.add_table(rows=1 + len(rows), cols=len(header)); tb.style = d.styles["Table Grid"] if "Table Grid" in [s.name for s in d.styles] else tb.style
        for j, h in enumerate(header):
            c = tb.rows[0].cells[j]; c.text = ""; r = c.paragraphs[0].add_run(h); r.bold = True; r.font.size = Pt(7.5)
        for i, row in enumerate(rows):
            for j, v in enumerate(row):
                c = tb.rows[i + 1].cells[j]; c.text = ""; r = c.paragraphs[0].add_run(str(v)); r.font.size = Pt(7.5)
        style_table(tb, widths)
        from docx.oxml import OxmlElement
        for ri, row in enumerate(tb.rows):
            trPr = row._tr.get_or_add_trPr(); cs = OxmlElement("w:cantSplit"); trPr.append(cs)
            if ri < len(tb.rows) - 1:
                for c in row.cells:
                    for pp in c.paragraphs: pp.paragraph_format.keep_with_next = True
        add_par("", space_after=4)
    elif kind == "pagebreak":
        _PB_NEXT = True   # start the next section heading on a new page (never leaves an empty page)
    elif kind == "small":
        for line in blk[1].split("\n"): add_par(line, size=8.5, space_after=2)
# move sectPr to end
body.remove(sect); body.append(sect)
os.makedirs("report/out", exist_ok=True)
d.save("report/out/report.docx"); print("saved report/out/report.docx")
