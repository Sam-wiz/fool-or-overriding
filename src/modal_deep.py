# Modal runner for the post-review experiments (new). No volumes: results come back as bytes.
# Runs fof.py (leak anchors under the paper's X/N layer scan + neutral pushback) then deep.py (graded leakage,
# matched pairs, read-out gain, patching) in one container.
# usage: MODAL_PROFILE=acctN FOF_GPU=A100-80GB modal run src/modal_deep.py --model Qwen/Qwen3-4B --tag qwen3-4b
import modal, io, os, subprocess, tarfile
image = (modal.Image.debian_slim(python_version="3.12")
         .pip_install("torch==2.8.0", "transformers>=5.0", "accelerate", "scikit-learn", "numpy", "peft")
         .add_local_dir(os.path.dirname(__file__), "/root/src")
         .add_local_dir(os.path.join(os.path.dirname(__file__), "..", "data"), "/root/data")
         .add_local_dir(os.path.join(os.path.dirname(__file__), "..", "prev"), "/root/prev"))
app = modal.App("fof-deep", image=image)
FILT = "grep --line-buffered -v -E 'Loading weights|Fetching|it/s]'"

@app.function(gpu=os.environ.get("FOF_GPU", "A100-40GB"), timeout=3 * 3600)
def run(model: str, tag: str, adapter: str = "") -> bytes:
    ad = f"--adapter {adapter}" if adapter else ""
    os.makedirs(f"/tmp/out/v4-{tag}", exist_ok=True); os.makedirs("/tmp/res", exist_ok=True)
    subprocess.run(f"python /root/src/fof.py --model {model} --tag v4-{tag} {ad} --data /root/data --out /tmp/out --anchor "
                   f"--phases act,gennew,nx,push2 --prev /root/prev/{tag}.json 2>&1 | {FILT} | tee /tmp/out/v4-{tag}/run.log", shell=True)
    subprocess.run(f"python /root/src/deep.py --model {model} --tag {tag} {ad} --data /root/data --out /tmp/out --bs 8 "
                   f"--tests act,grad,patch 2>&1 | {FILT} | tee /tmp/out/deep-{tag}.log", shell=True)
    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode="w:gz") as tf:
        tf.add("/tmp/out", arcname=".", filter=lambda ti: None if ti.name.endswith(".npy") else ti)
    return buf.getvalue()

@app.local_entrypoint()
def main(model: str, tag: str, adapter: str = ""):
    b = run.remote(model, tag, adapter)
    tarfile.open(fileobj=io.BytesIO(b), mode="r:gz").extractall(os.path.join(os.path.dirname(__file__), "..", "results"))
    print("saved", tag, len(b))
