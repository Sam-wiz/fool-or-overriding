# docx -> pdf with headless LibreOffice on Modal (no volumes). usage: modal run src/modal_pdf.py --src report/out/report.docx
import modal, os
image = modal.Image.debian_slim(python_version="3.12").apt_install("libreoffice-writer", "fonts-dejavu", "fonts-liberation", "fonts-crosextra-carlito", "fonts-crosextra-caladea", "fonts-noto-core").apt_install("ca-certificates", "curl", "unzip", "fontconfig").run_commands(
    "mkdir -p /usr/share/fonts/opentype/xcharter && cd /tmp && curl -sL -o x.zip https://mirrors.ctan.org/fonts/xcharter.zip "
    "&& unzip -q x.zip && cp xcharter/opentype/XCharter-Roman.otf xcharter/opentype/XCharter-Bold.otf xcharter/opentype/XCharter-Italic.otf xcharter/opentype/XCharter-BoldItalic.otf /usr/share/fonts/opentype/xcharter/ && fc-cache -f")
app = modal.App("fof-pdf", image=image)
@app.function(timeout=600)
def convert(b: bytes) -> bytes:
    import subprocess, tempfile
    d = tempfile.mkdtemp(); open(f"{d}/report.docx", "wb").write(b)
    subprocess.run(["soffice", "--headless", "--convert-to", "pdf", "--outdir", d, f"{d}/report.docx"], check=True, capture_output=True)
    return open(f"{d}/report.pdf", "rb").read()
@app.local_entrypoint()
def main(src: str = "report/out/report.docx"):
    pdf = convert.remote(open(src, "rb").read()); out = src.replace(".docx", ".pdf"); open(out, "wb").write(pdf); print("saved", out, len(pdf))
