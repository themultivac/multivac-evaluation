# Multivac Evaluation Report

**Evaluation ID:** EVAL-20260402-182524
**Timestamp:** 2026-04-02T18:25:24.136072
**Category:** Reasoning & Logic
**Model Pool:** 10 reasoning-optimized models

## Question

During WWII, analysts studied bullet holes on returning bombers to decide where to add armor. They found most damage on the wings and fuselage, almost none on the engines. Their recommendation: armor the wings. Abraham Wald disagreed. (1) What was Wald's reasoning? (2) Give 5 modern examples of survivorship bias in business/tech. (3) 'We studied 100 successful startups and found they all did X.' Why is this analysis worthless without a control group?

---

## Rankings

| Rank | Model | Score | Min | Max | Std Dev |
|------|-------|-------|-----|-----|---------|
| 1 | Claude Opus 4.6 | 9.65 | 8.65 | 10.00 | 0.54 |
| 2 | GPT-OSS-120B | 9.58 | 9.00 | 9.80 | 0.27 |
| 3 | Claude Sonnet 4.6 | 9.54 | 8.65 | 10.00 | 0.52 |
| 4 | Grok 4.20 | 9.47 | 8.65 | 10.00 | 0.47 |
| 5 | GPT-5.4 | 9.44 | 8.25 | 10.00 | 0.54 |
| 6 | MiniMax M2.5 | 9.44 | 8.25 | 9.85 | 0.56 |
| 7 | Gemini 2.5 Flash | 9.41 | 8.65 | 10.00 | 0.52 |
| 8 | MiMo-V2-Flash | 9.26 | 8.60 | 10.00 | 0.58 |
| 9 | DeepSeek V3 | 9.07 | 8.25 | 9.80 | 0.45 |
| 10 | Gemini 3.1 Pro | 9.02 | 8.45 | 10.00 | 0.51 |

---

## Meta Analysis

### Judge Strictness

| Rank | Judge | Avg Score Given |
|------|-------|-----------------|
| 1 | GPT-OSS-120B | 8.52 |
| 2 | MiniMax M2.5 | 8.99 |
| 3 | Grok 4.20 | 9.09 |
| 4 | GPT-5.4 | 9.39 |
| 5 | Claude Sonnet 4.6 | 9.39 |
| 6 | Claude Opus 4.6 | 9.53 |
| 7 | DeepSeek V3 | 9.59 |
| 8 | MiMo-V2-Flash | 9.67 |
| 9 | Gemini 2.5 Flash | 9.84 |
| 10 | Gemini 3.1 Pro | 9.89 |

**Strictest Judge:** gpt_oss_120b
**Most Lenient Judge:** gemini_31_pro
**Total Judgments:** 100
**Valid Judgments:** 89

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

**Generation Time:** 20528ms
**Tokens:** 2144

```
Here are the answers to your three questions, breaking down the mechanics of survivorship bias from WWII to modern business.

### 1. Abraham Wald’s Reasoning
Abraham Wald, a statistician working for the Statistical Research Group (SRG) during WWII, realized the military was falling victim to what is now called **survivorship bias**. 

The military was only looking at the planes that *survived* the missions. Wald pointed out a crucial flaw in their logic: the bullet holes on the returning bombers didn't show where the planes were most vulnerable; **they showed where a plane could take a hit and still survive to fly home.**

Wald reasoned that the planes were likely getting hit relatively evenly across their entire bodies. The reason returning planes had no bullet holes in the engines was that **planes shot in the engines crashed and did not return.** Therefore, Wald recommended putting armor exactly where there were *no* bullet holes on the surviving planes—the engines and cockpit—because those were the fatal strike zones. 

***

### 2. Five Modern Examples of Survivorship Bias in Business/Tech

**1. The "College Dropout Tech Billionaire" Myth**
*   **The Bias:** Business media loves to highlight Steve Jobs, Bill Gates, and Mark Zuckerberg to push the narrative that dropping out of college to pursue an idea is a hallmark of visionary success.
*   **The Reality:** We don't see the thousands of tech founders who dropped out, failed, and ended up with no company, no degree, and massive debt. Statistically, the vast majority of successful tech founders have college degrees.

**2. Customer Feedback and Feature Development**
*   **The Bias:** A SaaS company pushes a major UI update and surveys its active users. The feedback is mostly positive, so the product team declares the update a massive success.
*   **The Reality:** They only surveyed the *survivors*—the users who stayed. They completely missed the thousands of users who hated the update so much that they canceled th...
```

### DeepSeek V3

**Generation Time:** 12072ms
**Tokens:** 550

```
### (1) Wald's Reasoning  
Abraham Wald realized that the bullet holes showed where planes could be hit **and still survive**—the engines were likely critical, so planes hit there didn't return. Thus, armor should go where the returning planes *weren’t* hit (e.g., engines), not where they were. This is a classic example of **survivorship bias**: focusing only on observed "survivors" while ignoring unseen failures.  

---

### (2) Modern Examples of Survivorship Bias  
1. **Startup Advice**: "All successful founders dropped out of college (e.g., Zuckerberg, Gates)."  
   - *Bias*: Ignores the thousands who dropped out and failed.  

2. **Stock Picking**: "This fund manager beat the market 5 years in a row!"  
   - *Bias*: Ignores the hundreds of failed funds that didn’t survive.  

3. **Tech Products**: "Viral apps like TikTok grew via word-of-mouth!"  
   - *Bias*: Ignores apps with similar strategies that flopped.  

4. **Entrepreneurship**: "Self-made billionaires worked 100-hour weeks!"  
   - *Bias*: Ignores those who worked just as hard but didn’t succeed.  

5. **A/B Testing**: "Our winning ad had bold headlines!"  
   - *Bias*: Ignores other bold headlines that performed poorly (only winners are analyzed).  

---

### (3) Why the Startup Analysis is Worthless  
The study only looks at successes ("survivors") and ignores failed startups that may have also done **X**. Without comparing failures, you can’t determine if **X** actually causes success or is just common to all startups (e.g., "had a website"). A control group (failures) might reveal that **X** is irrelevant or even harmful.  

**Example**: If all successful startups drank coffee, but *failed* ones also drank coffee, coffee isn’t a success factor—it’s just noise. Survivorship bias conflates correlation with causation.
```

### Claude Opus 4.6

**Generation Time:** 269766ms
**Tokens:** 1558

```
# Abraham Wald and Survivorship Bias

## 1. Wald's Reasoning

The military was making a critical logical error: **they were only examining planes that survived**.

Wald's insight was elegantly simple but profound:

- The bullet holes on returning bombers showed where a plane **could be hit and still fly home**
- The engines showed almost no damage — not because engines weren't being hit, but because **planes hit in the engines weren't coming back at all**
- The damage pattern on survivors was essentially a **negative image** of the truly fatal vulnerabilities
- His recommendation: **armor the engines**, precisely the areas showing *no* damage on returning aircraft

The missing data — the destroyed bombers lying in fields and oceans — held the real answer. The military was studying the **survivors** and drawing conclusions about the **entire population**, which is the textbook definition of survivorship bias.

---

## 2. Five Modern Examples in Business/Tech

### Example 1: "Learn from Successful Founders"
Business media obsessively profiles founders who dropped out of college and succeeded — Gates, Zuckerberg, Dell. This creates a narrative that dropping out is a viable strategy. **The thousands who dropped out and failed** are invisible because nobody interviews them. The dropout strategy likely has a catastrophic failure rate that the survivor-focused narrative completely obscures.

### Example 2: App Store Success Stories
Apple and Google showcase apps that went from garage projects to millions in revenue. Aspiring developers see these and conclude the market is full of opportunity. **The 99%+ of apps that generate almost no revenue and are quietly abandoned** never appear in any keynote. Platforms have an incentive to amplify survivors because it attracts more developers to their ecosystem.

### Example 3: "Our Users Love the Product"
A company surveys its current active users and finds high satisfaction scores, concluding the product is excellent. **The users w...
```

### GPT-5.4

**Generation Time:** 14132ms
**Tokens:** 707

```
1) Wald’s reasoning

Wald said the analysts were looking only at planes that survived.

So the bullet holes on returning bombers showed where a plane could be hit and still make it back. The missing damage mattered more: if returning planes rarely had engine hits, that suggested planes hit in the engines usually did not return at all.

Therefore, you should armor the places with little or no observed damage on surviving planes, especially the engines, because those were the fatal-hit zones.

In short:
- Observed damage = survivable damage
- Unobserved damage = likely fatal damage
- So armor the areas where surviving planes are not hit

2) Five modern examples of survivorship bias in business/tech

1. Studying only successful startups
“Successful startups pivoted three times, so pivoting causes success.”
Problem: you’re ignoring the many startups that also pivoted repeatedly and failed.

2. Copying famous founder habits
“Top founders wake up at 4 a.m., so that must help build billion-dollar companies.”
Problem: many unsuccessful founders have the same habits. You’re only seeing the winners.

3. Venture capital performance
People notice funds that backed unicorns and conclude their strategy is superior.
Problem: many funds used similar strategies but had poor outcomes and disappeared quietly.

4. Product advice from big tech companies
“Company X removed meetings / went fully remote / adopted microservices and succeeded.”
Problem: large successful firms can survive bad decisions. Their visible practices may not be what caused success.

5. App store or creator economy success stories
“Top YouTubers/newsletters/apps post every day, so daily posting is the key.”
Problem: thousands of others also post daily and get no traction. You only hear from the winners.

3) Why “We studied 100 successful startups and found they all did X” is worthless without a control group

Because you can’t tell whether X is:
- a cause of success,
- merely common among all startups,
- or even harm...
```

### Grok 4.20

**Generation Time:** 3693ms
**Tokens:** 839

```
**1. Abraham Wald's reasoning:**

Wald realized the analysts were only looking at the planes that *returned*. The planes that got hit in the engines never made it back—they were shot down. Therefore, the areas with the *least* bullet holes on the surviving planes (the engines) were actually the *most* critical. Those were the vulnerable spots where hits were fatal.

This is the classic survivorship bias: you're only studying the survivors, so you miss the data from the failures that matter most. Wald recommended putting armor where the returning planes had *few* holes (engines), not where they had many (wings/fuselage).

**2. Five modern examples of survivorship bias in business/tech:**

- **Startup "success formula" books/articles**: Analyzing only successful companies (e.g., "We studied 100 unicorns and they all moved fast/broke things/used OKRs/grew via viral loops") and concluding those traits caused success. Ignores the thousands of failed companies that did the exact same things.

- **"What I learned from interviewing 50 successful founders"** content: These pieces rarely interview founders who did the same things but went bankrupt. The advice becomes heavily distorted.

- **Mutual fund / hedge fund performance marketing**: Funds advertise their strong past performance, but the ones that performed terribly often shut down or are merged away. The surviving funds make active management look better than it is.

- **"Best practices" from successful tech companies**: "Netflix did X, Google did Y, Amazon did Z—therefore you should too." Ignores that hundreds of other companies tried the same practices and failed, or that correlation with success ≠ causation.

- **App Store / Play Store "growth hacking" advice**: People who write "How I grew my app to 10M users" only represent the winners. The vast majority of apps that used the exact same tactics got <1,000 downloads and died quietly.

**3. Why "We studied 100 successful startups and found they all did X" is worthle...
```

### Claude Sonnet 4.6

**Generation Time:** 52355ms
**Tokens:** 2167

```
# Survivorship Bias: The Wald Problem and Beyond

## Part 1: Wald's Reasoning

Wald recognized a **fundamental sampling error** that the analysts missed entirely.

The data wasn't showing where planes got hit. It was showing **where planes could get hit and still return.**

His actual logic:

- The sample was **conditioned on survival** - only planes that made it back were studied
- Engines with almost no bullet holes didn't mean engines weren't being targeted
- It meant planes hit in the engines **didn't come back** - they were at the bottom of the English Channel
- The absence of damage was therefore the **most important signal in the data**
- Wings could absorb damage and still function; engines apparently could not

**The counterintuitive conclusion:** Armor where you see *no* damage, because that's where damage is fatal.

This required recognizing that the **missing data was systematically missing** - not randomly missing. Planes weren't randomly failing to return. They were failing to return *because of specific damage patterns* that were therefore invisible in the dataset.

The deeper insight Wald formalized: you must always ask **"what would my dataset look like if my hypothesis were wrong?"** The analysts never asked what the data would look like if engines were the critical vulnerability. It would look exactly like what they were seeing.

---

## Part 2: Five Modern Examples of Survivorship Bias in Business/Tech

### 1. The "Dropout Billionaire" Narrative
**What we see:** Gates, Zuckerberg, Dell, Ellison - brilliant dropouts who built empires.

**What we ignore:** The hundreds of thousands of people who dropped out of elite universities to pursue startups and are now working retail. 

**The damage this causes:** Real people make genuinely catastrophic life decisions based on a sample of maybe 12 famous cases selected from a population of millions. The selection criterion for the famous cases wasn't "dropped out" - it was "dropped out AND succeeded despite ...
```

### MiMo-V2-Flash

**Generation Time:** 12419ms
**Tokens:** 1557

```
Here is the breakdown of the Abraham Wald story, modern examples of survivorship bias, and the statistical explanation regarding startup analysis.

### (1) Abraham Wald’s Reasoning

Abraham Wald, a mathematician and economist, pointed out a critical flaw in the analysts' logic: **they were only analyzing the planes that survived.**

Wald reasoned that the bullet holes found on the wings and fuselage were actually proof that those areas could sustain damage and the plane could still return home. The military did not need to reinforce those areas because the planes were already proving they could survive hits there.

**The critical missing data was the location of bullet holes on the planes that were shot down.** Since no planes returned with engine damage, Wald deduced that hits to the engines were likely fatal. Therefore, the armor should be added to the engines (where there was no visible damage on the returning planes), not the wings.

**The Takeaway:** You must analyze the missing data (the planes that didn't return) to see where the "lethal" damage was occurring.

***

### (2) 5 Modern Examples of Survivorship Bias in Business/Tech

Survivorship bias occurs when we focus on the survivors (or successes) of a process and inadvertently ignore the failures (non-survivors) because they are less visible.

**1. "Dropout Billionaires" (Tech & Education)**
*   **The Observation:** People often cite Bill Gates, Mark Zuckerberg, and Steve Jobs as proof that dropping out of college is a path to wealth. They point to these highly visible "survivors" of the dropout path.
*   **The Missing Data:** We do not hear about the millions of dropouts who did not build a billion-dollar company and instead struggle with debt and lower lifetime earnings. The success of a few outliers does not prove the strategy is statistically sound for the average person.

**2. "Best Practices" from Fortune 500 Companies**
*   **The Observation:** Business schools and consultants often study current Fo...
```

### GPT-OSS-120B

**Generation Time:** 48219ms
**Tokens:** 1806

```
## 1️⃣  Abraham Wald’s “missing‐data” insight  

| What the analysts saw | What Wald saw instead |
|-----------------------|-----------------------|
| **Most bullet holes were on the wings and fuselage.**  <br>→ “Re‑armor the places that get hit most.” | **The planes they were looking at were *the survivors*.**  <br>→ The aircraft that were **hit in the wings/fuselage and still came back** proved those areas could tolerate damage.  <br>→ The **absence of bullet holes on the engines** meant that **any aircraft hit there never made it back** – otherwise we would see damage there too. |
| Recommendation: add armor to the wings. | **Recommendation: reinforce the *engine* (and any other “missing‑hole” zones).** |

Wald’s reasoning in a nutshell:

1. **Sample bias** – the data set consists only of aircraft that survived the mission.  
2. **Missing‑data inference** – the parts that show *no* damage are the *critical* parts; a hit there is fatal, so those aircraft are absent from the data.  
3. **Optimal allocation** – armor should be placed where a hit would most likely cause loss, not where hits are most frequently observed among survivors.

---

## 2️⃣  Five modern, concrete examples of survivorship bias in business & technology  

| # | Situation (what we *see*) | Why it’s survivorship bias | What’s being ignored |
|---|---------------------------|----------------------------|----------------------|
| **1** | **Unicorn startup case studies** – “These 20 companies all raised >$1 bn, they all built a marketplace, so you should do the same.” | Only the *winners* are profiled. | Hundreds (or thousands) of marketplace‑oriented startups that raised money, failed, or never reached unicorn status. |
| **2** | **Tech‑stock “must‑buy” lists** – “These 10 dot‑com survivors turned $10 k into $1 M, buy similar names.” | The list is built from the handful of companies that survived the 2000 crash. | The 90 %+ of dot‑coms that went bust (many with similar business models, valuation mu...
```

### Gemini 2.5 Flash

**Generation Time:** 9602ms
**Tokens:** 1273

```
Let's break down each part of your question.

## (1) What was Wald's reasoning?

Abraham Wald's reasoning was a brilliant application of **survivorship bias**. He realized that the bombers returning with bullet holes *were the ones that survived*. The areas with no bullet holes, like the engines, were precisely the areas where damage was **catastrophic**. If a plane was hit in the engine, it likely didn't make it back.

Therefore, Wald recommended **adding armor to the areas that showed *no* damage on the returning planes, especially the engines.** These were the critical vulnerabilities that, if hit, led to the plane being shot down. The wings and fuselage, while showing damage, were clearly robust enough to sustain hits and still return.

In essence, Wald understood that what they were observing was a biased sample – only the survivors. He inferred the characteristics of the *non-survivors* from this biased data.

## (2) Give 5 modern examples of survivorship bias in business/tech.

Here are 5 modern examples of survivorship bias in business/tech:

1.  **Startup Success Stories/Unicorns:** We constantly hear about the Facebooks, Googles, and Apples – the companies that made it big. This leads to the misconception that success is common or that following their specific path (e.g., dropping out of college, working 100-hour weeks, pivoting multiple times) is a formula for success. We rarely hear about the thousands of startups that failed despite similar efforts, making it seem like the survivors are the norm, not the exception.

2.  **"Best Practices" from Highly Successful Companies:** Companies often adopt "best practices" from industry leaders (e.g., Google's open office plan, Apple's minimalist design philosophy, Amazon's customer obsession). The assumption is that these practices *caused* their success. However, many other companies might have implemented similar practices and failed, or the successful companies might have succeeded *despite* these practices, o...
```

### MiniMax M2.5

**Generation Time:** 8221ms
**Tokens:** 1133

```
Excellent questions. Let's break this down.

### (1) Wald's Reasoning

The analysts were committing what is now called **survivorship bias**. They looked at the *returning* bombers and saw bullet holes on the wings and fuselage, so they reasoned that was where armor was needed.

**Wald's crucial insight was to look at the *missing* data: the bombers that *didn't* return.** He realized:
*   The bullet holes they saw were where a plane **could be hit and still survive**.
*   The engines had *no* holes because **planes hit in the engines were knocked out of the sky and didn't return** to be analyzed.

His recommendation was to armor the **engines and cockpit**—the "empty" spaces on the returning planes—because that's where damage was *not* seen but was *fatal*. He was analyzing the **vulnerability** of the aircraft by looking at what caused it to *fail* (not return), rather than just where it could *survive* damage.

---

### (2) Five Modern Examples of Survivorship Bias in Business/Tech

1.  **Studying Only "Unicorns":** Analyzing what made companies like Airbnb, Uber, or Stripe successful (e.g., "they ignored revenue to grow users") and recommending that strategy to all startups. This ignores the thousands of similar companies that did the same thing and *failed*.

2.  **"Pivot" Narratives:** Celebrating companies that "pivoted" from a failed idea to a successful one (e.g., Slack from a gaming company). This overlooks the many companies that pivoted and still failed, making the pivot seem like a magic bullet.

3.  **Successful Founder Advice:** Compiling a book of advice from successful CEOs (e.g., "work less," "hire slowly"). This ignores the strategies of the vast majority of CEOs who followed similar advice but whose companies failed.

4.  **Tech Tool Success Stories:** Claiming that a specific methodology (e.g., Agile, Six Sigma) or tool (e.g., a particular CRM or programming language) leads to success by only studying companies that used it and succeeded. It fai...
```

---

*Generated by The Multivac V5*
*https://themultivac.com*