# Multivac Evaluation Report

**Evaluation ID:** EVAL-20260207-144351
**Timestamp:** 2026-02-07T14:43:51.639044
**Category:** Analysis & Research
**Model Pool:** 10 analysis-optimized models

## Question

Your team ran an A/B test on a checkout flow. Here are the results:

Control (A): 10,000 visitors, 320 conversions (3.2%)
Treatment (B): 10,000 visitors, 380 conversions (3.8%)

The product manager says: "B wins! Let's ship it - that's an 18.75% improvement!"

1. Calculate the statistical significance (provide p-value)
2. What's the 95% confidence interval for the true difference?
3. The test ran for 2 days. What concerns does this raise?
4. You discover Treatment B had a bug on iOS that blocked 2,000 users from even reaching checkout. How does this change your analysis?
5. What would you recommend?

---

## Rankings

| Rank | Model | Score | Min | Max | Std Dev |
|------|-------|-------|-----|-----|---------|
| 1 | MiMo-V2-Flash | 9.69 | 9.00 | 10.00 | 0.37 |
| 2 | Claude Sonnet 4.5 | 9.61 | 8.80 | 10.00 | 0.44 |
| 3 | DeepSeek V3.2 | 9.56 | 8.80 | 10.00 | 0.48 |
| 4 | Claude Opus 4.5 | 9.53 | 8.80 | 10.00 | 0.50 |
| 5 | Gemini 3 Flash Preview | 9.43 | 8.55 | 10.00 | 0.56 |
| 6 | Grok 4.1 Fast | 9.39 | 9.00 | 9.55 | 0.22 |
| 7 | GPT-OSS-120B | 8.63 | 8.10 | 9.00 | 0.30 |
| 8 | Gemini 2.5 Flash | 8.33 | 6.50 | 9.45 | 1.11 |
| 9 | GPT-OSS-120B (Legal) | 7.69 | 5.80 | 9.00 | 1.05 |
| 10 | Gemini 3 Pro Preview | 2.82 | 1.50 | 5.80 | 1.41 |

---

## Meta Analysis

### Judge Strictness

| Rank | Judge | Avg Score Given |
|------|-------|-----------------|
| 1 | GPT-OSS-120B | 4.92 |
| 2 | GPT-OSS-120B (Legal) | 7.59 |
| 3 | Claude Opus 4.5 | 7.99 |
| 4 | MiMo-V2-Flash | 8.12 |
| 5 | Claude Sonnet 4.5 | 8.45 |
| 6 | DeepSeek V3.2 | 8.47 |
| 7 | Gemini 2.5 Flash | 8.76 |
| 8 | Gemini 3 Flash Preview | 8.91 |
| 9 | Grok 4.1 Fast | 8.98 |

**Strictest Judge:** gpt_oss_120b
**Most Lenient Judge:** grok_4_1_fast
**Total Judgments:** 100
**Valid Judgments:** 73

---

## Model Pool

Models selected for **Analysis & Research** evaluation:

1. **MiMo-V2-Flash** (openrouter)
2. **Gemini 3 Flash Preview** (openrouter)
3. **Gemini 2.5 Flash** (openrouter)
4. **GPT-OSS-120B** (openrouter)
5. **DeepSeek V3.2** (openrouter)
6. **Claude Sonnet 4.5** (openrouter)
7. **Claude Opus 4.5** (openrouter)
8. **GPT-OSS-120B (Legal)** (openrouter)
9. **Gemini 3 Pro Preview** (openrouter)
10. **Grok 4.1 Fast** (openrouter)

---

## Model Responses

### MiMo-V2-Flash

**Generation Time:** 14443ms
**Tokens:** 2247

```
Here is the analysis of your A/B test results.

### 1. Statistical Significance (P-value)

To calculate the statistical significance, we perform a two-proportion z-test.

*   **Null Hypothesis ($H_0$):** There is no difference in conversion rates between Control and Treatment ($p_A = p_B$).
*   **Alternative Hypothesis ($H_1$):** There is a difference ($p_A \neq p_B$).

**The Data:**
*   **Control (A):** $n_A = 10,000$, $x_A = 320$, $\hat{p}_A = 0.032$
*   **Treatment (B):** $n_B = 10,000$, $x_B = 380$, $\hat{p}_B = 0.038$
*   **Pooled Proportion ($\hat{p}$):** $\frac{320 + 380}{10,000 + 10,000} = \frac{700}{20,000} = 0.035$

**Standard Error (SE):**
$$SE = \sqrt{\hat{p}(1-\hat{p}) \left(\frac{1}{n_A} + \frac{1}{n_B}\right)}$$
$$SE = \sqrt{0.035 \times 0.965 \times \left(\frac{1}{10,000} + \frac{1}{10,000}\right)}$$
$$SE = \sqrt{0.033775 \times 0.0002} \approx 0.0026$$

**Z-Score:**
$$z = \frac{\hat{p}_B - \hat{p}_A}{SE} = \frac{0.038 - 0.032}{0.0026} \approx 2.31$$

**P-value:**
Using a standard normal distribution table, a Z-score of 2.31 corresponds to a p-value of approximately **0.021** (two-tailed).

**Conclusion:** Since $p < 0.05$, the result is statistically significant. However, it is not highly significant (which usually requires $p < 0.01$).

***

### 2. 95% Confidence Interval for the True Difference

We want to estimate the true difference in conversion rates ($p_B - p_A$).

*   **Difference ($\Delta$):** $0.038 - 0.032 = 0.006$ (or 0.6%)
*   **Standard Error (using unpooled variances for CI):**
    $$SE = \sqrt{\frac{\hat{p}_A(1-\hat{p}_A)}{n_A} + \frac{\hat{p}_B(1-\hat{p}_B)}{n_B}}$$
    $$SE = \sqrt{\frac{0.032 \times 0.968}{10,000} + \frac{0.038 \times 0.962}{10,000}}$$
    $$SE = \sqrt{0.0000031 + 0.0000037} = \sqrt{0.0000068} \approx 0.00261$$

*   **Margin of Error (95% Confidence, $z=1.96$):**
    $$ME = 1.96 \times 0.00261 \approx 0.0051$$

*   **Confidence Interval:**
    $$0.006 \pm 0.0051$$
    **Lower Bound:** 0.0009 (0.09%)
    **Upper Bo...
```

### Gemini 3 Flash Preview

**Generation Time:** 12886ms
**Tokens:** 1209

```
Here are the responses to your A/B test analysis:

### 1. Statistical Significance (p-value)
To calculate this, we use a two-proportion Z-test.
*   **Control Rate ($p_A$):** 0.032
*   **Treatment Rate ($p_B$):** 0.038
*   **Pooled Proportion ($p$):** $(320 + 380) / (10,000 + 10,000) = 0.035$
*   **Standard Error ($SE$):** $\sqrt{p(1-p) \cdot (1/n_A + 1/n_B)} = \sqrt{0.035 \cdot 0.965 \cdot (1/10,000 + 1/10,000)} \approx 0.0026$
*   **Z-score:** $(0.038 - 0.032) / 0.0026 = 2.307$

**The p-value is approximately 0.021.**
Since 0.021 < 0.05, the result is technically **statistically significant** at the 95% confidence level.

### 2. 95% Confidence Interval for the Difference
The observed difference is **0.6%** (or 0.006).
Using the formula $CI = (p_B - p_A) \pm 1.96 \cdot \sqrt{\frac{p_A(1-p_A)}{n_A} + \frac{p_B(1-p_B)}{n_B}}$:
*   $SE_{diff} = \sqrt{0.0000030976 + 0.0000036556} \approx 0.00259$
*   $Margin of Error = 1.96 \cdot 0.00259 \approx 0.00508$

**The 95% Confidence Interval is [0.09%, 1.11%].**
While the PM claims an 18.75% relative lift, the absolute lift could be as low as 0.09 percentage points.

### 3. Concerns with a 2-day Duration
Running a test for only 2 days is problematic for several reasons:
*   **Weekly Seasonality:** User behavior on a Tuesday is often different from a Saturday. You haven't captured a full "business cycle."
*   **Sample Selection Bias:** You may be capturing only "early adopters" or a specific subset of traffic that doesn't represent your long-term user base.
*   **Novelty Effect:** Users might click on "B" simply because it looks new, but this behavior will normalize (and potentially drop) over time.

### 4. The iOS Bug (2,000 users blocked)
This discovery **invalidates the current results.** 
*   **The "Hidden" Conversion Rate:** If 2,000 iOS users were blocked, the 380 conversions actually came from only **8,000** reachable users. That is a **4.75% conversion rate** for those who could actually see the page.
*   **Selection Bi...
```

### Gemini 2.5 Flash

**Generation Time:** 10716ms
**Tokens:** 2232

```
Let's break down this A/B test analysis.

### 1. Calculate the Statistical Significance (p-value)

To calculate statistical significance, we'll use a two-proportion z-test.

**Hypotheses:**
*   **Null Hypothesis ($H_0$):** There is no difference in conversion rates between Control (A) and Treatment (B). ($p_A = p_B$)
*   **Alternative Hypothesis ($H_1$):** There is a difference in conversion rates between Control (A) and Treatment (B). ($p_A \neq p_B$)

**Data:**
*   $N_A = 10,000$, $X_A = 320$, $p_A = 320/10000 = 0.032$
*   $N_B = 10,000$, $X_B = 380$, $p_B = 380/10000 = 0.038$

**Pooled Proportion ($\hat{p}$):**
$\hat{p} = (X_A + X_B) / (N_A + N_B) = (320 + 380) / (10000 + 10000) = 700 / 20000 = 0.035$

**Standard Error of the Difference ($\text{SE}_{diff}$):**
$\text{SE}_{diff} = \sqrt{\hat{p}(1-\hat{p}) * (1/N_A + 1/N_B)}$
$\text{SE}_{diff} = \sqrt{0.035(1-0.035) * (1/10000 + 1/10000)}$
$\text{SE}_{diff} = \sqrt{0.035 * 0.965 * (0.0001 + 0.0001)}$
$\text{SE}_{diff} = \sqrt{0.033775 * 0.0002}$
$\text{SE}_{diff} = \sqrt{0.000006755}$
$\text{SE}_{diff} \approx 0.002599$

**Z-score:**
$Z = (p_B - p_A) / \text{SE}_{diff}$
$Z = (0.038 - 0.032) / 0.002599$
$Z = 0.006 / 0.002599$
$Z \approx 2.308$

**P-value (two-tailed):**
Using a standard normal distribution table or calculator, the p-value for $Z \approx 2.308$ is approximately $2 * P(Z > 2.308) \approx 2 * 0.01048 \approx 0.02096$.

**P-value $\approx 0.021$**

**Conclusion for Significance:**
Since the p-value (0.021) is less than the common significance level of 0.05, we **reject the null hypothesis**. This means there is statistically significant evidence to suggest that Treatment B has a different conversion rate than Control A.

### 2. What's the 95% Confidence Interval for the True Difference?

The confidence interval for the difference in proportions is calculated as:
$(p_B - p_A) \pm Z_{\alpha/2} * \text{SE}_{diff\_unpooled}$

Here, we need the *unpooled* standard error for the confidence interval.
**Standar...
```

### GPT-OSS-120B

**Generation Time:** 15994ms
**Tokens:** 2271

```
.Below is a step‑by‑step walk‑through of the numbers and the practical implications.  

---

## 1.  Statistical significance of the original result  

| Variant | Visitors (n) | Conversions (x) | Conversion rate (p̂) |
|---------|--------------|----------------|----------------------|
| Control (A) | 10 000 | 320 | 0.0320 (3.20 %) |
| Treatment (B) | 10 000 | 380 | 0.0380 (3.80 %) |

**Difference in conversion rates**  
\[
\Delta = \hat p_B-\hat p_A = 0.0380-0.0320 = 0.0060\;(0.60\% \text{ absolute increase})
\]

**Two‑sample proportion z‑test**  

* Pooled proportion:  

\[
\hat p = \frac{x_A+x_B}{n_A+n_B}= \frac{320+380}{20\,000}=0.035
\]

* Standard error of the difference:  

\[
SE = \sqrt{\hat p(1-\hat p)\Big(\frac{1}{n_A}+\frac{1}{n_B}\Big)}
     = \sqrt{0.035\times0.965\Big(\frac{1}{10\,000}+\frac{1}{10\,000}\Big)}
     = \sqrt{0.033775\times0.0002}=0.00260
\]

* z‑statistic:  

\[
z = \frac{\Delta}{SE}= \frac{0.0060}{0.00260}=2.31
\]

* Two‑tailed p‑value:  

\[
p = 2\bigl[1-\Phi(2.31)\bigr] \approx 2(1-0.9896)=0.021
\]

**Result:** *p ≈ 0.02* → the uplift is statistically significant at the conventional 5 % level (but not at 1 %).  

---

## 2.  95 % confidence interval for the true difference  

\[
\text{CI}_{95\%}= \Delta \pm 1.96 \times SE
                = 0.0060 \pm 1.96\times0.00260
                = 0.0060 \pm 0.0051
\]

\[
\boxed{0.0009\; \text{to}\; 0.0111}
\]

Interpretation: we are 95 % confident that the **absolute** lift lies between **0.09 % and 1.11 %** (i.e., between roughly a 2.8 % and 34.7 % *relative* increase over the control).

---

## 3.  “Only 2 days” – why that matters  

Running an A/B test for just two days raises several methodological red flags:

| Issue | Why it matters |
|-------|----------------|
| **Day‑of‑week / time‑of‑day effects** | Traffic composition (e.g., business vs. leisure shoppers) can differ dramatically between weekdays and weekends. Two days may capture an atypical pattern. |
| **Novelty / “first‑day” effect** ...
```

### DeepSeek V3.2

**Generation Time:** 69698ms
**Tokens:** 3940

```
### 1. Statistical Significance (p-value)
Using a two-proportion z-test:
- Control proportion: \( p_A = 320/10000 = 0.032 \)
- Treatment proportion: \( p_B = 380/10000 = 0.038 \)
- Pooled proportion: \( p = (320 + 380) / (10000 + 10000) = 0.035 \)
- Standard error under null:  
  \[
  SE = \sqrt{p(1-p) \left( \frac{1}{10000} + \frac{1}{10000} \right)} = \sqrt{0.035 \times 0.965 \times 0.0002} \approx 0.002599
  \]
- Test statistic:  
  \[
  z = \frac{p_B - p_A}{SE} = \frac{0.006}{0.002599} \approx 2.308
  \]
- Two-sided p-value:  
  \[
  p = 2 \times P(Z > 2.308) \approx 0.021
  \]

**p-value ≈ 0.021**

---

### 2. 95% Confidence Interval for the True Difference
- Difference: \( \hat{d} = p_B - p_A = 0.006 \)
- Standard error:  
  \[
  SE_{\hat{d}} = \sqrt{ \frac{p_A(1-p_A)}{n_A} + \frac{p_B(1-p_B)}{n_B} } = \sqrt{ \frac{0.032 \times 0.968}{10000} + \frac{0.038 \times 0.962}{10000} } \approx 0.002599
  \]
- Margin of error: \( 1.96 \times SE_{\hat{d}} \approx 0.005093 \)
- 95% CI:  
  \[
  0.006 \pm 0.005093 \quad \Rightarrow \quad (0.0009,\ 0.0111)
  \]
  or approximately **(0.09%, 1.11%)**.

---

### 3. Concerns with a 2-Day Test
- **Day-of-week effects**: The results may not be representative if the test only covered specific days (e.g., weekdays vs. weekends).
- **Novelty or learning effects**: Users may react differently to a new feature initially.
- **Insufficient data**: Short tests may not capture long-term behavior or repeat visits.
- **External events**: Unusual occurrences on those days could skew results.
- **Sample representativeness**: A longer duration ensures a more diverse and stable sample.

---

### 4. Impact of the iOS Bug
The bug blocked 2,000 users in Treatment B from reaching checkout, likely preventing them from converting. This means:
- The reported conversion rate for B (3.8%) is based on all 10,000 visitors, but 2,000 had no chance to convert.
- If we consider only the 8,000 unaffected users, the conversion rate becomes \( 380/8000 = 4.75\...
```

### Claude Sonnet 4.5

**Generation Time:** 25963ms
**Tokens:** 1265

```
# A/B Test Analysis

## 1. Statistical Significance

Using a two-proportion z-test:

**Calculations:**
- p_A = 320/10,000 = 0.032
- p_B = 380/10,000 = 0.038
- p_pooled = (320 + 380)/(10,000 + 10,000) = 0.035
- SE = √[0.035 × 0.965 × (1/10,000 + 1/10,000)] = 0.00259
- z = (0.038 - 0.032)/0.00259 = 2.316

**p-value ≈ 0.021** (two-tailed)

At α = 0.05, this *is* statistically significant, but barely.

## 2. 95% Confidence Interval

For the difference in conversion rates (B - A):

- Difference = 0.006 (0.6 percentage points)
- SE_diff = √[(0.032 × 0.968/10,000) + (0.038 × 0.962/10,000)] = 0.00259
- 95% CI = 0.006 ± 1.96 × 0.00259

**95% CI: [0.09%, 1.11%]** or **[0.0009, 0.0111]**

The confidence interval barely excludes zero, confirming marginal significance.

## 3. Concerns About 2-Day Duration

🚩 **Major red flags:**

- **Day-of-week bias**: 2 days can't capture weekly patterns (weekend vs. weekday behavior)
- **Novelty/newness effects**: Changes haven't stabilized
- **Insufficient sample for segmentation**: Can't analyze by user type, device, etc.
- **External validity**: Marketing campaigns, news events, or other temporal factors
- **Primacy/recency effects**: Users may need time to adapt
- **Small effect size with marginal significance**: Need more data to be confident

**Best practice**: Run for at least 1-2 full weeks to capture complete behavioral cycles.

## 4. Impact of iOS Bug

This **completely invalidates the test**. Here's why:

**The selection bias problem:**
- 2,000 iOS users were blocked from checkout in Treatment B
- These users were likely *pre-filtered* before conversion measurement
- The 10,000 "visitors" in Treatment B may actually represent a biased sample

**What probably happened:**
- Treatment B: 12,000 actual visitors → 2,000 blocked → 10,000 measured → 380 conversions
- If those 2,000 iOS users had normal ~3% conversion: ~60 additional conversions lost
- True conversion rate might be: 380/12,000 = **3.17%** (worse than control!)

**Even if t...
```

### Claude Opus 4.5

**Generation Time:** 23002ms
**Tokens:** 1316

```
# A/B Test Analysis: Checkout Flow

## 1. Statistical Significance Calculation

**Using a two-proportion z-test:**

```
p_A = 0.032 (320/10,000)
p_B = 0.038 (380/10,000)
p_pooled = 700/20,000 = 0.035

SE = √[p_pooled × (1-p_pooled) × (1/n_A + 1/n_B)]
SE = √[0.035 × 0.965 × (2/10,000)]
SE = √[0.00000676] = 0.0026

z = (0.038 - 0.032) / 0.0026 = 2.31
```

**p-value = 0.021 (two-tailed)**

This *is* statistically significant at α = 0.05, but just barely.

---

## 2. 95% Confidence Interval for True Difference

```
Difference = 0.6 percentage points
SE_diff = √[(p_A(1-p_A)/n_A) + (p_B(1-p_B)/n_B)]
SE_diff = √[0.0000031 + 0.0000037] = 0.0026

95% CI = 0.006 ± (1.96 × 0.0026)
       = 0.006 ± 0.0051
```

**95% CI: [+0.09pp to +1.11pp]** or in relative terms: **[+2.8% to +34.7%]**

The wide interval means the true lift could be anywhere from trivial to substantial.

---

## 3. Concerns About 2-Day Test Duration

| Concern | Why It Matters |
|---------|----------------|
| **Day-of-week effects** | Weekend vs. weekday behavior differs dramatically |
| **No full business cycle** | Missing paydays, typical shopping patterns |
| **Novelty effects** | Users may react differently to new UI initially |
| **Bot/crawler noise** | Short windows amplify non-human traffic impact |
| **Multiple testing risk** | Was this checked repeatedly before "significance"? |
| **Segment blindness** | Can't detect if effect varies by user cohort |

**Rule of thumb:** Run tests for minimum 1-2 full weeks to capture behavioral cycles.

---

## 4. The iOS Bug Changes Everything

This is critical. Let me recalculate:

```
BEFORE (what we measured):
Treatment B: 380/10,000 = 3.8%

AFTER (correcting for blocked users):
Actual B visitors who could convert: 10,000 - 2,000 = 8,000
Corrected B rate: 380/8,000 = 4.75%
```

**But wait—this makes it more complicated, not simpler:**

| Scenario | Implication |
|----------|-------------|
| If blocked users would have converted at 3.8% | ~76 lost conversions; true ...
```

### GPT-OSS-120B (Legal)

**Generation Time:** 15697ms
**Tokens:** 2271

```
.## 1.  Statistical significance (p‑value)

We have two independent binomial samples:

|                | Visitors (n) | Conversions (x) | Conversion rate (p̂) |
|----------------|--------------|-----------------|-----------------------|
| **Control (A)**| 10 000       | 320             | 0.0320  (3.2 %)       |
| **Treatment (B)**| 10 000     | 380             | 0.0380  (3.8 %)       |

The null hypothesis is **H₀: p_A = p_B** (no difference in true conversion rates).  
A two‑sided two‑proportion Z‑test gives:

*Pooled proportion*  

\[
\hat p = \frac{x_A+x_B}{n_A+n_B}= \frac{320+380}{20 000}=0.035
\]

*Standard error*  

\[
SE = \sqrt{\hat p(1-\hat p)\Big(\frac1{n_A}+\frac1{n_B}\Big)}
     =\sqrt{0.035\cdot0.965\;(0.0001+0.0001)}
     \approx 0.00260
\]

*Z‑statistic*  

\[
Z = \frac{\hat p_B-\hat p_A}{SE}= \frac{0.038-0.032}{0.00260}\approx 2.31
\]

*Two‑sided p‑value*  

\[
p = 2\bigl(1-\Phi(2.31)\bigr) \approx 2(1-0.9896)=0.021
\]

**Result:** p ≈ 0.02 → the lift is statistically significant at the 5 % level (but not at the 1 % level).

---

## 2.  95 % confidence interval for the *true* difference in conversion rates  

We use the standard error that does **not** pool the proportions:

\[
SE_{\Delta}= \sqrt{\frac{\hat p_A(1-\hat p_A)}{n_A}+
                \frac{\hat p_B(1-\hat p_B)}{n_B}}
            =\sqrt{0.032\cdot0.968/10 000+0.038\cdot0.962/10 000}
            \approx 0.00260
\]

Difference in observed rates  

\[
\Delta\hat p = \hat p_B-\hat p_A = 0.038-0.032 = 0.0060\;(0.60\%)
\]

95 % CI (Wald)  

\[
\Delta\hat p \pm 1.96\,SE_{\Delta}
 = 0.0060 \pm 1.96(0.00260)
 = 0.0060 \pm 0.0051
 = [0.0009,\;0.0111]
\]

**Interpretation**

* The absolute lift is between **0.09 % and 1.11 %** points.  
* In relative terms (divide by the control rate 3.2 %), the lift is between **≈ 2.8 % and 34.7 %**.

Because the interval does **not** contain zero, the result is statistically significant at the 5 % level.

---

## 3.  Concerns about the *2‑day* test duration  

| I...
```

### Gemini 3 Pro Preview

**Generation Time:** 19485ms
**Tokens:** 2229

```
Here is the analysis of the A/B test results.

### 1. Statistical Significance
To determine significance, we perform a **two-tailed Z-test for the difference of proportions**.

*   **Control (A):** $p_A = 320 / 10,000 = 0.032$
*   **Treatment (B):** $p_B = 380 / 10,000 = 0.038$
*   **Pooled Proportion ($\hat{p}$):** $(320 + 380) / (20,000) = 0.035$
*   **Standard Error ($SE$):** $\sqrt{0.035(1 - 
```

### Grok 4.1 Fast

**Generation Time:** 24748ms
**Tokens:** 2812

```
1. **Statistical significance (p-value)**:  
   Using a two-proportion z-test (pooled variance):  
   - Sample proportions: \( \hat{p}_A = 0.032 \), \( \hat{p}_B = 0.038 \)  
   - Pooled proportion: \( \hat{p} = 0.035 \)  
   - Standard error: \( SE = \sqrt{0.035 \times 0.965 \times (1/10000 + 1/10000)} \approx 0.00260 \)  
   - z-score: \( z = (0.038 - 0.032) / 0.00260 \approx 2.31 \)  
   - Two-tailed p-value: **0.021** (significant at α=0.05, but borderline; one-tailed would be ~0.010).  
   *Note: Exact chi-squared test yields p=0.0207, confirming ~0.021.*

2. **95% confidence interval for the true difference**:  
   Difference: \( \delta = 0.038 - 0.032 = 0.006 \) (0.6 percentage points).  
   Unpooled SE ≈ 0.00260 (nearly identical to pooled).  
   95% CI: \( 0.006 \pm 1.96 \times 0.00260 \) → **(0.0009, 0.0111)** or **0.09% to 1.11%**.  
   (Includes 0, so not definitively positive.)

3. **Concerns from 2-day test duration**:  
   - **Seasonality/day-of-week bias**: Traffic patterns, conversion rates, and user behavior vary (e.g., weekdays vs. weekends, promotions). 2 days likely doesn't capture a full cycle.  
   - **Insufficient exposure**: Small sample for segments (device, geo, etc.); random fluctuations amplified.  
   - **No ramp-up/stability**: Early adopter effects or external events (e.g., news, competitors) unaccounted for.  
   - **Low power for subgroups**: Overall sample is decent (20k), but short time risks non-random assignment over time. Recommend 1-2 weeks minimum.

4. **Impact of iOS bug blocking 2,000 users**:  
   - **Biases Treatment B downward**: The 10k visitors include 2k blocked users (0 conversions from them). The 380 conversions came from ~8k effective users → inflated rate of 380/8k = 4.75% *among reachers*, but overall 3.8%.  
   - Without bug, those 2k would likely convert at ~3-4% (similar to control or unaffected B users), adding ~60-80 conversions → *true* B rate ~4.4-4.6% (25-40% relative lift).  
   - **Invalidates test**: B...
```

---

*Generated by The Multivac V5*
*https://multivac.com*