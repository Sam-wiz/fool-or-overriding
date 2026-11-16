# Modal runner for models added after the review (new). No volumes: results come back as bytes.
#   full: the paper's v2 pipeline (+ matched random steering controls) -> v4 leak/pushback additions -> deep.py
#   t5  : base vs instruct, deep.py --raw on both checkpoints
# usage: MODAL_PROFILE=acctN modal run src/modal_new.py::full_main --model Qwen/Qwen2.5-7B-Instruct --tag qwen25-7b
import modal, io, os, subprocess, tarfile
image = (modal.Image.debian_slim(python_version="3.12")
         .pip_install("torch==2.8.0", "transformers>=5.0", "accelerate", "scikit-learn", "numpy", "peft", "sentencepiece", "protobuf")
         .add_local_dir(os.path.dirname(__file__), "/root/src")
         .add_local_dir(os.path.join(os.path.dirname(__file__), "..", "data"), "/root/data"))
app = modal.App("fof-new", image=image)
FILT = "grep --line-buffered -v -E 'Loading weights|Fetching|it/s]'"
def sh(cmd, log): subprocess.run(f"{cmd} 2>&1 | {FILT} | tee {log}", shell=True)
def pack():
    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode="w:gz") as tf:
        tf.add("/tmp/out", arcname=".", filter=lambda ti: None if ti.name.endswith(".npy") else ti)
    return buf.getvalue()

@app.function(gpu=os.environ.get("FOF_GPU", "A100-40GB"), timeout=4 * 3600)
def full(model: str, tag: str) -> bytes:
    for d in (f"v2-{tag}", f"v4-{tag}"): os.makedirs(f"/tmp/out/{d}", exist_ok=True)
    base = f"python /root/src/fof.py --model {model} --data /root/data --out /tmp/out"
    sh(f"{base} --tag v2-{tag} --phases act,gen,probe,nx,xsteer,xsteer2,push", f"/tmp/out/v2-{tag}/run.log")
    sh(f"{base} --tag v4-{tag} --anchor --phases act,gennew,nx,push2 --prev /tmp/out/v2-{tag}/rows.json", f"/tmp/out/v4-{tag}/run.log")
    sh(f"python /root/src/deep.py --model {model} --tag {tag} --data /root/data --out /tmp/out --bs 8 --tests act,grad,patch", f"/tmp/out/deep-{tag}.log")
    return pack()

@app.function(gpu=os.environ.get("FOF_GPU", "A100-40GB"), timeout=3 * 3600)
def t5(base_model: str, inst_model: str, tag: str) -> bytes:
    os.makedirs("/tmp/out", exist_ok=True)
    for m, t in ((base_model, f"{tag}-base-raw"), (inst_model, f"{tag}-inst-raw")):
        sh(f"python /root/src/deep.py --model {m} --tag {t} --raw --data /root/data --out /tmp/out --bs 8 --tests act", f"/tmp/out/deep-{t}.log")
    return pack()

@app.function(gpu=os.environ.get("FOF_GPU", "A100-40GB"), timeout=3 * 3600)
def steer(model: str, tag: str, layer: int, adapter: str = "") -> bytes:
    # post-review: matched-control steering at the first X-valid layer >= n_layers//2
    os.makedirs(f"/tmp/out/v5-{tag}", exist_ok=True); ad = f"--adapter {adapter}" if adapter else ""
    sh(f"python /root/src/fof.py --model {model} {ad} --data /root/data --out /tmp/out --tag v5-{tag} --phases act,xsteer2 --steer_layer {layer}",
       f"/tmp/out/v5-{tag}/run.log")
    return pack()

def _save(b, tag):
    tarfile.open(fileobj=io.BytesIO(b), mode="r:gz").extractall(os.path.join(os.path.dirname(__file__), "..", "results"))
    print("saved", tag, len(b))

@app.local_entrypoint()
def full_main(model: str, tag: str): _save(full.remote(model, tag), tag)

@app.local_entrypoint()
def t5_main(base_model: str, inst_model: str, tag: str): _save(t5.remote(base_model, inst_model, tag), tag)

@app.local_entrypoint()
def steer_main(model: str, tag: str, layer: int, adapter: str = ""): _save(steer.remote(model, tag, layer, adapter), tag)
