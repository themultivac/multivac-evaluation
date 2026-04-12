# Multivac Evaluation Report

**Evaluation ID:** EVAL-20260402-193016
**Timestamp:** 2026-04-02T19:30:16.588404
**Category:** Analysis & Research
**Model Pool:** 10 analysis-optimized models

## Question

A bank uses an ML model for loan approvals. Accuracy: 92%. But analysis shows: approval rate for Group A: 78%, Group B: 45%. The bank says 'the model doesn't use race as a feature.' (1) Explain how the model can be discriminatory without using race directly. (2) What proxy variables might cause this? (3) Is equalizing approval rates the right fix? What are the tradeoffs? (4) Design an audit procedure.

---

## Rankings

| Rank | Model | Score | Min | Max | Std Dev |
|------|-------|-------|-----|-----|---------|
| 1 | Grok 4.20 | 9.47 | 8.65 | 10.00 | 0.51 |
| 2 | GPT-5.4 | 9.34 | 8.80 | 9.80 | 0.42 |
| 3 | MiMo-V2-Flash | 9.22 | 8.80 | 10.00 | 0.42 |
| 4 | MiniMax M2.5 | 9.16 | 8.65 | 9.80 | 0.41 |
| 5 | DeepSeek V3 | 9.03 | 8.60 | 9.80 | 0.46 |
| 6 | Gemini 3 Flash Preview | 8.94 | 8.45 | 9.80 | 0.41 |
| 7 | GPT-OSS-120B | 8.48 | 6.65 | 9.45 | 0.90 |
| 8 | Gemini 3.1 Pro | 8.31 | 7.25 | 9.45 | 0.70 |
| 9 | Claude Sonnet 4.6 | 8.15 | 6.50 | 9.80 | 0.95 |
| 10 | Claude Opus 4.6 | 8.04 | 6.75 | 9.45 | 1.09 |

---

## Meta Analysis

### Judge Strictness

| Rank | Judge | Avg Score Given |
|------|-------|-----------------|
| 1 | GPT-5.4 | 7.99 |
| 2 | GPT-OSS-120B | 8.19 |
| 3 | MiniMax M2.5 | 8.48 |
| 4 | Grok 4.20 | 8.68 |
| 5 | Claude Opus 4.6 | 8.93 |
| 6 | Gemini 3.1 Pro | 8.96 |
| 7 | MiMo-V2-Flash | 8.97 |
| 8 | Claude Sonnet 4.6 | 9.03 |
| 9 | DeepSeek V3 | 9.25 |
| 10 | Gemini 3 Flash Preview | 9.68 |

**Strictest Judge:** gpt_5_4
**Most Lenient Judge:** gemini_3_flash
**Total Judgments:** 100
**Valid Judgments:** 90

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

**Generation Time:** 20136ms
**Tokens:** 2146

```
Here is a comprehensive breakdown of the situation, the underlying mechanisms of the bias, and a framework for addressing it.

### 1. How the Model Can Be Discriminatory Without Using Race Directly
The bank is relying on a flawed concept known as **"fairness through unawareness"**—the belief that if a model doesn't explicitly see a protected attribute (like race), it cannot discriminate based on it. 

In reality, machine learning models are exceptional at finding hidden patterns. If the training data contains historical biases (e.g., past loan officers discriminating against Group B), the model will learn to replicate those outcomes. Because the model doesn't have "race" to rely on, it triangulates race by combining other seemingly neutral variables that are highly correlated with race. This is known as **proxy discrimination**. The model reconstructs the missing demographic variable using the data it *does* have, thereby maintaining the discriminatory status quo while appearing mathematically objective.

### 2. Proxy Variables That Might Cause This
In lending, several neutral-sounding variables often serve as strong proxies for race or socioeconomic status due to historical and systemic inequalities:
*   **ZIP Code / Neighborhood:** Because of historical practices like redlining, neighborhoods are often highly segregated. A model can easily use geographic data to indirectly identify race.
*   **Education:** The specific high school attended, or whether an applicant attended a community college versus a private university, can correlate strongly with racial demographics.
*   **Employment Type / Industry:** Certain demographics may be overrepresented in specific industries (e.g., service sector vs. tech) or have different average tenures due to systemic employment barriers.
*   **Length of Credit History:** Systemically marginalized groups are more likely to be "unbanked" or underbanked, leading to shorter credit histories.
*   **Alternative Financial Data:** Use of ...
```

### Claude Opus 4.6

**Generation Time:** 44697ms
**Tokens:** 2159

```
# Algorithmic Discrimination in Lending: A Comprehensive Analysis

## 1. How the Model Can Be Discriminatory Without Using Race Directly

### The Fundamental Misconception

The bank's defense—"we don't use race as a feature"—reflects a common but deeply flawed understanding of how discrimination operates in machine learning. This is known as the **"fairness through unawareness" fallacy**.

### Mechanisms of Indirect Discrimination

```
THE DISCRIMINATION PIPELINE (Even Without Protected Attributes)
═══════════════════════════════════════════════════════════════

Real World                    Training Data                 Model Behavior
┌─────────────────┐      ┌──────────────────┐      ┌──────────────────────┐
│ Historical       │      │ Labels encode    │      │ Model learns to      │
│ redlining denied │─────▶│ past biased      │─────▶│ replicate historical │
│ mortgages to     │      │ decisions as     │      │ discrimination as    │
│ Black borrowers  │      │ "ground truth"   │      │ "accurate prediction"│
└─────────────────┘      └──────────────────┘      └──────────────────────┘
         │                        │                          │
         ▼                        ▼                          ▼
┌─────────────────┐      ┌──────────────────┐      ┌──────────────────────┐
│ Less wealth      │      │ Lower credit     │      │ Systematically lower │
│ accumulation,    │      │ scores, fewer    │      │ approval rates for   │
│ fewer banking    │      │ assets appear as │      │ Group B despite      │
│ relationships    │      │ "higher risk"    │      │ comparable ability   │
└─────────────────┘      └──────────────────┘      └──────────────────────┘
```

### Three Distinct Causal Pathways

```python
"""
Pathway 1: HISTORICAL BIAS IN LABELS
The training data itself encodes past discrimination.
"""

# If historical loan officers were biased:
historical_data = {
    "applicant_1": {"qualified": True, "group": "B", "approved": False},  # Wrongly denied
    "...
```

### GPT-5.4

**Generation Time:** 45281ms
**Tokens:** 2152

```
Here’s a structured answer.

## 1) How can the model be discriminatory without using race directly?

Yes, it absolutely can.

A model can discriminate **without explicitly using race** because:

- **Proxy variables** can encode race indirectly.
- **Historical data** may reflect past discrimination.
- **Feature-label relationships** may differ across groups.
- **Optimization for overall accuracy** can still produce unequal outcomes.

### Why “we don’t use race” is not enough
If race is correlated with other variables in the data, the model can reconstruct it indirectly. So even if race is removed, the model may behave similarly to a race-aware model.

Example:
- ZIP code
- income
- employment history
- education
- home ownership
- banking history

These may correlate strongly with race because of historical segregation, unequal access to wealth, education, and credit.

### Historical bias problem
If the training labels reflect past human decisions, then the model may learn those biases.

For example:
- If past loan approvals were biased against Group B,
- then “approved in the past” or variables shaped by past approvals may encode discrimination,
- and the model will treat those biased outcomes as ground truth.

### Accuracy can hide unfairness
A 92% accuracy sounds good overall, but:
- It says nothing about **who benefits** or **who is harmed**.
- The model may perform very well on the majority group and poorly on the minority group.
- It may have different false positive or false negative rates across groups.

So a model can be “accurate” and still unfair.

---

## 2) What proxy variables might cause this?

Common proxy variables in lending include:

### Direct or near-direct proxies
- **ZIP code / neighborhood**
- **Census tract**
- **Address stability**
- **Property value**
- **School district**

These can strongly reflect residential segregation.

### Socioeconomic proxies
- **Income**
- **Wealth / savings balance**
- **Debt-to-income ratio**
- **Employment stat...
```

### DeepSeek V3

**Generation Time:** 40801ms
**Tokens:** 853

```
### (1) How can the model be discriminatory without using race directly?  
Even if the model doesn’t explicitly use race as a feature, it can still discriminate if it relies on **proxy variables**—features that correlate strongly with race due to historical or societal biases. For example:  
- **Zip codes** may reflect segregated housing patterns.  
- **Income/wealth metrics** may reflect systemic disparities (e.g., redlining).  
- **Education levels** or **occupation types** may be unevenly distributed across racial groups.  

The model could inadvertently learn these patterns, leading to disparate outcomes for Group A (78% approval) vs. Group B (45%), even if race isn’t a direct input.

---

### (2) What proxy variables might cause this?  
Potential proxies include:  
- **Geographic data**: Neighborhood, zip code, or proximity to certain amenities.  
- **Socioeconomic indicators**: Income, debt-to-income ratio, credit history length (affected by generational wealth gaps).  
- **Behavioral data**: Spending patterns, types of purchases (e.g., correlated with cultural practices).  
- **Names or language**: Surnames or dialects might indirectly signal race to the model.  

These proxies can encode racial disparities present in historical data, perpetuating bias.

---

### (3) Is equalizing approval rates the right fix? Tradeoffs?  
**Pros of equalizing rates**:  
- Addresses fairness by ensuring equal opportunity.  
- Mitigates legal/reputational risks from discriminatory outcomes.  

**Cons/Tradeoffs**:  
- **Accuracy vs. fairness**: Forcing equal rates might reduce overall accuracy if true risk factors differ between groups.  
- **Moral hazard**: Approving higher-risk applicants from Group B to meet quotas could increase default rates.  
- **Masking root causes**: Doesn’t address systemic biases in data (e.g., credit history disparities).  

**Better approaches**:  
- **Fairness constraints**: Use techniques like demographic parity *weighted* by risk (e.g., equalizi...
```

### MiMo-V2-Flash

**Generation Time:** 18721ms
**Tokens:** 1846

```
Here is a comprehensive analysis of the scenario, broken down into the four requested parts.

---

### (1) How the model can be discriminatory without using race directly

Even if the explicit feature "race" is removed from the dataset, the model can still be discriminatory through **proxy discrimination** and **historical bias**.

*   **Proxy Variables:** Machine learning models find correlations in data. If a variable (like zip code) is highly correlated with race due to societal segregation, the model will use that variable as a stand-in (proxy) for race. The model learns that "Zip Code X" predicts a certain outcome, effectively discriminating against the group residing there without ever seeing the race label.
*   **Historical Bias in Training Data:** If the training data reflects historical lending practices that were biased (e.g., redlining), the model will learn those patterns as "ground truth." For example, if Group A was historically approved at higher rates due to systemic advantages, the model will learn that the features associated with Group A represent "creditworthiness."
*   **Intersectionality:** The model might combine multiple seemingly neutral features to create a unique fingerprint for a demographic group. For example, combining "occupation," "education level," and "neighborhood" can predict race with high accuracy.
*   **The Accuracy Paradox:** An overall accuracy of 92% can hide disparities. If Group A constitutes 80% of the training data, a model can achieve high accuracy by simply predicting "approve" for Group A and being conservative with Group B, even if Group B is actually creditworthy. This is known as the **accuracy paradox**—high aggregate accuracy can mask poor performance on minority subgroups.

### (2) Proxy variables that might cause this disparity

Proxy variables are features that are not race themselves but are correlated with race due to systemic social and economic factors.

1.  **Geographic Location (Zip Code / Neighborhood):...
```

### Claude Sonnet 4.6

**Generation Time:** 39493ms
**Tokens:** 2160

```
# Fairness in ML: Loan Approval Discrimination Analysis

## (1) How Discrimination Occurs Without Using Race Directly

### The Core Problem: Disparate Impact

```
The model doesn't need to "know" about race to discriminate by race.
This is legally recognized as disparate impact discrimination.

CAUSAL CHAIN:

Historical Society
      │
      ▼
Structural Inequalities ──────────────────────────────────┐
(redlining, wage gaps,                                     │
 wealth concentration)                                     │
      │                                                     │
      ▼                                                     ▼
Observable Features          Training Data
(zip code, income,     ──►  (historical decisions,    ──► MODEL
 credit score, assets)       themselves biased)
      │                             │
      │                             │
      └─────────────────────────────┘
                    │
                    ▼
         Proxy Discrimination
         (race reconstructible
          from features)
```

### Three Distinct Mechanisms

**Mechanism 1: Feature-Encoded Correlation**
```python
# Race is statistically recoverable from "neutral" features
# This is empirically demonstrated:

correlation_with_race = {
    'zip_code':           0.71,  # residential segregation legacy
    'income':             0.58,  # wage gap history
    'credit_score':       0.52,  # banking access disparities
    'employment_type':    0.45,  # occupational segregation
    'college_degree':     0.41,  # educational access gaps
}

# The model effectively reconstructs race as a latent variable
# even when explicitly excluded
```

**Mechanism 2: Biased Training Data**
```
Historical loan officers (human) → Biased decisions
         │
         ▼
Training labels are ALREADY discriminatory
         │
         ▼
Model learns: "people who look like Group B are bad risks"
         │
         ▼
Model replicates historical discrimination at scale
         │
        ...
```

### Grok 4.20

**Generation Time:** 11623ms
**Tokens:** 1726

```
**1. How the model can be discriminatory without using race directly**

This is the classic problem of **proxy discrimination** or **redundant encoding**. Even if the model is not given an explicit "race" feature, it can still learn to replicate historical racial disparities if race is statistically correlated with other variables the model *is* allowed to use.

The training data almost certainly reflects decades of systemic patterns: on average, certain racial groups have had lower incomes, lower homeownership rates, different neighborhoods, different educational attainment, different credit histories, different occupations, etc., due to past discrimination, redlining, unequal access to capital, and other factors. A high-accuracy model that optimizes for "who repaid loans in the past" will therefore learn to treat applicants differently along these correlated dimensions. The model is accurately capturing historical outcomes, but those outcomes were themselves racially biased. This produces **disparate impact** even though the model never saw the protected attribute.

In ML terms: race is not *causally* used, but it is *statistically* recoverable from the other features. This is sometimes called "fairness through unawareness" — the naive belief that simply removing the variable makes the system fair. Modern fairness literature (e.g., Barocas, Hardt, Narayanan) shows this approach usually fails.

**2. Common proxy variables that could cause the observed gap (78% vs 45%)**

Likely proxies include (especially when used in combination):

- **Zip code / census tract / neighborhood** — one of the strongest proxies for race in the U.S. due to historical residential segregation.
- **Credit score or credit history length** — if past discrimination affected credit-building opportunities.
- **Income, debt-to-income ratio, savings, or wealth proxies** (e.g., down payment size, home equity).
- **Education level, college attended, or educational debt**.
- **Occupation, industry, ...
```

### GPT-OSS-120B

**Generation Time:** 28877ms
**Tokens:** 2215

```
Below is a structured response that walks through each of the four questions you asked.  I’ve kept the language concrete (e.g., “ZIP‑code”, “credit‑score”) so you can map the concepts directly onto a typical loan‑approval pipeline, but I also flag the broader methodological and legal considerations that often arise in a real‑world audit.

---

## 1️⃣ How a model can be discriminatory *without* using race as an explicit input  

| Concept | Why it matters | Typical manifestation in a loan model |
|--------|----------------|--------------------------------------|
| **Historical bias** | Training data reflect past lending decisions that were themselves racially biased (e.g., red‑lining, differential underwriting standards). | The model learns that applicants from certain neighborhoods or with certain credit‑history patterns are “risky,” even if race never appears. |
| **Statistical correlation (proxy variables)** | Some non‑protected attributes are highly correlated with race. | If “ZIP‑code” or “home‑ownership status” is strongly linked to the demographic composition of a region, the model will indirectly treat race as a factor. |
| **Sample‑selection bias** | The training set may over‑represent one group (e.g., approved loans) and under‑represent the other, causing the learned decision boundary to be skewed. | If most historical approvals came from Group A, the model will be better calibrated for that group and systematically under‑score Group B. |
| **Label bias** | The target variable (e.g., “defaulted”) can be biased because default rates are themselves a product of structural inequities (e.g., lower wealth buffers, higher cost‑of‑credit for minorities). | The model may learn that “higher default risk” is associated with features that are more common for Group B, even though the underlying cause is not creditworthiness but exposure to adverse economic conditions. |
| **Algorithmic bias from regularisation / class imbalance** | When the loss function is optimized f...
```

### Gemini 3 Flash Preview

**Generation Time:** 12597ms
**Tokens:** 1016

```
This scenario illustrates a classic challenge in algorithmic fairness: **disparate impact** occurring in the absence of **disparate treatment.**

### 1. How the model is discriminatory without using race
Even if a "protected attribute" like race is removed from the dataset, a model can still learn to discriminate through **redundant encoding**.

Machine learning models are designed to find patterns that minimize error. If historical data contains systemic biases (e.g., Group B was historically denied loans due to redlining or lower generational wealth), the model will identify other features that correlate strongly with being in Group B. The model essentially "reconstructs" the missing race variable using the remaining data, leading to biased outcomes that mirror historical prejudices.

### 2. Proxy Variables
Proxy variables are features that are highly correlated with a protected attribute. Common examples include:
*   **Zip Code:** Due to residential segregation, geography is often a near-perfect proxy for race.
*   **Educational Background:** Attendance at specific institutions (e.g., HBCUs) or highest degree attained can correlate with race and socioeconomic status.
*   **Employment Industry:** Certain sectors may have over- or under-representation of specific demographic groups.
*   **Digital Footprint/Usage:** Types of devices used or social media behavior can correlate with demographic segments.
*   **Length of Credit History:** Because credit access has historically been unequal, younger or immigrant populations (who may fall into specific racial groups) may have shorter histories despite being creditworthy.

### 3. Equalizing Approval Rates: Fixes and Trade-offs
Equalizing approval rates (a metric known as **Demographic Parity**) is one way to address the gap, but it is controversial.

*   **The Argument "For":** It ensures "Equality of Outcome," correcting for historical systemic exclusion and preventing the model from perpetuating a cycle of poverty in Gr...
```

### MiniMax M2.5

**Generation Time:** 21732ms
**Tokens:** 1738

```
Excellent set of questions that get to the heart of modern algorithmic fairness. Let's break this down.

### (1) How the Model Can Be Discriminatory Without Using Race Directly

This is the classic problem of **indirect discrimination** or **disparate impact**. The model can be discriminatory even without a race feature due to:

1.  **Historical Bias:** The training data reflects past human decisions and societal inequities. If Group A historically had better access to credit, higher wealth, or more stable employment (due to systemic discrimination), the model learns to associate these outcomes with "creditworthiness" and perpetuates the status quo.
2.  **Feature Correlation:** Race can be **correlated** with other features in the model. If certain zip codes, names, or financial patterns are highly correlated with race (a phenomenon known as **redlining** in reverse), the model uses these correlated signals to make decisions, effectively proxying for race.
3.  **Learned Biases:** The model optimizes for the outcome (loan repayment) as defined by historical data. If that historical data encoded biases against Group B (e.g., through biased underwriting or less favorable offers), the model learns and amplifies these patterns.

**In short:** The model doesn't know it's discriminating; it's simply finding statistical patterns in biased data and using correlated proxies.

### (2) Proxy Variables That Might Cause This

These are features that are correlated with race due to historical and social factors:

*   **Geographic Data:** Zip code, neighborhood, city. Highly correlated with race due to residential segregation.
*   **Name:** Certain names may be strongly associated with specific racial or ethnic groups.
*   **Financial History:** Features like **credit utilization, account balance volatility, or having a "thin" credit file** can correlate with race due to disparities in wealth and banking access.
*   **Employment Type/Industry:** Certain occupations or industries ma...
```

---

*Generated by The Multivac V5*
*https://themultivac.com*