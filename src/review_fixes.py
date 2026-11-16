# Review-driven statistics (per-layer CI rule, steering-layer validity, monitor at 3/4 depth, accuracy, pushback gaps).
# usage: python src/review_fixes.py  -> results/review_fixes.json
import json, numpy as np, sys
sys.path.insert(0,'src')
from analyze import load, parse_semantic, prob
from sklearn.metrics import roc_auc_score
import os
ORDER=[t for t in ["qwen3-14b","llama31-8b","qwen3-8b","qwen3-4b","qwen25-3b","gemma2-9b","gate-3b","qwen25-7b","mistral-7b","llama32-3b"] if os.path.exists(f"results/v2-{t}/v2summary.json")]
out={}
for t in ORDER:
    d=f"results/v2-{t}"; sc=json.load(open(f"{d}/layerscan.json")); NL=json.load(open(f"{d}/v2summary.json"))["NL"]
    o={}
    # (a) pre-registered per-layer CI rule over valid deep layers
    for p in ("X_dm","N_dm_crossfit"):
        c={"Overriding":0,"Mixed":0,"Fooled":0}
        for L,v in sc["layers"].items():
            v=v[p]
            if not v["valid"] or int(L)/NL<0.5: continue
            lo,hi=v["FI_L2"]["ci"]
            c["Overriding" if hi<0.25 else "Fooled" if lo>0.5 else "Mixed"]+=1
        o["ci_rule_"+p]=c
        # max FI among valid deep layers
        fis=[v[p]["FI_L2"]["point"] for L,v in sc["layers"].items() if v[p]["valid"] and int(L)/NL>=0.5]
        o["maxFI_"+p]=max(fis) if fis else None
    # (b) validity of X at steering layer NL//2
    v=sc["layers"][str(NL//2)]["X_dm"]; o["steer_layer"]=NL//2; o["steer_layer_valid"]=v["valid"]; o["steer_layer_FI"]=v["FI_L2"]["point"]; o["steer_layer_pc"]=v["posctrl_know_L0_L2"]["point"]
    # (c) monitor at 3NL//4 with X direction (cached acts_sel)
    meta,rows=load(d); sel=meta["probe"]["sel_layers"]; L3=(3*NL)//4
    if os.path.exists(f"{d}/acts_sel.npy"):  # not returned for the three post-review models
        A=np.load(f"{d}/acts_sel.npy").astype(np.float32); X=A[:, sel.index(L3)]
        xi=[i for i,r in enumerate(rows) if r["set"]=="xfer" and r["level"]=="L2"]; y=np.array([rows[i]["label"] for i in xi])
        u=X[xi][y==1].mean(0)-X[xi][y==0].mean(0); s=X@u/(u@u)
        ans=[i for i,r in enumerate(rows) if r["set"] in("nse","flag") and r.get("decision")=="ANSWER"]
        yb=[rows[i]["label"] for i in ans]
        o["monitor_L3"]=dict(layer=L3, valid=sc["layers"][str(L3)]["X_dm"]["valid"], xprobe=float(roc_auc_score(yb,[s[i] for i in ans])) if len(set(yb))==2 else None)
    else: o["monitor_L3"]=None
    # (d) know L2 accuracy unsteered
    kn=[r for r in rows if r["set"]=="nse" and r["label"]==0 and r["level"]=="L2" and r.get("decision")=="ANSWER" and r.get("prob_yes") is not None]
    o["know_L2_acc"]=float(np.mean([(r["prob_yes"]>50)==r["gold"] for r in kn])) if kn else None
    # (e) ask P(unk) means
    o["ask_unk_L2"]=float(np.mean([r["ask_unk"] for r in rows if r["set"]=="nse" and r["label"]==1 and r["level"]=="L2"]))
    o["ask_unk_L2fab"]=float(np.mean([r["ask_unk"] for r in rows if r["set"]=="nse" and r["label"]==1 and r["level"]=="L2fab"]))
    o["ask_unk_min_item"]=float(min(r["ask_unk"] for r in rows if r["set"]=="nse" and r["label"]==1 and r["level"] in ("L2","L2fab")))
    # (f) pushback: x shift of unknowable vs knowable, in class-gap units
    P=json.load(open(f"{d}/push.json")); idr={r["iid"]:r for r in rows}
    g=lambda arm,lv,k: float(np.mean([p[k] for p in P if idr[p["iid"]]["level"]==lv and (idr[p["iid"]]["label"]==(arm=="unk"))]))
    o["push_x"]=dict(unk_before=g("unk","L2","x_before"),unk_after=g("unk","L2","x_after"),know_before=g("know","L2","x_before"),know_after=g("know","L2","x_after"))
    o["push_x"]["gap_before"]=o["push_x"]["unk_before"]-o["push_x"]["know_before"]; o["push_x"]["gap_after"]=o["push_x"]["unk_after"]-o["push_x"]["know_after"]
    # (g) pushback know L2 correct answers abandoned (among correct)
    tot=0;ab=0
    for p in P:
        r=idr[p["iid"]]
        if r["label"]==0 and r["level"]=="L2" and r.get("decision")=="ANSWER" and r.get("prob_yes") is not None and (r["prob_yes"]>50)==r["gold"]:
            tot+=1; ab+= parse_semantic(p["text"])!="ANSWER"
    o["push_correct_abandoned"]=(ab,tot)
    out[t]=o
    print(t, json.dumps({k:(round(v,3) if isinstance(v,float) else v) for k,v in o.items() if k!="push_x"}), {k:round(v,2) for k,v in o["push_x"].items()})
json.dump(out,open("results/review_fixes.json","w"),indent=1)
