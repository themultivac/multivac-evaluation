# Multivac Evaluation Report

**Evaluation ID:** EVAL-20260402-153453
**Timestamp:** 2026-04-02T15:34:53.682125
**Category:** Reasoning & Logic
**Model Pool:** 10 reasoning-optimized models

## Question

Estimate how many piano tuners there are in Chicago. Show your reasoning step by step, including:
1. All assumptions you make
2. How you derived each number
3. Sensitivity analysis (what if your assumptions are wrong?)
4. Final estimate with confidence interval

---

## Rankings

| Rank | Model | Score | Min | Max | Std Dev |
|------|-------|-------|-----|-----|---------|
| 1 | GPT-5.4 | 9.07 | 8.40 | 9.80 | 0.45 |
| 2 | GPT-OSS-120B | 9.05 | 8.15 | 10.00 | 0.54 |
| 3 | Claude Opus 4.6 | 8.90 | 8.15 | 10.00 | 0.58 |
| 4 | Grok 4.20 | 8.74 | 8.35 | 9.40 | 0.34 |
| 5 | MiMo-V2-Flash | 8.74 | 7.90 | 10.00 | 0.62 |
| 6 | Claude Sonnet 4.6 | 8.70 | 8.25 | 9.40 | 0.37 |
| 7 | Gemini 2.5 Flash | 8.63 | 8.25 | 9.00 | 0.26 |
| 8 | DeepSeek V3 | 8.42 | 7.75 | 9.20 | 0.52 |
| 9 | Gemini 3.1 Pro | 2.67 | 0.65 | 6.00 | 1.71 |

---

## Meta Analysis

### Judge Strictness

| Rank | Judge | Avg Score Given |
|------|-------|-----------------|
| 1 | GPT-5.4 | 7.26 |
| 2 | GPT-OSS-120B | 7.69 |
| 3 | MiniMax M2.5 | 7.84 |
| 4 | Claude Opus 4.6 | 7.86 |
| 5 | Claude Sonnet 4.6 | 7.91 |
| 6 | Grok 4.20 | 8.11 |
| 7 | MiMo-V2-Flash | 8.40 |
| 8 | DeepSeek V3 | 8.44 |
| 9 | Gemini 2.5 Flash | 9.16 |
| 10 | Gemini 3.1 Pro | 9.20 |

**Strictest Judge:** gpt_5_4
**Most Lenient Judge:** gemini_31_pro
**Total Judgments:** 100
**Valid Judgments:** 80

---

## Model Pool

Models selected for **Reasoning & Logic** evaluation:

1. **Gemini 3.1 Pro** (openrouter)
2. **DeepSeek V3** (openrouter)
3. **Claude Opus 4.6** (openrouter)
4. **GPT-5.4** (openrouter)
5. **Grok 4.20** (openrouter)
6. **Claude Sonnet 4.6** (openrouter)
7. **MiMo-V2-Flash** (openrouter)
8. **GPT-OSS-120B** (openrouter)
9. **Gemini 2.5 Flash** (openrouter)
10. **MiniMax M2.5** (openrouter)

---

## Model Responses

### Gemini 3.1 Pro

**Generation Time:** 27424ms
**Tokens:** 2101

```
This is a classic "Fermi problem," which requires breaking down a complex estimation into logical, manageable steps. To estimate the number of piano tuners in Chicago, we need to balance the **demand** for piano tuning (how many pianos exist and how often they are tuned) against the **supply** (how many pianos one tuner can tune in a year).

Here is the step-by
```

### DeepSeek V3

**Generation Time:** 17321ms
**Tokens:** 750

```
### Estimating the Number of Piano Tuners in Chicago

#### Step 1: Determine the Population of Chicago
Assumption: The population of Chicago is approximately **2.7 million people**.  
Source: This is based on recent census data (~2023).

#### Step 2: Estimate Household Size
Assumption: The average household size is **2 people**.  
Derivation: Common urban household size in the U.S. ranges from 1.5 to 2.5; I chose 2 for simplicity.  
Sensitivity: If it's actually 1.5, households increase; if 2.5, households decrease.

Number of households = Population / Household size = 2,700,000 / 2 = **1,350,000 households**.

#### Step 3: Estimate Piano Ownership
Assumption: **1 in 100 households owns a piano**.  
Derivation: Pianos are expensive and niche; ownership likely ranges from 0.5% to 2%.  
Sensitivity: If 0.5%, pianos = 6,750; if 2%, pianos = 27,000.

Number of pianos = 1,350,000 × 1% = **13,500 pianos**.

#### Step 4: Estimate Tunings per Piano per Year
Assumption: Each piano is tuned **once per year** on average.  
Derivation: Professionals recommend 1-2 tunings/year; some may skip years.  
Sensitivity: If 0.5 tunings/year, demand halves; if 2, demand doubles.

Annual tunings = 13,500 pianos × 1 = **13,500 tunings/year**.

#### Step 5: Estimate Tunings per Tuner per Year
Assumption: A tuner can perform **4 tunings/day** and works **250 days/year** (5 days/week, 50 weeks).  
Derivation: Tunings take ~2 hours (including travel), allowing 4/day. Full-time work ≈ 250 days.  
Sensitivity: If 3 tunings/day/day, tuners increase; if 5, tuners decrease.

Annual tunings per tuner = 4 × 250 = **1,000 tunings/year**.

#### Step 6: Calculate Number of Piano Tuners
Number of tuners = Total tunings / Tunings per tuner = 13,500 / 1,000 = **13.5 tuners**.  
Round to **~14 piano tuners**.

#### Confidence Interval: Given assumptions, plausible range is **5 to 30 tuners** (accounting for ownership, tuning frequency, and tuner efficiency).

---

### Final Estimate:  
There are approximate...
```

### Claude Opus 4.6

**Generation Time:** 264706ms
**Tokens:** 1668

```
# Fermi Estimation: Piano Tuners in Chicago

## Step 1: Estimate the Number of Pianos in Chicago

### Population Base
- Chicago metro area population: ~2.7 million (city proper); I'll use the city proper since "in Chicago" is specified, but piano tuners likely serve the metro area (~9.5 million). I'll work with **~9.5 million metro** since tuners don't stop at city limits, then narrow down to tuners *based* in Chicago at the end.

### Household Piano Ownership
- **Assumption:** ~10% of households have a piano
  - Rationale: The US has an estimated 10–18 million pianos. With ~130 million households, that's roughly 8–14%. I'll use 10% as a moderate estimate.
- **Average household size in Chicago metro:** ~2.6 people
- **Number of households:** 9,500,000 ÷ 2.6 ≈ **3,650,000 households**
- **Household pianos:** 3,650,000 × 0.10 = **365,000 pianos**

### Institutional Pianos
- Schools, churches, universities, concert halls, recording studios, bars/restaurants
- **Assumption:** Institutions add roughly 15% more pianos on top of household pianos
- Institutional pianos: 365,000 × 0.15 ≈ **55,000 pianos**

### Total Pianos
- **~420,000 pianos** in the Chicago metro area

---

## Step 2: How Often Are Pianos Tuned?

- **Assumption:** The *average* piano is tuned **1.2 times per year**
  - Many pianos sit neglected and are tuned 0 times per year (maybe 30–40% of them)
  - Active household pianos: tuned 1–2 times/year
  - Professional/institutional pianos: tuned 2–4 times/year
  - Weighted average: ~1.2 seems reasonable

### Total Tunings Per Year
- 420,000 × 1.2 = **504,000 tunings per year**

---

## Step 3: How Many Tunings Can One Tuner Do Per Year?

### Per-Day Capacity
- **Travel time between appointments:** ~30 minutes average
- **Tuning time:** ~1.5–2 hours per piano (call it 1.75 hours)
- **Total per appointment:** ~2.25 hours
- **Working hours per day:** ~8 hours
- **Tunings per day:** 8 ÷ 2.25 ≈ **3.5 tunings/day** → I'll round to **4 tunings/day** (experienced tuner...
```

### GPT-5.4

**Generation Time:** 19530ms
**Tokens:** 1541

```
Here’s a clean **Fermi estimate** for the number of **piano tuners in Chicago**, with assumptions, derivations, sensitivity analysis, and a confidence interval.

---

# 1) Assumptions

I’ll estimate demand for piano tuning, then convert that into the number of full-time piano tuners needed.

## A. Population and households
- **City of Chicago population**: about **2.7 million**
- **Average household size**: about **2.5 people**
- So number of households:
  \[
  2.7\text{ million} / 2.5 \approx 1.08\text{ million households}
  \]

I’ll round to **1.1 million households**.

## B. Fraction of households with a piano
This is the hardest assumption. Pianos are not common, but they’re not rare either.

I’ll assume:
- **2%–5% of households have a piano**
- Central estimate: **3%**

So household pianos:
\[
1.1\text{ million} \times 3\% = 33{,}000
\]

## C. Institutional pianos
In addition to homes, there are pianos in:
- schools
- churches
- music venues
- colleges
- hotels
- rehearsal spaces

Rather than estimating each category in full detail, I’ll add an institutional stock equal to about **20% of household pianos**.

So:
\[
33{,}000 \times 20\% = 6{,}600
\]

Total pianos:
\[
33{,}000 + 6{,}600 = 39{,}600
\]

Round to **40,000 pianos**.

## D. Tunings per piano per year
Not every piano is tuned yearly. Some active pianos are tuned 1–2 times per year; neglected ones may go years without tuning.

Assume average:
- **0.8 tunings per piano per year**  
This averages over frequently used and rarely used pianos.

Annual tuning demand:
\[
40{,}000 \times 0.8 = 32{,}000 \text{ tunings/year}
\]

## E. Productivity of one piano tuner
A tuner typically:
- travels between jobs
- spends around 1.5–2.5 hours per tuning including setup and travel
- works about 5 days/week
- does not spend 100% of time tuning (admin, scheduling, downtime)

Assume:
- **3 tunings/day**
- **5 days/week**
- **48 working weeks/year**

So tunings per tuner per year:
\[
3 \times 5 \times 48 = 720
\]

---

# 2)...
```

### Grok 4.20

**Generation Time:** 5444ms
**Tokens:** 1045

```
**Fermi Estimation: Number of Piano Tuners in Chicago**

### Step-by-Step Reasoning

**1. Estimate the population of Chicago**  
Assumption: Chicago has approximately **2.7 million** people (city proper).  
(This is a standard figure; the metro area is ~9.5M, but "in Chicago" usually refers to the city itself.)

**2. Estimate the number of households**  
Assumption: Average household size = **2.5 people per household**.  
Households = 2,700,000 ÷ 2.5 = **1.08 million households**.

**3. Estimate fraction of households that own a piano**  
Assumption: Roughly **1 in 50 households** owns a piano that gets tuned at least occasionally.  
(This is conservative. Pianos are relatively rare — most people have keyboards or nothing. In wealthier or more cultured neighborhoods the rate is higher, in poorer areas much lower.)

→ Pianos = 1,080,000 × (1/50) = **21,600 pianos**.

**4. Estimate how often pianos are tuned**  
Assumption: The average tuned piano is tuned **once every 2 years**.  
(Many serious musicians tune 2–4 times/year; most casual owners tune every 3–5 years or never. "Once every 2 years" is a reasonable average for pianos that *are* tuned.)

→ Total tunings per year = 21,600 ÷ 2 = **10,800 tunings per year**.

**5. Estimate how many tunings one piano tuner can do per year**  
Assumptions:
- A tuner works ~**220 days per year** (accounting for weekends, holidays, vacation).
- Average of **4 pianos per day** (includes travel time across a big city; a full tuning takes 1–2 hours).
- Some tuners also do repairs, teaching, or sell instruments, so they don't tune full time.

→ Tunings per tuner per year = 220 × 4 = **880 tunings/year**.

**6. Calculate number of tuners**  
Tuners needed = Total tunings per year ÷ Tunings per tuner per year  
= 10,800 ÷ 880 ≈ **12.3**

**Final point estimate: ~12–13 full-time equivalent piano tuners.**

However, this doesn't account for part-time tuners, retirees, or people who tune only occasionally. Realistically, the total number ...
```

### Claude Sonnet 4.6

**Generation Time:** 25083ms
**Tokens:** 1252

```
# Estimating Piano Tuners in Chicago

## The Core Logic

The number of tuners needed = Total tunings per year ÷ Tunings one tuner can do per year

---

## Step 1: Population of Chicago Metro Area

**Assumption:** Using greater Chicago metro area (~3 million households is more relevant than city proper)
- City of Chicago: ~2.7 million people
- I'll use **1 million households** (city proper, ~2.7 people/household)
- If including suburbs: ~3.5 million households

**I'll work with Chicago city: ~1 million households**

---

## Step 2: How Many Pianos Exist?

**Assumptions:**
- Pianos are expensive and space-intensive → not common
- Roughly **1 in 20 households** owns a piano = 5%
- Supporting logic: Piano ownership peaked mid-20th century; many sit untuned in living rooms; feels right vs. 1 in 10 (too high) or 1 in 50 (too low)

**Household pianos:** 1,000,000 × 0.05 = **50,000 pianos**

**Non-household pianos** (schools, churches, bars, concert halls, recording studios):
- ~600 schools × 5 pianos avg = 3,000
- ~1,000 churches × 1 piano avg = 1,000
- Bars, hotels, studios: ~1,000
- **Institutional pianos: ~5,000**

**Total pianos: ~55,000**

---

## Step 3: How Often Are Pianos Tuned?

**Assumptions:**
- Recommendation is 2x/year, but many owners ignore this
- Institutional pianos: tuned more regularly (~2-4x/year)
- Household pianos: maybe **half are tuned at all**, averaging **1x/year** among those tuned

| Category | Count | % Tuned | Frequency | Annual Tunings |
|----------|-------|---------|-----------|----------------|
| Household | 50,000 | 50% | 1x/year | 25,000 |
| Institutional | 5,000 | 90% | 2x/year | 9,000 |
| **Total** | | | | **~34,000** |

---

## Step 4: How Many Tunings Can One Tuner Do Per Year?

**Assumptions:**
- Tuning takes ~1.5 hours (including travel in Chicago traffic)
- Working ~48 weeks/year, 5 days/week = 240 days
- ~4 tunings/day (accounting for travel, scheduling gaps, admin)
- 4 × 240 = **~960 tunings/tuner/year**

I'll round to **~1,000 ...
```

### MiMo-V2-Flash

**Generation Time:** 13963ms
**Tokens:** 1999

```
Here is a step-by-step estimation of the number of piano tuners in Chicago using a Fermi problem approach (order-of-magnitude estimation).

### 1. Key Assumptions
To solve this, we must make several reasonable assumptions about the population and behavior of Chicago residents.

*   **Geographic Area:** We are estimating for the city proper of Chicago, not the greater metropolitan area.
*   **Population:** The population is approximately 2.7 million people.
*   **Household Size:** The average household contains 2.5 people.
*   **Piano Ownership:** Pianos are owned not only by households but also by institutions (schools, churches, bars, concert halls). We assume a piano ownership rate per capita rather than per household.
*   **Tuning Frequency:** Acoustic pianos require tuning 1–2 times per year. We will use an average of 1.5 times per year.
*   **Workload:** A full-time professional tuner works standard full-time hours but accounts for travel time, administration, and downtime.

---

### 2. Derivation of Numbers

We will use a bottom-up approach: starting with the total population and filtering down to the specific demand for piano tuning services.

#### Step A: Total Population
*   **Source:** U.S. Census estimates.
*   **Number:** 2,700,000 people.

#### Step B: Number of Households
*   **Assumption:** Average household size is 2.5 people.
*   **Calculation:**
    $$2,700,000 \text{ people} \div 2.5 \text{ people/household} = 1,080,000 \text{ households}$$

#### Step C: Number of Pianos
It is difficult to estimate pianos purely by household, as many are located in institutions. We will estimate based on a "per capita" ownership rate.

*   **Assumption:** Based on industry data (e.g., Piano Technicians Guild), roughly 1 in 10 to 1 in 15 people in a developed urban area has access to an acoustic piano (either owned personally or in a local institution like a school or church).
*   **Selected Ratio:** 1 piano per 12 people.
*   **Calculation:**
    $$2,700,000 \text...
```

### GPT-OSS-120B

**Generation Time:** 21627ms
**Tokens:** 2170

```
**Fermi‑style estimate of the number of piano‑tuning professionals who work in the Chicago metro area**  

Below is a step‑by‑step calculation, with every assumption spelled out, the arithmetic that follows from it, a quick “what‑if” sensitivity check for each major input, and a final range that reflects the plausible uncertainty.

---

## 1. DEFINING THE “CHICAGO AREA”

| Item | Value (assumption) | Reason |
|------|-------------------|--------|
| **Geographic scope** | Chicago‑Metropolitan Statistical Area (MSA) – the city of Chicago plus its 4‑county suburbs (Cook, DuPage, Lake, Will) | This is the standard market area used by most service‑business statistics. |
| **Population** | **≈ 9.6 million** people (2023 Census estimate) | Official MSA population. |
| **Number of households** | **≈ 3.6 million** households | 9.6 M / 2.7 persons per household (U.S. average). |

---

## 2. HOW MANY PIANOS ARE IN THE AREA?

### 2.1 Residential pianos  

| Assumption | Value | Source / Rationale |
|------------|-------|--------------------|
| **% of households that own a piano** | **5 %** | National surveys (e.g., NAMM, 2022) show about 4–6 % of U.S. homes own a piano (including upright & grand). Chicago is a large‑city market, so 5 % is a reasonable midpoint. |
| **Number of residential pianos** | 3.6 M × 0.05 = **180 000** | Simple multiplication. |

### 2.2 Institutional/commercial pianos  

| Institution | Approx. # in Chicago area | Reasoning |
|-------------|--------------------------|-----------|
| Public & private K‑12 schools (≈ 800 schools) | 1–2 pianos per school → **≈ 1 200** | Many schools have a single practice piano; larger schools have a few. |
| Colleges & universities (≈ 70 institutions) | 5–10 pianos each → **≈ 500** | Music departments, practice rooms, recital halls. |
| Churches & worship centers (≈ 2 000) | 0.5–1 piano each → **≈ 1 000** | Many have an organ but a fair number keep a piano for choir practice. |
| Concert halls, theaters, recording studios,...
```

### Gemini 2.5 Flash

**Generation Time:** 10583ms
**Tokens:** 1869

```
Let's estimate the number of piano tuners in Chicago using a Fermi estimate approach.

**1. Assumptions:**

*   **Chicago Population:** Approximately 2.7 million people. (Source: Quick Google search for "Chicago population")
*   **Household Size:** Average of 2.5 people per household. (Source: Quick Google search for "average household size Chicago")
*   **Percentage of Households with a Piano:** This is the trickiest assumption. Let's break it down:
    *   **High-income households:** More likely to have pianos.
    *   **Musically inclined households:** More likely.
    *   **Space availability:** Pianos take up space, so smaller apartments might not have them.
    *   **Cost:** Pianos are an investment.
    *   **Cultural factors:** Pianos were more common in the past.
    *   **My Estimate:** I'll assume that 1 out of every 50 households (2%) in Chicago has a piano that requires tuning. This feels like a reasonable starting point, considering the factors above. It's not 1 in 10, but also not 1 in 100.
*   **Tuning Frequency:** A piano should ideally be tuned once a year. Some might do it every two years, some twice a year. Let's average it to **once every 1.5 years** per piano. This is a common recommendation for household pianos.
*   **Time per Tuning:** An experienced tuner can tune a piano in about 1.5 to 2 hours. Let's use **1.75 hours** as an average. This includes travel time to some extent, but we'll account for more explicit travel time later.
*   **Working Hours per Tuner per Year:**
    *   **Working days per year:** 5 days/week * 50 weeks/year = 250 working days (allowing for holidays and vacation).
    *   **Working hours per day:** 8 hours/day.
    *   **Total potential working hours:** 250 days * 8 hours/day = 2000 hours/year.
    *   **Billable hours percentage:** Not all working hours are billable. There's travel, administrative tasks, marketing, breaks, etc. Let's assume **50% of their time is spent on actual tuning appointments**. So, 1000 bill...
```

### MiniMax M2.5

**Generation Time:** 33653ms
**Tokens:** 2143

```

```

---

*Generated by The Multivac V5*
*https://themultivac.com*