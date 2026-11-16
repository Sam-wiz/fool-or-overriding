# Modal runner (new sprint work). No volumes: results are returned as bytes and written locally.
# usage: MODAL_PROFILE=acctN modal run src/modal_run.py --model unsloth/gemma-2-9b-it --tag gemma2-9b
import modal, io, os, subprocess, tarfile

image = (modal.Image.debian_slim(python_version="3.12")
         .pip_install("torch==2.8.0", "transformers>=5.0", "accelerate", "scikit-learn", "numpy", "peft")
         .add_local_dir(os.path.join(os.path.dirname(__file__)), "/root/src")
         .add_local_dir(os.path.join(os.path.dirname(__file__), "..", "data"), "/root/data")
         .add_local_dir(os.path.join(os.path.dirname(__file__), "..", "prev"), "/root/prev"))
app = modal.App("fof-sprint", image=image)

@app.function(gpu=os.environ.get("FOF_GPU", "A100-40GB"), timeout=3 * 3600)
def run(model: str, tag: str, extra: str = "") -> bytes:
    cmd = f"python /root/src/fof.py --model {model} --tag {tag} --data /root/data --out /tmp/out {extra}"
    os.makedirs(f"/tmp/out/{tag}", exist_ok=True)
    subprocess.run(cmd + f" 2>&1 | grep --line-buffered -v -E 'Loading weights|Fetching|it/s]' | tee /tmp/out/{tag}/run.log", shell=True)
    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode="w:gz") as tf:
        tf.add(f"/tmp/out/{tag}", arcname=tag, filter=lambda ti: None if ti.name.endswith("/acts.npy") else ti)
    return buf.getvalue()

@app.local_entrypoint()
def main(model: str, tag: str, extra: str = ""):
    b = run.remote(model, tag, extra)
    dst = os.path.join(os.path.dirname(__file__), "..", "results")
    os.makedirs(dst, exist_ok=True)
    tarfile.open(fileobj=io.BytesIO(b), mode="r:gz").extractall(dst)
    print("saved", tag, len(b), "bytes")
