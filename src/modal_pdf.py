# docx -> pdf with headless LibreOffice on Modal (no volumes). usage: modal run src/modal_pdf.py --src report/out/report.docx
import modal, os
image = modal.Image.debian_slim(python_version="3.12").apt_install("libreoffice-writer", "fonts-dejavu", "fonts-liberation", "fonts-crosextra-carlito", "fonts-crosextra-caladea", "fonts-noto-core")
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
