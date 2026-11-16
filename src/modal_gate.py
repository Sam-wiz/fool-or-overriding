# Modal: train the gate then run fof.py on it (new sprint glue). No volumes.
import modal, io, os, subprocess, tarfile
image = (modal.Image.debian_slim(python_version="3.12")
         .pip_install("torch==2.8.0", "transformers>=5.0", "accelerate", "scikit-learn", "numpy", "peft", "datasets")
         .add_local_dir(os.path.dirname(__file__), "/root/src")
         .add_local_dir(os.path.join(os.path.dirname(__file__), "..", "data"), "/root/data"))
app = modal.App("fof-gate", image=image)

@app.function(gpu="A100-40GB", timeout=3 * 3600)
def run(tag: str) -> bytes:
    os.makedirs(f"/tmp/out/{tag}", exist_ok=True)
    subprocess.run("python /root/src/train_gate.py /tmp/gate /root/data 2>&1 | grep --line-buffered -v -E 'it/s]' | tee /tmp/train.log", shell=True)
    subprocess.run(f"python /root/src/fof.py --model Qwen/Qwen2.5-3B-Instruct --adapter /tmp/gate --tag {tag} --data /root/data --out /tmp/out 2>&1 | grep --line-buffered -v -E 'Loading weights|Fetching|it/s]' | tee /tmp/out/{tag}/run.log", shell=True)
    subprocess.run(f"cp /tmp/train.log /tmp/out/{tag}/train.log", shell=True)
    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode="w:gz") as tf:
        tf.add(f"/tmp/out/{tag}", arcname=tag, filter=lambda ti: None if ti.name.endswith("/acts.npy") else ti)
        if os.path.exists("/tmp/gate"): tf.add("/tmp/gate", arcname=f"{tag}/adapter")
    return buf.getvalue()

@app.local_entrypoint()
def main(tag: str = "gate-3b"):
    b = run.remote(tag)
    tarfile.open(fileobj=io.BytesIO(b), mode="r:gz").extractall(os.path.join(os.path.dirname(__file__), "..", "results"))
    print("saved", tag, len(b))
