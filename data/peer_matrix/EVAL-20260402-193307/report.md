# Multivac Evaluation Report

**Evaluation ID:** EVAL-20260402-193307
**Timestamp:** 2026-04-02T19:33:07.184798
**Category:** Analysis & Research
**Model Pool:** 10 analysis-optimized models

## Question

A mobile app shows: DAU 100K (up 50%), WAU 200K (up 20%), MAU 500K (up 10%), D1 retention 40%, D7 retention 15%, D30 retention 5%, Session length 8min (down 20%), Sessions/day 2.1 (up 30%). The PM says 'we're growing fast.' (1) What story does this data actually tell? (2) What's concerning about the DAU/MAU ratio? (3) Why might session length decrease as sessions increase? (4) What one metric would you focus on and why?

---

## Rankings

| Rank | Model | Score | Min | Max | Std Dev |
|------|-------|-------|-----|-----|---------|
| 1 | Claude Sonnet 4.6 | 9.43 | 8.85 | 10.00 | 0.44 |
| 2 | Claude Opus 4.6 | 9.18 | 8.20 | 10.00 | 0.63 |
| 3 | Grok 4.20 | 9.13 | 8.65 | 9.80 | 0.39 |
| 4 | GPT-5.4 | 9.07 | 8.45 | 9.80 | 0.46 |
| 5 | GPT-OSS-120B | 9.04 | 7.95 | 10.00 | 0.60 |
| 6 | MiniMax M2.5 | 8.99 | 8.45 | 9.80 | 0.40 |
| 7 | Gemini 3 Flash Preview | 8.93 | 8.25 | 9.80 | 0.47 |
| 8 | DeepSeek V3 | 8.87 | 8.00 | 9.80 | 0.62 |
| 9 | MiMo-V2-Flash | 8.70 | 6.25 | 9.80 | 0.98 |
| 10 | Gemini 3.1 Pro | 7.72 | 6.30 | 8.85 | 0.93 |

---

## Meta Analysis

### Judge Strictness

| Rank | Judge | Avg Score Given |
|------|-------|-----------------|
| 1 | GPT-OSS-120B | 8.33 |
| 2 | GPT-5.4 | 8.40 |
| 3 | MiniMax M2.5 | 8.66 |
| 4 | Grok 4.20 | 8.72 |
| 5 | Claude Sonnet 4.6 | 8.88 |
| 6 | Claude Opus 4.6 | 8.96 |
| 7 | Gemini 3.1 Pro | 9.03 |
| 8 | DeepSeek V3 | 9.11 |
| 9 | MiMo-V2-Flash | 9.22 |
| 10 | Gemini 3 Flash Preview | 9.76 |

**Strictest Judge:** gpt_oss_120b
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

**Generation Time:** 22295ms
**Tokens:** 2195

```
Here is a breakdown of what the data actually reveals, which paints a very different picture than the PM’s optimistic assessment.

### 1. What story does this data actually tell?
The data tells the story of a **"leaky bucket."** The PM is mistaking a massive spike in top-of-funnel acquisition for sustainable growth. 

*   **Acquisition is masking churn:** DAU is up 50%, but MAU is only up 10%. This means the app is currently acquiring a massive number of *new* users every day (likely due to a marketing push, a viral event, or aggressive user acquisition spending). 
*   **Users are fleeing quickly:** The retention numbers are abysmal. While 40% of users come back on Day 1, only 15% remain by Day 7, and a mere 5% are left by Day 30. 
*   **The "growth" is a mirage:** Because 95% of acquired users are gone within a month, the moment the user acquisition budget runs out (or the viral trend fades), the DAU will plummet. The app is growing its *daily visitors*, but it is failing to grow its *core user base*.

### 2. What's concerning about the DAU/MAU ratio?
The DAU/MAU ratio is exactly **20%** (100K / 500K). This is generally considered mediocre to poor for most consumer apps (a healthy app usually targets 40%+, and elite apps hit 50%+). 

However, the real concern is **how the ratio is changing.** 
DAU grew by 50%, while MAU only grew by 10%. In a healthy product, DAU and MAU grow at relatively similar rates as new users become habitual daily users. Here, the massive disparity means the 100K DAU consists almost entirely of *brand new users* who are cycling through the app and churning out. The 500K MAU is mostly a graveyard of inactive accounts. The app is failing to turn monthly users into daily habitual users.

### 3. Why might session length decrease as sessions increase?
Sessions per day are up 30% (to 2.1), but session length is down 20% (to 8 min). This shift from fewer/longer sessions to more frequent/shorter sessions can happen for a few reasons:

*   **Aggressi...
```

### Claude Opus 4.6

**Generation Time:** 48780ms
**Tokens:** 2195

```
# Deconstructing the "We're Growing Fast" Narrative

## (1) The Real Story This Data Tells

The PM's statement isn't wrong — but it's dangerously incomplete. Let me reconstruct what's actually happening.

**The headline numbers look great on a slide deck.** But when you read them together as a system, they reveal something specific:

**This app is acquiring users aggressively but failing to retain them.**

Here's the logic chain:

```
DAU growing at 50% but MAU growing at only 10%
→ The new users flooding in are masking a retention crisis

D1: 40% → D7: 15% → D30: 5%
→ You lose 60% of users on day one
→ Of those who stay, you lose another 63% by day seven
→ Of THOSE survivors, you lose another 67% by day thirty

For every 1,000 new users:
  Day 1:  400 remain
  Day 7:  150 remain
  Day 30:  50 remain → 95% total churn
```

**The growth is real. The retention is catastrophic.** The company is almost certainly spending heavily on acquisition (paid campaigns, viral loops, or a press moment), and the influx of new users is temporarily inflating DAU. But the underlying product isn't generating enough value to keep people.

**This is the classic "leaky bucket" pattern** — you're pouring water in faster, but the holes in the bottom are getting bigger. The moment acquisition spend slows or the viral moment fades, DAU will collapse.

---

## (2) The DAU/MAU Ratio Problem

The DAU/MAU ratio (often called "stickiness") is **100K / 500K = 0.20 or 20%**.

**Why this is concerning:**

```
Benchmark Context:
  Facebook/Instagram:  ~50-60% (habitual daily use)
  Good consumer app:   ~25-30%
  Mediocre app:        ~15-20% ← You are here
  Utility apps:        ~10-15%

Your ratio: 20% — meaning on any given day, only 1 in 5
monthly users bothers to open the app.
```

**But the deeper concern is what the growth rates reveal about trajectory:**

| Metric | Growth | What it implies |
|--------|--------|-----------------|
| DAU | +50% | New users flooding in, showing up today |
| WAU | +...
```

### GPT-5.4

**Generation Time:** 13814ms
**Tokens:** 933

```
1. The real story: growth is happening, but quality of engagement looks mixed.

- Top-of-funnel is clearly improving:
  - DAU +50%
  - WAU +20%
  - MAU +10%
- That usually means a recent acquisition spike or reactivation wave, especially because daily growth is much faster than monthly growth.

But engagement depth and retention are weak:

- D1 retention 40%: decent, suggests users see some initial value.
- D7 retention 15%: big drop.
- D30 retention 5%: very weak long-term retention.
- Session length down 20% while sessions/day up 30%:
  - users are opening more often, but spending less time each visit.

So the likely interpretation is:

- The app is getting more people in.
- Many are trying it.
- Not many are sticking around long enough to become durable users.
- Usage may be becoming more lightweight, habitual, or fragmented rather than deeply engaged.

So “we’re growing fast” is only partially true. More precisely: acquisition is growing fast, but retention and sustained value look fragile.

2. What’s concerning about the DAU/MAU ratio?

DAU/MAU = 100K / 500K = 20%.

That means only 1 in 5 monthly active users is active on a given day.

Why that’s concerning:

- 20% is not terrible for every category, but it is not strong if this is meant to be a frequent-use product.
- Combined with D30 retention of 5%, it suggests the MAU base may include lots of casual, recently acquired, or low-intent users rather than a loyal core.
- DAU is growing much faster than MAU, which can happen during a short-term spike, but if retention is poor, that DAU lift may not last.

In short: the app may be buying or generating bursts of activity without creating a strong habit.

3. Why might session length decrease as sessions increase?

Several plausible reasons:

- The product is becoming more efficient:
  - users accomplish tasks faster, so each session is shorter.
  - This is the healthy explanation.

- Usage is becoming more fragmented:
  - instead of 1 long session, users do multipl...
```

### DeepSeek V3

**Generation Time:** 13600ms
**Tokens:** 695

```
Here’s the breakdown of the data and its implications:

### 1. **What story does this data actually tell?**
   - **Growth in users**: The app is experiencing rapid growth in DAU (+50%), WAU (+20%), and MAU (+10%), indicating successful acquisition efforts.
   - **High engagement**: Strong D1 retention (40%) suggests good onboarding, but D7 (15%) and D30 (5%) drop-offs reveal challenges in retaining users long-term.
   - **Usage patterns**: Session length is declining (-20%) despite more sessions per day (+30%), implying users are engaging more frequently but less deeply (potential "snacking" behavior or superficial use).

### 2. **What's concerning about the DAU/MAU ratio?**
   - **DAU/MAU = 100K/500K = 0.2 (20%)**: This is **low** for a healthy app (typical benchmarks: 20% is "average," but >50% is strong for social/productivity apps).  
   - **Implication**: Only 20% of monthly users return *daily*—most users are casual or churning quickly. The growth in DAU may be driven by new users (not retained ones), which is unsustainable.

### 3. **Why might session length decrease as sessions increase?**
   - **New users diluting metrics**: Influx of less-engaged users (from acquisition campaigns) may shorten average session time.
   - **Feature changes**: Quicker interactions (e.g., push notifications driving shallow clicks) or degraded UX (e.g., slower load times).
   - **Behavioral shift**: Users may be checking the app more briefly but frequently (e.g., for notifications), reducing per-session depth.

### 4. **What one metric would you focus on and why?**
   - **Focus: D7 retention (15%)**.  
   - **Why**: 
      - It bridges the gap between strong D1 (40%) and dismal D30 (5%), pinpointing where retention collapses.
      - Improving D7 would signal better habit formation and likely boost DAU/MAU and long-term growth.
      - Fixing this requires understanding *why* users disengage after onboarding (e.g., feature fatigue, lack of value).

#### Bonus: Other red flags
  ...
```

### MiMo-V2-Flash

**Generation Time:** 10889ms
**Tokens:** 1302

```
Here is an analysis of the mobile app’s performance data, broken down by your four questions.

### 1. What story does this data actually tell?

The data tells a story of **inefficient growth driven by shallow engagement.**

While the PM is correct that the app is growing in terms of raw user acquisition (DAU, WAU, MAU are all up significantly), the underlying health of the product is questionable. Here is the narrative arc:

*   **Acquisition is strong:** The app is successfully attracting new or returning users at a rapid pace (DAU +50% is a massive spike).
*   **Engagement is shifting, not necessarily improving:** Users are coming back more frequently (Sessions/day +30%), but they are spending less time per session (-20%).
*   **Retention is poor:** While we don't have the previous retention numbers, current benchmarks suggest the user base is churning quickly. The funnel from Day 1 to Day 30 loses 87.5% of users (40% → 15% → 5%).
*   **Conclusion:** The app is growing top-of-funnel but struggling to keep users deeply engaged or retained long-term. It is becoming a "high-churn, high-acquisition" product.

### 2. What's concerning about the DAU/MAU ratio?

To calculate this, we divide DAU (100K) by MAU (500K), resulting in a **20% stickiness ratio**.

**The Concerns:**
*   **Low Industry Benchmark:** For most successful consumer apps, a healthy DAU/MAU ratio is typically between 20% and 25% for utilities and 40%+ for habit-forming social/communication apps. While 20% is the threshold for "okay," it is on the lower end.
*   **The "Casual" User Problem:** A 20% ratio means that, on average, a user opens the app only **6 days out of a 30-day month**. This indicates the app is not a daily habit but an occasional utility.
*   **The Growth Paradox:** DAU is up 50% while MAU is up only 10%. This mathematically forces the DAU/MAU ratio *up*. However, if the app were truly becoming stickier, we would expect retention metrics (D7, D30) to improve. Since retention is low, the...
```

### Claude Sonnet 4.6

**Generation Time:** 44434ms
**Tokens:** 2194

```
# Decoding This App's Growth Story

## (1) What the Data Actually Tells You

### The Headline vs. Reality Gap

The PM is technically correct but **strategically misleading**.

```
What looks good:          What it obscures:
─────────────────────     ──────────────────────────────
DAU +50%                  D30 retention = 5%
Sessions/day +30%         Session length -20%
WAU +20%                  MAU growth slowest of all (10%)
```

### The Real Narrative: **Acquisition Masking Retention Collapse**

You're almost certainly running a **leaky bucket operation**:

```
New users pouring in (DAU surge)
        ↓
Most leave within 30 days (5% D30 retention)
        ↓
MAU growing slowly because churn ≈ new acquisition
        ↓
The "growth" is a treadmill, not a flywheel
```

**The retention funnel tells a brutal story:**
| Cohort Stage | Retention | Loss |
|---|---|---|
| Day 1 | 40% | **60% gone immediately** |
| Day 7 | 15% | 62.5% of survivors gone |
| Day 30 | 5% | 66.7% of survivors gone |

You're losing **95 out of every 100 users within a month**. That's not a growth story — it's a **distribution story**.

---

## (2) The DAU/MAU Ratio Problem

### What It Measures
DAU/MAU = **stickiness ratio** — how often monthly users return daily

```
Your ratio: 100K / 500K = 0.20 (20%)
```

### Benchmarks for Context
```
World-class (Facebook, WhatsApp):  50-65%  ████████████
Good (healthy consumer app):       25-35%  ██████
YOUR APP:                          20%     ████
Struggling:                        <15%    ███
```

### Why 20% Is Concerning Here

**The math exposes the problem:**
- 500K MAU but only 100K use it daily
- That means **400K monthly users aren't showing up today**
- With D30 retention at 5%, most of that MAU base is **recently acquired users on their way out**

**The dangerous dynamic:**
```
Today's MAU = 
  (Genuinely engaged users) + (New users in honeymoon period)
                                        ↑
                              This is inflating yo...
```

### Grok 4.20

**Generation Time:** 4037ms
**Tokens:** 1046

```
**1. What story does this data actually tell?**

The app is **acquiring a lot of new users** very quickly, but it is **failing to retain them**.

- Strong growth in all user bases (especially DAU +50%) shows the acquisition/marketing engine is working well.
- However, the retention curve is terrible: 40% D1 → 15% D7 → 5% D30. This is a classic “leaky bucket” situation. You’re pouring a lot of new users in the top, but they’re draining out extremely fast.
- The fact that DAU grew much faster than MAU (+50% vs +10%) means the recent growth is almost entirely driven by **new users** rather than existing users coming back more often.
- Session length dropping 20% while sessions/day increase 30% suggests users are coming back more frequently but engaging **less deeply** each time (more habitual/light usage or increased friction).

**Overall narrative:** “We’re growing fast on the top line, but the product is not sticky. We’re buying growth at the expense of long-term user quality.”

**2. What's concerning about the DAU/MAU ratio?**

Current DAU/MAU = 100k / 500k = **20%**.

This is actually quite low for most consumer apps (good benchmarks are usually 20–40%+ for highly engaging apps; <15–20% is often concerning).

**Why it’s worrying here:**
- DAU grew 5× faster than MAU. This inflates the DAU/MAU ratio in the short term, making the product *look* stickier than it really is.
- In reality, the underlying retention is very poor. The ratio is being artificially propped up by the massive influx of new users.
- Once acquisition slows down, this ratio will likely collapse because the new users aren’t sticking around.

It’s a classic “growth masking retention problems” signal.

**3. Why might session length decrease as sessions increase?**

Several plausible (and common) explanations:

- ** shallower use cases**: Users are opening the app more often for quick checks (notifications, streaks, social feed glances) rather than deep engagement.
- **Increased friction or poorer expe...
```

### GPT-OSS-120B

**Generation Time:** 39762ms
**Tokens:** 2152

```
**(1) The story the numbers are really telling**

| Metric | Current value | Growth vs. prior period | What it really means |
|--------|---------------|------------------------|----------------------|
| **DAU** | 100 k | **+50 %** | Lots of new users are showing up **today**. |
| **WAU** | 200 k | **+20 %** | The weekly active pool is expanding, but the weekly growth‑rate is far slower than the daily surge. |
| **MAU** | 500 k | **+10 %** | The overall audience is growing, but the **monthly** pace is the slowest of the three. |
| **Retention** (D1 40 %, D7 15 %, D30 5 %) |  |  | Only 4‑out of 100 users who ever install are still around after a month. The funnel collapses dramatically after the first day. |
| **Session length** | 8 min (‑20 %) |  | Users are spending less time per visit – a sign that the product is either becoming less “sticky” or that usage is shifting to more bite‑size interactions. |
| **Sessions / day per user** | 2.1 (↑30 %) |  | People are opening the app more often, but each visit is shorter. |

**Bottom‑line narrative**

- **Acquisition is hot.** The 50 % jump in DAU shows a successful marketing / onboarding push.
- **Engagement/Retention is weak.** The steep drop‑off after day‑1 (15 % D7, 5 % D30) tells us that most of those new users are not becoming regular users.
- **Stickiness is declining.** The DAU/MAU “stickiness” ratio is only 20 % and is falling as the user base expands, indicating that a growing share of the audience is only “sampling” the app.
- **Behavior is shifting to more frequent, shorter sessions.** This could be a symptom of a “quick‑task” usage pattern or of product changes that fragment the experience.

So the headline “we’re growing fast” is true **only for acquisition**; the health of the product – measured by how many of those acquired users stay, return, and spend time – is deteriorating.

---

**(2) Why the DAU/MAU ratio is concerning**

- **Current ratio:** DAU ÷ MAU = 100 k ÷ 500 k = 0.20 (20 %).
- **Industry bench...
```

### Gemini 3 Flash Preview

**Generation Time:** 6291ms
**Tokens:** 905

```
This data paints a picture of a product experiencing a **"growth spike" driven by aggressive acquisition or a viral trend**, rather than sustainable product-market fit.

Here is the breakdown of the situation:

### 1. What story does this data actually tell?
The story is **"Leaky Bucket Growth."** 

The app is successfully bringing in a massive wave of new users (DAU is up 50%, far outstripping MAU growth), but it is failing to keep them. The retention numbers (D30 at 5%) are quite low for a healthy app, suggesting that while the marketing or "hype" is working, the core product experience isn't "sticky." 

The disparity between DAU growth (50%) and MAU growth (10%) indicates that the current traffic is heavily front-loaded with new users who likely won't be there next month.

### 2. What’s concerning about the DAU/MAU ratio?
The **DAU/MAU ratio (Stickiness)** is currently **20%** (100K / 500K). 

*   **The Trend is the Problem:** While 20% is a standard benchmark for many apps, the *math* behind the growth is concerning. DAU grew by 50% while MAU only grew by 10%. This means the "Daily" number is being inflated by a massive influx of "New Users" today, rather than "Returning Users" over the month. 
*   **Future Collapse:** If the DAU/MAU is rising only because of a temporary spike in new installs, the ratio will crash as soon as the acquisition budget stops or the virality fades, because the D30 retention (5%) isn't high enough to convert these new users into long-term MAU.

### 3. Why might session length decrease as sessions increase?
This is a classic shift in user behavior, often seen in two scenarios:
*   **Micro-Consumption:** Users are moving toward "snackable" content. They check the app more frequently (2.1 sessions/day, up 30%) but stay for shorter bursts. This isn't necessarily bad if the app is a utility (like WhatsApp or a weather app).
*   **Friction or Shallow Engagement:** The more likely scenario here—given the poor retention—is that new users are o...
```

### MiniMax M2.5

**Generation Time:** 24306ms
**Tokens:** 1312

```
Excellent. Let's break this down critically.

**(1) What story does this data actually tell?**

The data tells a story of **acquisition-driven growth with weakening engagement and retention**. The PM is focused on the top-of-funnel (user counts) which are indeed growing, but the underlying health metrics paint a more nuanced picture.

*   **Growth is Real but Shallow:** The app is acquiring many new users (DAU, WAU, MAU all up), but the depth of their engagement is declining.
*   **The "Leaky Bucket" Problem:** High acquisition is masking poor retention. D1 (40%), D7 (15%), and D30 (5%) retention form a steep decay curve. This means the vast majority of new users are churning within the first month.
*   **Habit Not Formed:** The combination of low D30 retention and a low DAU/MAU ratio (see below) indicates the app is not becoming a daily habit for most of its users.

**(2) What's concerning about the DAU/MAU ratio?**

The DAU/MAU ratio here is **100K / 500K = 0.20 or 20%**.

*   **What it means:** Only 20% of the monthly active user base engages with the app on any given day. This is a measure of **stickiness** or **habit formation**.
*   **Why it's concerning:** For most successful consumer apps, a ratio of 20% is considered **low**. For context:
    *   ~20% is typical for utility/communication apps (e.g., email).
    *   40-50%+ is typical for high-engagement social or entertainment apps (e.g., Facebook, TikTok).
    *   A declining ratio (even if absolute DAU is up) signals that the *new* users being acquired are less engaged than the existing core. The app is becoming "wider" but not "deeper."

**(3) Why might session length decrease as sessions increase?**

This is a classic symptom of **shallow, fragmented engagement**. Possible explanations:
*   **Notification-Driven Usage:** More frequent notifications or prompts are driving users to open the app repeatedly ("sessions up 30%"), but for just a quick check or to dismiss a notification, leading to shorter sess...
```

---

*Generated by The Multivac V5*
*https://themultivac.com*