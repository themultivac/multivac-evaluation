# Multivac Evaluation Report

**Evaluation ID:** EVAL-20260402-195829
**Timestamp:** 2026-04-02T19:58:29.258432
**Category:** Analysis & Research
**Model Pool:** 10 analysis-optimized models

## Question

A 5-year-old codebase has: 45% test coverage, 200 known bugs (50 critical), 15 engineers maintaining it, average deployment takes 4 hours, 3 production incidents/month. A complete rewrite is estimated at 12 months with 8 engineers. (1) Should you rewrite or refactor incrementally? (2) Calculate the cost of technical debt using downtime and developer productivity. (3) Design a 6-month plan that reduces critical bugs by 80% without a rewrite. (4) When IS a rewrite justified?

---

## Rankings

| Rank | Model | Score | Min | Max | Std Dev |
|------|-------|-------|-----|-----|---------|
| 1 | Grok 4.20 | 9.14 | 8.55 | 9.80 | 0.55 |
| 2 | MiniMax M2.5 | 8.84 | 7.95 | 9.55 | 0.48 |
| 3 | GPT-5.4 | 8.52 | 7.35 | 9.60 | 0.64 |
| 4 | Gemini 3 Flash Preview | 8.39 | 7.75 | 9.20 | 0.46 |
| 5 | GPT-OSS-120B | 8.16 | 7.00 | 9.60 | 0.81 |
| 6 | DeepSeek V3 | 8.10 | 6.75 | 9.15 | 0.77 |
| 7 | MiMo-V2-Flash | 7.39 | 5.80 | 9.00 | 1.13 |
| 8 | Claude Sonnet 4.6 | 7.34 | 3.40 | 9.00 | 1.74 |
| 9 | Claude Opus 4.6 | 7.04 | 4.45 | 8.80 | 1.59 |
| 10 | Gemini 3.1 Pro | 6.26 | 3.50 | 8.60 | 1.71 |

---

## Meta Analysis

### Judge Strictness

| Rank | Judge | Avg Score Given |
|------|-------|-----------------|
| 1 | GPT-5.4 | 6.49 |
| 2 | GPT-OSS-120B | 6.73 |
| 3 | MiniMax M2.5 | 7.47 |
| 4 | Claude Opus 4.6 | 7.83 |
| 5 | Grok 4.20 | 7.95 |
| 6 | Gemini 3.1 Pro | 7.98 |
| 7 | Claude Sonnet 4.6 | 8.12 |
| 8 | MiMo-V2-Flash | 8.57 |
| 9 | DeepSeek V3 | 8.85 |
| 10 | Gemini 3 Flash Preview | 9.31 |

**Strictest Judge:** gpt_5_4
**Most Lenient Judge:** gemini_3_flash
**Total Judgments:** 100
**Valid Judgments:** 87

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

**Generation Time:** 19089ms
**Tokens:** 2166

```
Here is a comprehensive analysis and strategy for your codebase, addressing all four parts of your prompt from an engineering leadership perspective.

### 1. Should you rewrite or refactor incrementally?
**Decision: Refactor Incrementally.**

A complete rewrite is a trap in this scenario. Here is why:
*   **The "Second System" Fallacy:** Rewrites almost always take longer than estimated. A 12-month estimate usually becomes 18–24 months. 
*   **The Split-Brain Problem:** If you put 8 engineers on the rewrite, you leave 7 engineers to maintain a buggy legacy system. The legacy system will continue to generate incidents, burning out the maintenance team. Meanwhile, the rewrite team will constantly be chasing a moving target as the business demands new features in the legacy app.
*   **You have a foundation:** 5 years is not ancient. 45% test coverage is actually a decent safety net (many legacy apps have 0%). 
*   **The real problems are operational:** A 4-hour deployment time and 3 incidents a month point to CI/CD and DevOps bottlenecks, not necessarily a fundamentally broken architecture. A rewrite won't fix bad deployment practices.

### 2. Calculate the Cost of Technical Debt
To calculate this, we must make standard industry assumptions. Let's assume an average fully burdened engineer cost of **$150,000/year ($75/hour)** and an average cost of downtime/incidents at **$10,000/hour** (adjust this based on your actual revenue).

**A. Cost of Downtime / Incidents**
*   **Downtime Revenue Loss:** 3 incidents/month. Assuming an average of 2 hours of downtime/degraded performance per incident = 6 hours/month. 
    *   *Cost: 6 hrs × $10,000 = $60,000/month ($720,000/year).*
*   **Incident Triage & Fix:** 3 incidents usually require ~3 engineers context-switching for about 4 hours each (investigation, fixing, post-mortem
```

### Claude Opus 4.6

**Generation Time:** 33959ms
**Tokens:** 2184

```
# The Rewrite vs. Refactor Decision: A Complete Engineering Analysis

## Part 1: Should You Rewrite or Refactor?

### **The Answer: Incremental Refactoring (with strategic exceptions)**

Let me build the case systematically.

```
┌─────────────────────────────────────────────────────────────────────┐
│                    JOEL SPOLSKY'S LAW                                │
│                                                                     │
│  "The single worst strategic mistake that any software company      │
│   can make: rewrite the code from scratch."                         │
│                                                                     │
│  Netscape (1999): Rewrote Navigator → Lost browser war              │
│  Basecamp: Incremental improvement → Market leader                  │
│  Twitter: Incremental Ruby→JVM migration → Scaled successfully      │
│                                                                     │
│  BUT: There ARE exceptions (see Part 4)                             │
└─────────────────────────────────────────────────────────────────────┘
```

### The Rewrite Risk Matrix

```
WHAT YOU THINK WILL HAPPEN:
Month 1-3:   ████████░░ Build new foundation
Month 4-6:   ████████░░ Core features rebuilt  
Month 7-9:   ████████░░ Feature parity
Month 10-12: ████████░░ Migration complete ✓

WHAT ACTUALLY HAPPENS:
Month 1-3:   ████████░░ Build new foundation (on schedule!)
Month 4-6:   ██████░░░░ Core features (harder than expected)
Month 7-9:   ████░░░░░░ "Why does the old system do THIS?"
Month 10-12: ███░░░░░░░ Discovering undocumented business rules
Month 13-15: ███░░░░░░░ Still not at feature parity
Month 16-18: ████░░░░░░ Running TWO systems simultaneously
Month 19-24: █████░░░░░ Finally migrating... with new bugs

Meanwhile, the old system still needs maintenance by remaining 7 engineers.
```

### Quantified Comparison

```
╔══════════════════════════════════════════════════════════════════╗
║                    REWRITE SCENARIO     ...
```

### GPT-5.4

**Generation Time:** 34789ms
**Tokens:** 2167

```
Here’s a practical engineering answer.

---

## 1) Rewrite or refactor incrementally?

## Recommendation: **Do not do a complete rewrite now. Refactor incrementally.**

Given your numbers, a full rewrite is usually the wrong first move.

### Why
A rewrite would:
- consume **8 engineers for 12 months**
- delay feature work and operational improvement
- likely reintroduce old bugs in new forms
- require rebuilding years of business logic and edge-case knowledge
- create a long period where the old system still needs maintenance anyway

Meanwhile, your current pain points are classic **stabilization/refactoring** targets:
- **45% test coverage** → can be improved selectively around risky areas
- **200 bugs, 50 critical** → triage and attack hot spots
- **4-hour deployments** → CI/CD and release engineering improvements can produce fast wins
- **3 incidents/month** → likely tied to poor observability, fragile modules, and weak release safety

A rewrite does not automatically solve these. In fact, it often worsens them for a year.

### Better approach
Use **incremental modernization**:
- identify the bug-heavy/high-change modules
- add characterization tests before changes
- isolate unstable components behind interfaces
- refactor module by module
- improve deployment pipeline and release safety
- aggressively reduce critical defects first

### Business view
The current system is expensive, but not obviously unsalvageable.  
A rewrite is justified when the architecture fundamentally blocks the business, not just because the code is messy.

---

## 2) Calculate the cost of technical debt using downtime and developer productivity

We don’t have enough data for a precise dollar amount, so the best answer is to provide a **model** and an **illustrative calculation**.

---

## A. Downtime / incident cost

You said:
- **3 production incidents per month**

But you did **not** specify:
- average incident duration
- number of affected users
- revenue loss per hour
- engineer resp...
```

### DeepSeek V3

**Generation Time:** 58328ms
**Tokens:** 1081

```
### (1) Rewrite or Refactor Incrementally?

**Recommendation: Refactor incrementally.**  

**Reasons:**  
- **High Risk of Rewrite:** A 12-month rewrite with 8 engineers is costly and risky. The current system is mission-critical (evidenced by production incidents), and a rewrite could introduce new bugs, delay features, and demotivate teams.  
- **Incremental Refactoring is Safer:** Address the worst technical debt first (e.g., critical bugs, slow deployments) while keeping the system operational.  
- **Team Continuity:** 15 engineers are familiar with the codebase; losing that knowledge during a rewrite could hurt productivity.  
- **Low Test Coverage (45%):** A rewrite without better tests risks recreating the same problems.  

**Exceptions where a rewrite *might* be justified:**  
- If the system is built on obsolete technology (e.g., deprecated frameworks, unsupported languages).  
- If the business logic is fundamentally flawed and can’t be fixed incrementally.  

---

### (2) Cost of Technical Debt  

**Assumptions:**  
- **Downtime Cost:** 3 incidents/month × 4 hours/deployment = 12 hours/month.  
  - If hourly revenue impact = $10k, downtime cost = **$120k/month**.  
- **Developer Productivity:**  
  - 15 engineers × 20% time spent on bugs/debt (estimated) = 3 engineers "lost" to debt.  
  - Avg engineer cost = $150k/year → $37.5k/quarter lost per engineer → **$112.5k/quarter** (or **$37.5k/month**) in lost productivity.  
- **Critical Bug Cost:**  
  - 50 critical bugs × avg 8 hours to fix = 400 engineer-hours.  
  - At $75/hour, cost = **$30k** (one-time, but bugs may recur).  

**Total Estimated Cost:** ~$157.5k/month (downtime + productivity) + one-time bug costs.  

---

### (3) 6-Month Plan to Reduce Critical Bugs by 80%  

**Goal:** Reduce critical bugs from 50 to 10.  

**Phase 1 (Month 1-2): Triage & Stabilize**  
- **Prioritize Bugs:** Classify critical bugs by impact (e.g., security, crashes) and fix the top 10 highest-impact ones.  
- **Improve ...
```

### MiMo-V2-Flash

**Generation Time:** 28859ms
**Tokens:** 2204

```
Below is a structured response to your query. I'll address each part sequentially based on the provided scenario. My recommendations draw from established software engineering principles (e.g., from Martin Fowler's "Refactor or Rewrite?" and industry best practices like the "Strangler Fig" pattern for incremental changes). The analysis assumes a typical enterprise software environment (e.g., SaaS or internal tooling) where downtime and productivity losses have quantifiable business impacts. If you have additional context (e.g., team salaries, revenue impact), these could be refined.

### (1) Should You Rewrite or Refactor Incrementally?
**Recommendation: Refactor incrementally.**

A complete rewrite is rarely advisable for a 5-year-old codebase with these metrics, as it introduces massive risk, delays, and opportunity costs. Here's why:

- **Risks of Rewrite:**
  - **Time and Resource Sink:** 12 months with 8 engineers means ~768 person-months (8 engineers × 12 months). During this period, the existing system continues to accrue bugs (200 known, 50 critical) and incidents (3/month), potentially worsening user trust and revenue.
  - **Business Disruption:** The rewrite won't deliver value until completion, while the old system degrades. You'd need parallel maintenance (15 engineers still needed), leading to burnout or neglect of the old system.
  - **Uncertainty:** Rewrites often underestimate edge cases in legacy code, leading to scope creep (e.g., "While we're at it, let's add features"). Success rates for full rewrites are low (~30-50% per industry studies like those from Gartner).
  - **Opportunity Cost:** Diverting 8 engineers halts other roadmap progress.

- **Benefits of Incremental Refactoring:**
  - **Lower Risk:** Tackle critical bugs first (e.g., via targeted fixes) while maintaining the system. Use patterns like the Strangler Fig to gradually replace components.
  - **Faster ROI:** Improvements (e.g., test coverage, bug reductions) can be delivered in wee...
```

### Claude Sonnet 4.6

**Generation Time:** 37046ms
**Tokens:** 2185

```
# Technical Debt Analysis & Strategic Decision Framework

## Executive Summary

This is a classic "rewrite vs. refactor" dilemma with quantifiable stakes. My answer upfront: **do not rewrite** — but execute a disciplined, aggressive incremental improvement program. Here's the complete analysis.

---

## Part 1: Rewrite vs. Incremental Refactor Decision

### The Rewrite Trap

```
The Seductive Logic:
"If we just started fresh, everything would be clean"
                    ↓
The Reality:
You are proposing to spend 12 months building
a system you don't fully understand yet,
while the existing system continues accumulating debt.
```

### Quantified Risk Analysis

```
REWRITE SCENARIO
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Timeline Risk:
  Estimated:     12 months
  Industry avg:  1.5-3x overrun
  Realistic:     18-36 months

  Why estimates fail:
  ├── Hidden business logic in the old system
  ├── Edge cases discovered only in production
  ├── "Simple" features with complex dependencies
  └── Integration points nobody documented

Cost During Rewrite (12 months):
  8 engineers × $150k/yr        = $1,200,000
  + Opportunity cost (no features) = $800,000 (est.)
  + Old system still maintained   = 7 engineers × $150k = $1,050,000
  ─────────────────────────────────────────────────────
  Total minimum cost:             = $3,050,000

  And you still have:
  ├── 3 incidents/month during transition
  ├── Zero new features for 12 months
  ├── Team morale risk (rewrites are demoralizing)
  └── The new system WILL have new bugs

INCREMENTAL REFACTOR SCENARIO
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Timeline:       6 months to stability
                12 months to healthy codebase

Cost:
  15 engineers × $150k × 0.5yr  = $1,125,000
  (with productivity improvements starting month 2)

Benefits:
  ├── System stays in production
  ├── Features continue shipping
  ├── Learning is incremental and reversible
  └── Risk is distributed, not concentrated
```

### Decis...
```

### Grok 4.20

**Generation Time:** 8291ms
**Tokens:** 1806

```
**1. Should you rewrite or refactor incrementally?**

**Refactor incrementally.** Do not do a full rewrite.

**Reasons:**
- The codebase is only 5 years old — not ancient. Most of the domain knowledge and business rules are still fresh.
- You have 15 engineers. A rewrite with 8 engineers for 12 months means you are taking more than half your capacity offline for a year while the other half tries to keep the buggy system alive. This is extremely high risk.
- Rewrites almost always take 2–3× longer than estimated and usually re-introduce many of the same bugs or create new ones.
- You already have 200 known bugs. A rewrite will create a new unknown set of bugs while the old system continues to generate incidents.

**Rule of thumb:** Only rewrite when one or more of these are true (see part 4). None of them are clearly true here yet.

**Recommended approach:** Aggressive incremental refactoring + strangler fig pattern + heavy investment in quality for 6–12 months.

---

**2. Calculate the cost of technical debt (rough but realistic numbers)**

Let's assign conservative industry numbers:

### Assumptions
- Engineer fully loaded cost: $180k/year ≈ **$15,000/month**
- Average incident cost: $12,000 (blended — includes lost revenue, customer support, engineering time). This is low for many B2B/SaaS companies.
- Downtime / incident impact: each of the 3 monthly incidents causes 2 hours of degraded service or full outage.
- Developer productivity tax from tech debt: 35% (very common with 45% test coverage and 200 bugs). This is time spent on firefighting, complex debugging, slow velocity, etc.

### Monthly Cost of Tech Debt

| Item | Calculation | Monthly Cost |
|------|-------------|--------------|
| **Incident cost** | 3 incidents × $12k | **$36,000** |
| **Downtime engineering cost** | 3 incidents × 4 engineers × 8 hours × $90/hr | **$8,600** |
| **Productivity tax** | 15 engineers × 35% × $15k | **$78,750** |
| **Bug fixing overhead** | 200 bugs (50 critical) — estimate ...
```

### GPT-OSS-120B

**Generation Time:** 63578ms
**Tokens:** 2228

```
## Executive Summary  

| Aspect | Key Take‑away |
|--------|---------------|
| **Rewrite vs. incremental refactor** | **Incremental refactor** is the safer, cheaper, and faster way to achieve the business‑critical goal (80 % reduction in critical bugs) while keeping the system in production. |
| **Technical‑debt cost (estimated)** | **≈ $1.2 M / year** in lost productivity + downtime. |
| **6‑month “no‑rewrite” plan** | A focused, data‑driven program that (a) raises test coverage to ≥ 70 %, (b) clears the critical‑bug backlog, (c) builds a robust CI/CD pipeline, and (d) embeds a “technical‑debt burn‑down” sprint every two weeks. |
| **When a full rewrite is justified** | When the **cost of keeping the system alive > ~30 % of the product’s annual revenue** *or* when **non‑technical constraints** (e.g., security compliance, regulatory mandates, strategic platform shift) make the existing codebase an absolute barrier. |

Below you’ll find the detailed reasoning, calculations, and the concrete 6‑month plan.

---

## 1. Rewrite or Incremental Refactor?  

### 1.1 Decision matrix (high‑level)

| Factor | Rewrite (12 mo, 8 engineers) | Incremental Refactor (6 mo, 15 engineers) |
|--------|------------------------------|-------------------------------------------|
| **Time to value** | 12 mo before any new feature or stability gain | 0 mo – immediate gains each sprint |
| **Risk** | High (knowledge loss, integration gaps, “big‑bang” failure) | Low‑medium (changes are localized, can be rolled back) |
| **Cost (engineer‑months)** | 96 EM (8 × 12) | 90 EM (15 × 6) – but 6 mo of production work continues |
| **Impact on current operations** | System must stay up while a parallel codebase is built → double‑maintenance overhead | System stays live; refactor work is done in‑place with feature toggles |
| **Team morale & knowledge retention** | Possible loss of domain knowledge as old code is abandoned | Knowledge stays within the team; they become “code‑owners” of the parts they ...
```

### Gemini 3 Flash Preview

**Generation Time:** 8191ms
**Tokens:** 1179

```
This scenario represents a classic "legacy trap." The metrics indicate a system that is failing but still operational enough to be dangerous.

### 1. The Verdict: Refactor Incrementally
**You should refactor incrementally.**

A 12-month rewrite estimate for a 5-year-old codebase is almost certainly an underestimate (Hofstadter's Law). 
*   **The Risk:** During the 12 months, the 7 engineers left on the old system will be overwhelmed by the 3 monthly incidents and 200 bugs. Feature parity will be a moving target.
*   **The Reality:** Most rewrites fail because the "Second System Effect" leads to over-engineering, while the domain knowledge embedded in the "messy" old code is lost.

---

### 2. Calculating the Cost of Technical Debt

To quantify the cost, we look at **Opportunity Cost** and **Operational Drag.**

#### A. Developer Productivity Loss
*   **Context Switching & Friction:** With 45% coverage and 200 bugs, engineers likely spend 60% of their time on "run-the-shop" activities (bug fixing, manual testing, babysitting deployments).
*   **Calculation:** 15 engineers × 60% waste = **9 Full-Time Equivalents (FTEs) lost to debt.** 
*   **Annual Cost:** If an average engineer costs \$150k, the debt tax is **\$1.35M/year** in wasted salary alone.

#### B. Downtime & Deployment Cost
*   **Deployment Drag:** 4 hours/deploy × 15 engineers (assuming a sync culture) or lost velocity. If they deploy 4x a month, that’s 240 man-hours spent just watching progress bars.
*   **Incident Impact:** 3 incidents/month. If each averages 2 hours of downtime affecting a \$10M/year revenue stream:
    *   72 hours of downtime/year = ~0.8% of yearly revenue.
    *   **Annual Cost:** **\$80,000 in direct revenue loss** + reputational damage.

---

### 3. The 6-Month "Stabilization" Plan
The goal is to move from **Reactive** to **Proactive** without stopping feature work entirely.

| Phase | Focus | Key Actions |
| :--- | :--- | :--- |
| **Month 1: The Safety Net** | **Observability & CI*...
```

### MiniMax M2.5

**Generation Time:** 15364ms
**Tokens:** 2134

```
Excellent questions. This is a classic "Strangler Fig" scenario. Let's break this down systematically.

### (1) Should you rewrite or refactor incrementally?

**Recommendation: Refactor incrementally (Strangler Fig Pattern).**

**Reasoning:**
*   **Risk:** A complete rewrite (12 months, 8 engineers) is a high-risk "big bang" release. You are essentially betting the business's operations on a new system being perfect on day one, while the old system continues to decay.
*   **Opportunity Cost:** 8 engineers for a year is a massive investment that freezes development of new features, potentially losing market share.
*   **Knowledge Loss:** A rewrite often discards years of tribal knowledge embedded in the codebase, even if it's "messy." That messiness often contains hard-won bug fixes and business logic.
*   **The Numbers Don't Support a Rewrite:** You have a functional (if flawed) system. The goal should be to improve it iteratively while it runs.

### (2) Cost of Technical Debt (Downtime + Developer Productivity)

**Assumptions for Calculation:**
*   **Engineer Annual Fully-Loaded Cost:** $150,000 (salary + overhead).
*   **Average Revenue/Profit per Hour of Downtime:** $10,000 (conservative for a business with this level of incidents).
*   **Developer Time Allocation:** 20% of 15 engineers' time goes to maintaining/fixing the 200 bugs (this is a conservative estimate for a high-bug codebase).

**Calculations:**

1.  **Developer Productivity Cost:**
    *   15 engineers * 20% = 3 FTE dedicated to bug fixes.
    *   Cost = 3 * $150,000 = **$450,000/year**.

2.  **Downtime Cost:**
    *   **Incident Downtime:** 3 incidents/month * assume avg 2 hours downtime per incident = 6 hours/month.
    *   **Deployment Downtime:** 4 hours/deployment * assume 1 deployment/week = 16 hours/month.
    *   **Total Downtime:** 22 hours/month = 264 hours/year.
    *   Cost = 264 hours * $10,000/hour = **$2,640,000/year**.

**Total Annual Technical Debt Cost: ~$3.09 Million**

*(This doe...
```

---

*Generated by The Multivac V5*
*https://themultivac.com*