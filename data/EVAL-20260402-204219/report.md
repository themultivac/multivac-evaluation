# Multivac Evaluation Report

**Evaluation ID:** EVAL-20260402-204219
**Timestamp:** 2026-04-02T20:42:19.886678
**Category:** Analysis & Research
**Model Pool:** 10 analysis-optimized models

## Question

A company wants to acquire a startup for $50M. The startup claims $5M ARR growing 100% YoY, 85% gross margins, net retention 130%. During due diligence, you discover: (1) 40% of revenue is from a single customer, (2) the 'ARR' includes one-time implementation fees, (3) three of five engineers have unvested equity and might leave. What's the real valuation? What deal terms would protect the acquirer?

---

## Rankings

| Rank | Model | Score | Min | Max | Std Dev |
|------|-------|-------|-----|-----|---------|
| 1 | GPT-5.4 | 9.06 | 8.35 | 9.80 | 0.54 |
| 2 | Grok 4.20 | 8.99 | 8.55 | 9.80 | 0.42 |
| 3 | Claude Opus 4.6 | 8.92 | 8.40 | 10.00 | 0.55 |
| 4 | MiMo-V2-Flash | 8.75 | 7.75 | 9.80 | 0.70 |
| 5 | Claude Sonnet 4.6 | 8.75 | 7.80 | 10.00 | 0.74 |
| 6 | Gemini 3 Flash Preview | 8.26 | 6.75 | 9.35 | 0.79 |
| 7 | DeepSeek V3 | 7.91 | 6.60 | 9.80 | 0.90 |
| 8 | MiniMax M2.5 | 7.64 | 6.50 | 9.00 | 0.94 |
| 9 | Gemini 3.1 Pro | 6.56 | 3.90 | 8.60 | 1.63 |
| None | GPT-OSS-120B | 3.57 | 0.45 | 7.55 | 3.65 |

---

## Meta Analysis

### Judge Strictness

| Rank | Judge | Avg Score Given |
|------|-------|-----------------|
| 1 | GPT-5.4 | 6.68 |
| 2 | Grok 4.20 | 7.19 |
| 3 | Claude Opus 4.6 | 7.24 |
| 4 | GPT-OSS-120B | 7.84 |
| 5 | MiniMax M2.5 | 8.10 |
| 6 | Claude Sonnet 4.6 | 8.19 |
| 7 | Gemini 3.1 Pro | 8.68 |
| 8 | DeepSeek V3 | 8.82 |
| 9 | MiMo-V2-Flash | 8.92 |
| 10 | Gemini 3 Flash Preview | 9.57 |

**Strictest Judge:** gpt_5_4
**Most Lenient Judge:** gemini_3_flash
**Total Judgments:** 100
**Valid Judgments:** 85

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

**Generation Time:** 20447ms
**Tokens:** 2154

```
The discoveries made during due diligence fundamentally change the risk profile of this acquisition. The initial $50M valuation was based on a **10x ARR multiple**, which assumes high-quality, highly predictable revenue and a well-oiled machine. 

The due diligence findings reveal that this is actually a high-risk asset with inflated metrics. Here is a breakdown of the "real" valuation and the deal structure required to protect the acquirer.

---

### Part 1: Calculating the "Real" Valuation

To find the true valuation, we must adjust both the baseline revenue and the multiple applied to it.

**1. Adjusting the Revenue (The "True ARR")**
Implementation and one-time fees are non-recurring and should *never* be counted in ARR. 
*   *Assumption:* In enterprise SaaS, one-time implementation fees typically account for 15% to 25% of first-year contract values. Let's assume it accounts for 20% of the claimed $5M. 
*   **True ARR = $4.0M** (down from $5M).

**2. Adjusting the Multiple (Risk Discounting)**
A 10x multiple is a premium for a flawless SaaS startup. We must compress this multiple based on the newly discovered risks:
*   **Customer Concentration Risk (40%):** If $1.6M of the $4M True ARR is tied to one client, the 130% Net Revenue Retention (NRR) and 100% YoY growth are likely skewed by this single "whale" expanding their contract. If this customer churns, growth stalls and cash flow bleeds. *Discount applied: 20-30%.*
*   **Key Personnel Risk:** Losing 3 out of 5 engineers (60% of the core technical team) means product development will stall, technical debt will accrue, and the acquirer will face immediate and expensive recruiting costs. *Discount applied: 10-15%.*

**3. The Revised Valuation**
*   **True ARR:** $4.0M
*   **Adjusted Multiple:** 5x to 7x (down from 10x due to extreme concentration and flight risk).
*   **Real Enterprise Value
```

### Claude Opus 4.6

**Generation Time:** 51478ms
**Tokens:** 2164

```
# Startup Acquisition: Due Diligence Deep Dive

## Deconstructing the Claimed Metrics

### What They Claim vs. Reality

Let me work through each discovery systematically.

---

## 1. Revenue Reality Check

### Adjusting the ARR

**Claimed ARR: $5M**

**Problem 1: One-time implementation fees baked into "ARR"**

Implementation fees are non-recurring by definition. In typical B2B SaaS, implementation can be 10-30% of first-year contract value. Let's estimate conservatively that 15-20% of reported revenue is implementation fees.

```
Claimed ARR:                          $5.00M
Less: Estimated implementation fees:  ($0.85M)  ~17% of reported
Adjusted recurring revenue:           $4.15M
```

**Problem 2: Customer concentration — 40% from a single customer**

This is a structural risk, not just a line-item adjustment. That single customer represents ~$2.0M of the claimed ARR (~$1.66M adjusted). A risk-weighted approach:

```
Single customer revenue (adjusted):    $1.66M
Probability of retention (generous):   70%
Risk-adjusted value of that revenue:   $1.16M
Risk discount on that portion:         ($0.50M)

Remaining customer base (adjusted):    $2.49M
Assumed retention probability:         90%
Risk-adjusted:                         $2.24M

Total risk-adjusted ARR:              $3.40M
```

### Adjusting the Growth Rate

The 100% YoY growth claim needs scrutiny:
- **If the large customer was acquired in the past year**, organic growth from diversified customers could be far lower — potentially 40-60%
- **Implementation fees inflate apparent growth** in landing years
- Real sustainable growth rate is probably **50-70% YoY** at best

### Adjusting Net Revenue Retention (NRR)

Claimed NRR of 130% likely includes:
- Implementation fee "expansion" when new modules are deployed
- Outsized expansion from the single large customer
- **Realistic NRR after adjustments: 105-115%**

---

## 2. Team/IP Risk — The Engineering Problem

Three of five engineers with unvested equity is poten...
```

### GPT-5.4

**Generation Time:** 34968ms
**Tokens:** 1736

```
The headline $50M is almost certainly too high on the facts you found.

## 1) What’s the “real” valuation?

You’d re-underwrite this on normalized ARR, concentration risk, and team/key-person risk.

### Step 1: Fix the ARR
They say **$5M ARR**, but ARR improperly includes **one-time implementation fees**.

So true recurring revenue is lower. Without the exact split, the answer is a range:

- If implementation fees are **10%** of reported ARR, real ARR is about **$4.5M**
- If **20%**, real ARR is about **$4.0M**
- If **30%**, real ARR is about **$3.5M**

For diligence purposes, I’d probably underwrite to **$3.5M–$4.5M true ARR** unless proven otherwise.

### Step 2: Apply a multiple adjusted for quality
At face value, a business with:
- 100% YoY growth
- 85% gross margins
- 130% NRR

could maybe deserve a strong SaaS multiple.

But the risk factors are severe:

#### Negative adjustments
1. **40% revenue concentration in one customer**
   - This is a major discount.
   - If that customer churns or reprices, the company is impaired immediately.
   - Buyers often haircut concentration heavily or exclude some portion of concentrated revenue from premium multiple treatment.

2. **Questionable ARR quality**
   - Misclassifying implementation fees as ARR undermines trust in metrics.
   - That creates both a valuation discount and stronger legal protections in the deal.

3. **Key employee retention risk**
   - Losing 3 of 5 engineers post-close could materially damage product continuity.
   - This lowers the value of the acquired platform unless retention is locked down.

### Step 3: Use more realistic multiples
A clean, high-growth SaaS business might trade at, say, **8x–12x ARR** in a favorable market.

This is not clean.

Given the issues, I’d think more like:

- **4x–7x normalized ARR** if acquired as a going concern
- Possibly lower if concentration/customer diligence is poor
- Possibly structure part of value as earnout instead of upfront

### Valuation range
Using nor...
```

### DeepSeek V3

**Generation Time:** 102927ms
**Tokens:** 1577

```
### Understanding the Given Information

Before diving into the valuation and deal terms, it's crucial to fully understand the information provided about the startup:

1. **Acquisition Offer**: The company is offering to acquire the startup for $50 million.
2. **Startup's Financial Claims**:
   - **Annual Recurring Revenue (ARR)**: $5 million, growing at 100% year-over-year (YoY).
   - **Gross Margins**: 85%.
   - **Net Revenue Retention (NRR)**: 130%.
3. **Due Diligence Findings**:
   - **Customer Concentration**: 40% of revenue comes from a single customer.
   - **ARR Composition**: The reported ARR includes one-time implementation fees.
   - **Employee Retention Risk**: Three out of five engineers have unvested equity and might leave post-acquisition.

### Analyzing the Startup's Valuation

The initial valuation is based on the startup's claimed metrics. However, the due diligence reveals several red flags that could significantly impact the startup's true valuation. Let's break down each factor:

#### 1. Customer Concentration (40% from a single customer)

- **Impact**: High dependence on a single customer is risky. If this customer leaves, 40% of the revenue disappears.
- **Valuation Adjustment**: Typically, investors apply a discount for customer concentration. A common approach is to increase the discount rate or apply a revenue multiple discount. For instance, if the standard multiple is 10x ARR, with high concentration, it might be adjusted downward to 6-8x.

#### 2. ARR Includes One-Time Implementation Fees

- **Definition**: ARR should represent recurring, predictable revenue. One-time fees are non-recurring and shouldn't be included in ARR.
- **Impact**: If part of the $5M ARR is one-time fees, the true recurring revenue is lower.
- **Calculation**: Suppose 20% of ARR is one-time fees (this is an assumption; the exact percentage isn't given). Then:
  - One-time fees: $5M * 20% = $1M
  - True ARR: $5M - $1M = $4M

#### 3. Employee Retention Risk (Engineer...
```

### MiMo-V2-Flash

**Generation Time:** 17061ms
**Tokens:** 1804

```
This is a classic case of "revenue quality" over "revenue quantity." The startup’s headline metrics are impressive, but the due diligence findings reveal significant risks that fundamentally undermine the $50M valuation.

Here is an analysis of the real valuation and the deal terms required to mitigate these risks.

---

### Part 1: The Real Valuation

To determine the real valuation, we must adjust the financial metrics for quality and sustainability. A standard SaaS valuation formula uses a multiple of ARR, but that multiple must be discounted based on risk.

**1. Adjusting the ARR (The Revenue Quality)**
*   **Reported ARR:** $5M
*   **Adjustment A (One-time fees):** ARR stands for *Annual Recurring* Revenue. Implementation fees are non-recurring services. If these are included, they inflate the multiple.
    *   *Assumption:* If implementation fees are typically 20% of contract value, and they are improperly booked as ARR, we must strip them out.
    *   *Adjusted ARR:* $4.0M (conservative estimate).
*   **Adjustment B (Customer Concentration):** 40% of revenue comes from one customer.
    *   In SaaS, high concentration increases "churn risk." If that single customer leaves, revenue drops by 40% overnight.
    *   Standard valuation multiples assume a diversified customer base. A single customer at 40% concentration typically reduces the valuation multiple by 20-30% due to the "key man risk" of the account.

**2. Adjusting the Multiple**
*   **Base Multiple:** A company with 100% growth and 85% margins would typically trade at 10x–12x ARR.
*   **Risk Discounts:**
    *   *Concentration Discount:* 40% customer concentration applies a ~20% haircut to the multiple.
    *   *Product/Revenue Quality Discount:* Including one-time fees in ARR is a GAAP violation and suggests poor financial controls. This applies another ~10% haircut.
    *   *Growth Sustainability Discount:* 100% YoY growth is often driven by a few large logos. With one customer at 40%, this growth ma...
```

### Claude Sonnet 4.6

**Generation Time:** 47861ms
**Tokens:** 2164

```
# Startup Acquisition Analysis: Uncovering Real Value

## Step 1: Reconstructing True ARR

### Stripping Out the Noise

| Revenue Component | Claimed | Adjustment | Reality |
|-------------------|---------|------------|---------|
| Total "ARR" | $5.0M | — | — |
| One-time implementation fees | Included | Remove ~15-25% | ($750K-$1.25M) |
| **Recurring ARR** | $5.0M | | **~$3.75-4.25M** |
| Single customer concentration | 40% = $1.5-1.7M | Risk-weight at 50% | Effective loss exposure |
| **Risk-adjusted ARR** | | | **~$2.8-3.5M** |

**The honest number: call it $3.5M real ARR, not $5M**

### Why This Matters Immediately
- The growth rate claim deserves scrutiny: if prior year also included one-time fees, the 100% growth may be **partially fabricated momentum**
- Net retention of 130% needs verification: does it include upsells to the concentrated customer? If so, it's **one relationship masquerading as product-market fit**

---

## Step 2: Rebuilding the Valuation

### What They're Claiming vs. Reality

```
CLAIMED VALUATION BASIS:
$5M ARR × 10x multiple = $50M
(Reasonable for 100% growth, 85% GM, 130% NRR)

REALITY CHECK:
$3.5M real ARR × adjusted multiple = ?
```

### Multiple Compression Factors

| Factor | Premium/Discount | Rationale |
|--------|-----------------|-----------|
| Baseline SaaS (85% GM, strong NRR) | 8-10x | Legitimate quality metrics |
| Customer concentration >40% | -30 to -40% | Single point of failure |
| ARR quality issues | -20% | Trust/accounting red flag |
| Engineering team flight risk | -15% | 60% of technical capability at risk |
| **Net adjusted multiple** | **4-5x** | |

```
REAL VALUATION RANGE:
$3.5M × 4x = $14M (bear case)
$3.5M × 5x = $17.5M (base case)
$3.5M × 6x = $21M (bull case, if risks mitigated)

vs. Asking Price: $50M
Overvaluation: 2.4x to 3.6x
```

**The $50M ask has essentially no justification on current fundamentals.**

---

## Step 3: The Three Risk Vectors Unpacked

### Risk 1: Customer Concentration — This Is Existe...
```

### Grok 4.20

**Generation Time:** 4937ms
**Tokens:** 1158

```
**Realistic Valuation: $18M–$25M** (roughly 3.6x–5x *true* recurring revenue, not the claimed 10x).

### Why the $50M ask is wildly inflated

Let's normalize the numbers with what due diligence actually revealed:

- **True recurring revenue is materially lower than $5M.**
  - 40% concentration from one customer (huge key-man risk).
  - "ARR" includes one-time implementation fees. In early-stage SaaS, implementation fees are often 20–40% of first-year contract value. Conservatively, this likely inflates reported ARR by ~25–35%. Real recurring ARR is probably **$3.2M–$3.7M**.
  - 100% YoY growth on a polluted base is less impressive. True like-for-like recurring growth is likely closer to 60–75%.

- **Unit economics are good but not exceptional once concentration is factored in.**
  - 85% gross margins are strong.
  - 130% net retention is excellent *if* it holds without the big customer. But losing or even flat-renewing the 40% customer would destroy the metric.

- **Key technical talent risk is severe.**
  - 3 of 5 engineers have mostly unvested equity and "might leave." This is a major red flag in an acquisition. The product could stagnate or degrade post-deal. This alone can destroy 20–40% of the perceived value.

**Adjusted multiples (what a sophisticated buyer would actually pay):**
- Clean SaaS businesses with <20% customer concentration, clean recurring revenue, and a real engineering bench trade at 6–10x ARR in this range.
- With 40% concentration, polluted ARR, and key person risk, this is a **3.5–5.5x true recurring revenue** deal at best.

→ $3.4M normalized recurring revenue × 4–6x = **$18M–$25M** is the fair range. Anything above $28–30M is generous.

### Protective Deal Terms the Acquirer Should Demand

The acquirer should heavily structure the deal to protect against these risks. Here's the realistic term sheet:

1. **Majority of consideration in Earn-Outs / Holdbacks (very important)**
   - Only 30–50% paid at closing ($8M–$12M cash).
   - 50–70% in p...
```

### GPT-OSS-120B

**Generation Time:** 0ms
**Tokens:** 0

```

```

### Gemini 3 Flash Preview

**Generation Time:** 6610ms
**Tokens:** 983

```
This scenario highlights the difference between "headline metrics" and "investable quality." The startup is marketing itself at a **10x ARR multiple**, which is standard for high-growth SaaS, but the due diligence reveals significant structural risks that compress that multiple.

### 1. The "Real" Valuation Adjustment

To find the real valuation, we must first normalize the revenue and then apply a risk-adjusted multiple.

*   **Normalize the ARR:** If 20% of the $5M "ARR" is actually one-time implementation fees (a common ratio), the true recurring revenue is **$4M**.
*   **Concentration Discount:** A single customer representing 40% of revenue ($1.6M) is a "binary risk." If that customer leaves, the growth story ends. This usually triggers a 20–30% discount on the total valuation.
*   **Key Man Risk:** The potential departure of 60% of the engineering team threatens the product roadmap and post-merger integration (PMI).

**The Math:**
*   **Stated Valuation:** $50M (10x of $5M)
*   **Adjusted Revenue:** $4M
*   **Adjusted Multiple:** Due to concentration and talent risk, the multiple should drop from 10x to roughly 6x–7x.
*   **Estimated Real Valuation:** **$24M – $28M.**

The $50M asking price is likely aggressive unless the acquirer sees "strategic value" (e.g., the startup’s IP is the missing piece for a billion-dollar product line).

---

### 2. Deal Terms to Protect the Acquirer

If the acquirer still wants to proceed at or near the $50M price point, they must shift the risk from the balance sheet to the sellers using the following structures:

#### A. The Earn-out (Price Protection)
Instead of $50M upfront, structure the deal as **$25M at closing** with the remaining $25M tied to performance over 12–24 months.
*   **Specific Trigger:** The earn-out should be contingent on the "Single Large Customer" renewing their contract. If that customer churns, the payout is forfeited.

#### B. Holdbacks and Escrows (Indemnification)
Set aside 15–20% of the purchase pric...
```

### MiniMax M2.5

**Generation Time:** 52843ms
**Tokens:** 1647

```
Excellent question. This is a classic SaaS due diligence发现问题 (discovering issues). Let's break down the "real" valuation and protective deal terms.

### 1. Real Valuation Analysis

First, we must "normalize" the startup's claimed metrics to derive a realistic financial picture.

**Step 1: Normalize ARR**
*   **Issue:** "ARR includes one-time implementation fees." You need to estimate what % is truly recurring.
*   **Assumption:** For a startup of this size, a reasonable estimate might be 20-30% of the claimed $5M is one-time.
*   **Normalized ARR:** ~$3.5M - $4.0M. Let's use **$3.5M** as a conservative base.

**Step 2: Adjust for Growth & Retention**
*   **100% YoY Growth:** Impressive, but often decelerates. At $3.5M ARR, this is a small company. The growth rate is a major driver of valuation, but it's now viewed with skepticism given the other issues.
*   **Net Retention of 130%:** This is **below the benchmark** for a high-quality SaaS company (which is typically >120% and often 140%+ for best-in-class). It means existing customers are spending 30% more over time, but 70% of the cohort's starting revenue is gone or unchanged. This **reduces the value of the base**.

**Step 3: Apply a Valuation Multiple**
*   A typical SaaS multiple for a growth company (with these issues) might be **4x - 6x ARR** (public markets are lower, but private SaaS deals often command a premium for growth).
*   However, we must apply a **"risk discount"** for the following:
    *   **Customer Concentration (40% from one customer):** This is a massive risk. A rule of thumb is no single customer should be >10% of ARR. This alone could warrant a 20-30% discount to the multiple.
    *   **Key Person Risk (3 of 5 engineers may leave):** This threatens product continuity and execution. Another significant discount.
    *   **Accounting/Reporting Quality Risk:** The inclusion of one-time fees in ARR raises concerns about financial discipline and reporting.

**Conservative Valuation Estimate:**
*...
```

---

*Generated by The Multivac V5*
*https://themultivac.com*