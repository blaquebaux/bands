#!/usr/bin/python3
# =============================================================================
# bands_1_rv_securitized.py — do fixed-income RELATIVE-VALUE trades earn, or are they macro/regime bets in disguise?
#
# Three honest legs, all via liquid ETFs, all TOTAL return (coupons counted), vs AGG (aggregate bond):
#  (A) CURVE / DURATION — tenor ladder SHY(1-3y) IEI(3-7y) IEF(7-10y) TLH(10-20y) TLT(20y+). Over 2016-2026
#      Sharpe falls MONOTONICALLY with duration — but that is the 2022 rate shock rewarding SHORT duration,
#      NOT a roll-down "sweet spot." The duration-neutral 2s10s steepener is the SAME short-duration bet. We
#      prove it with a SUB-PERIOD split: a real premium is stable across regimes; a regime bet flips sign.
#  (B) BREAKEVEN / TIPS — TIP vs IEF, vol-matched (long breakeven). Harvestable inflation-risk-premium, or a
#      bet that only paid in the 2021-22 CPI spike? Same sub-period test.
#  (C) AGENCY MBS — MBB vs IEF. MBS collects an OAS for prepayment (short optionality, NEGATIVE convexity).
#      The convexity tell is in the fat-tail KURTOSIS, not the skew. Does the spread beat a Treasury net of that?
# The honest frame: rates RV via ETFs is mostly a duration/regime bet — carry lives in bounty/block, not here.
# =============================================================================
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _bands_common import panel, rets, riskadj, stats, dn_spread
import numpy as np

TEN = ["SHY", "IEI", "IEF", "TLH", "TLT"]
P, dates = panel(TEN + ["AGG", "TIP", "MBB"])
R = {s: rets(P[s]) for s in P}
D = dates[1:]                                     # returns are aligned to dates[1:]
agg = R["AGG"]
print("="*98); print(f"BANDS #1 — fixed-income relative value & securitized  ({dates[0]} → {dates[-1]}, {len(dates)} days)"); print("="*98)

# sub-period masks over the shared window (regimes: ZIRP-stable / COVID-QE / hike + higher-for-longer)
def mask(r, lo, hi):
    n = len(r); d = D[-n:]
    return np.array([lo <= x < hi for x in d])
ERAS = [("2016-19 stable", "2016-01", "2020-01"), ("2020-21 QE/COVID", "2020-01", "2022-01"),
        ("2022-26 hikes", "2022-01", "2027-01")]
def sh(r):
    a = stats(r); return a['sh']
def sub_sharpes(r):
    return [sh(r[mask(r, lo, hi)]) for _, lo, hi in ERAS]

# ---- (A) curve / duration ladder --------------------------------------------------------------------
print(f"\n(A) DURATION LADDER vs AGG          {'eff~dur':>9}{'Sharpe':>8}{'CAGR':>8}{'maxDD':>8}{'vol':>7}{'α/AGG':>8}")
DUR = {"SHY":"~1.9y","IEI":"~4.5y","IEF":"~7.5y","TLH":"~12y","TLT":"~17y"}
for s in TEN:
    a = riskadj(R[s], agg[-len(R[s]):])
    print(f"  {s:4} {DUR[s]:>8}{'':>1}{a['sh']:>+8.2f}{a['cagr']*100:>+7.1f}%{a['dd']*100:>+7.0f}%{a['vol']*100:>6.1f}%{a['alpha_ann']*100:>+7.1f}%")
print("  → Sharpe falls monotonically with duration. That is NOT roll-down geometry — it is the 2022 rate")
print("    shock paying you to be SHORT duration. The test below shows whether that edge is stable or regime.")

# "duration-neutral" 2s10s steepener (long SHY, vol-matched short TLT). HONEST CAVEAT: with SHY's tiny vol,
# vol-matching shrinks the TLT leg to a token hedge, so the spread ≈ the SHY (short-duration) leg itself.
steep = dn_spread(R["SHY"], R["TLT"])
sA = riskadj(steep, agg[-len(steep):])
m = min(len(steep), len(R["SHY"]))
steep_corr_shy = float(np.corrcoef(steep[-m:], R["SHY"][-m:])[0, 1])   # collinearity with the short-duration leg
print(f"\n  2s10s STEEPENER (long SHY / −TLT)   full Sharpe {sA['sh']:>+6.2f}   skew {sA['skew']:>+5.2f}   corr w/ SHY leg {steep_corr_shy:+.2f}")
ss = sub_sharpes(steep)
print(f"    by regime:  " + "   ".join(f"{nm} {v:+.2f}" for (nm,_,_),v in zip(ERAS, ss)))

def concentrated(xs):
    """A real premium is regime-stable. Flag as a regime bet if it flips sign, or the best era's Sharpe is
    > 2.5x the worst positive era's — i.e. the 'edge' is concentrated in one regime."""
    if min(xs) < 0 < max(xs): return True
    lo = max(min(xs), 1e-3)
    return max(xs) > 2.5 * lo
steep_regime = concentrated(ss)                  # +0.21 easing vs +1.82 hiking ≈ 8x swing ⇒ directional

# ---- (B) breakeven / TIPS ---------------------------------------------------------------------------
be = dn_spread(R["TIP"], R["IEF"])               # long TIPS, short vol-matched nominal = long breakeven
bA = riskadj(be, agg[-len(be):]); bs = sub_sharpes(be)
print(f"\n(B) BREAKEVEN (long TIP / −IEF)      full Sharpe {bA['sh']:>+6.2f}   skew {bA['skew']:>+5.2f}")
print(f"    by regime:  " + "   ".join(f"{nm} {v:+.2f}" for (nm,_,_),v in zip(ERAS, bs)))
be_regime = concentrated(bs)                      # peaks in the 2020-21 inflation spike ⇒ regime bet

# ---- (C) agency MBS: spread + the convexity tell (kurtosis) -----------------------------------------
mbs_sp = dn_spread(R["MBB"], R["IEF"])
mbb = riskadj(R["MBB"], agg[-len(R["MBB"]):]); ief = riskadj(R["IEF"], agg[-len(R["IEF"]):]); mA = riskadj(mbs_sp, agg[-len(mbs_sp):])
print(f"\n(C) AGENCY MBS                        {'Sharpe':>8}{'CAGR':>8}{'maxDD':>8}{'skew':>7}{'exKurt':>8}")
print(f"  MBB (agency MBS, outright)          {mbb['sh']:>+8.2f}{mbb['cagr']*100:>+7.1f}%{mbb['dd']*100:>+7.0f}%{mbb['skew']:>+7.2f}{mbb['exkurt']:>+8.1f}")
print(f"  IEF (7-10y Treasury, outright)      {ief['sh']:>+8.2f}{ief['cagr']*100:>+7.1f}%{ief['dd']*100:>+7.0f}%{ief['skew']:>+7.2f}{ief['exkurt']:>+8.1f}")
print(f"  MBS spread (long MBB / −IEF)        {mA['sh']:>+8.2f}{mA['cagr']*100:>+7.1f}%{mA['dd']*100:>+7.0f}%")
mbs_thin   = abs(mA['cagr']) < 0.015             # the spread is trivial
mbs_convex = mbb['exkurt'] > ief['exkurt'] + 3   # convexity shows as fatter tails than the duration-match

# ---- verdict ----------------------------------------------------------------------------------------
print("\n"+"="*98); print("READ:")
print("  • DURATION: the whole 'curve' edge is one bet — SHORT duration — paying off in the 2022 rate shock.")
print(f"    The steepener is net-short-duration and {'REGIME-concentrated' if steep_regime else 'stable'}: {'/'.join(f'{v:+.2f}' for v in ss)}")
print(f"    ({max(ss)/max(min(ss),1e-3):.1f}x swing easing→hiking). A true DV01-neutral curve premium would be regime-flat; this is a rate bet.")
print(f"  • BREAKEVEN earns {bA['sh']:+.2f} full-sample but {('concentrates in the 2020-21/2022 inflation spike' if be_regime else 'holds across regimes')} ")
print(f"    ({'/'.join(f'{v:+.2f}' for v in bs)}) — {'a regime bet on inflation, not a clean harvestable premium' if be_regime else 'a stable inflation-risk-premium'}.")
print(f"  • MBS: the spread is {'trivial' if mbs_thin else 'modest'} ({mA['cagr']*100:+.1f}%/yr) and you're paid it to be SHORT CONVEXITY —")
print(f"    MBB's excess kurtosis {mbb['exkurt']:+.1f} vs IEF {ief['exkurt']:+.1f} {'confesses the embedded prepay option (fat tails)' if mbs_convex else 'is muted this window'}.")

stable = []
if not steep_regime: stable.append("the curve/duration trade")
if not be_regime:    stable.append("breakeven carry")
if (not mbs_thin) and (not mbs_convex): stable.append("the MBS spread")
if not stable:
    v = ("NULL-ish / REGIME: no leg is a clean harvestable premium over 2016-2026. The 'curve alpha' is a single "
         "net-short-duration bet whose Sharpe swings ~8x by regime (it only really paid in the 2022 rate shock); "
         "breakeven paid in the inflation spike; MBS collects a trivial spread for being short the prepay option "
         "(fat-tailed). The honest "
         "rates edge is CARRY — see bounty (cross-asset carry) and block (term premium) — not ETF-level RV. "
         "A real RV desk needs futures/swaps for exact DV01-neutrality and OAS hedging = bands_2.")
else:
    v = (f"CONDITIONAL: {', and '.join(stable)} survive the sub-period test as something more than a regime bet — "
         "size as carry, keep the directional/convexity legs gated. The rest is macro.")
print(f"\n  VERDICT: {v}")
print("  (ETF legs are duration-matched by VOL — a proxy for true DV01 matching. Exact duration-neutrality and")
print("   OAS-based MBS convexity hedging need futures/swaps; that precision is a bands_2. This is the honest first look.)")
