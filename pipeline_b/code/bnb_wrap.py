"""Run fo_run / fo_jlens on a pre-quantized 4-bit (bitsandbytes NF4) checkpoint: same code, the model loads in 4-bit."""
import sys, torch, transformers
_orig = transformers.AutoModelForCausalLM.from_pretrained.__func__
def fp(cls, name, *a, **kw):
    kw.pop("dtype", None)
    kw["quantization_config"] = transformers.BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_quant_type="nf4",
                                                                bnb_4bit_compute_dtype=torch.bfloat16)
    kw["dtype"] = torch.bfloat16
    return _orig(cls, name, *a, **kw)
transformers.AutoModelForCausalLM.from_pretrained = classmethod(fp)
import fo_run as F
if sys.argv[1] == "run":
    F.main()
else:
    import fo_jlens as J
    J.main()
