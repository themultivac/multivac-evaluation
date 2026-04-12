# Multivac Evaluation Report

**Evaluation ID:** EVAL-20260403-103635
**Timestamp:** 2026-04-03T10:36:35.549321
**Category:** Analysis & Research
**Model Pool:** 10 analysis-optimized models

## Question

A quantitative trading firm backtests a strategy: 15% annual return, Sharpe ratio 2.1, max drawdown 8%. They want to go live. (1) What could go wrong between backtest and live trading? List at least 5 risks. (2) The backtest used 5 years of data and tested 200 parameter combinations. Calculate the probability this outperformance is due to overfitting. (3) Design a live testing protocol that minimizes capital at risk while validating the strategy.

---

## Rankings

| Rank | Model | Score | Min | Max | Std Dev |
|------|-------|-------|-----|-----|---------|
| 1 | GPT-5.4 | 9.29 | 8.80 | 9.80 | 0.34 |
| 2 | Grok 4.20 | 8.52 | 7.00 | 9.55 | 0.87 |
| 3 | Claude Opus 4.6 | 7.67 | 4.95 | 9.20 | 1.52 |
| 4 | MiMo-V2-Flash | 7.55 | 5.10 | 9.00 | 1.30 |
| 5 | GPT-OSS-120B | 7.51 | 4.40 | 9.20 | 1.70 |
| 6 | DeepSeek V3 | 7.49 | 6.05 | 9.00 | 0.96 |
| 7 | Claude Sonnet 4.6 | 7.09 | 3.80 | 9.20 | 1.82 |
| 8 | Gemini 3.1 Pro | 2.65 | 0.85 | 5.45 | 1.69 |

---

## Meta Analysis

### Judge Strictness

| Rank | Judge | Avg Score Given |
|------|-------|-----------------|
| 1 | GPT-5.4 | 4.64 |
| 2 | Claude Opus 4.6 | 5.94 |
| 3 | GPT-OSS-120B | 6.44 |
| 4 | Grok 4.20 | 7.08 |
| 5 | MiniMax M2.5 | 7.30 |
| 6 | Claude Sonnet 4.6 | 7.31 |
| 7 | Gemini 3.1 Pro | 7.50 |
| 8 | MiMo-V2-Flash | 8.14 |
| 9 | Gemini 3 Flash Preview | 8.32 |
| 10 | DeepSeek V3 | 8.56 |

**Strictest Judge:** gpt_5_4
**Most Lenient Judge:** deepseek_v4
**Total Judgments:** 100
**Valid Judgments:** 74

---

## Model Pool

Models selected for **Analysis & Research** evaluation:

1. **Gemini 3.1 Pro** (openrouter)
2. **Claude Opus 4.6** (openrouter)
3. **GPT-5.4** (openrouter)
4. **DeepSeek V3** (openrouter)
5. **MiMo-V2-Flash** (openrouter)
6. **Claude Sonnet 4.6** (openrouter)
7. **Grok 4.20** (openrouter)
8. **GPT-OSS-120B** (openrouter)
9. **Gemini 3 Flash Preview** (openrouter)
10. **MiniMax M2.5** (openrouter)

---

## Model Responses

### Gemini 3.1 Pro

**Generation Time:** 18261ms
**Tokens:** 2149

```
 *Self-Correction/Nuance:* Wait, are the 200 trials *independent*? In parameter optimization, they are highly correlated (e.g., moving average 50 vs 51). If they are correlated, the effective number of independent trials $N_{eff} \ll 200$. This means the actual probability of overfitting is *even lower* than
```

### Claude Opus 4.6

**Generation Time:** 364984ms
**Tokens:** 2171

```
# From Backtest to Live Trading: Comprehensive Risk Analysis

## Part 1: What Could Go Wrong — Critical Risks

### The Backtest-to-Live Gap

The 15% return / 2.1 Sharpe / 8% max drawdown profile looks attractive on paper. Here's a systematic taxonomy of what breaks in production:

**Risk 1: Overfitting / Data Snooping Bias**
Testing 200 parameter combinations on 5 years of data virtually guarantees that the "best" parameter set captures noise, not signal. The reported Sharpe of 2.1 is the *maximum* over 200 trials — the true unconditional Sharpe is almost certainly much lower.

**Risk 2: Transaction Cost Underestimation**
Backtests typically use simplified cost models. In reality:
- Bid-ask spreads widen during the exact moments the strategy wants to trade (volatility events, news releases)
- Market impact: your own orders move the price, especially in less liquid instruments
- Slippage between signal generation and execution can be 5-50bps per trade
- A strategy trading frequently with a 2.1 Sharpe can easily become a 1.0 Sharpe strategy after realistic costs

**Risk 3: Survivorship and Look-Ahead Bias**
- If the backtest universe only includes stocks that *currently exist*, it excludes delistings and bankruptcies (survivorship bias)
- Fundamental data (earnings, book value) is often revised retroactively — the backtest may use data that wasn't available at the time (look-ahead bias)
- Index composition changes: backtesting on "current S&P 500 members" over 5 years is wrong because membership changed

**Risk 4: Regime Change / Non-Stationarity**
- The 5-year window (say 2019-2024) includes COVID crash, unprecedented monetary stimulus, rapid rate hikes, and AI mania — highly unusual regimes
- Market microstructure evolves: the strategy may exploit a pattern that was present historically but has been arbitraged away
- Correlation structures shift: a "diversified" strategy may become concentrated in a new regime

**Risk 5: Execution and Infrastructure Risk**
- Latency...
```

### GPT-5.4

**Generation Time:** 37200ms
**Tokens:** 2044

```
Here’s a practical way to think about it.

## (1) What could go wrong from backtest to live?  
At least 5 risks — in practice, there are many more:

1. **Overfitting / data snooping**  
   The strategy may have fit noise in the historical sample, especially if many parameter combinations were tried.

2. **Regime change**  
   The last 5 years may not represent future market conditions. Volatility, correlations, rates, liquidity, and participant behavior can shift.

3. **Transaction costs underestimated**  
   Live commissions, fees, exchange costs, borrow fees, financing, market impact, and slippage may be higher than assumed.

4. **Execution risk**  
   Backtests often assume fills at mid or close; live trading may get partial fills, delays, missed fills, queue position effects, and adverse selection.

5. **Liquidity risk**  
   The strategy may work on historical prices but not at the size the firm wants to trade.

6. **Look-ahead bias**  
   The backtest may inadvertently use information not available at trade time.

7. **Survivorship bias / selection bias**  
   If the historical dataset excluded delisted names or used a filtered universe, results can be overstated.

8. **Model decay / crowding**  
   If others trade similar signals, alpha can disappear once deployed.

9. **Operational / technology risk**  
   Bugs, bad data, exchange outages, clock sync issues, order routing failures, and monitoring gaps can create losses.

10. **Risk model mismatch**  
   Real drawdowns may exceed 8% if correlations spike or tail events occur that were absent in the sample.

11. **Capacity risk**  
   Performance may degrade sharply as capital scales.

12. **Shorting / borrow risk**  
   Borrow may be unavailable or expensive live even if assumed in backtest.

---

## (2) Probability the outperformance is due to overfitting

This **cannot be calculated exactly** from only:
- 5 years of data
- 200 parameter combinations
- observed annual return / Sharpe / drawdown

because we a...
```

### DeepSeek V3

**Generation Time:** 23976ms
**Tokens:** 1061

```
### (1) Risks Between Backtest and Live Trading

Several risks could cause live performance to deviate from backtested results:

1. **Overfitting (Data Snooping Bias):**  
   The strategy may have been optimized to historical data but fails to generalize to unseen market conditions. Testing 200 parameter combinations increases this risk.

2. **Market Regime Changes:**  
   The backtest period may not include all market regimes (e.g., high inflation, flash crashes, liquidity crises). Live trading could encounter new regimes where the strategy breaks down.

3. **Execution Assumptions:**  
   Backtests often assume perfect execution (no slippage, fills at mid-price, no latency). In reality, market impact, latency, and adverse selection can degrade performance.

4. **Survivorship Bias:**  
   If the backtest used survivorship-biased data (e.g., Expressing universe of current stocks without accounting for delisted ones), live trading may underperform.

5. **Liquidity Constraints:**  
   Backtests might ignore liquidity limits. Live trading larger sizes could face wider spreads or insufficient order book depth, especially during volatile periods.

---

### (2) Probability of Overfitting Calculation

To estimate the probability that the outperformance is due to overfitting, we can use the **Probability of Backtest Overfitting (PBO)** framework by Bailey et al. (2015). Here’s a simplified approach:

1. **Sharpe Ratio Adjustment:**  
   The annualized Sharpe ratio (SR) is 2.1. For a strategy tested on 200 combinations, the expected maximum Sharpe ratio due to randomness is higher than the true SR.  
   The formula for the expected maximum SR under overfitting is approximately:  
   \[
   \text{Max SR} \approx \text{True SR} + \sqrt{2 \ln(200)} \cdot \frac{1}{\sqrt{T}}
   \]  
   Where \( T = 5 \) years (assuming daily returns, ~252*5 = 1260 observations).  
   If the true SR were 0 (no skill), the max SR due to randomness would be:  
   \[
   \text{Max SR} \approx 0 + \sqrt{...
```

### MiMo-V2-Flash

**Generation Time:** 22600ms
**Tokens:** 2195

```
Here is a detailed breakdown of the risks, the statistical analysis of the backtest, and a proposed live testing protocol.

---

### (1) Risks Between Backtest and Live Trading

A Sharpe ratio of 2.1 and a max drawdown of 8% on a 15% annual return strategy looks exceptionally good on paper. However, this performance is highly susceptible to specific real-world frictions. Here are five critical risks:

1.  **Market Impact and Slippage:**
    *   **The Issue:** Backtests often assume "point-and-click" execution at the closing price or the midpoint of the bid-ask spread. In reality, large orders move the market.
    *   **The Risk:** If the strategy trades illiquid assets or requires rapid entry/exit, the actual fill price will be worse than the backtest price (slippage). A strategy with a 15% return can easily become unprofitable if execution costs are 20–50 basis points per trade.

2.  **Look-Ahead Bias and Data Snooping:**
    *   **The Issue:** The backtest used 5 years of data and tested 200 parameter combinations.
    *   **The Risk:** By testing 200 variations, the firm likely "mined" for a lucky outcome. Even if no explicit future data was used, the act of selecting the best-performing parameter set after the fact introduces significant bias. The strategy may have simply curve-fitted the noise of the past 5 years rather than capturing a persistent market anomaly.

3.  **Regime Shifts (Non-Stationarity):**
    *   **The Issue:** Financial markets are non-stationary; statistical properties change over time. The 5-year backtest period likely included specific macroeconomic conditions (e.g., low interest rates, specific volatility regimes).
    *   **The Risk:** If the market regime changes (e.g., a shift from low inflation to high inflation, or a transition from quantitative easing to tightening), the correlations and volatilities that drove the backtest results may break down entirely.

4.  **Liquidity Risk and Capacity Constraints:**
    *   **The Issue:** A str...
```

### Claude Sonnet 4.6

**Generation Time:** 41655ms
**Tokens:** 2171

```
# Backtest-to-Live Trading: Comprehensive Risk Analysis

## Part 1: What Could Go Wrong — The Full Taxonomy of Failure

### Category A: Market Microstructure Risks

**1. Slippage and Market Impact**
The backtest almost certainly used **mid-price or close-price fills** — the world doesn't work that way.

```
Backtest assumption:  Buy 10,000 shares @ $50.00 = $500,000
Reality:              
  - Bid/ask spread:   $49.98 / $50.02 → immediate $200 cost
  - Market impact:    Large order moves price against you
  - Partial fills:    Only 6,000 shares filled at target price
  
Slippage model:
  Expected slippage = k × σ × √(Q/ADV)
  
  Where:
    k = market impact constant (~0.1-0.5)
    σ = daily volatility
    Q = order quantity
    ADV = average daily volume
    
  Example: σ=2%, Q/ADV=5%, k=0.3
  Slippage = 0.3 × 0.02 × √0.05 = 0.134% per trade
  
  At 100 trades/year: 13.4% annual drag
  → Eliminates the entire 15% return
```

**2. Liquidity Illusion**
```
Backtest shows:  Strategy trades $50M in small-cap stocks
Reality:         Average daily volume = $2M per stock
                 
Position sizing constraint:
  Max position = participation_rate × ADV × holding_period
  Safe rule: never exceed 10-20% of ADV
  
  $50M / 20 stocks = $2.5M per position
  $2.5M / $2M ADV = 125% of daily volume ← IMPOSSIBLE
  
Result: Strategy simply cannot be executed at intended scale
```

**3. Bid-Ask Spread Costs**
```
High-frequency component analysis:
  If strategy holds positions for 2 days average:
  
  Round-trip spread cost = spread / mid_price
  Typical small-cap spread: 0.3-0.5%
  
  Annual cost = (spread × trades_per_year)
  200 trades × 0.4% = 0.8% annual drag (minimum)
  
  This is NEVER captured in close-to-close backtests
```

---

### Category B: Data and Model Risks

**4. Look-Ahead Bias**
The most insidious backtest killer:

```
Common sources:
┌─────────────────────────────────────────────────────────┐
│ SUBTLE LOOK-AHEAD BIAS EXAMPLES                         │
├──────...
```

### Grok 4.20

**Generation Time:** 6779ms
**Tokens:** 1440

```
**Here is a direct, professional answer to the three questions:**

### (1) What could go wrong between backtest and live trading? (Key risks)

Here are the most important risks that consistently kill quant strategies when moving from backtest to live:

1. **Overfitting / Data-snooping bias** – The strategy was tuned on the same 5 years of data (especially with 200 parameter combinations). The backtest performance is likely spurious.

2. **Look-ahead / Survivorship / Data-cleaning bias** – The backtest used cleaned or point-in-time incorrect data (e.g., using future delisting information, incorrect corporate-action adjustments, or unsynchronized timestamps).

3. **Transaction cost & market impact mismatch** – The backtest used unrealistic slippage, spread, or commission assumptions. In live trading, especially with larger size, impact becomes material.

4. **Regime shift / Structural break** – The 5-year period may have been a particularly favorable regime (e.g., strong trend, low volatility, specific central-bank policy). The edge disappears in new regimes.

5. **Liquidity & capacity risk** – The strategy works on small notional in the backtest but cannot be scaled without moving the market or suffering severe slippage.

6. **Execution & microstructure differences** – Live execution (order routing, venue choice, latency, queue position) differs dramatically from the backtest assumptions.

7. **Crowding / Arbitrage** – Other firms may have already discovered similar signals and the edge has been arbitraged away or turned toxic.

8. **Risk-model failure in tails** – Max drawdown of 8% in backtest is meaningless if the strategy has hidden tail exposure to events not present in the 5-year sample (flash crashes, liquidity dry-ups, geopolitical shocks).

### (2) Probability that the outperformance is due to overfitting

This is a classic multiple-testing / data-snooping problem.

**Key facts given:**
- 5 years of daily data ≈ 1,260 observations
- 200 independent parameter...
```

### GPT-OSS-120B

**Generation Time:** 28912ms
**Tokens:** 2223

```
Below is a concise, yet thorough, answer to the three questions.  
I treat the request as a **risk‑management / research‑design** exercise rather than a “prove‑the‑strategy‑works” memo – the goal is to surface hidden pitfalls and to propose a disciplined, low‑capital‑exposure rollout plan.

---

## 1️⃣  What could go wrong when you move from back‑test to live trading?  
(5 + risks, each with a short explanation)

| # | Risk | Why it matters (back‑test vs. live) |
|---|------|-----------------------------------|
| 1 | **Data‑snooping / Over‑fitting** | 200 parameter combos on only 5 y of history creates a huge multiple‑testing problem. The “best” set may be fitting random noise, not a true edge. |
| 2 | **Look‑ahead / survivorship bias** | If any price series, corporate actions, or factor data were cleaned after the fact (e.g., using future dividend adjustments), the back‑test will be unrealistically optimistic. |
| 3 | **Execution slippage & market impact** | Back‑tests normally assume fill at the mid‑price with zero latency. In reality you pay the bid‑ask spread, incur latency, and large orders move the market, eroding the 15 % return and raising draw‑down. |
| 4 | **Regime shift / non‑stationarity** | Five years may have been a relatively “quiet” period (low volatility, trending markets). A regime change (e.g., higher volatility, different correlation structure) can instantly break a high‑Sharpe signal. |
| 5 | **Model‑drift / parameter decay** | The optimal parameters today may become sub‑optimal tomorrow because the underlying statistical relationships evolve. Without periodic re‑training the strategy’s edge decays. |
| 6 | **Liquidity & order‑size constraints** | The back‑test often assumes you can trade any size at any time. In live markets the instrument’s daily volume, market depth, and exchange rules limit how much capital you can safely allocate. |
| 7 | **Operational / infrastructure failures** | Connectivity outages, API version changes, or bugs in order...
```

### Gemini 3 Flash Preview

**Generation Time:** 0ms
**Tokens:** 0

```

```

### MiniMax M2.5

**Generation Time:** 12006ms
**Tokens:** 2190

```

```

---

*Generated by The Multivac V5*
*https://themultivac.com*