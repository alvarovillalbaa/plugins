# Financial Fundamentals Reference

Reference for fundamental company analysis: statement structure, unit economics, valuation inputs, and business-quality assessment. Use repo-local company facts (entity, fiscal calendar, accounts) over any defaults here. Always state period, currency, and basis (cash vs. accrual).

## The three statements

### Income statement (P&L) — a period
Measures profitability over a window (month/quarter/year).

```
Revenue
− COGS                      → Gross profit        (Gross margin %)
− Operating expenses (S&M, R&D, G&A)
                            → Operating income / EBIT  (Operating margin %)
± Interest, other
− Taxes
                            → Net income          (Net margin %)
```
- **Gross margin** = Gross profit / Revenue → pricing power & cost of delivery.
- **Operating margin** = EBIT / Revenue → core operating efficiency.
- **EBITDA** = EBIT + D&A → rough cash proxy; useful for comparison, but not a substitute for cash flow.

### Balance sheet — a point in time
Snapshot of what's owned and owed. **Assets = Liabilities + Equity.**
- Assets: current (cash, AR, inventory, prepaids) + non-current (PP&E, intangibles, goodwill).
- Liabilities: current (AP, accrued, deferred revenue, short-term debt) + non-current (long-term debt).
- Equity: paid-in capital + retained earnings − treasury.

### Cash flow statement — a period
Reconciles net income to actual cash. Three sections:
- **CFO (operating)** — cash from running the business. Most important for quality.
- **CFI (investing)** — capex, acquisitions, asset sales.
- **CFF (financing)** — debt, equity raises, dividends, buybacks.
- **Free cash flow (FCF)** = CFO − capex. The number that compounds enterprise value.

Why all three: a company can show accounting profit while burning cash (or vice versa). Tie net income → CFO via working-capital changes to catch this.

## Unit economics

The per-customer or per-unit version of the P&L — the engine beneath aggregate numbers.

| Metric | Formula | Reads as |
| --- | --- | --- |
| CAC | Fully-loaded S&M / new customers | Cost to acquire |
| ACV / ARPA | Annual contract value per account | Revenue density |
| Gross margin per unit | (Price − variable cost) / Price | Contribution |
| LTV | (ARPA × gross margin %) / churn rate | Lifetime value |
| LTV/CAC | LTV ÷ CAC | ≥3x healthy; <1 unsustainable |
| CAC payback | CAC / (ARPA × gross margin % per month) | Months to recoup; <12 strong for SaaS |
| Churn / retention | Lost / start; gross vs. net revenue retention | NRR >100% = expansion engine |
| Magic number | Net new ARR / prior-period S&M | Sales efficiency; >0.75 good |
| Burn multiple | Net burn / net new ARR | <1 great, >2 inefficient |
| Rule of 40 | Growth % + profit (or FCF) margin % | ≥40 healthy for scaled SaaS |

Watch for: blended CAC hiding paid-vs-organic mix, LTV using revenue instead of gross profit, cohort churn masked by new-logo growth.

## Financial ratios

**Liquidity** — can it pay near-term bills?
- Current ratio = current assets / current liabilities (>1).
- Quick ratio = (current assets − inventory) / current liabilities.

**Leverage / solvency** — debt load and coverage.
- Debt/equity = total debt / equity.
- Interest coverage = EBIT / interest expense (>3 comfortable).
- Net debt = total debt − cash.

**Profitability** — returns on capital.
- ROE = net income / equity. ROA = net income / assets.
- ROIC = NOPAT / invested capital → does it earn above its cost of capital?

**Efficiency** — working-capital turns.
- DSO (days sales outstanding), DPO (days payable), DIO (days inventory).
- Cash conversion cycle = DSO + DIO − DPO (lower = less cash tied up).

## Valuation inputs

Fundamentals feed valuation; they aren't the valuation. Common multiples:
- **EV/Revenue** — early/high-growth, pre-profit. Pair with growth + gross margin.
- **EV/EBITDA** — scaled, profitable; capital-structure-neutral.
- **P/E** — mature, steady earnings.
- **EV/FCF or FCF yield** — cash-generative businesses.

Enterprise value = equity value + net debt. Use EV multiples with operating metrics (revenue/EBITDA), equity multiples (P/E) with net income.

**DCF essentials:** project FCF → discount at WACC → add terminal value (perpetuity growth or exit multiple). Sensitive to discount rate and terminal assumptions — always run a range, never a single point.

## Business-quality assessment

Beyond the numbers, judge durability:
- **Revenue quality**: recurring vs. one-time, concentration (top-customer %), contracted vs. usage, deferred revenue trend.
- **Margin trajectory**: improving with scale, or structurally capped?
- **Moat**: switching costs, network effects, scale economics, brand, IP.
- **Capital intensity**: how much reinvestment per dollar of growth (capex + working capital)?
- **Management/accounting hygiene**: aggressive revenue recognition, growing gap between net income and CFO, frequent one-offs, related-party items.

## Red flags checklist

- Net income rising while CFO falls (earnings quality).
- AR growing faster than revenue (collection or channel-stuffing risk).
- Gross margin declining as revenue grows (pricing/mix erosion).
- Rising days-inventory or deferred-revenue burn-down (demand softening).
- Heavy reliance on non-GAAP/adjusted figures that exclude recurring costs.
- Customer concentration above ~20% in one account.
- Capitalizing costs that peers expense.

## Output discipline

State the period, currency, and accounting basis. Source every figure to a statement line or model cell. Separate actuals from estimates. Show the formula behind derived ratios. When data is missing, name the gap rather than guessing.
