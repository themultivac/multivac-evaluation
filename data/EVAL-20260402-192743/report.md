# Multivac Evaluation Report

**Evaluation ID:** EVAL-20260402-192743
**Timestamp:** 2026-04-02T19:27:43.803760
**Category:** Analysis & Research
**Model Pool:** 10 analysis-optimized models

## Question

A SaaS startup shares these metrics: MRR $50K, growth 15% month-over-month, CAC $500, LTV $2,400, churn 5% monthly, burn rate $200K/month, runway 8 months. (1) Is this business healthy? (2) Calculate the LTV:CAC ratio and explain why it's misleading at 5% monthly churn. (3) At what churn rate does this business become viable? (4) They're raising at $20M valuation. Would you invest? Why or why not?

---

## Rankings

| Rank | Model | Score | Min | Max | Std Dev |
|------|-------|-------|-----|-----|---------|
| 1 | GPT-5.4 | 9.12 | 8.45 | 9.80 | 0.47 |
| 2 | Gemini 3 Flash Preview | 8.43 | 7.15 | 9.45 | 0.79 |
| 3 | Grok 4.20 | 8.28 | 6.35 | 9.80 | 1.22 |
| 4 | Claude Opus 4.6 | 8.02 | 6.25 | 9.80 | 1.26 |
| 5 | MiMo-V2-Flash | 7.89 | 6.30 | 9.80 | 1.27 |
| 6 | DeepSeek V3 | 7.87 | 6.10 | 9.80 | 1.10 |
| 7 | Claude Sonnet 4.6 | 7.42 | 5.35 | 9.00 | 1.17 |
| 8 | GPT-OSS-120B | 6.65 | 4.70 | 8.80 | 1.27 |
| 9 | Gemini 3.1 Pro | 5.47 | 2.70 | 7.60 | 1.58 |

---

## Meta Analysis

### Judge Strictness

| Rank | Judge | Avg Score Given |
|------|-------|-----------------|
| 1 | GPT-5.4 | 6.12 |
| 2 | Gemini 3.1 Pro | 6.88 |
| 3 | GPT-OSS-120B | 7.20 |
| 4 | Grok 4.20 | 7.28 |
| 5 | Claude Opus 4.6 | 7.52 |
| 6 | MiniMax M2.5 | 7.78 |
| 7 | Claude Sonnet 4.6 | 8.02 |
| 8 | MiMo-V2-Flash | 8.49 |
| 9 | DeepSeek V3 | 8.84 |
| 10 | Gemini 3 Flash Preview | 8.90 |

**Strictest Judge:** gpt_5_4
**Most Lenient Judge:** gemini_3_flash
**Total Judgments:** 100
**Valid Judgments:** 80

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

**Generation Time:** 31120ms
**Tokens:** 2174

```
Here is an analysis of the SaaS startup based on the metrics provided:

### 1. Is this business healthy?
**No, this business is not healthy.** It is a classic "leaky bucket." 

While the 15% month-over-month (MoM) growth is exceptional (translates to over 400% annualized growth), it is masking a fatal flaw: the **5% monthly churn**. A 5% monthly churn compounds to an annual customer loss of roughly **46%**. 


```

### Claude Opus 4.6

**Generation Time:** 41939ms
**Tokens:** 2183

```
# SaaS Startup Deep Dive Analysis

## (1) Is This Business Healthy?

**No. This business is critically unhealthy despite impressive headline growth.**

Let me walk through why by examining the tension between the metrics:

**The seductive narrative:**
- 15% MoM growth sounds exceptional (would be ~5.3x annual)
- LTV:CAC looks solid at first glance
- $50K MRR means they have *some* product-market fit

**The brutal reality:**

```
Monthly Revenue:        $50,000
Monthly Burn:          $200,000
Monthly Cash Gap:      -$150,000
Runway:                 8 months

Revenue covers only 25% of operating costs.
```

**The churn problem is existential.** At 5% monthly churn, you're losing roughly half your customers every year. Let me show what this means concretely:

```
Month    Starting    Churned    New Needed    Just to Stay Flat
  1       1,000        50          50              50
  6       1,000        50          50              50
 12       1,000        50          50              50

Annual retention rate: (0.95)^12 = 54%
You lose 46% of your customer base every year.
```

This means the 15% MoM growth is masking a **leaky bucket** — they're pouring customers in the top while nearly half drain out the bottom annually. Growth is expensive when you're constantly replacing churned customers before you can even grow.

---

## (2) LTV:CAC Ratio — And Why It's Misleading

### The Stated Calculation

```
LTV:CAC = $2,400 / $500 = 4.8x
```

The standard benchmark says 3x+ is healthy, so 4.8x looks great. **But this number is almost certainly wrong.**

### Why It's Misleading at 5% Monthly Churn

**Let's calculate what LTV *should* be from first principles:**

LTV formula: **LTV = ARPU / Churn Rate**

```
We can back-derive ARPU from their stated LTV:
If LTV = $2,400 and they're using some assumed churn rate...

But with ACTUAL 5% monthly churn:
Average customer lifetime = 1 / 0.05 = 20 months

If ARPU = LTV × churn = $2,400 × 0.05 = $120/month
Then LTV = $120 / 0.05 = $2,400...
```

### GPT-5.4

**Generation Time:** 24716ms
**Tokens:** 1538

```
1) **Is this business healthy?**  
**Not really.** There are some good signals, but overall this is **not yet a healthy business**.

### What looks good
- **MRR = $50K**
- **Growth = 15% MoM**, which is strong on paper
- **CAC = $500** looks low
- Reported **LTV = $2,400** suggests decent unit economics at first glance

### What looks bad
- **Churn = 5% monthly** is very high for SaaS
- **Burn = $200K/month** on only **$50K MRR** is extremely aggressive
- **Runway = 8 months** is short, especially with high churn
- Raising at **$20M valuation** on **$600K ARR** implies about **33x ARR**, which is very expensive given the risk profile

### Core issue
The business may be **buying growth**, but the customer base is **leaky**. At 5% monthly churn, customers do not stay long enough to support durable compounding. Strong top-line growth can mask weak retention.

---

2) **Calculate LTV:CAC ratio and explain why it's misleading at 5% monthly churn**

### LTV:CAC
Given:
- **LTV = $2,400**
- **CAC = $500**

So:

\[
LTV:CAC = \frac{2400}{500} = 4.8x
\]

That sounds great. Normally, 3x+ is considered strong.

### Why it's misleading
At **5% monthly churn**, average customer lifetime is roughly:

\[
\frac{1}{0.05} = 20 \text{ months}
\]

If LTV is being calculated as:

\[
LTV = \frac{ARPU \times \text{gross margin}}{\text{churn}}
\]

then it can look mathematically fine, but this can still be misleading for several reasons:

#### a) 5% monthly churn is bad in SaaS
5% monthly churn means annual retention is roughly:

\[
(1 - 0.05)^{12} \approx 54\%
\]

So after one year, only about **54%** of customers remain. That is weak for most SaaS businesses.

#### b) LTV assumes stable retention over time
This formula assumes churn behaves smoothly and predictably. In reality, high churn often means:
- poor product-market fit
- low customer satisfaction
- weak expansion potential
- fragile growth

#### c) Gross LTV ignores burn and payback timing
Even if LTV is 4.8x CAC eventually, the co...
```

### DeepSeek V3

**Generation Time:** 43950ms
**Tokens:** 1122

```
Let's break this down step by step:

---

### **(1) Is the business healthy?**
- **Growth (15% MoM):** Strong, but likely unsustainable long-term without scaling efficiently.
- **LTV ($2,400) vs. CAC ($500):** LTV:CAC = 4.8 (good on surface, but see part 2).
- **Churn (5% monthly):** Very high—translates to ~46% annual churn (1 - (1 - 0.05)^12). This erodes LTV.
- **Burn ($200K/mo) & Runway (8 months):** Urgent need to extend runway or raise more capital.
- **MRR ($50K):** Low relative to burn ($200K/mo)—spending $4 to generate $1 in MRR.  

**Verdict:** **Unhealthy** due to high churn, low MRR relative to burn, and short runway. Growth is promising but not sustainable without fixing churn.

---

### **(2) Calculate LTV:CAC and why it's misleading at 5% churn**
- **LTV Calculation:**  
  - Gross Margin (assume 80% for SaaS): $2,400 * 0.8 = **$1,920**  
  - LTV:CAC = $1,920 / $500 = **3.84**  
  *(Note: Some use pre-margin LTV, so $2,400/$500 = 4.8. Both are acceptable but clarify assumptions.)*  

- **Why it’s misleading:**  
  - **5% monthly churn means customers last ~20 months on average (1/0.05).**  
  - High churn inflates CAC payback pressure—you have <2 years to recoup $500.  
  - **Rule of thumb:** LTV:CAC > 3 is "good," but not if churn is unsustainable. At 5% churn, the LTV is likely overstated because:  
    - Customer decay is rapid, so realized LTV may be lower.  
    - High churn demands constant spending to replace lost revenue.  

---

### **(3) At what churn does this business become viable?**  
To be viable:  
1. **LTV > 3x CAC** (after gross margin):  
   - Target LTV > $1,500 (since CAC = $500).  
   - Solve for churn:  
     - LTV = (MRR * Gross Margin) / Churn  
     - $1,500 = ($50 * 0.8) / Churn → Churn = $40 / $1,500 = **2.67% monthly** (~28% annualized).  

2. **Profitability:**  
   - To stop burning $200K/month, MRR must cover costs.  
   - If burn is $200K and MRR is $50K, need **$150K more MRR** or **cut burn by 75%**.  
   - Lower chur...
```

### MiMo-V2-Flash

**Generation Time:** 37295ms
**Tokens:** 2043

```
Here is a detailed analysis of the SaaS startup based on the metrics provided.

### (1) Is this business healthy?

**Short Answer: No.**

While the top-line growth and unit economics look attractive on the surface, the business is **structurally unhealthy and in critical danger.**

*   **The Growth-Churn Conflict:** You cannot sustain 15% month-over-month growth with a 5% monthly churn rate. If you churn 5% of customers every month, you are effectively churning 60% of your customer base annually. To grow at 15% monthly, you must acquire enough new customers to replace the ones leaving *plus* grow the base by 15%. This requires an exponentially increasing acquisition machine that will inevitably collapse under its own weight.
*   **Burn Rate vs. Runway:** The company is burning $200k per month with only 8 months of runway. This is an emergency. The "Runway" metric usually assumes no growth (flat revenue). However, because the company is growing, they are likely spending heavily on CAC to fuel that 15% growth. If they stop spending on acquisition to preserve cash, growth will stop, and churn will likely eat the revenue base. If they keep spending, they will run out of money in less than 8 months.

---

### (2) LTV:CAC Ratio & The "Churn Trap"

**The Calculation:**
*   **Formula:** LTV : CAC
*   **Given:** LTV = $2,400, CAC = $500
*   **Ratio:** **4.8:1**

**Why this is misleading:**
A ratio of 4.8:1 is usually considered excellent. However, with a **5% monthly churn rate**, this calculation is dangerously misleading for two reasons:

1.  **The Infinite Time Assumption:** Standard LTV calculations often assume a customer stays indefinitely or for a long period. If you calculate LTV using the standard formula ($2,400 / 5% = $48,000), you are mathematically assuming the customer stays for **20 months**. In reality, with 5% monthly churn, the *average* customer lifetime is only **1/0.05 = 20 months**.
    *   *Wait, isn't that the same?* No. If the LTV is *given* as $2,40...
```

### Claude Sonnet 4.6

**Generation Time:** 40418ms
**Tokens:** 2184

```
# SaaS Metrics Deep Dive: Brutal Honesty Required

## (1) Is This Business Healthy?

**Short answer: No. This business is in serious trouble despite impressive growth numbers.**

Let me show you why the headline metrics are hiding a structural crisis.

---

### The Growth Story vs. The Reality

```
WHAT THEY'RE SHOWING YOU        WHAT'S ACTUALLY HAPPENING
─────────────────────────────   ─────────────────────────────
✓ 15% MoM growth                ✗ Leaking bucket - growing AND losing
✓ $50K MRR                      ✗ $200K burn = losing $150K/month
✓ LTV:CAC of 4.8x               ✗ LTV calculation is mathematically wrong
✓ 8 months runway               ✗ Likely 5-6 months at real burn trajectory
```

### Key Health Indicators - Scored

| Metric | Value | Benchmark | Score | Verdict |
|--------|-------|-----------|-------|---------|
| MRR Growth | 15% MoM | >10% good | ✅ | Strong |
| Churn | 5% monthly | <1% good | 🚨 | Critical failure |
| LTV:CAC | 4.8x | >3x | ⚠️ | Misleading |
| Burn Multiple | 4x | <1.5x | 🚨 | Alarming |
| Runway | 8 months | >18 months | 🚨 | Dangerous |
| CAC Payback | ~10 months | <12 months | ⚠️ | Borderline |

**Burn Multiple = Net Burn / Net New ARR**
```
Net New MRR = $50K × 15% = $7,500/month
Annualized = $90K ARR added per year
Net Burn = $200K/month = $2.4M/year

Burn Multiple = $2.4M / $90K = 26.7x

Benchmark: Under 1x = excellent, Under 1.5x = good
26.7x = burning $26.70 for every $1 of ARR added
This is catastrophic
```

---

## (2) LTV:CAC Ratio and Why It's Deeply Misleading

### The Calculation They're Presenting

```
LTV:CAC = $2,400 / $500 = 4.8x

On the surface: Looks great (benchmark is >3x)
In reality: Built on a broken foundation
```

### Why the LTV Number is Wrong at 5% Monthly Churn

**The LTV formula most people use:**
```
LTV = ARPU × Gross Margin / Churn Rate
```

**But this assumes churn is an annual rate. Here's the problem:**

```
5% MONTHLY churn = what annual churn rate?

Annual Retention = (1 - 0.05)^12 = 0.95^12...
```

### Grok 4.20

**Generation Time:** 5732ms
**Tokens:** 1230

```
**1. Is this business healthy?**

**No, it's not healthy.** It's in a dangerous "growth-at-all-costs" trap with unsustainable unit economics and cash burn.

Key problems:
- **Extremely high churn**: 5% monthly churn = ~46% annual churn. This is catastrophic for most SaaS businesses (healthy is <1% monthly / <10-12% annual for SMB, even lower for mid-market/enterprise).
- **Burning cash rapidly**: $200K burn/month with only 8 months runway is a major red flag. At $50K MRR, they're burning 4x their monthly revenue.
- **Unit economics are broken**: They're spending $500 to acquire a customer worth only $2,400 (see below), while growing at a high rate that requires even more CAC spend.

The 15% MoM growth looks impressive on the surface but is masking fundamental problems.

**2. LTV:CAC ratio and why it's misleading at 5% monthly churn**

**Simple calculation**: LTV:CAC = $2,400 / $500 = **4.8x**

This looks "okay" on paper (investors like 3x+), but **it's highly misleading** because of how LTV is calculated with high churn.

The given LTV of $2,400 almost certainly assumes the standard formula:

LTV = (ARPU × Gross Margin) / Churn

At 5% monthly churn, the average customer lifetime is only **20 months** (1/0.05). This means the LTV number is extremely sensitive to small changes in churn.

**Why it's misleading**:
- High churn makes LTV calculations unstable and optimistic.
- Most of the LTV is back-loaded. With 5% churn, a huge percentage of the "value" comes from the tiny % of customers who stay 3+ years.
- In reality, with 5% churn, many customers never even pay back their CAC.
- True payback period is likely 10-12+ months (very slow).

A better way to think about it: **What's the real payback multiple in the first 12-18 months?** That's what actually matters for cash flow.

**3. At what churn rate does this business become viable?**

Let's define "viable" as:
- LTV:CAC of at least 3x (ideally 4x+)
- Reasonable payback period (<9 months)
- Path to positive cash flow ...
```

### GPT-OSS-120B

**Generation Time:** 30405ms
**Tokens:** 2231

```
### TL;DR  
1. **Health check:** The startup shows decent growth and a solid LTV:CAC ≈ 4.8, but the cash‑flow picture is shaky – high burn, a short runway and a 5 % monthly churn (≈ 55 % annual) make the business **borderline** at best.  
2. **LTV : CAC = 4.8** – looks “good” on paper, but because the LTV figure already assumes a very high churn rate it **over‑states** the true lifetime value and hides the fact that you’ll lose most of the revenue in a few years.  
3. **Churn threshold for viability:**  
   * LTV > CAC ⇒ churn < ARPU / CAC ≈ 24 % /mo.  
   * Preferred “healthy” benchmark (LTV : CAC ≥ 3) ⇒ churn ≤ ARPU / (3 × CAC) ≈ 8 % /mo.  
   The company is already under that 8 % mark, but the 5 % /mo churn is still high for a SaaS business that must fund a $200 k/month burn.  
4. **Investment decision:** At a **$20 M pre‑money valuation** the company is trading at **≈ 33× ARR** (ARR = $600 k). Combined with a short runway, a cash‑negative profile and a churn that would require aggressive acquisition spend to sustain growth, the deal is **over‑valued** for a seed‑/Series‑A‑stage SaaS. I would **not invest now** unless the founders can (a) dramatically lower churn, (b) extend runway (e.g., raise a bridge round at a lower cap), or (c) demonstrate a clear path to profitability that brings the valuation down to a more conventional 5‑10× ARR range.

Below is a step‑by‑step walk‑through of each question.

---

## 1. Is the business “healthy”?

| Metric | What it tells us | Interpretation |
|--------|------------------|----------------|
| **MRR = $50 k** | Current revenue base. | Small but typical for an early SaaS. |
| **Growth = 15 % MoM** | Momentum. | Strong month‑over‑month growth; however growth must outpace churn and acquisition spend to be sustainable. |
| **CAC = $500** | Cost to acquire a customer. | Low relative to the quoted LTV, but still a sizeable cash outflow each month. |
| **LTV = 
```

### Gemini 3 Flash Preview

**Generation Time:** 7695ms
**Tokens:** 1055

```
Here is an analysis of the startup’s health and investment potential based on the provided metrics.

### 1. Is this business healthy?
**No.** While the 15% month-over-month growth is impressive, the underlying unit economics and capital efficiency are alarming.

*   **The Burn/Revenue Gap:** They are burning $200K to generate $50K in MRR. This is a "Burn Multiple" of 4.0x (Burning $4 for every $1 of incremental revenue), which is considered inefficient for a seed/Series A stage company.
*   **The Churn Crisis:** A 5% monthly churn rate is "existential threat" territory. It means 60% of their customer base turns over every year. They are essentially pouring water into a leaky bucket.
*   **Runway Risk:** With only 8 months of runway and such high burn, they are in a "raise or die" position.

---

### 2. Calculate the LTV:CAC and explain why it is misleading.
**Calculation:**
*   $LTV:CAC = \$2,400 / \$500 = \mathbf{4.8x}$

**Why it is misleading at 5% churn:**
An LTV:CAC of 4.8x usually suggests a very healthy business (3.0x is the standard benchmark). However, LTV is a "forward-looking" projection based on the inverse of churn ($1 / \text{churn rate}$). 
*   At 5% monthly churn, the average customer lifetime is only **20 months**.
*   If the Average Revenue Per User (ARPU) is roughly $120/mo ($2,400 / 20 months), it takes **4.2 months just to break even on the CAC** (Payback Period). 
*   **The Trap:** LTV assumes the customer stays for the full 20 months. High churn usually indicates a "broken" product or a poor market fit. In a high-churn environment, the probability of a customer actually reaching that 20-month "average" is low, making the "Lifetime Value" a theoretical number that the company rarely actually collects in cash.

---

### 3. At what churn rate does this business become viable?
For a B2B SaaS company, "viability" generally begins when monthly churn drops below **2% to 3%**, but true "health" is found at **<1%**.

*   **The Math of Survival:** At 5% ...
```

### MiniMax M2.5

**Generation Time:** 35519ms
**Tokens:** 2200

```

```

---

*Generated by The Multivac V5*
*https://themultivac.com*