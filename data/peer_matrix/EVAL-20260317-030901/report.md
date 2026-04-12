# Multivac Evaluation Report

**Evaluation ID:** EVAL-20260317-030901
**Timestamp:** 2026-03-17T03:09:01.551037
**Category:** Project Qwen
**Model Pool:** 8 qwen-optimized models

## Question

During WWII, analysts studied bullet holes on returning bombers to decide where to add armor. They found most damage on the wings and fuselage, almost none on the engines. Their recommendation: armor the wings. Abraham Wald disagreed. (1) What was Wald's reasoning? (2) Give 5 modern examples of survivorship bias in business/tech. (3) 'We studied 100 successful startups and found they all did X.' Why is this analysis worthless without a control group?

---

## Rankings

| Rank | Model | Score | Min | Max | Std Dev |
|------|-------|-------|-----|-----|---------|
| 1 | Qwen 3.5 397B-A17B | 9.95 | 9.80 | 10.00 | 0.10 |
| 2 | Qwen 3 32B | 9.90 | 9.80 | 10.00 | 0.12 |
| 3 | Qwen 3 Coder Next | 9.85 | 9.60 | 10.00 | 0.19 |
| 4 | Qwen 3.5 122B-A10B | 9.81 | 9.25 | 10.00 | 0.32 |
| 5 | Qwen 3 8B | 9.80 | 9.60 | 10.00 | 0.14 |
| 6 | Qwen 3.5 35B-A3B | 7.76 | 5.45 | 10.00 | 1.66 |
| 7 | Qwen 3.5 27B | 7.62 | 5.65 | 9.60 | 1.63 |
| 8 | Qwen 3.5 9B | 7.48 | 5.25 | 9.60 | 1.75 |

---

## Meta Analysis

### Judge Strictness

| Rank | Judge | Avg Score Given |
|------|-------|-----------------|
| 1 | Qwen 3.5 122B-A10B | 7.82 |
| 2 | Qwen 3.5 27B | 7.83 |
| 3 | Qwen 3.5 397B-A17B | 8.56 |
| 4 | Qwen 3 8B | 9.18 |
| 5 | Qwen 3 32B | 9.29 |
| 6 | Qwen 3.5 35B-A3B | 9.80 |
| 7 | Qwen 3 Coder Next | 9.89 |

**Strictest Judge:** qwen35_122b_a10b
**Most Lenient Judge:** qwen3_coder_next
**Total Judgments:** 64
**Valid Judgments:** 39

---

## Model Pool

Models selected for **Project Qwen** evaluation:

1. **Qwen 3.5 9B** (openrouter)
2. **Qwen 3 8B** (openrouter)
3. **Qwen 3 32B** (openrouter)
4. **Qwen 3 Coder Next** (openrouter)
5. **Qwen 3.5 35B-A3B** (openrouter)
6. **Qwen 3.5 27B** (openrouter)
7. **Qwen 3.5 122B-A10B** (openrouter)
8. **Qwen 3.5 397B-A17B** (openrouter)

---

## Model Responses

### Qwen 3.5 9B

**Generation Time:** 18038ms
**Tokens:** 2158

```
Here are the answers to your questions regarding survivorship bias and Abraham Wald's famous analysis.

### (1) What was Abraham Wald's reasoning?

Abraham Wald, a mathematician and statistician working for the Statistical Research Group, realized that the analysts were looking at the wrong data.

*   **The Flaw:** The analysts were looking at the bombers that **returned** to base. They saw bullet holes on the wings and fuselage and planned to armor those areas.
*   **Wald's Insight:** Wald asked, "Where are the planes that didn't make it back?" He realized that planes hit in the wings or fuselage often survived because those areas could sustain damage without killing the plane. However, planes hit in the **engines** or **cockpit** were the ones that didn't return.
*   **The Conclusion:** Therefore, you should armor the areas with **no** visible bullet holes. The absence of damage on the returning planes indicated that those were the critical zones where damage would be fatal. By armoring the wings, they would likely add unnecessary weight without saving the pilots, whereas armoring the engines saved the planes that actually mattered.

### (2) Give 5 modern examples of survivorship bias in business/tech.

1.  **The "Dropout" Narrative:** Silicon Valley culture often glorifies tech founders who dropped out of college (e.g., Steve Jobs, Bill Gates, Mark Zuckerberg). This ignores the millions of other students who dropped out of college and failed to build companies, or who struggled with unemployment. The narrative assumes dropping out is a prerequisite for success, rather than an outlier trait among the survivors.
2.  **Venture Capital Portfolios:** A VC firm will often announce a "10x return on investment" citing their one massive exit (e.g., a company like Uber or Airbnb). They rarely highlight the 99 other companies they invested in that failed or returned \$0. This skews investment decisions toward high-risk bets because the failures are invisible.
3.  **Stock Ma...
```

### Qwen 3 8B

**Generation Time:** 18259ms
**Tokens:** 1398

```
**1. Wald's Reasoning:**  
Abraham Wald argued that the data from the returning bombers only reflected the areas that could withstand damage (e.g., wings and fuselage), as planes with critical engine damage were less likely to survive. By focusing solely on the survivors, analysts overlooked the fact that the engines—where damage was less visible in the data—were actually the most vulnerable. Wald recommended adding armor to the engines, recognizing that the **survivorship bias** (only considering successful outcomes) skewed the analysis.  

---

**2. Modern Examples of Survivorship Bias in Business/Tech:**  
1. **Venture Capital:** Investors often study successful startups (e.g., Uber, Airbnb) and replicate their strategies, ignoring the countless failed ventures that tried similar approaches.  
2. **Tech "Success Stories":** Companies like Tesla or SpaceX are celebrated for their innovations, but the broader tech ecosystem includes many failed attempts that weren’t highlighted.  
3. **Influencer Culture:** People analyze the tactics of successful influencers (e.g., content strategies, follower growth) without accounting for the vast majority who fail to gain traction.  
4. **Business School Case Studies:** Courses often teach strategies from companies like Apple or Amazon, but these cases ignore the failures of similar approaches in different markets.  
5. **Dot-Com Bubble:** Post-bubble analyses focused on survivors (e.g., eBay, Amazon) while ignoring the thousands of failed startups, leading to flawed lessons about scalability and growth.  

---

**3. Why the Analysis is Worthless Without a Control Group:**  
Studying only successful startups (e.g., "they all did X") is flawed due to **survivorship bias**. Without a control group (startups that didn’t succeed), you cannot determine whether X is a cause of success or merely a coincidence. For example:  
- Startups that did X might have had other advantages (e.g., better funding, team quality) unrelated to X.  
- ...
```

### Qwen 3 32B

**Generation Time:** 28850ms
**Tokens:** 927

```
This is a classic case of **survivorship bias**, and the story of Abraham Wald during WWII is a powerful illustration of how critical it is to recognize hidden information when analyzing data.

---

### (1) **What was Wald's reasoning?**

Abraham Wald, a mathematician working for the U.S. government during World War II, looked at the bullet hole data on returning bombers and **questioned the assumption** that armor should be added where damage was most commonly seen. His key insight was:

> **"The planes that didn't return are not in the sample."**

In other words:
- The data only came from **bombers that survived** their missions.
- Planes with **bullet holes in the engines** were less likely to return.
- So, the **absence of damage on engines** in the returned planes actually indicated that **engine damage was fatal**.

Wald recommended that **armor be placed on the parts where no damage was observed**: the engines — precisely because those planes with engine damage did **not survive** to be studied.

This is now known as **Wald’s Paradox** or part of **operational research** thinking, emphasizing that we must consider **what is missing** from the data.

---

### (2) **5 Modern Examples of Survivorship Bias in Business/Tech**

**Survivorship bias** occurs when we focus only on successful cases and ignore failures, leading to flawed conclusions. Here are five modern examples:

1. **Startup Success Stories**
   - Many articles claim "successful startups all did X", but they ignore the thousands who tried the same thing and failed. This leads to misleading advice like “hire young” or “move fast and break things”.

2. **Investment Advice Based on High-Performing Stocks**
   - Recommendations like “invest in companies that went public in 2018” are often based on a few high-performing IPOs while ignoring many others that tanked or failed.

3. **CEO Advice from Tech Giants**
   - Books and talks by billionaire CEOs often suggest paths to success, but they represent rare ...
```

### Qwen 3 Coder Next

**Generation Time:** 7094ms
**Tokens:** 953

```
**(1) Wald’s reasoning:**  
Abraham Wald recognized **survivorship bias**: the data only included bombers that *returned*. The planes that were hit in critical areas—like the engines, cockpit, or fuel systems—*didn’t return*, so their damage patterns were missing from the dataset. The *absence* of holes on engines in the returning planes likely meant engines *were* being hit—and those hits were fatal. Therefore, Wald argued to **armor the areas with *no* observed damage** (e.g., engines), because those were the zones where hits caused planes to be lost, not return. His insight was to model the *missing data* (the downed aircraft) and protect the *vulnerable* (not the *already-hit-and-surviving*) parts.

---

**(2) Five modern examples of survivorship bias in business/tech:**

1. **“Startup Success Stories” Books & Media**  
   Books like *The Lean Startup* or media profiles (e.g., Airbnb, Dropbox) highlight founders who succeeded—ignoring the >90% of startups that failed despite similar tactics (e.g., MVPs, rapid iteration). Readers overgeneralize strategies from survivors, not the full population.

2. **Tech “Best Practices” from Industry Leaders**  
   Companies like Google or Netflix publish engineering practices (e.g., microservices, chaos engineering). Startups adopt them without considering that these practices were only viable *after* massive scale and failure—early-stage startups lack the resources to sustain the same trade-offs.

3. **VC Portfolio Analysis**  
   VCs often cite “the top 10 exits” to justify strategy, ignoring the dozens of failed investments. For example, Sequoia’s “Google, WhatsApp, Stripe” narrative obscures the 50+ duds in the same fund—leading others to overvalue “founder charisma” or “first-mover advantage” as universal predictors.

4. **Influencer & Creator Advice**  
   “How I made $1M on TikTok in 3 months” case studies omit the 10,000 creators who quit after months of no growth. Learners replicate tactics (e.g., viral trends, high ...
```

### Qwen 3.5 35B-A3B

**Generation Time:** 26601ms
**Tokens:** 2158

```
Here is the breakdown of Abraham Wald's insight, modern examples of survivorship bias, and an analysis of the startup fallacy.

### 1. Wald's Reasoning: The Logic of the Missing Data
Abraham Wald's reasoning was based on the fundamental principle of **Survivorship Bias**: *The data you have is a biased subset of the total population because it only represents the survivors.*

*   **The Data:** The bullet holes on the returning bombers represented planes that *could* take damage and still survive.
*   **The Inference:** If the engines had bullet holes on the returning planes, it would imply that planes could take engine damage and fly home. Since there were almost no bullet holes on the engines in the returning fleet, Wald deduced that planes hit in the engine did **not** return to the base.
*   **The Conclusion:** The areas with **no** bullet holes were the critical areas. If a plane was hit there, it was shot down and lost from the dataset. Therefore, armor should be added to the engines, the cockpit, and the fuel tanks—the areas that were statistically "missing" damage because the planes that took damage there didn't make it back.

### 2. Five Modern Examples of Survivorship Bias in Business/Tech

1.  **The "Guru" Founder Myth:**
    *   **The Bias:** We study the daily habits of successful founders (e.g., Steve Jobs, Elon Musk, Mark Zuckerberg) and assume these habits (e.g., waking up at 4 AM, extreme frugality, sleep deprivation) caused their success.
    *   **The Reality:** Thousands of failed founders also woke up at 4 AM and worked 80-hour weeks. Because the data only looks at the "survivors" (the successful companies), we attribute their success to habits that were actually common among everyone, successful or not.

2.  **MBA and Bootcamp Marketing:**
    *   **The Bias:** Schools often advertise the high salaries of their *employed* graduates.
    *   **The Reality:** They often omit the drop-out rate or the graduates who could not find jobs in the field. ...
```

### Qwen 3.5 27B

**Generation Time:** 24546ms
**Tokens:** 2158

```
Here are the answers to your questions regarding Abraham Wald and survivorship bias.

### 1. Wald's Reasoning
Abraham Wald’s reasoning was based on **missing data**.

The analysts were looking at the "survivors"—the planes that returned. They reasoned that because the wings had the most holes, that was where the planes were most vulnerable. Wald pointed out that the data was skewed: **The planes that were hit in the engines did not return.**

If a plane returned with bullet holes in the wings but no holes in the engine, it meant the engine was structurally sound enough to survive the flight home. However, the planes that were hit in the engine were likely shot down immediately and never made it back to the hangar to be analyzed. Therefore, Wald recommended reinforcing the areas with **no** bullet holes (the engines), because damage there was fatal.

### 2. Five Modern Examples of Survivorship Bias in Business/Tech

1.  **The "Dropout" Myth:** Tech leaders often point to Bill Gates, Mark Zuckerberg, and Steve Jobs to argue that college is unnecessary. This ignores the thousands of dropouts who did *not* found billion-dollar companies. You are studying the survivors of the "dropout" group, not the failure rate of dropouts.
2.  **Venture Capital "Playbooks":** Investors study the strategies of "Unicorns" (startups valued over $1B) to replicate their success. They often ignore the thousands of startups that followed similar strategies but failed. They attribute success to the strategy, not realizing the strategy is actually common among the failures.
3.  **Hiring from "Elite" Companies:** Recruiters often prefer candidates from Google, Amazon, or Meta, assuming they were "the best" because of their past employers. This ignores the talented people who worked at those companies but were fired or left for better opportunities, and it ignores the high performers who came from non-elite backgrounds.
4.  **Open Source "Starred" Repos:** Developers often choose to use a GitHub...
```

### Qwen 3.5 122B-A10B

**Generation Time:** 22015ms
**Tokens:** 2309

```
### (1) Wald’s Reasoning

Abraham Wald recognized that the data provided by the military was **incomplete**. The analysts were only looking at planes that had *survived* to return to base.

*   **The Visible Data:** The bullet holes on the returning planes represented areas that could sustain damage and still allow the plane to fly.
*   **The Missing Data:** The planes that were shot down never returned. Therefore, their bullet hole patterns were absent from the study.

Wald reasoned that the areas with **no damage** on the returning planes (specifically the engines) were actually the most critical. If a plane was hit in the engine, it likely didn't return to be counted in the study. Therefore, armor should be placed where the damage *wasn't* found, not where it was.

**The Lesson:** You must account for the "invisible" data (the failures) to understand the true cause of survival.

***

### (2) 5 Modern Examples of Survivorship Bias in Business/Tech

**1. The "Dropout Billionaire" Narrative**
*   **Observation:** Steve Jobs, Bill Gates, and Mark Zuckerberg dropped out of college and became successful.
*   **The Bias:** We ignore the thousands of dropouts who struggled, failed, or ended up in low-wage jobs.
*   **The Reality:** Dropping out is not a strategy for success; it is a risk taken by a few. The "control group" of failed dropouts is invisible, leading people to underestimate the value of education.

**2. Product Feature Adoption Based on Power Users**
*   **Observation:** A SaaS company adds complex features because their top 5% of power users request them.
*   **The Bias:** They ignore the 50% of users who churned because the product was too complicated or the features weren't relevant to them.
*   **The Reality:** By optimizing for the survivors (loyal users), they alienate new or average users, leading to stagnation in growth.

**3. App Store Ratings**
*   **Observation:** An app has a 4.8-star rating.
*   **The Bias:** Only users who are extremely satisfi...
```

### Qwen 3.5 397B-A17B

**Generation Time:** 39438ms
**Tokens:** 2313

```
### 1. Abraham Wald's Reasoning

Wald's insight was that the data was **truncated**. The analysts were only looking at the planes that *survived* the mission to return home.

*   **The Visible Data:** The bullet holes on the returning planes represented areas where a bomber could sustain damage and *still fly*.
*   **The Invisible Data:** The planes that were hit in the engines (and other areas with no holes) did not return. They were shot down.

Therefore, Wald recommended armoring the places where there were **no** bullet holes (the engines and cockpit). He reasoned that damage in those areas was fatal, which was why no planes with damage there were present in the sample. The military needed to protect the vulnerabilities that prevented survival, not the areas that proved survivable.

***

### 2. Five Modern Examples of Survivorship Bias in Business & Tech

1.  **The "College Dropout" Myth:**
    *   **Bias:** Aspiring entrepreneurs often cite Bill Gates, Steve Jobs, and Mark Zuckerberg as proof that dropping out of college leads to tech success.
    *   **Reality:** This ignores the vast "graveyard" of dropouts who failed and never made headlines. Statistically, college graduates generally have higher lifetime earnings and startup success rates than non-graduates. The survivors are visible; the failures are invisible.

2.  **Mutual Fund Performance Tracking:**
    *   **Bias:** Investors analyze the 10-year performance of currently existing mutual funds to determine average market returns.
    *   **Reality:** Funds that perform poorly are often liquidated or merged into successful funds, disappearing from the dataset. Analyzing only the surviving funds inflates the perceived average return of the asset class because the "losers" have been deleted from the record.

3.  **Customer Feature Requests:**
    *   **Bias:** Product managers prioritize features requested by their most active, vocal users.
    *   **Reality:** This ignores the silent majority who churned ...
```

---

*Generated by The Multivac V5*
*https://themultivac.com*