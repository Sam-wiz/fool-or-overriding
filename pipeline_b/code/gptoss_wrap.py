"""Run fo_run / fo_jlens on openai/gpt-oss-120b (harmony chat format).
The prompt goes in one user turn as for every other model; the assistant turn is opened directly on the 'final' channel
(reasoning_effort=low, analysis channel skipped) so the decision prefix sits where the visible answer starts."""
import sys
import fo_run as F

def chat_ids(tok, text):
    s = tok.apply_chat_template([{"role": "user", "content": text}], tokenize=False, add_generation_prompt=True,
                                reasoning_effort="low")
    s += "<|channel|>final<|message|>"
    return tok(s, add_special_tokens=False).input_ids

F.chat_ids = chat_ids
if sys.argv[1] == "run":
    F.main()
else:
    import fo_jlens as J
    J.F.chat_ids = chat_ids
    J.main()
