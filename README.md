# Blaque Baux Bands

**Fixed-income relative value & securitized — curve shape, breakeven/TIPS, agency MBS. Via ETFs: a regime bet, not a premium.**

Bands probes the rates white space the family's carry work (bounty, block) doesn't reach: the **relative-value**
and **securitized** trades — "stacks of an asset class." The honest first pass uses liquid Treasury/credit ETFs,
and the finding is a clean one: at the ETF level, what *looks* like curve alpha is a single short-duration bet
that happened to win the 2016–2026 rate cycle.

> **Not investment advice.** Educational/research software. See [DISCLAIMER](DISCLAIMER.md) and [LICENSE](LICENSE).

```bash
python3 research/bands_1_rv_securitized.py   # needs Alpaca data keys in the environment
```

## The finding (honest null / regime)

[`research/bands_1_rv_securitized.py`](research/bands_1_rv_securitized.py) — three legs, all TOTAL return vs AGG,
each put through a **sub-period split** (stable / QE-COVID / hiking) because a real premium is regime-flat and a
regime bet is not.

**(A) Duration ladder** — Sharpe falls *monotonically* with maturity:

| tenor | eff. dur | Sharpe | maxDD |
|---|---|---|---|
| SHY | ~1.9y | **+1.08** | −6% |
| IEI | ~4.5y | +0.40 | −15% |
| IEF | ~7.5y | +0.19 | −24% |
| TLH | ~12y | +0.02 | −41% |
| TLT | ~17y | +0.01 | −48% |

That is **not** a roll-down "sweet spot" — it's the 2022 rate shock paying you to be short duration. The
"duration-neutral" 2s10s steepener is the same bet: positive every era but with an **8.6× Sharpe swing**
(+0.21 easing → +1.82 hiking). A DV01-neutral curve *premium* would be regime-flat; this is a rate view.

**(B) Breakeven** (long TIP / −IEF, vol-matched): +0.47 full-sample but concentrated in the 2020–21/2022
inflation spike (regime Sharpes +0.31 / +0.94 / +0.30), skew −1.04 — an inflation bet, not a clean premium.

**(C) Agency MBS** (MBB vs IEF): the spread is trivial (+0.5%/yr) and you collect it for being **short convexity** —
MBB's excess kurtosis **+11.4** vs IEF's +3.3 confesses the embedded prepayment option (fat tails, not free carry).

## Verdict

**NULL-ish / REGIME — no ETF leg is a clean harvestable RV premium over 2016–2026.** The "curve alpha" is one
net-short-duration bet that only really paid in the 2022 shock; breakeven paid in the inflation spike; MBS pays a
pittance for short optionality. The honest rates edge is **carry** — already covered by `bounty` (cross-asset
carry) and `block` (term premium) — not ETF-level relative value. A real RV desk gets DV01-neutrality and
OAS-based MBS hedging from **futures and swaps**, which ETFs can't replicate; that precision is a `bands_2`. This
is the honest first look, and it says the ETF white space here is thinner than it appears.

## Status

**Research.** Honest null/regime finding — a mapped-and-closed white space, in the family tradition where the red
scorecard is the point. Fat-tail scorecard (Sharpe / CAGR / maxDD / skew / excess-kurtosis / Jensen's α / M²),
Alpaca SIP daily total return, causal, sub-period-validated. No live capital.
