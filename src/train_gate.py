# Re-train the paper's SFT-2 gate (Aggarwal 2026 recipe, reused from PREEXISTING_upstream_sft2.py, MIT)
# in bf16 on an A100, then save the LoRA adapter.  New sprint glue code only.
import os, sys, json, random, torch
SEED = int(os.environ.get("SEED", "0")); OUTD = sys.argv[1]; DATA = sys.argv[2]
src = open(os.path.join(os.path.dirname(__file__), "PREEXISTING_upstream_sft2.py")).read()
src = src.split("def train():")[0].replace('os.environ["CUDA_VISIBLE_DEVICES"] = "0"', "")
g = {"__name__": "upstream"}; exec(src, g)
from datasets import Dataset
from transformers import AutoModelForCausalLM, AutoTokenizer, Trainer, TrainingArguments, DataCollatorForSeq2Seq
from peft import LoraConfig, get_peft_model
MODEL = "Qwen/Qwen2.5-3B-Instruct"; rng = random.Random(SEED)
tok = AutoTokenizer.from_pretrained(MODEL); tok.pad_token = tok.pad_token or tok.eos_token
model = AutoModelForCausalLM.from_pretrained(MODEL, dtype=torch.bfloat16, device_map={"": 0})
model.gradient_checkpointing_enable(); model.enable_input_require_grads()
model = get_peft_model(model, LoraConfig(r=32, lora_alpha=64, target_modules=["q_proj", "k_proj", "v_proj", "o_proj"], task_type="CAUSAL_LM"))
cases = json.load(open(os.path.join(DATA, "knowability_train.json")))
rows = []
for c in cases:
    unk = c["label"] == "unknowable"; sed = bool(c.get("evidenceL2")) and unk
    ev = g["enrich_panel"](c, rng) if (sed and rng.random() < 0.5) else None
    if unk:
        for fr in (g["TOOLF"] if sed else rng.sample(g["TOOLF"], 2)): rows.append((fr(c, ev), g["gold_completion"](c)))
        for fr in rng.sample(g["PLAIN"], 2): rows.append((fr(c, ev), g["gold_completion"](c)))
    else:
        for fr in rng.sample(g["PLAIN"] + g["TOOLF"], 3): rows.append((fr(c), g["gold_completion"](c)))
rng.shuffle(rows); print("rows", len(rows), flush=True)
def enc(pr, comp):
    p = tok(tok.apply_chat_template([{"role": "user", "content": pr}], add_generation_prompt=True, tokenize=False), add_special_tokens=False)["input_ids"]
    full = tok(tok.apply_chat_template([{"role": "user", "content": pr}, {"role": "assistant", "content": comp}], tokenize=False), add_special_tokens=False)["input_ids"][:768]
    lp = min(len(p), len(full))
    return {"input_ids": full, "attention_mask": [1] * len(full), "labels": [-100] * lp + full[lp:]}
ds = Dataset.from_list([enc(p, c) for p, c in rows])
args = TrainingArguments(output_dir="/tmp/gate_ckpt", per_device_train_batch_size=8, gradient_accumulation_steps=2,
                         num_train_epochs=3, learning_rate=2e-4, bf16=True, seed=SEED, logging_steps=25,
                         save_strategy="no", report_to="none", remove_unused_columns=False)
Trainer(model=model, args=args, train_dataset=ds, data_collator=DataCollatorForSeq2Seq(tok, padding=True, label_pad_token_id=-100)).train()
model.save_pretrained(OUTD); print("saved", OUTD)
