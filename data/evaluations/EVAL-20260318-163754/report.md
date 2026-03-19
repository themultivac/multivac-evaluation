# Multivac Evaluation Report

**Evaluation ID:** EVAL-20260318-163754
**Timestamp:** 2026-03-18T16:37:54.681634
**Category:** Project MiniMax
**Model Pool:** 9 minimax-optimized models

## Question

During WWII, analysts studied bullet holes on returning bombers to decide where to add armor. They found most damage on the wings and fuselage, almost none on the engines. Their recommendation: armor the wings. Abraham Wald disagreed. (1) What was Wald's reasoning? (2) Give 5 modern examples of survivorship bias in business/tech. (3) 'We studied 100 successful startups and found they all did X.' Why is this analysis worthless without a control group?

---

## Rankings

| Rank | Model | Score | Min | Max | Std Dev |
|------|-------|-------|-----|-----|---------|
| 1 | GPT-5.4 | 9.73 | 9.00 | 10.00 | 0.38 |
| 2 | MiniMax M2 | 9.69 | 9.00 | 10.00 | 0.37 |
| 3 | MiniMax M2.7 | 9.67 | 8.45 | 10.00 | 0.58 |
| 4 | MiniMax M1 | 9.66 | 9.00 | 10.00 | 0.36 |
| 5 | Claude Sonnet 4.6 | 9.61 | 8.65 | 10.00 | 0.47 |
| 6 | MiniMax M2.5 | 9.40 | 8.25 | 10.00 | 0.60 |
| 7 | MiniMax M2.1 | 9.29 | 7.65 | 9.85 | 0.79 |
| 8 | MiniMax-01 | 8.83 | 8.25 | 9.60 | 0.47 |

---

## Meta Analysis

### Judge Strictness

| Rank | Judge | Avg Score Given |
|------|-------|-----------------|
| 1 | GPT-5.4 | 8.61 |
| 2 | MiniMax M1 | 9.33 |
| 3 | MiniMax M2.7 | 9.36 |
| 4 | Claude Sonnet 4.6 | 9.38 |
| 5 | MiniMax M2 | 9.66 |
| 6 | MiniMax M2.1 | 9.75 |
| 7 | MiniMax-01 | 9.88 |
| 8 | MiniMax M2.5 | 9.91 |

**Strictest Judge:** judge_gpt54
**Most Lenient Judge:** minimax_m25
**Total Judgments:** 72
**Valid Judgments:** 56

---

## Model Pool

Models selected for **Project MiniMax** evaluation:

1. **MiniMax M2.7** (openrouter)
2. **MiniMax M2.5** (openrouter)
3. **MiniMax M2.1** (openrouter)
4. **MiniMax M2** (openrouter)
5. **MiniMax M1** (openrouter)
6. **MiniMax-01** (openrouter)
7. **Claude Sonnet 4.6** (openrouter)
8. **GPT-5.4** (openrouter)
9. **Gemini 3.1 Pro** (openrouter)

---

## Model Responses

### MiniMax M2.7

**Generation Time:** 28239ms
**Tokens:** 1370

```
Excellent questions. Let's break this down.

### (1) Abraham Wald's Reasoning

Wald's genius was to recognize the critical flaw in the analysts' methodology: **they were only looking at the planes that *survived*.**

*   **The Analysts' Error:** They recommended armoring the wings and fuselage (where returning planes had the most bullet holes), reasoning they needed to reinforce these high-damage areas.
*   **Wald's Correction:** He pointed out that the planes they *couldn't* study were the ones that **didn't return**—the ones that were shot down. Their damage was the key to survival.
*   **The Reasoning:** The bullet holes they found on returning planes represented areas that could *withstand* damage (wings, fuselage). A plane hit in those areas might return. Therefore, the **absence of damage on the engines** in the surviving planes meant that **hits to the engines were catastrophic and led to loss of the plane.** The engines were the critical vulnerability.
*   **Conclusion:** Armor should be placed where there is *no* damage on returning planes—i.e., the engines. You should reinforce the areas that, if hit, would cause the plane to be lost.

---

### (2) Five Modern Examples of Survivorship Bias in Business/Tech

1.  **"Diligently Studied 10,000+ Unicorns to Find Their Secrets."**
    *   **Bias:** Only studying companies that became billion-dollar "unicorns," ignoring the millions of similar companies that did everything "right" but failed.
    *   **Reality:** Many failed companies had the same characteristics (e.g., similar business models, funding rounds, pivots) as the successes. The "secrets" found might be common but not sufficient.

2.  **"Look at all the successful actors who dropped out of college—school isn't needed for success!"**
    *   **Bias:** Only highlighting famous college-dropout CEOs (e.g., Bill Gates, Mark Zuckerberg) while ignoring the vastly larger number of dropouts who failed.
    *   **Reality:** Selection on the outcome (fame/success...
```

### MiniMax M2.5

**Generation Time:** 18658ms
**Tokens:** 870

```
**(1) Wald's Reasoning**  
Abraham Wald recognized that the analysts were making a critical error: they were only looking at the *surviving* bombers. The holes on returning planes showed where they could *afford* to be hit—because they came back despite that damage. The absence of bullet holes on the engines meant that hits there were **fatal**; such planes never returned to be analyzed. Therefore, Wald argued, the armor should be placed where the returning planes were *not* damaged—i.e., the engines and fuel system—to protect against the *non-survivable* hits.

---

**(2) Five Modern Examples of Survivorship Bias in Business/Tech**  
1. **"Why did our successful competitor pivot?"** – Analyzing only successful companies that pivoted, ignoring the many that pivoted and still failed.  
2. **"All successful founders have this trait."** – Studying only famous entrepreneurs (e.g., Bill Gates, Mark Zuckerberg) and overlooking the thousands with similar traits who failed.  
3. **"Our app's UI is like Instagram's, so we'll succeed."** – Modeling only on successful apps without accounting for the countless apps with similar designs that were ignored.  
4. **"Our startup culture is like Google's, so we'll innovate."** – Emulating practices of successful companies without considering the many companies with identical cultures that failed.  
5. **"Cryptocurrency made some people rich."** – Highlighting only the winners in crypto while ignoring the vast majority who lost money—a classic case of focusing on visible successes and ignoring hidden failures.

---

**(3) Why the Analysis is Worthless Without a Control Group**  
The statement "We studied 100 successful startups and found they all did X" suffers from survivorship bias because it examines only **survivors** (successful startups). Without a **control group** (e.g., startups that did *not* do X, or startups that tried X and failed), you cannot determine if X is actually correlated with success or if it's just a common cha...
```

### MiniMax M2.1

**Generation Time:** 77260ms
**Tokens:** 2188

```
# Survivorship Bias: Wald's Insight and Modern Applications

## 1. Wald's Reasoning: The Genius of Asking "What Are We Not Seeing?"

Abraham Wald's contribution to the bomber armor problem represents a masterclass in counterfactual thinking. While military analysts recommended armoring the wings and fuselage—the areas showing the most damage on returning aircraft—Wald recognized a fundamental flaw in their reasoning: **they were only looking at the planes that survived**.

Wald's crucial insight was to ask the question no one else was asking: *Where are the missing bullet holes?* The returning bombers showed extensive damage to wings and fuselage, but virtually no damage to the engines. The naive conclusion was to reinforce the damaged areas. Wald argued the exact opposite—armor the engines, and the areas showing no damage on surviving planes.

His reasoning rested on a simple but profound statistical principle: the sample was not random. The analysts were examining only aircraft that had survived their missions. Any plane hit in critical areas—particularly the engines—never made it back to be analyzed. The absence of engine damage on returning planes wasn't because engines were naturally bulletproof; it was because *damaged engines meant crashed planes*. The analysts were essentially studying the wrong population entirely.

This is the essence of survivorship bias: when you only analyze "survivors," you systematically miss the crucial information contained in the failures. Wald understood that the holes they *didn't* see were more important than the holes they did see. The missing data told the real story.

---

## 2. Five Modern Examples of Survivorship Bias in Business and Technology

### Example 1: The "Unicorn Formula" Fallacy

Business media frequently profiles successful startups and identifies common patterns among them: "We studied 50 billion-dollar companies and found they all had charismatic founders, moved fast, and embraced disruption." This analysis su...
```

### MiniMax M2

**Generation Time:** 30181ms
**Tokens:** 1336

```
Excellent questions. Let's break this down.

### (1) Abraham Wald's Reasoning

The analysts made a critical error by focusing on where the *returning* bombers were hit, rather than considering where the bombers that *didn't return* were hit.

Wald's core insight was: **The holes show where the plane *can* be hit and survive.** The missing holes show where the plane *must* be hit to be destroyed.

*   **The Data:** They saw many holes in wings/fuselage, few in engines.
*   **The Fallacy:** The initial recommendation was to armor the wings, as that seemed most damaged.
*   **Wald's Argument:** The wings and fuselage are non-critical areas. A bullet there might damage the plane but it can still fly home. The engines, however, showed almost *no* holes. Why? Because a bullet hitting an engine is much more likely to cause a catastrophic failure, leading to the plane being *lost* (not returning). Therefore, the returning sample is biased.
*   **The Conclusion:** Armor the **engines** (and other critical areas like the cockpit), not the wings. You should armor the areas with the *fewest* holes on the returning planes, because that's where hits are lethal.

This is a classic example of **survivorship bias**—focusing on the successful "survivors" (returning bombers) and drawing false conclusions about the population.

---

### (2) Five Modern Examples of Survivorship Bias in Business/Tech

1.  **"All successful startups have a founder with a beard/hustle/garage."** We celebrate the Bill Gateses and Mark Zuckerbergs, but we never study the millions of people with similar traits who started similar companies and failed. The "beard" is not the key to success.
2.  **"Our product went viral on social media."** Analysis focuses on viral successes but ignores the vast majority of products that also had similar features, content, or timing but failed to gain traction. The "viral" success is a survivor.
3.  **"E-commerce is easy; just look at Amazon's success."** This ignores the mass...
```

### MiniMax M1

**Generation Time:** 59078ms
**Tokens:** 1722

```
# Survivorship Bias: The WWII Bomber Problem and Its Modern Legacy

## 1. Wald's Reasoning

The key insight Wald provided was about **what data was missing**.

The analysts studied returning bombers and found:
- Many holes in wings and fuselage
- Almost no holes in engines

Their conclusion: *Armor the wings.*

Wald's counter-argument was brilliant in its simplicity:

> **The planes that returned are not a random sample—they're the survivors.**

The holes on returning planes show where a plane *can* get hit and still fly home. The absence of engine damage doesn't mean engines are well-protected—it means **planes hit in the engines never returned**. Those missing planes are the data point everyone ignored.

Wald's recommendation: **Armor the engines**—the very place the analysts wanted to leave exposed.

This is a foundational lesson in statistical reasoning: **The data you don't see often matters more than the data you do see.**

---

## 2. Five Modern Examples of Survivorship Bias in Business/Tech

| # | Example | The Hidden Data |
|---|---------|-----------------|
| 1 | **Studying "successful" founders** | We analyze Harvard-dropouts who became billionaires, ignoring thousands with identical backgrounds who failed. |
| 2 | **Looking at surviving companies in an industry** | "What made Company X succeed?" — Meanwhile, 50 competitors with similar strategies went bankrupt. |
| 3 | **Analyzing products that won** | We study iPhones and Nokias, but there's a graveyard of Palm Pilots and BlackBerrys we never examine. |
| 4 | **Reviewing retained customers only** | "Our customers love the product!" — Meanwhile, 40% churned and weren't surveyed. |
| 5 | **Backtesting trading strategies on surviving funds** | "This strategy works!" — Ignoring the 80% of funds that used it and closed. |

In every case, **the success stories are a filtered subset**, and the filter (survival) is often correlated with the outcome in ways that make the lessons misleading.

---

## 3. Why "All 1...
```

### MiniMax-01

**Generation Time:** 21904ms
**Tokens:** 1595

```
### (1) What was Wald's reasoning?

Wald's reasoning was based on the concept of **survivorship bias**. The analysts were only looking at the bullet holes on the bombers that **returned** from their missions. These bombers survived despite the damage, which meant that the areas with the most bullet holes (wings and fuselage) were actually the **least critical** for survival. The bombers that were hit in the engines likely did not return, and therefore, the absence of damage on the engines in the observed data was misleading.

Wald argued that the engines were the most vulnerable part of the aircraft because the bombers that were hit there did not make it back. Therefore, he recommended adding armor to the engines, not the wings or fuselage.

### (2) Give 5 modern examples of survivorship bias in business/tech:

1. **Tech Company Success Stories**: Many business books and articles focus on the success stories of tech giants like Apple, Google, and Amazon. However, these stories often ignore the countless failed companies that followed similar strategies but did not achieve the same success. This creates a survivorship bias, leading people to believe that these strategies are more successful than they actually are.

2. **Venture Capital Investment Patterns**: Venture capitalists often focus on the startups that have achieved high valuations or successful exits. This can lead to a bias towards certain types of companies or industries, ignoring the many startups that failed despite having similar characteristics.

3. **Stock Market Analysis**: Financial analysts sometimes look at the historical performance of stocks that are currently successful, ignoring the stocks that have been delisted or gone bankrupt. This can lead to an overestimation of the potential returns and an underestimation of the risks.

4. **University Rankings**: University rankings often focus on the top-performing institutions, ignoring the many universities that have failed to achieve similar levels...
```

### Claude Sonnet 4.6

**Generation Time:** 49987ms
**Tokens:** 2167

```
# Survivorship Bias: The Full Analysis

## Part 1: Wald's Reasoning

Wald recognized the analysts had made a **fundamental logical error** about their sample.

### The Core Insight

The data wasn't showing where planes *got hit*. It was showing where planes got hit **and still came back**.

The planes with engine damage weren't in the dataset - **they were at the bottom of the English Channel.**

### The Actual Inference

| Observation | Wrong Conclusion | Wald's Conclusion |
|-------------|-----------------|-------------------|
| Wings heavily damaged | Wings need armor | Wings can sustain damage and survive |
| Engines rarely damaged | Engines are safe | Engine hits are fatal - those planes never returned |

### The Precise Logic

The returning planes represented a **conditional sample**: P(data | survived), when the analysts needed to reason about P(survived | damage location).

The absence of engine damage in the data was *the most important signal in the dataset* - not evidence of safety, but evidence of **systematic elimination** of that outcome from the observable record.

**Recommendation: Armor the engines.** Which was correct.

### Why Smart People Got This Wrong

The error was seductive because:
- The data was real and large
- The pattern was clear and consistent
- The wrong conclusion felt intuitive
- Nobody asked "what data *can't* we see?"

The critical discipline Wald applied: **always characterize your sampling mechanism before interpreting your sample.**

---

## Part 2: Five Modern Examples of Survivorship Bias

### 1. The "Dropout Billionaire" Narrative in Tech

**The bias:** Gates, Zuckerberg, Dell, Ellison dropped out and became billionaires. Therefore dropping out signals entrepreneurial genius.

**What's missing:** The tens of thousands of dropouts who failed and returned to obscurity. We don't profile them. Universities don't invite them to speak.

**The actual data:** College graduates still dramatically outperform dropouts economically acro...
```

### GPT-5.4

**Generation Time:** 16941ms
**Tokens:** 839

```
1) **Wald’s reasoning**

The observed planes were the ones that **survived** and made it back. So the bullet holes showed where a bomber could be hit **and still survive**.

The lack of bullet holes on the engines did **not** mean engines were safe. It meant the opposite: planes hit in the engines likely **didn’t return**, so they were missing from the sample.

So Wald’s conclusion was:

- **Do not armor where the returning planes are full of holes**
- **Armor where returning planes are not hit much**, because hits there are probably fatal

This is the classic case of **survivorship bias**: drawing conclusions from the survivors while ignoring the non-survivors.

---

2) **Five modern examples of survivorship bias in business/tech**

### 1. Startup founder habits
“We analyzed unicorn founders and found they wake up at 5 a.m., work 100-hour weeks, and dropped out of college.”

Problem:
- Many failed founders did the same things
- Those traits may be **common among all founders**, not causes of success

### 2. “Follow successful companies’ culture”
A company copies Netflix/Amazon/Google-style culture because those firms succeeded with it.

Problem:
- Many firms with similar cultures failed
- The culture may be survivable only with other hidden advantages: timing, capital, talent density, market power

### 3. Venture capital pattern matching
Investors say, “The best founders are young, technical, and from top schools because many winners fit that profile.”

Problem:
- They may be seeing the traits of funded/successful founders, not the traits that truly predict success
- Count all the people with those traits who built nothing or failed

### 4. Product advice from breakout apps
“Every great consumer app launched with a minimalist MVP and no monetization, so that’s the best strategy.”

Problem:
- You’re looking at breakout winners only
- Plenty of dead apps also launched that way
- Without comparing against failures, you can’t know if that strategy helps

### 5. Remote ...
```

---

*Generated by The Multivac V5*
*https://themultivac.com*