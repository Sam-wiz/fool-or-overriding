import subprocess, os
M = "unsloth/Llama-3.3-70B-Instruct-bnb-4bit"
with open("/content/b70.log", "a") as f:
    subprocess.run("pip install -q -U bitsandbytes datasets", shell=True, stdout=f, stderr=subprocess.STDOUT)
    base = dict(os.environ, DATA="/content/fo_data_small.json", MODELS=M, TOKENIZERS_PARALLELISM="false",
                PYTORCH_CUDA_ALLOC_CONF="expandable_segments:True")
    rc = subprocess.run(["python", "/content/bnb_wrap.py", "run"], env=dict(base, OUT="/content/b70_main", LIMIT="0", STEER="0", BS="4"),
                        stdout=f, stderr=subprocess.STDOUT, cwd="/content").returncode
    f.write(f"MAIN_END rc={rc}\n"); f.flush()
    rc = subprocess.run(["python", "/content/bnb_wrap.py", "jlens"], env=dict(base, OUT="/content/b70_jlens", BS="2", NCORP="32", NFD="8", SEQ="128"),
                        stdout=f, stderr=subprocess.STDOUT, cwd="/content").returncode
    f.write(f"JL_END rc={rc}\n")
print("finished")
