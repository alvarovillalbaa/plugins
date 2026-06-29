# Quantitative Methods Reference

Reference for financial modeling, scenario analysis, and statistical methods applied to financial data. Make every model auditable: explicit assumptions, visible formulas, labeled units and periods. Never present a black-box number.

## Modeling principles

- **Separate inputs, calculations, and outputs.** Assumptions in one place, formulas reference them, outputs read-only. Never hardcode a number inside a formula.
- **One driver, one cell.** Each assumption lives once and flows everywhere; change it in a single place.
- **Label everything** — units, currency, period, basis. Ambiguous units are the top source of model error.
- **Build for sensitivity.** A model you can't flex on key drivers is a snapshot, not a model.
- **Sanity-check magnitudes.** Compare outputs to actuals, benchmarks, or back-of-envelope estimates before trusting them.
- **Document the logic.** A reviewer should reconstruct the result from assumptions alone.

## Financial modeling building blocks

### Driver-based revenue model
Model the engine, not just a growth %:
```
Revenue = Volume × Price
Volume  = f(funnel: traffic × conversion, or accounts × seats, or units sold)
```
Bottoms-up (capacity/funnel-driven) beats tops-down (% of TAM) for operating decisions.

### Three-statement linkage
P&L → cash flow → balance sheet must tie:
- Net income flows to retained earnings and is the start of CFO.
- Working-capital changes (ΔAR, ΔInventory, ΔAP) bridge net income to CFO.
- Capex hits CFI and builds PP&E; depreciation is non-cash add-back.
- Financing flows change debt/equity and cash. **Balance sheet must balance** — it's the integrity check.

### Cohort modeling
For retention/subscription businesses, model by cohort:
- Each acquisition cohort retains/expands on its own curve.
- Aggregate = sum of cohorts at their respective ages.
- Reveals whether growth is durable (improving cohorts) or treadmill (new logos masking churn).

## Time value of money

| Concept | Formula |
| --- | --- |
| Future value | FV = PV × (1 + r)^n |
| Present value | PV = FV / (1 + r)^n |
| NPV | Σ CFₜ / (1 + r)^t − initial outlay |
| IRR | rate where NPV = 0 |
| Perpetuity | CF / r |
| Growing perpetuity | CF / (r − g) |
| Annuity PV | CF × [1 − (1+r)^−n] / r |

- **Discount rate (r)** = cost of capital (WACC for the firm, or required return).
- **Decision rules**: take projects with NPV > 0; IRR > hurdle rate. Beware IRR with non-conventional cash flows (multiple sign changes → multiple IRRs).

## Scenario & sensitivity analysis

Three complementary techniques:

1. **Scenario analysis** — coherent bundles of assumptions (base / bull / bear). Change several drivers together to tell a story.
2. **Sensitivity (one-way)** — flex one driver across a range, hold others; find what the output is most exposed to.
3. **Two-way data table** — two drivers on a grid (e.g., growth × margin → valuation).

Best practice:
- Identify the 2–3 drivers that move the output most; focus analysis there.
- Express ranges as low/base/high with a stated rationale, not arbitrary ±10%.
- Report the **break-even** value of key drivers (the growth rate that yields NPV = 0, the churn that kills LTV/CAC).

### Monte Carlo (when distributions matter)
- Assign probability distributions to uncertain inputs, sample thousands of runs, read the output distribution.
- Reports P10/P50/P90 outcomes and probability of hitting a target — richer than point scenarios.
- Caution: output is only as good as the input distributions and assumed correlations. Don't imply false precision.

## Statistical methods for financial data

### Descriptive
- **Central tendency**: mean vs. median — use median for skewed data (deal sizes, revenue per customer often right-skewed).
- **Dispersion**: standard deviation, variance, coefficient of variation (σ/μ for comparing volatility across scales).
- **Distribution shape**: skew and kurtosis; financial returns are fat-tailed — normal assumptions understate tail risk.

### Relationships
- **Correlation** (−1 to 1): co-movement strength. **Correlation ≠ causation.** Watch for spurious correlation and confounders.
- **Linear regression**: y = β₀ + β₁x + ε. Read R² (variance explained), coefficient sign/size, and p-values. Don't over-trust low-n or extrapolate beyond the data range.
- **Multiple regression**: multiple drivers; watch multicollinearity (correlated predictors inflate uncertainty).

### Time series
- **Trend / seasonality / cycle / noise** decomposition.
- **Moving averages & smoothing** for noisy series; **YoY** to strip seasonality.
- **Growth rates**: CAGR = (End/Start)^(1/years) − 1 for compounding; avoid averaging period growth rates (use geometric mean).
- Don't forecast far past the pattern's stability; recent regime changes break historical models.

### Portfolio / risk metrics
- **Expected return**: probability-weighted average.
- **Volatility**: standard deviation of returns.
- **Sharpe ratio** = (return − risk-free) / volatility → return per unit of risk.
- **Value at Risk (VaR)**: loss not exceeded at a confidence level over a horizon (note: says nothing about tail beyond it).
- **Diversification**: portfolio variance depends on correlations, not just individual variances.

## Common pitfalls

- **Spurious precision** — reporting many decimals on a guess. Match precision to input quality.
- **Garbage in** — elegant model, fabricated inputs. Validate assumptions first.
- **Survivorship/selection bias** in historical data.
- **Overfitting** — a model tuned to past noise predicts poorly.
- **Ignoring correlation** in scenarios — drivers move together (a recession hits growth *and* churn *and* fundraising at once).
- **Linear extrapolation** of non-linear dynamics (saturation, network effects).
- **Confusing accounting profit with cash** — model both.

## Output discipline

State assumptions, units, period, and currency up front. Show the formula or method behind each output. Present ranges/scenarios, not false single-point certainty. Flag the drivers the result is most sensitive to. When inputs are weak, say so and give the break-even instead of a forecast.
