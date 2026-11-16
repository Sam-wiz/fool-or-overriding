import subprocess, os
models = open("/content/jl_models.txt").read().strip()
env = dict(os.environ, DATA="/content/fo_data2.json", OUT="/content/jlens", BS="4", NCORP="64", NFD="16", SEQ="128",
           TOKENIZERS_PARALLELISM="false", MODELS=models, PYTORCH_CUDA_ALLOC_CONF="expandable_segments:True")
subprocess.run(["pip", "install", "-q", "datasets"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
with open("/content/jl.log", "a") as f:
    rc = subprocess.run(["python", "/content/fo_jlens.py"], env=env, stdout=f, stderr=subprocess.STDOUT).returncode
print("finished rc", rc)
