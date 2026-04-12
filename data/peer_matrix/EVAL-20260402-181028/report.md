# Multivac Evaluation Report

**Evaluation ID:** EVAL-20260402-181028
**Timestamp:** 2026-04-02T18:10:28.958263
**Category:** Reasoning & Logic
**Model Pool:** 10 reasoning-optimized models

## Question

A teacher gives a test. Students who scored in the top 10% get praised. Students who scored in the bottom 10% get extra tutoring. On the next test, the top scorers decline slightly and the bottom scorers improve. The teacher concludes: 'Praise is counterproductive, but tutoring works.' (1) What's actually happening? (2) Design a study that separates regression to the mean from real effects. (3) Give three real-world examples where this fallacy leads to bad policy decisions.

---

## Rankings

| Rank | Model | Score | Min | Max | Std Dev |
|------|-------|-------|-----|-----|---------|
| 1 | Claude Opus 4.6 | 9.61 | 8.65 | 10.00 | 0.55 |
| 2 | GPT-5.4 | 9.31 | 8.45 | 10.00 | 0.51 |
| 3 | MiMo-V2-Flash | 9.19 | 8.65 | 10.00 | 0.52 |
| 4 | GPT-OSS-120B | 9.16 | 8.15 | 10.00 | 0.60 |
| 5 | MiniMax M2.5 | 9.15 | 8.65 | 10.00 | 0.49 |
| 6 | Grok 4.20 | 9.13 | 8.45 | 9.45 | 0.37 |
| 7 | Gemini 2.5 Flash | 9.11 | 8.65 | 10.00 | 0.42 |
| 8 | Claude Sonnet 4.6 | 9.04 | 8.05 | 10.00 | 0.72 |
| 9 | DeepSeek V3 | 8.97 | 8.25 | 10.00 | 0.54 |
| 10 | Gemini 3.1 Pro | 8.18 | 7.25 | 9.45 | 0.67 |

---

## Meta Analysis

### Judge Strictness

| Rank | Judge | Avg Score Given |
|------|-------|-----------------|
| 1 | GPT-OSS-120B | 8.46 |
| 2 | GPT-5.4 | 8.57 |
| 3 | MiniMax M2.5 | 8.63 |
| 4 | Grok 4.20 | 8.76 |
| 5 | Claude Opus 4.6 | 9.10 |
| 6 | Claude Sonnet 4.6 | 9.11 |
| 7 | MiMo-V2-Flash | 9.42 |
| 8 | DeepSeek V3 | 9.44 |
| 9 | Gemini 3.1 Pro | 9.55 |
| 10 | Gemini 2.5 Flash | 9.82 |

**Strictest Judge:** gpt_oss_120b
**Most Lenient Judge:** gemini_25_flash
**Total Judgments:** 100
**Valid Judgments:** 90

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

**Generation Time:** 60525ms
**Tokens:** 2151

```
Here is a breakdown of the statistical phenomenon at play, a study design to uncover the truth, and real-world examples of this fallacy in action.

### 1. What is actually happening? 
The teacher is being fooled by a statistical phenomenon known as **Regression to the Mean (RTM)**. 

A student’s score on any given test is a combination of two things: **True Skill + Random Variance (Luck)**. Variance includes factors like how well they slept, whether they guessed right, or if the test happened to focus on the one chapter they studied most.

*   **The Top 10%:** To score in the absolute top tier, a student usually needs high skill *and* good luck. On the second test, their skill remains high, but their "luck" normalizes. Consequently, their scores naturally drop slightly closer to their true average.
*   **The Bottom 10%:** Conversely, the lowest scorers likely had low skill *and* bad luck (e.g., they felt sick, or the test hit their weakest subjects). On the second test, their luck normalizes, so their scores naturally improve.

The teacher is confusing a natural statistical fluctuation (regression to the mean) with a causal relationship (praise hurts, tutoring helps). This exact scenario was famously observed by Nobel laureate Daniel Kahneman when observing Israeli flight instructors, who falsely concluded that screaming at pilots improved their flying, while praising them made them worse.

### 2. Design a study to separate regression to the mean from real effects
To find out if praise and tutoring actually work, we must remove RTM as a confounding variable. We do this using a **Randomized Controlled Trial (RCT)**.

**Step 1: Baseline**
Administer Test 1 to a large representative sample of students (e.g., 1,000 students) and identify the Top 10% and Bottom 10%.

**Step 2: Random Assignment (The Control Group)**
*   Take the **Top 10%** and randomly divide them into two groups: 
    *   *Group A (Intervention):* Receives praise.
    *   *Group B (Control):* Receives ...
```

### DeepSeek V3

**Generation Time:** 22567ms
**Tokens:** 1245

```
### Understanding the Scenario

Let's break down the given scenario to understand what's happening.

1. **Initial Test**: Students take a test.
   - **Top 10%**: These students are praised.
   - **Bottom 10%**: These students receive extra tutoring.
   
2. **Next Test**:
   - **Top scorers (previously praised)**: Their performance declines slightly.
   - **Bottom scorers (previously tutored)**: Their performance improves.
   
3. **Teacher's Conclusion**:
   - "Praise is counterproductive" because the praised students did worse.
   - "Tutoring works" because the tutored students did better.

### (1) What's Actually Happening?

The phenomenon observed here is likely **regression to the mean**. This is a statistical concept where extreme observations (very high or very low scores) tend to be followed by more moderate observations when measured again, simply due to random variability.

- **Top 10% Students**: Their high scores on the first test were partly due to ability and partly due to random good luck. On the next test, their scores decrease slightly because the luck component isn't as favorable, regressing toward their true mean performance.
  
- **Bottom 10% Students**: Their low scores on the first test were partly due to lack of ability and partly due to random bad luck. On the next test, their scores increase slightly because the luck component isn't as unfavorable, regressing toward their true mean performance.

The teacher attributes these changes to praise and tutoring, but the changes are largely due to statistical regression rather than the interventions.

### (2) Designing a Study to Separate Regression to the Mean from Real Effects

To distinguish between regression to the mean and actual effects of praise or tutoring, we can design a randomized controlled trial (RCT) as follows:

1. **Random Assignment**:
   - After the first test, randomly assign students from the top 10% to two groups:
     - Group A: Praised.
     - Group B: Not praised (control grou...
```

### Claude Opus 4.6

**Generation Time:** 198798ms
**Tokens:** 1869

```
# Regression to the Mean: A Complete Analysis

## (1) What's Actually Happening

The teacher is observing **regression to the mean** and misattributing it to causal interventions.

**The core mechanism:**

Any single test score is a combination of two components:

```
Observed Score = True Ability + Random Variation (luck, sleep, mood, guessing)
```

Students who scored in the **top 10%** likely had true ability working in their favor *plus* positive random variation that day. On the next test, that random component is unlikely to be equally extreme in the same direction. Their scores drift back toward their true average. This looks like decline.

Students who scored in the **bottom 10%** likely had true ability working against them *plus* negative random variation. On retest, the random component shifts back toward zero. Their scores drift upward. This looks like improvement.

**The critical insight:** This pattern would occur even if the teacher did absolutely nothing — no praise, no tutoring, no intervention at all. You could replace both interventions with reading students a phone book and observe the same result.

The teacher has committed a specific error: selecting groups based on extreme values of a noisy measurement, then interpreting the statistically inevitable regression as evidence for or against an intervention.

---

## (2) Designing a Study That Separates Regression from Real Effects

### The Proper Experimental Design

```
Step 1: IDENTIFY extreme scorers
├── Top 10% (n students)
└── Bottom 10% (n students)

Step 2: RANDOMLY ASSIGN within each group
├── Top 10% → Random split
│   ├── Group A: Receives praise
│   └── Group B: No praise (control)
│
└── Bottom 10% → Random split
    ├── Group C: Receives tutoring
    └── Group D: No tutoring (control)

Step 3: RETEST all four groups

Step 4: COMPARE
├── Effect of praise = Score change in A minus score change in B
└── Effect of tutoring = Score change in C minus score change in D
```

### Why This Works...
```

### GPT-5.4

**Generation Time:** 17622ms
**Tokens:** 998

```
1) What’s actually happening

This is a classic case of regression to the mean.

The students were selected because they had extreme scores on the first test:
- Top 10% likely scored high partly because of real ability and partly because of luck, unusually good performance, easy questions for them, low stress that day, etc.
- Bottom 10% likely scored low partly because of weaker preparation and partly because of bad luck, distraction, anxiety, misunderstanding a few items, etc.

On the next test, those random factors are less likely to be as extreme in the same direction:
- Top scorers tend to come down a bit.
- Bottom scorers tend to come up a bit.

This happens even if:
- praise has no effect at all, and
- tutoring has no effect at all.

So the teacher is mistaking a statistical tendency for a causal effect.

Key idea:
Extreme observations tend to be followed by less extreme ones when there is any randomness in measurement or performance.

2) Design a study that separates regression to the mean from real effects

You need a randomized controlled design.

A good study:

Step 1: Give all students a baseline test.

Step 2: Identify:
- top 10%
- bottom 10%

Step 3: Randomly assign within each extreme group:
- Top group:
  - half receive praise
  - half do not receive praise, or receive neutral feedback
- Bottom group:
  - half receive tutoring
  - half do not receive tutoring, or receive a comparison intervention

Step 4: Give a second test of comparable difficulty.

Step 5: Compare outcomes within each extreme group:
- Among top scorers, did praised students decline less, the same, or more than unpraised students?
- Among bottom scorers, did tutored students improve more than untutored students?

Why this works:
- Both randomized subgroups start from similarly extreme scores.
- Both should experience similar regression to the mean.
- Any difference between treatment and control can be more credibly attributed to praise or tutoring.

Even better design features:
- Use...
```

### Grok 4.20

**Generation Time:** 4485ms
**Tokens:** 1053

```
**1. What's actually happening?**

This is a classic case of **regression to the mean** combined with selection on extremes.

- Student performance on any test = true ability + temporary factors (luck, sleep, mood, specific topics studied, test conditions, etc.).
- The top 10% are disproportionately students who had *both* high true ability *and* positive temporary luck.
- The bottom 10% are disproportionately students who had *both* lower true ability *and* negative temporary luck.

On the next test, the temporary factors regress toward their average (zero). Therefore:
- The top group will tend to score lower even if praise has *no effect at all*.
- The bottom group will tend to score higher even if tutoring has *no effect at all*.

The teacher is attributing the purely statistical regression effect to the interventions. This is the same error made in the famous "Israeli Air Force" example with pilot training (scolding for bad landings seemed to work; praising good landings seemed to hurt).

**2. Design a study that separates regression to the mean from real effects.**

Use a **randomized controlled trial with regression-to-the-mean controls**:

**Method:**
- Give Test 1 to a large group.
- Identify the top 10% and bottom 10% as usual.
- *Randomly assign* students *within* the top 10% to either "Praise" or "No Praise" (control).
- *Randomly assign* students *within* the bottom 10% to either "Tutoring" or "No Tutoring" (control).
- Give Test 2 to everyone.

**Analysis:**
- Compare Praise vs. No-Praise groups *among the originally top 10%*. Any difference beyond the expected regression is the causal effect of praise.
- Compare Tutoring vs. No-Tutoring groups *among the originally bottom 10%*. Any difference beyond the expected regression is the causal effect of tutoring.

You can also include a pure random sample (not selected on extremes) as an additional control to measure the baseline regression effect directly.

This is essentially what Daniel Kahneman suggested ...
```

### Claude Sonnet 4.6

**Generation Time:** 47658ms
**Tokens:** 2167

```
# Regression to the Mean: A Complete Analysis

## Part 1: What's Actually Happening

### The Core Mechanism

The teacher is observing **regression to the mean** — one of the most systematically misunderstood phenomena in human judgment — and constructing a causal narrative around a purely statistical artifact.

Here's what's actually happening mathematically:

**Any observed score = True ability + Measurement error + Situational noise**

When you select the *top 10%* on a given test, you are selecting people who had:
- High true ability, AND
- Unusually good luck/conditions that day

The second component is not stable. It will not repeat. On the next test, those students still have high true ability, but their situational noise regresses toward zero — so their scores **must fall on average**, regardless of what the teacher does.

The same logic inverts for bottom scorers: they had low true ability AND unusually bad luck. Their luck normalizes upward.

### Why the Teacher's Inference is Wrong

```
What the teacher sees:
Top scorers → praised → scores decline    ∴ praise hurts
Bottom scorers → tutored → scores improve  ∴ tutoring helps

What's actually true:
Top scorers → [anything] → scores decline    ∴ regression
Bottom scorers → [anything] → scores improve  ∴ regression
```

The intervention is **completely confounded** with the selection criterion. The teacher selected groups *because* they were at the extremes, and extreme measurements contain extreme error components that must regress.

### The Deeper Problem: Causal Attribution to Coincidence

The teacher has committed a specific chain of errors:

1. **Selection bias**: Groups defined by the very variable that will regress
2. **No counterfactual**: No comparison group received neither praise nor tutoring
3. **Confirmation asymmetry**: The narrative feels coherent because praise-then-decline and tutoring-then-improvement fit cultural intuitions
4. **Intervention timing confound**: Interventions were applied prec...
```

### MiMo-V2-Flash

**Generation Time:** 12704ms
**Tokens:** 1509

```
Here is an analysis of the statistical phenomenon at play, a design for a proper study, and real-world examples of this fallacy.

### (1) What’s actually happening? Regression to the Mean

The teacher is witnessing **regression to the mean**, a statistical phenomenon first identified by Sir Francis Galton. It occurs when an initial measurement is extreme, and a subsequent measurement is closer to the average.

Here is the breakdown of the mechanics:

*   **The Extremes:** The top 10% and bottom 10% represent statistical outliers. While some students may genuinely be that much better or worse than their peers, a portion of their extreme scores is likely due to **random chance** (luck, guessing, specific question topics that matched their exact knowledge gaps, fatigue, or testing conditions).
*   **The Natural Fluctuation:** On a second test, these random factors will likely not align in the same way. The lucky top scorer will likely get a slightly less lucky score (declining), and the unlucky bottom scorer will likely get a slightly less unlucky score (improving).
*   **The False Attribution:** The teacher incorrectly attributes the natural movement toward the average to the interventions (praise and tutoring). In reality, the top students would have likely declined slightly even without praise, and the bottom students would have improved slightly even without extra tutoring, simply because their first scores were statistical anomalies.

**Visualizing the error:**
Imagine a dartboard where the bullseye is the "average score." A player who hits the very outer edge (bottom 10%) on the first throw is likely to hit closer to the center on the second throw, not because they practiced, but because the first throw was an extreme outlier.

---

### (2) Designing a Study to Separate Regression from Real Effects

To determine if praise is actually counterproductive or if tutoring is actually effective, we need a **Randomized Controlled Trial (RCT)** that accounts for initial s...
```

### GPT-OSS-120B

**Generation Time:** 27866ms
**Tokens:** 2223

```
**1. What’s really happening?**  

| Observation | Teacher’s (incorrect) inference | Statistical reality |
|------------|--------------------------------|----------------------|
| Top‑10 % scores drop a little on the next test | “Praise makes them lazy / complacent.” | Those students were **extremely high** on the first test partly because of random “good luck” (easier questions, being well‑rested, a good mood, etc.). On a second test the random component is unlikely to be as favorable, so their scores **regress toward their true ability** – they look worse even though nothing harmful was done. |
| Bottom‑10 % scores improve a little on the next test | “Tutoring works.” | Those students were **extremely low** on the first test partly because of random “bad luck” (hard questions, fatigue, anxiety). On the second test the random component is likely to be less adverse, so their scores **regress upward** toward their true ability. Any real tutoring effect, if it exists, is mixed with this statistical pull. |

**Regression‑to‑the‑Mean (RTM)** is the tendency for extreme observations to be followed by measurements that are closer to the population average, simply because the extreme value contains a random error component. The teacher is mistaking this inevitable statistical “bounce‑back” for the causal impact of praise or tutoring.

---

**2. Study design that separates RTM from genuine effects**

The key is to **randomise** the interventions and include **proper control groups** so that the expected RTM is the same in all groups. Below is a concrete, step‑by‑step plan.

| Step | What to do | Why it helps |
|------|------------|--------------|
| **A. Baseline measurement** | Administer a **standardised, reliable test** to the whole class (or a large sample of classes). Record each student’s score. | Provides the initial distribution and identifies the extreme groups without yet applying any treatment. |
| **B. Random assignment** | **Within each extreme stratum** (top‑10...
```

### Gemini 2.5 Flash

**Generation Time:** 9376ms
**Tokens:** 1538

```
This is a classic example of **regression to the mean**. Let's break it down:

**(1) What's actually happening?**

Regression to the mean is the statistical phenomenon where, if a variable is extreme on its first measurement, it will tend to be closer to the average on its second measurement.

Here's how it applies to the teacher's scenario:

*   **Top 10% students:** These students likely had a combination of their true ability and some good luck (e.g., questions aligned with what they studied, feeling particularly sharp that day). On the next test, their "luck" component is less likely to be as high, so their scores will naturally tend to regress towards their average ability. The "praise" didn't make them worse; their unusually high previous score was just an outlier.
*   **Bottom 10% students:** Similarly, these students likely had a combination of their true ability and some bad luck (e.g., questions on topics they didn't study, feeling unwell). On the next test, their "bad luck" component is less likely to be as low, so their scores will naturally tend to regress towards their average ability. The "tutoring" might have helped, but a significant portion of their improvement would have happened anyway due to regression.

The teacher is committing the **regression fallacy** by attributing the change in scores solely to their interventions (praise and tutoring) without accounting for the natural tendency of extreme scores to move closer to the average.

**(2) Design a study that separates regression to the mean from real effects.**

To properly assess the impact of praise and tutoring, we need a controlled experiment that accounts for regression to the mean.

**Study Design:**

1.  **Baseline Test:** Administer the first test to all students.
2.  **Random Assignment (Key Step!):**
    *   **Identify Top 10%:** From the students who scored in the top 10%, randomly divide them into two groups:
        *   **Group A (Praise + Control):** Receive praise.
        *   *...
```

### MiniMax M2.5

**Generation Time:** 170519ms
**Tokens:** 1561

```
Excellent question. This is a classic and crucial demonstration of **regression to the mean**.

### (1) What's Actually Happening?

The teacher's conclusion is a classic example of confusing correlation with causation, but the core statistical phenomenon at play is **regression to the mean**.

*   **What it is:** Regression to the mean states that if you select a group based on an extreme outcome (like the top or bottom 10% on a test), that group's performance on a subsequent, independent test will, on average, move closer to the overall average (the mean). This happens because the first test score was a combination of **skill** (a stable, underlying ability) **and luck/random variation** (a one-time good or bad day, easy or hard questions for that person).
*   **What's happening in the story:**
    *   **Top 10%:** They likely got there partly due to exceptional luck on the first test. On the next test, even without any change in their true ability, their luck is likely to be average, so their scores decline. This decline is not because praise was "counterproductive."
    *   **Bottom 10%:** They likely got there partly due to exceptionally bad luck on the first test. On the next test, their luck is likely to improve, so their scores rise. This improvement is not because tutoring was "effective."

**In short:** The change observed is primarily a statistical artifact (regression to the mean), not a causal effect of the teacher's interventions. To prove causation, you need a control group.

---

### (2) Designing a Study to Separate the Effects

To properly test this, you need an **experimental design** with random assignment and a control group. Here is a simple, ethical design:

**Study Design: "The Praise & Tutoring Experiment"**

1.  **Population:** A large, representative group of students (e.g., all 500 students in a grade).
2.  **Initial Assessment:** Administer a well-designed, reliable test (Test A). Identify the top 10% and bottom 10% based on scores.
3.  *...
```

---

*Generated by The Multivac V5*
*https://themultivac.com*