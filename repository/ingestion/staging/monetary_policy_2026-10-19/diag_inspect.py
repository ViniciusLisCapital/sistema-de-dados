"""Inspect specific failure modes in the diagnostic outputs."""
import re
import sys
from collections import Counter
from pathlib import Path

D = Path(sys.argv[1])

def raw(stem): return (D / f"{stem}.raw.md").read_text(encoding="utf-8")
def cln(stem): return (D / f"{stem}.clean.md").read_text(encoding="utf-8")

print("=== long tokens (run-together words) ===")
for stem in ["basic_nk_model_ch3 (Gali, 2015)", "information_effect_hf_identification (Nakamura & Steinsson, 2018)",
             "time_inconsistency_optimal_plans (Kydland & Prescott, 1977)", "credit_channel_transmission (Bernanke & Gertler, 1995)",
             "it_and_debt_brazil (Favero & Giavazzi, 2004)"]:
    toks = [t for t in re.findall(r"[A-Za-z]+", raw(stem)) if len(t) >= 18]
    print(f"\n{stem}: {len(toks)} long tokens; sample:", Counter(toks).most_common(8))

print("\n=== paragraph sample, Gali ch3 (page 3 area) ===")
print(raw("basic_nk_model_ch3 (Gali, 2015)")[6000:7200])
print("\n=== paragraph sample, Nakamura-Steinsson ===")
print(raw("information_effect_hf_identification (Nakamura & Steinsson, 2018)")[8000:9000])

print("\n=== what clean_code removed (biggest removals) ===")
for stem in ["forward_guidance_effects (Campbell et al., 2012)", "dilemma_not_trilemma (Rey, 2013)",
             "trilemma_tradeoffs (Obstfeld, 2015)", "it_credibility_fx_volatility (Minella et al., 2003)",
             "systematic_monetary_policy_forward_premium_puzzle (Tambakis & Tarashev, 2012)",
             "us_monetary_policy_global_cycle (Miranda-Agrippino & Rey, 2020)"]:
    r_lines = [l.strip() for l in raw(stem).splitlines() if l.strip()]
    c_set = Counter(l.strip() for l in cln(stem).splitlines() if l.strip())
    removed = []
    for l in r_lines:
        if c_set[l] > 0:
            c_set[l] -= 1
        else:
            removed.append(l)
    rem_chars = sum(len(l) for l in removed)
    # where does the References cut start, and what heading ended it
    rr = raw(stem).splitlines()
    ref_idx = [i for i, l in enumerate(rr) if re.match(r"^\s*(References?|Bibliography)\s*$", l, re.I)]
    print(f"\n{stem}: removed {len(removed)} lines / {rem_chars:,} chars; References heading at lines {ref_idx} of {len(rr)}")
    # removed lines that look like prose (long, with common words) = potential content loss
    prose = [l for l in removed if len(l) > 60 and re.search(r"\b(the|and|of|that)\b", l) and not re.search(r"\(\d{4}\)|\d{4}\.|Journal|Review|Working Paper|Economics", l)]
    print(f"   prose-like removed lines: {len(prose)}")
    for l in prose[:6]:
        print("     -", l[:150])
    # the removed repeated lines (running headers)
    rep = Counter(removed).most_common(4)
    print("   most repeated removed:", [(l[:70], n) for l, n in rep])
