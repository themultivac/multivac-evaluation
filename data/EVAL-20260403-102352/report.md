# Multivac Evaluation Report

**Evaluation ID:** EVAL-20260403-102352
**Timestamp:** 2026-04-03T10:23:52.775393
**Category:** Analysis & Research
**Model Pool:** 10 analysis-optimized models

## Question

You receive a job offer: $150K base, $50K RSUs/year, $20K signing bonus. The company's Glassdoor shows similar roles at $140K-$180K. You have a competing offer at $165K base, no RSUs. (1) Calculate total compensation for both over 4 years (assume 10% annual RSU appreciation). (2) What non-financial factors should affect the decision? (3) Write the counter-offer email that maximizes your outcome without risking the offer.

---

## Rankings

| Rank | Model | Score | Min | Max | Std Dev |
|------|-------|-------|-----|-----|---------|
| 1 | GPT-5.4 | 9.11 | 8.15 | 9.80 | 0.47 |
| 2 | Claude Sonnet 4.6 | 8.79 | 7.55 | 10.00 | 0.79 |
| 3 | Grok 4.20 | 8.68 | 7.50 | 9.55 | 0.60 |
| 4 | MiMo-V2-Flash | 8.63 | 7.75 | 9.80 | 0.70 |
| 5 | Gemini 3 Flash Preview | 8.30 | 7.75 | 9.00 | 0.45 |
| 6 | GPT-OSS-120B | 7.94 | 5.40 | 9.00 | 1.46 |
| 7 | DeepSeek V3 | 7.36 | 5.90 | 8.75 | 0.99 |
| 8 | Claude Opus 4.6 | 7.34 | 5.00 | 9.45 | 1.68 |
| 9 | Gemini 3.1 Pro | 3.82 | 2.60 | 6.15 | 1.43 |

---

## Meta Analysis

### Judge Strictness

| Rank | Judge | Avg Score Given |
|------|-------|-----------------|
| 1 | GPT-5.4 | 6.43 |
| 2 | GPT-OSS-120B | 7.13 |
| 3 | Grok 4.20 | 7.27 |
| 4 | Claude Opus 4.6 | 7.49 |
| 5 | Claude Sonnet 4.6 | 7.69 |
| 6 | MiniMax M2.5 | 7.85 |
| 7 | Gemini 3.1 Pro | 7.94 |
| 8 | MiMo-V2-Flash | 8.35 |
| 9 | DeepSeek V3 | 8.57 |
| 10 | Gemini 3 Flash Preview | 9.03 |

**Strictest Judge:** gpt_5_4
**Most Lenient Judge:** gemini_3_flash
**Total Judgments:** 100
**Valid Judgments:** 81

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

**Generation Time:** 28694ms
**Tokens:** 2166

```
Here is a complete breakdown of your compensation comparison, the non-financial factors to consider, and a strategic counter-offer email.

### Part 1: 4-Year Total Compensation (TC) Calculation

*Assumption: The RSUs are granted at a fixed initial dollar value ($200K total, vesting $50K annually) and the stock price appreciates by 10% year-over-year from the grant date.*

**Offer A (The Primary Offer)**
*   **Base Salary:** $150,000 × 4 years = $600,000
*   **Signing Bonus:** $20,000 (paid in Year 1)
*   **RSUs (with 10% annual compounding appreciation):**
    *   Year 1 Vest: $50,000 × 1.10 = $55,000
    *   Year 2 Vest: $50,000 × 1.21 = $60,500
    *   Year 3 Vest: $50,000 ×
```

### Claude Opus 4.6

**Generation Time:** 41629ms
**Tokens:** 2170

```
# Comprehensive Job Offer Analysis & Negotiation Strategy

## Part 1: Four-Year Total Compensation Comparison

### Offer A: $150K Base + RSUs + Signing Bonus

**Base Salary (assuming no raises for clean comparison):**
- Year 1-4: $150,000 × 4 = **$600,000**

**RSUs with 10% Annual Appreciation:**
- Year 1 grant: $50,000 (vests at face value) = $50,000
- Year 2 grant: $50,000 + Year 1 grant appreciates 10% = $50,000 + $5,000 = $55,000 in new value
- But let me calculate this more precisely:

**RSU Vesting Schedule (standard 4-year with annual vesting):**

Assuming each year you receive $50K in RSUs that appreciate 10% annually after grant:

| Grant | Year 1 | Year 2 | Year 3 | Year 4 | Total Value |
|-------|--------|--------|--------|--------|-------------|
| Year 1 ($50K) | $50,000 | $55,000 | $60,500 | $66,550 | Cumulative appreciation |
| Year 2 ($50K) | — | $50,000 | $55,000 | $60,500 | |
| Year 3 ($50K) | — | — | $50,000 | $55,000 | |
| Year 4 ($50K) | — | — | — | $50,000 | |

**Realized RSU value per year (assuming each grant vests 25% per year):**

Let me recalculate with a clearer model. $50K/year granted, each grant vests over 4 years (25% annually), stock appreciates 10%/year:

**Year 1 RSU grant ($50K):**
- 25% vests Year 1: $12,500 × 1.0 = $12,500
- 25% vests Year 2: $12,500 × 1.1 = $13,750
- 25% vests Year 3: $12,500 × 1.21 = $15,125
- 25% vests Year 4: $12,500 × 1.331 = $16,638

**Year 2 RSU grant ($50K):**
- 25% vests Year 2: $12,500
- 25% vests Year 3: $13,750
- 25% vests Year 4: $15,125

**Year 3 RSU grant ($50K):**
- 25% vests Year 3: $12,500
- 25% vests Year 4: $13,750

**Year 4 RSU grant ($50K):**
- 25% vests Year 4: $12,500

**Total RSU income realized over 4 years:**

| Year | RSU Income Realized |
|------|-------------------|
| Year 1 | $12,500 |
| Year 2 | $13,750 + $12,500 = $26,250 |
| Year 3 | $15,125 + $13,750 + $12,500 = $41,375 |
| Year 4 | $16,638 + $15,125 + $13,750 + $12,500 = $58,013 |
| **4-Year Total** | **$138,138** |

**Note:** ...
```

### GPT-5.4

**Generation Time:** 31893ms
**Tokens:** 1889

```
## 1) 4-year total compensation comparison

I’ll assume:

- **Offer A**
  - Base: **$150,000**
  - RSUs: **$50,000 granted per year**
  - Sign-on: **$20,000 one-time**
  - RSUs appreciate **10% annually**
- **Offer B**
  - Base: **$165,000**
  - No RSUs
  - No sign-on mentioned

### Offer A: 4-year compensation

#### Base salary
- $150,000 × 4 = **$600,000**

#### Sign-on bonus
- **$20,000**

#### RSUs with 10% annual appreciation
Assuming each year’s $50K grant is worth more by the time it vests over the remaining years:

- Year 1 grant: $50,000 × 1.1³ = **$66,550**
- Year 2 grant: $50,000 × 1.1² = **$60,500**
- Year 3 grant: $50,000 × 1.1¹ = **$55,000**
- Year 4 grant: $50,000 × 1.0 = **$50,000**

Total RSU value over 4 years:
- **$66,550 + $60,500 + $55,000 + $50,000 = $232,050**

#### Total for Offer A
- Base: $600,000
- Sign-on: $20,000
- RSUs: $232,050

**Total = $852,050**

---

### Offer B: 4-year compensation

#### Base salary
- $165,000 × 4 = **$660,000**

#### Equity / sign-on
- None stated

**Total = $660,000**

---

### Comparison

- **Offer A total:** **$852,050**
- **Offer B total:** **$660,000**
- **Difference:** **$192,050 in favor of Offer A**

### Important caveat
This comparison assumes:
- You stay all 4 years
- RSUs vest and are actually retained/sold at appreciated value
- No refresh grants, raises, bonus, or promotion differences
- The stock actually appreciates 10% annually

If you value RSUs more conservatively, Offer A is still strong:

- Without appreciation, RSUs = $200,000 over 4 years
- Then Offer A total = $600,000 + $20,000 + $200,000 = **$820,000**
- Still **$160,000 ahead** of Offer B

---

## 2) Non-financial factors that should affect the decision

You should not choose purely on headline compensation. Key factors:

### Role quality and career trajectory
- Will the role build skills you want?
- Is the title stronger?
- Does one role position you better for future promotions or leadership?
- Which brand is better on your résumé?

#...
```

### DeepSeek V3

**Generation Time:** 22201ms
**Tokens:** 852

```
### (1) **Calculate Total Compensation Over 4 Years**  

#### **Offer 1: Current Offer**  
- **Base Salary:** $150K/year  
- **RSUs:** $50K/year (vesting over 4 years, assume 10% annual appreciation)  
- **Signing Bonus:** $20K (one-time)  

**RSU Calculation (10% Appreciation per Year):**  
- Year 1 RSUs: $50K × (1.1)^3 = $66.55K  
- Year 2 RSUs: $50K × (1.1)^2 = $60.50K  
- Year 3 RSUs: $50K × (1.1) = $55K  
- Year 4 RSUs: $50K  

**Total RSU Value (vested at end of each year):**  
= $66.55K + $60.50K + $55K + $50K = **$232.05K**  

**Total Compensation Over 4 Years:**  
= ($150K × 4) + $232.05K + $20K = **$852.05K**  

#### **Offer 2: Competing Offer**  
- **Base Salary:** $165K/year  
- **No RSUs or Bonus**  

**Total Compensation Over 4 Years:**  
= $165K × 4 = **$660K**  

**Comparison:**  
- Offer 1: **$852.05K** (higher due to RSU appreciation)  
- Offer 2: **$660K**  

*(Note: Taxes, liquidity, and company stock risk could adjust this.)*  

---

### (2) **Non-Financial Factors to Consider**  
- **Career Growth:** Which role offers better advancement opportunities?  
- **Company Culture:** Glassdoor reviews, work-life balance, and team fit.  
- **Job Security:** Stability of each company (startup vs. established).  
- **Remote/Work Policy:** Office vs. hybrid vs. remote flexibility.  
- **Benefits:** Healthcare, 401(k) matching, PTO, and perks.  
- **Equity Potential:** If RSUs are in a high-growth company, they could be worth much more.  
- **Commute/Relocation:** Time and cost of travel.  
- **Team & Leadership:** Better mentorship can accelerate career.  

---

### (3) **Counter-Offer Email (Maximizing Value Without Risking Offer)**  

**Subject:** Excited About the Opportunity – Discussing Offer Details  

Hi [Hiring Manager's Name],  

Thank you for extending the offer for [Role] at [Company]. I’m genuinely excited about the opportunity and the impact I can contribute to [specific project/team].  

Before finalizing, I wanted to discuss the compensation...
```

### MiMo-V2-Flash

**Generation Time:** 14612ms
**Tokens:** 2042

```
Here is a detailed breakdown of the offer, the financial analysis, non-financial considerations, and a strategic counter-offer email.

### Part 1: Financial Analysis (4-Year Projection)

**Assumptions:**
*   **Offer A:** $150K base, $50K RSUs/year, $20K signing bonus.
*   **Offer B:** $165K base, $0 RSUs, $0 signing bonus.
*   **RSU Appreciation:** 10% annually (compounded).
*   **Tax:** We will calculate gross pre-tax compensation to avoid variables in state/local tax rates.
*   **Vesting:** RSUs vest annually (standard single-trigger vesting).
*   **Bonuses:** We assume no annual cash bonus unless specified; only the signing bonus for Offer A.

#### Offer A: Total Compensation (4 Years)

| Year | Base Salary | Signing Bonus | RSU Value (Vesting) | Annual Total | Cumulative Total |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Year 1** | $150,000 | $20,000 | $50,000 | **$220,000** | $220,000 |
| **Year 2** | $150,000 | $0 | $55,000 ($50k × 1.10) | **$205,000** | $425,000 |
| **Year 3** | $150,000 | $0 | $60,500 ($55k × 1.10) | **$210,500** | $635,500 |
| **Year 4** | $150,000 | $0 | $66,550 ($60.5k × 1.10) | **$216,550** | **$852,050** |

*   **4-Year Gross Total:** **$852,050**
*   *Note:* If RSUs remain flat (0% appreciation), the 4-year total would be $820,000.

#### Offer B: Total Compensation (4 Years)

| Year | Base Salary | Signing Bonus | RSU Value | Annual Total | Cumulative Total |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Year 1** | $165,000 | $0 | $0 | **$165,000** | $165,000 |
| **Year 2** | $165,000 | $0 | $0 | **$165,000** | $330,000 |
| **Year 3** | $165,000 | $0 | $0 | **$165,000** | $495,000 |
| **Year 4** | $165,000 | $0 | $0 | **$165,000** | **$660,000** |

*   **4-Year Gross Total:** **$660,000**

#### Comparison & Break-Even Analysis

*   **Difference:** Offer A is worth **$192,050 more** over 4 years than Offer B.
*   **Break-even:** Even if Offer A's stock price dropped by **22%** every year (instead of growing 10%), the RSUs would s...
```

### Claude Sonnet 4.6

**Generation Time:** 41965ms
**Tokens:** 2169

```
# Comprehensive Job Offer Analysis

---

## Part 1: Total Compensation Analysis (4-Year Projection)

### Setting Up the RSU Calculation Correctly

Most people get this wrong. Let me be precise about assumptions:
- RSUs vest over 4 years (typical 25%/year cliff or monthly)
- 10% annual appreciation applies to the **grant price**, affecting future grant value
- Signing bonus is often subject to clawback if you leave within 12-24 months

**Offer A: $150K Base + $50K RSUs/year + $20K Signing**

| Year | Base Salary | RSU Vest (appreciated) | Signing Bonus | Annual Total |
|------|-------------|------------------------|---------------|--------------|
| 1 | $150,000 | $50,000 × 1.10 = $55,000 | $20,000 | **$225,000** |
| 2 | $150,000 | $50,000 × 1.21 = $60,500 | $0 | **$210,500** |
| 3 | $150,000 | $50,000 × 1.33 = $66,550 | $0 | **$216,550** |
| 4 | $150,000 | $50,000 × 1.46 = $73,205 | $0 | **$223,205** |
| **4-Year Total** | **$600,000** | **$255,255** | **$20,000** | **$875,255** |

> **Critical caveat:** RSU appreciation assumes stock price growth, which is not guaranteed. A 10% *decline* scenario yields only $776,000 over 4 years.

**Offer B: $165K Base, No RSUs, No Signing**

| Year | Base Salary | Annual Total |
|------|-------------|--------------|
| 1 | $165,000 | **$165,000** |
| 2 | $165,000 | **$165,000** |
| 3 | $165,000 | **$165,000** |
| 4 | $165,000 | **$165,000** |
| **4-Year Total** | **$660,000** | **$660,000** |

### Head-to-Head Comparison

| Metric | Offer A | Offer B | Difference |
|--------|---------|---------|------------|
| 4-Year Total (10% RSU growth) | $875,255 | $660,000 | **+$215,255 (Offer A)** |
| 4-Year Total (0% RSU growth) | $820,000 | $660,000 | **+$160,000 (Offer A)** |
| 4-Year Total (RSU -20%/yr) | $724,400 | $660,000 | **+$64,400 (Offer A)** |
| 4-Year Total (RSU -40%/yr) | $632,000 | $660,000 | **+$27,000 (Offer B)** |
| Year 1 cash in hand | $225,000* | $165,000 | *After signing |
| Guaranteed cash only | $620,000 | $660,000 | *...
```

### Grok 4.20

**Generation Time:** 4842ms
**Tokens:** 1204

```
**Here's a clear, professional breakdown:**

### (1) Total Compensation Calculation Over 4 Years

**Offer A (Current company):**
- Base: $150,000/year
- RSUs: $50,000/year (at grant value) with 10% annual appreciation
- Signing bonus: $20,000 (one-time, Year 0)

**RSU value with 10% annual appreciation** (assuming you receive a new $50k grant each year at the then-current stock price):

- Year 1 grant: $50k → value at end of Year 4: $50k × 1.1³ = **$66,550**
- Year 2 grant: $50k → value at end of Year 4: $50k × 1.1² = **$60,500**
- Year 3 grant: $50k → value at end of Year 4: $50k × 1.1¹ = **$55,000**
- Year 4 grant: $50k → value at end of Year 4: **$50,000**

**Total RSU value at end of Year 4: $232,050**

**Cash compensation:**
- Signing bonus: $20,000
- Base salary (4 years): $150k × 4 = $600,000
- **Total cash: $620,000**

**Total compensation (cash + appreciated RSUs): $852,050** over 4 years (~$213k annualized)

**Offer B (Competing offer):**
- Base: $165,000/year, no RSUs
- Total cash: $165k × 4 = **$660,000**

**Comparison:**
- Offer A is worth **~$192k more** in total compensation over 4 years under the 10% appreciation assumption.
- Even without any stock appreciation, Offer A is still ahead by ~$110k over 4 years.

### (2) Non-Financial Factors to Consider

- **Career growth & impact**: Which role offers better title, scope, learning opportunities, or exposure to high-visibility projects?
- **Team & manager quality**: Glassdoor/levels.fyi reviews, interview experience, and references from future teammates.
- **Work-life balance & culture**: Burnout risk, remote/hybrid policy, meeting load, on-call expectations.
- **Equity upside**: Is the company private or public? What’s the realistic growth potential beyond 10% (or downside risk)?
- **Location & cost of living**: Taxes, commute, and housing costs (especially important if one requires relocation).
- **Stability & mission alignment**: Do you believe in the company’s direction? Layoff risk?
- **Visa/immigr...
```

### GPT-OSS-120B

**Generation Time:** 171393ms
**Tokens:** 2222

```
**1️⃣ 4‑Year Compensation Comparison (USD)**  

| Component | Offer A (Base $150K + $50K RSUs / yr + $20K signing) | Offer B (Base $165K, no RSUs) |
|-----------|---------------------------------------------------|--------------------------------|
| **Base salary** (4 yr) | $150,000 × 4 = **$600,000** | $165,000 × 4 = **$660,000** |
| **Signing bonus** (one‑time) | **$20,000** | $0 |
| **RSU value** (10 % annual appreciation) | Year‑1 grant: $50K × 1.10³ = $66,550  <br>Year‑2 grant: $50K × 1.10² = $60,500  <br>Year‑3 grant: $50K × 1.10¹ = $55,000  <br>Year‑4 grant: $50K × 1.10⁰ = $50,000  <br>**Total RSU value:** **$232,050** | $0 |
| **Total 4‑yr cash‑plus‑equity** | $600,000 + $20,000 + $232,050 = **$852,050** | $660,000 |
| **Difference (A – B)** | **+$192,050** | — |

*Assumptions:* each year’s RSU grant vests in cash at the end of the 4‑year horizon and appreciates 10 % per year (compound). No tax effects are modelled.

---

**2️⃣ Non‑Financial Factors to Weigh**

| Category | Why It Matters | Questions to Ask Yourself |
|----------|----------------|---------------------------|
| **Role & Scope** | Does the job give you ownership, technical depth, and the kind of projects that align with your career story? | Will I be building core products or supporting peripheral features? |
| **Career Growth & Promotion Path** | Faster promotions, mentorship, and exposure to senior leadership accelerate long‑term earning power. | Is there a clear ladder (L5 → L6 → …) and a track record of internal promotions? |
| **Technology Stack & Learning** | Working with modern, in‑demand tech makes you more marketable. | Does the stack match the skills I want to deepen (e.g., cloud, AI, data‑platforms)? |
| **Company Stability & Funding** | A well‑capitalized, profitable firm reduces the risk of equity dilution or layoffs. | What is the runway, recent funding rounds, and revenue trajectory? |
| **Equity Liquidity & Vesting** | RSUs are only valuable if the company stays private long en...
```

### Gemini 3 Flash Preview

**Generation Time:** 7597ms
**Tokens:** 1174

```
### 1. Total Compensation Calculation (4-Year Outlook)

To compare these accurately, we will factor in the $20K signing bonus (Year 1 only) and a 10% annual appreciation on the RSU grants for Offer A.

#### **Offer A: $150K Base + $50K RSUs + $20K Sign-on**
*   **Year 1:** $150K + $50K + $20K = **$220,000**
*   **Year 2:** $150K + $55K (10% growth) = **$205,000**
*   **Year 3:** $150K + $60.5K (10% growth) = **$210,500**
*   **Year 4:** $150K + $66.5K (10% growth) = **$216,500**
*   **4-Year Total: $852,000**

#### **Offer B: $165K Base (No RSUs)**
*   **Year 1–4:** $165,000 x 4 = **$660,000**
*   **4-Year Total: $660,000**

**Financial Verdict:** Offer A leads by **$192,000** over four years. Even if the stock price remains flat (0% growth), Offer A still beats Offer B by $110,000.

---

### 2. Non-Financial Factors to Consider

While Offer A is financially superior, consider these "hidden" variables:
*   **Liquidity vs. Paper Wealth:** Offer B is 100% cash. If Offer A is a private startup, those RSUs may be worth $0 for years. If it is a public company, RSUs are as good as cash.
*   **The "Floor" vs. the "Ceiling":** $165K is your guaranteed floor. In a market downturn, Offer A’s total comp could drop if the stock price falls, whereas your base salary is protected.
*   **Work-Life Balance & Burnout:** Does the higher-paying role expect 60-hour weeks? A $192K gap is significant, but not if it costs you your mental health.
*   **Career Trajectory:** Which company has a stronger brand name for your resume? Which role offers a direct path to a promotion or management?
*   **Benefits Delta:** Compare 401(k) matching, health insurance premiums, and PTO. A 5% 401(k) match on $150K is an extra $7,500/year.

---

### 3. Counter-Offer Email Template

This email leverages your competing offer to nudge the base salary higher while remaining professional and "excited" to join, which minimizes the risk of rescission.

**Subject:** Regarding the offer for [Job Title] - [Your Nam...
```

### MiniMax M2.5

**Generation Time:** 97665ms
**Tokens:** 2192

```

```

---

*Generated by The Multivac V5*
*https://themultivac.com*