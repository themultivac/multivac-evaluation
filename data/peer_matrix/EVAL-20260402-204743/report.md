# Multivac Evaluation Report

**Evaluation ID:** EVAL-20260402-204743
**Timestamp:** 2026-04-02T20:47:43.323961
**Category:** Analysis & Research
**Model Pool:** 10 analysis-optimized models

## Question

A quantitative trading firm backtests a strategy: 15% annual return, Sharpe ratio 2.1, max drawdown 8%. They want to go live. (1) What could go wrong between backtest and live trading? List at least 5 risks. (2) The backtest used 5 years of data and tested 200 parameter combinations. Calculate the probability this outperformance is due to overfitting. (3) Design a live testing protocol that minimizes capital at risk while validating the strategy.

---

## Rankings

| Rank | Model | Score | Min | Max | Std Dev |
|------|-------|-------|-----|-----|---------|
| 1 | GPT-5.4 | 9.05 | 8.40 | 9.80 | 0.55 |
| 2 | Grok 4.20 | 8.34 | 6.80 | 9.20 | 0.89 |
| 3 | GPT-OSS-120B | 8.32 | 6.10 | 9.20 | 0.96 |
| 4 | Gemini 3 Flash Preview | 7.86 | 6.25 | 8.80 | 0.77 |
| 5 | MiMo-V2-Flash | 7.69 | 6.45 | 9.00 | 0.92 |
| 6 | Claude Sonnet 4.6 | 7.01 | 3.20 | 9.40 | 2.27 |
| 7 | DeepSeek V3 | 6.99 | 5.25 | 9.00 | 1.27 |
| 8 | Gemini 3.1 Pro | 2.81 | 1.35 | 5.00 | 1.20 |
| None | Claude Opus 4.6 | 5.56 | 0.45 | 8.05 | 3.53 |
| None | MiniMax M2.5 | 5.72 | 0.50 | 8.35 | 3.64 |

---

## Meta Analysis

### Judge Strictness

| Rank | Judge | Avg Score Given |
|------|-------|-----------------|
| 1 | GPT-5.4 | 5.02 |
| 2 | Claude Opus 4.6 | 6.24 |
| 3 | GPT-OSS-120B | 6.60 |
| 4 | MiniMax M2.5 | 6.79 |
| 5 | Grok 4.20 | 6.93 |
| 6 | Claude Sonnet 4.6 | 7.18 |
| 7 | Gemini 3.1 Pro | 7.61 |
| 8 | Gemini 3 Flash Preview | 8.05 |
| 9 | MiMo-V2-Flash | 8.09 |
| 10 | DeepSeek V3 | 8.43 |

**Strictest Judge:** gpt_5_4
**Most Lenient Judge:** deepseek_v4
**Total Judgments:** 100
**Valid Judgments:** 78

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

**Generation Time:** 30104ms
**Tokens:** 2150

```
**Capital Scaling based on Kelly/Half-Kelly or Milestones:** Increase capital incrementally (e.g., 5%, 25%, 50%, 100% of target allocation). Only advance if live Sharpe/Drawdown matches a predefined confidence interval of the backtest.
    *   *Key Monitoring Metrics:*
        *   **Slippage & Fill
```

### Claude Opus 4.6

**Generation Time:** 0ms
**Tokens:** 0

```

```

### GPT-5.4

**Generation Time:** 42479ms
**Tokens:** 2004

```
Here’s a practical answer in 3 parts.

## 1) What could go wrong between backtest and live trading?

A strong backtest can fail live for many reasons. At least 5 major risks:

1. **Overfitting / data mining**
   - The strategy may have fit noise in historical data rather than real signal.
   - Testing 200 parameter combinations makes this especially likely.

2. **Regime change**
   - Market structure may have changed.
   - A strategy that worked in the last 5 years may fail in a different volatility, correlation, or liquidity regime.

3. **Transaction costs underestimated**
   - Live commissions, fees, borrow costs, funding costs, exchange fees, and taxes may be higher than modeled.
   - Small edge strategies are especially vulnerable.

4. **Slippage and market impact**
   - Backtests often assume fills at or near observed prices.
   - In live trading, orders move the market or get worse fills, especially in less liquid names.

5. **Execution risk**
   - Delays, partial fills, missed orders, stale quotes, smart order routing failures, and exchange outages can materially reduce performance.

6. **Look-ahead bias**
   - The backtest may have accidentally used information not truly available at the time of trade.

7. **Survivorship bias / bad data**
   - Historical datasets may exclude delisted securities or contain cleaned data not available live.

8. **Model decay**
   - Once a signal is discovered, competition may arbitrage it away.

9. **Operational risk**
   - Bugs, infrastructure failures, bad position reconciliation, or broken risk controls can create losses unrelated to model quality.

10. **Capacity risk**
   - Strategy performance may degrade when scaled, even if small backtest trades looked attractive.

11. **Tail risk**
   - Max drawdown of 8% in backtest may understate real drawdowns under extreme events absent from the sample.

12. **Shorting / financing constraints**
   - If the strategy shorts, hard-to-borrow names or changing borrow rates can damage re...
```

### DeepSeek V3

**Generation Time:** 46469ms
**Tokens:** 797

```
### (1) Risks Between Backtest and Live Trading  

Several factors can cause live performance to deviate from backtests:  

1. **Market Regime Changes** – The strategy may perform well in historical data but fail in a different economic environment (e.g., rising rates, high volatility).  
2. **Slippage & Execution Costs** – Backtests often underestimate trading costs (bid-ask spreads, market impact, latency).  
3. **Data Snooping Bias** – Testing many parameter combinations increases the chance of selecting an overfitted model that doesn’t generalize.  
4. **Survivorship Bias** – If the backtest excludes delisted or illiquid assets, live performance may degrade.  
5. **Model Risk** – Assumptions (e.g., linear relationships, stationarity) may break down in live markets.  

### (2) Probability of Overfitting  

A rough estimate can be made using the **Probability of Backtest Overfitting (PBO)** framework (Bailey et al., 2014).  

Given:  
- **Number of parameter combinations (N)** = 200  
- **Sharpe ratio (SR)** = 2.1  
- **Sample size (T)** = 5 years (~1260 trading days)  

The **expected maximum Sharpe ratio** due to random chance (assuming uncorrelated tests) is:  
\[
\mathbb{E}[\max SR] \approx SR_0 + \sqrt{2 \ln N / T}
\]  
Where \(SR_0\) is the true Sharpe (assume 0 for noise).  

Plugging in:  
\[
\mathbb{E}[\max SR] \approx 0 + \sqrt{2 \ln(200) / 1260} \approx 0.10
\]  

But the observed SR (2.1) is much higher, suggesting the strategy may have some skill. However, **200 tests imply a high risk of selecting a lucky variant**.  

A more precise approach uses **Monte Carlo simulations** or **deflated Sharpe ratio** (DSR):  
\[
DSR = SR \times \sqrt{1 - \frac{\ln N}{T}}
\]  
\[
DSR \approx 2.1 \times \sqrt{1 - \frac{5.3}{1260}} \approx 2.08
\]  

This suggests limited overfitting, but **the high number of trials still raises concerns**.  

### (3) Live Testing Protocol  

To validate safely:  

1. **Forward Testing (Paper Trading)** – Run the strategy in real-tim...
```

### MiMo-V2-Flash

**Generation Time:** 12436ms
**Tokens:** 1573

```
Here is an analysis of the strategy, the risks involved, the probability of overfitting, and a recommended live testing protocol.

---

### (1) Risks Between Backtest and Live Trading

Even with a high Sharpe ratio and low drawdown in simulation, several factors can cause a strategy to fail in the real world:

1.  **Market Regime Change (Structural Breaks):** The backtest data (likely 2019–2024) captured a specific macroeconomic environment (e.g., low interest rates, specific Fed policies, or a post-COVID recovery). If the live environment shifts (e.g., high inflation, recession, or geopolitical conflict), the statistical relationships the strategy relies on may break down.
2.  **Slippage and Execution Costs:** Backtests often assume "perfect" execution at the closing price or the bid/ask midpoint. In reality, liquidity constraints, order routing delays, and crossing the spread can turn a profitable edge into a losing one, especially if the strategy is high-frequency or trades large sizes relative to daily volume.
3.  **Look-Ahead Bias / Survivorship Bias:** The data preparation might have inadvertently included information that wouldn't have been available at the time of the trade (e.g., using a quarterly report that was released *after* the trading period). Additionally, if the backtest only included stocks that "survived" the 5-year period, it ignores the performance of delisted (bankrupt) companies, artificially inflating returns.
4.  **Alpha Decay (Crowding):** A Sharpe of 2.1 is exceptionally high. If the firm found this edge using public data and standard tools, it is highly likely that other firms have found it too. As more capital chases the same opportunity, the edge diminishes or disappears entirely (arbitrage).
5.  **Operational & Technological Risk:** Backtests do not account for server outages, API rate limits, bugs in the live execution code, or database corruption. A 24/7 infrastructure requires redundancy that is often not modeled in a backtest envi...
```

### Claude Sonnet 4.6

**Generation Time:** 46050ms
**Tokens:** 2171

```
# Backtest-to-Live Trading: Comprehensive Risk Analysis

## Part 1: What Could Go Wrong — The Full Taxonomy of Failure

### Category A: Data-Related Risks

---

**1. Survivorship Bias**
```
Problem: Backtest universe likely excludes delisted, bankrupt, 
or merged securities

Magnitude: Studies show survivorship bias inflates returns by 
1-3% annually in equity strategies

Example: A momentum strategy backtested on S&P 500 
"current constituents" never experienced Enron, Lehman, 
or Kodak — companies that would have been held

Detection: Compare results using point-in-time universe 
vs. current universe
```

**2. Look-Ahead Bias**
```
Problem: Using information that wasn't available at trade time

Common Sources:
├── Earnings data revised after initial release
├── Index rebalancing known before announcement
├── Adjusted prices applied backward (splits, dividends)
└── Fundamental data with reporting lags ignored

Example: Using Q3 earnings filed in November to make 
October trades — impossible in real life

Severity: Can artificially boost Sharpe by 0.5-1.5 points
```

**3. Data Snooping / P-Hacking**
```
Problem: Historical data has random patterns; enough 
testing finds spurious ones

The Math:
- 200 parameter combinations tested
- Even random strategies: ~10 appear significant at p<0.05
- Selected "best" has no predictive power

Real Example: Testing 200 moving average combinations 
on 5 years of S&P data — some will show Sharpe > 2 
purely by chance
```

**4. Stale/Incorrect Data**
```
Problem: Vendor data contains errors that systematically 
favor the strategy

Issues:
├── Price errors on illiquid securities
├── Dividend adjustments miscalculated  
├── Corporate action handling inconsistencies
└── Timezone/timestamp mismatches in multi-asset

Impact: A single bad data point can generate a 
"perfect trade" that never existed
```

**5. Regime Non-Stationarity**
```
Problem: 5-year backtest may capture only one market regime

2019-2024 Example:
├── Low volatility bu...
```

### Grok 4.20

**Generation Time:** 7794ms
**Tokens:** 1533

```
**1. What could go wrong between backtest and live trading? (At least 5 risks)**

Here are the most important risks that consistently kill quant strategies when moving from backtest to live:

- **Overfitting / Data-snooping bias** – The strategy was curve-fit to the specific 5-year sample. The 200 parameter combinations dramatically increase the chance the observed performance is spurious (see part 2).

- **Transaction cost & slippage mismatch** – Backtests usually underestimate real-world slippage, especially in less liquid names or during volatility spikes. A strategy with 15% gross return can easily turn negative after realistic costs.

- **Regime change / Non-stationarity** – Markets evolve. The relationship that worked in 2019–2024 may disappear or reverse when liquidity, volatility regime, interest rates, or participant mix changes.

- **Look-ahead bias or data-cleaning errors** – Common in backtests: using future information, survivorship bias, point-in-time data issues, or incorrect corporate-action handling.

- **Liquidity and market impact** – The backtest assumes you can trade the desired size at the backtest price. In live trading, especially with larger capital, your own orders move the market or you get adverse selection (you get filled when you shouldn’t).

- **Execution risk & latency** – Live execution involves delays, partial fills, queue position, and venue differences that backtests rarely model accurately.

- **Risk-model breakdown** – The 8% max drawdown in backtest can explode in a new regime (e.g., March 2020 style event, liquidity crunch, or crowded-trade unwind).

- **Crowding / Arbitrage** – If the strategy is based on a well-known academic factor or signal, other firms may already be trading it, reducing or reversing its edge.

**2. Probability that the outperformance is due to overfitting**

This is a classic multiple-testing / data-snooping problem. We can approximate it using the **False Discovery Rate** approach commonly used in quant...
```

### GPT-OSS-120B

**Generation Time:** 27377ms
**Tokens:** 2223

```
## 1️⃣ What could go wrong when you move from a 5‑year back‑test to a live‑trading environment?

| # | Risk / Failure mode | Why it matters | Typical “red‑flag” symptoms |
|---|--------------------|----------------|----------------------------|
| 1 | **Data‑snooping / Multiple‑testing bias** | 200 parameter combos were inspected on the same 5‑year sample.  The best‑performing set is very likely a statistical fluke rather than a robust edge. | In‑sample Sharpe ≫ out‑of‑sample Sharpe; performance collapses as soon as you change the data window. |
| 2 | **Look‑ahead / survivorship bias** | If the data set contains future information (e.g., corporate actions, delisted symbols) or only surviving securities, the back‑test is artificially optimistic. | Sudden “gap‑up” profits that never materialise live; higher win‑rate in back‑test than in real‑time. |
| 3 | **Execution slippage & market impact** | Back‑tests normally assume you can trade at the mid‑price with infinite liquidity. In reality you pay the bid‑ask spread, incur latency, and move the market when you scale. | Real‑time fill prices consistently worse than simulated fills; increasing order size dramatically reduces realized return. |
| 4 | **Transaction‑cost under‑estimation** | Commissions, exchange fees, clearing fees, and the cost of crossing the spread are often omitted or grossly understated. | Net‑of‑cost Sharpe drops from >2 to <1; the strategy becomes unprofitable after a few weeks. |
| 5 | **Regime change / Non‑stationarity** | Five years of history may not capture future macro‑economic, volatility, or structural shifts (e.g., new market micro‑structure, regulatory changes). | Sharp deterioration when volatility spikes or when a new venue takes market share; correlations that the model relied on break down. |
| 6 | **Liquidity & position‑size limits** | The back‑test may trade symbols that are ill‑iquid or assume you can fill the full desired volume. | Orders sit on the book for minutes, get partially fi...
```

### Gemini 3 Flash Preview

**Generation Time:** 9677ms
**Tokens:** 1113

```
This scenario presents a classic case of a strategy that looks "too good to be true." A Sharpe ratio of 2.1 is exceptionally high for most liquid strategies, suggesting either a niche alpha source or, more likely, significant backtest bias.

### 1. Risks Between Backtest and Live Trading

Even with honest intentions, several factors can cause a strategy to fail when transitioning to live capital:

1.  **Overfitting (Data Snooping):** With 200 parameter iterations, the firm likely "mined" the data to find a combination that fit the noise of the past 5 years rather than the signal.
2.  **Execution Shortfalls (Slippage/Market Impact):** Backtests often assume they can fill orders at the mid-price or last traded price. In reality, large orders move the market against the trader, and the "bid-ask spread" eats into the 15% return.
3.  **Look-ahead Bias:** The backtest might inadvertently use information not available at the time of the trade (e.g., using the daily "close" price to enter a trade that should have occurred at the "open").
4.  **Regime Change:** The 5-year backtest period might cover a specific market environment (e.g., a low-volatility bull market). If live trading begins during a period of high volatility or rising rates, the strategy may be structurally unsuited for the new regime.
5.  **Latency and Infrastructure:** The backtest assumes instantaneous execution. In live markets, delays in data feeds or order routing (latency) can result in missed opportunities or worse fills, especially for high-turnover strategies.

---

### 2. Probability of Overfitting (Haircut Sharpe Ratio)

To estimate the probability that this performance is due to chance, we use the **"Haircut Sharpe Ratio"** framework (pioneered by Harvey and Liu). 

When testing multiple configurations, the required t-statistic for significance must increase to account for multiple testing.
*   **Number of tests ($N$):** 200
*   **Backtest Sharpe ($SR$):** 2.1
*   **Observations ($T$):** 5 years

...
```

### MiniMax M2.5

**Generation Time:** 0ms
**Tokens:** 0

```

```

---

*Generated by The Multivac V5*
*https://themultivac.com*