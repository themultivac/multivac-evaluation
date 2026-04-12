# Multivac Evaluation Report

**Evaluation ID:** EVAL-20260402-232602
**Timestamp:** 2026-04-02T23:26:02.881065
**Category:** Communication & Writing
**Model Pool:** 10 communication-optimized models

## Question

Your company's AI product generated offensive content that went viral. Write: (1) An immediate public statement (first 2 hours — acknowledge, no excuses), (2) A detailed follow-up 24 hours later (root cause, what you're doing about it), (3) An internal all-hands message to employees who are demoralized. Each must be genuine, take responsibility, and not use passive voice or the phrase 'we take this seriously' (which everyone uses and nobody believes).

---

## Rankings

| Rank | Model | Score | Min | Max | Std Dev |
|------|-------|-------|-----|-----|---------|
| 1 | GPT-5.4 | 9.38 | 8.80 | 10.00 | 0.51 |
| 2 | Grok 4.20 | 9.33 | 8.80 | 10.00 | 0.39 |
| 3 | Mistral Small Creative | 9.21 | 8.80 | 10.00 | 0.43 |
| 4 | MiMo-V2-Flash | 9.17 | 8.30 | 9.80 | 0.53 |
| 5 | Claude Sonnet 4.6 | 9.10 | 8.45 | 10.00 | 0.58 |
| 6 | Claude Opus 4.6 | 8.98 | 7.20 | 10.00 | 0.91 |
| 7 | Seed 1.6 Flash | 8.98 | 7.90 | 9.80 | 0.67 |
| 8 | GPT-OSS-120B | 8.86 | 6.95 | 9.80 | 0.83 |
| 9 | DeepSeek V3 | 8.79 | 8.25 | 9.60 | 0.41 |
| 10 | Gemini 3.1 Pro | 6.22 | 4.35 | 8.65 | 1.62 |

---

## Meta Analysis

### Judge Strictness

| Rank | Judge | Avg Score Given |
|------|-------|-----------------|
| 1 | GPT-5.4 | 8.10 |
| 2 | GPT-OSS-120B | 8.29 |
| 3 | Grok 4.20 | 8.47 |
| 4 | Gemini 3.1 Pro | 8.52 |
| 5 | Seed 1.6 Flash | 8.67 |
| 6 | Claude Sonnet 4.6 | 8.81 |
| 7 | Claude Opus 4.6 | 8.82 |
| 8 | MiMo-V2-Flash | 8.97 |
| 9 | DeepSeek V3 | 9.62 |
| 10 | Mistral Small Creative | 9.74 |

**Strictest Judge:** gpt_5_4
**Most Lenient Judge:** mistral_small_creative
**Total Judgments:** 100
**Valid Judgments:** 90

---

## Model Pool

Models selected for **Communication & Writing** evaluation:

1. **Claude Opus 4.6** (openrouter)
2. **GPT-5.4** (openrouter)
3. **Claude Sonnet 4.6** (openrouter)
4. **Gemini 3.1 Pro** (openrouter)
5. **Grok 4.20** (openrouter)
6. **DeepSeek V3** (openrouter)
7. **GPT-OSS-120B** (openrouter)
8. **MiMo-V2-Flash** (openrouter)
9. **Mistral Small Creative** (openrouter)
10. **Seed 1.6 Flash** (openrouter)

---

## Model Responses

### Claude Opus 4.6

**Generation Time:** 70484ms
**Tokens:** 2161

```
# AI Content Incident: Three-Phase Communication Plan

---

## (1) IMMEDIATE PUBLIC STATEMENT (Within 2 Hours)

**FOR IMMEDIATE RELEASE**
**From: [CEO Name], Chief Executive Officer**

---

**We failed today, and we owe you a direct accounting of that failure.**

Earlier today, our AI product generated deeply offensive content involving [brief, honest description — e.g., "racist stereotypes and dehumanizing language targeting Black communities"]. That content spread widely before we identified and removed it. We know many people saw it. We know it caused real harm, and no technical explanation changes that fact.

I want to be clear about three things right now:

**Our product generated this content.** We built the system. We deployed it. We own this.

**We are not going to hide behind the word "algorithm."** A team of human beings at this company made decisions about training data, safety filters, and deployment timelines. Those decisions proved inadequate, and the people who were harmed by this content bear the cost of our inadequacy.

**We have taken the following actions in the last 90 minutes:**
- We pulled the specific feature that generated this content offline. It will remain offline.
- We assembled our full safety engineering team and an independent review group to determine exactly how this happened.
- We contacted the advocacy organizations representing the communities targeted by this content, because they deserve to hear from us directly, not through a press release.

To anyone who encountered this content and was hurt, degraded, or angered by it: you deserved better from us. An apology without action is just reputation management, so I will return within 24 hours with a full accounting of what went wrong and what we are changing. Not what we are "exploring" or "considering." What we are changing.

I will answer press questions personally at [time/channel]. I will not send a spokesperson.

**[CEO Name]**
**[Direct email address]**
**[Date, Time]**

---

...
```

### GPT-5.4

**Generation Time:** 35822ms
**Tokens:** 1766

```
Below are three drafts tailored to the moment, audience, and level of detail you asked for.

---

## 1) Immediate public statement  
**Timing: First 2 hours**  
**Goal: Acknowledge harm, accept responsibility, no excuses**

Today, our AI product generated offensive content. People saw it, shared it, and many were hurt by it. We are sorry.

The responsibility is ours. Our product should not have produced this output, and our safeguards should have stopped it. They did not.

We have already started taking action. We are disabling the specific feature path involved, preserving logs and evidence for review, and beginning an urgent investigation into how this happened.

Right now, our focus is on three things: stopping further harm, understanding exactly what failed, and sharing clear updates as we learn more.

If you were targeted, insulted, or made to feel unsafe by this content, we apologize. You deserved better from us.

We will provide a fuller update within 24 hours.

---

## 2) Detailed public follow-up  
**Timing: ~24 hours later**  
**Goal: Explain root cause, responsibility, and concrete actions**

Yesterday, our AI product generated offensive content that spread widely online. That content caused real harm. We are responsible for it, and we owe the public a clear explanation of what happened and what we are doing now.

### What happened
Our initial investigation found a failure across multiple layers of our system.

A chain of changes introduced a gap between our safety policies and the live behavior of the product. In plain terms: one part of our system instructed the model to avoid harmful content, but another part of the system created conditions that let offensive output slip through. Our testing did not catch that conflict before release. Our monitoring also failed to escalate the issue fast enough once the harmful content appeared.

This was not one isolated miss. It exposed weaknesses in how we design, test, launch, and monitor AI behavior.

### Root ca...
```

### Claude Sonnet 4.6

**Generation Time:** 51484ms
**Tokens:** 2161

```
# Crisis Communications: AI Offensive Content Incident

---

## (1) IMMEDIATE PUBLIC STATEMENT
### *To be posted within 2 hours — Twitter/X, LinkedIn, company blog*

---

**From [CEO Name], [Company Name]**

Our AI product generated offensive content today. You saw it. We saw it. It caused real harm, and I own that.

I'm not going to hide behind technical explanations right now, because you deserve acknowledgment before you deserve explanation. Here's what I know in this moment:

**What happened:** Our AI generated [specific description — e.g., "racially offensive imagery / hateful text targeting X group"]. It spread widely. People were hurt by it.

**What we did immediately:** We pulled the feature offline at [time]. We are not bringing it back until we understand exactly how this happened and have fixed it.

**What I want to say directly:** If you were harmed or offended by what our product created, I'm sorry. Not "we regret if anyone was offended" — I'm sorry. We built this, we deployed it, and today it failed the people we're supposed to serve.

I'll have a full accounting for you in 24 hours. I won't ask you to trust us right now. I'll ask you to watch what we do next.

— [CEO Name]
[Time stamp]

---

*The feature remains offline. Updates will post here: [link]*

---

---

## (2) DETAILED FOLLOW-UP STATEMENT
### *24 hours later — long-form blog post*

---

**What Happened, Why It Happened, and What We're Changing**
*By [CEO Name] — [Date]*

---

Yesterday I promised you a full accounting. Here it is.

### What the content was

At [time] on [date], our AI generated [specific description of content]. Screenshots spread across [platforms]. Approximately [X] people saw it before we took the feature offline at [time] — [Y minutes] after the first report reached our team.

I'm describing it specifically because vagueness is its own form of dishonesty.

### What we found when we investigated

Our engineering and safety teams spent the last 18 hours doing a forensic re...
```

### Gemini 3.1 Pro

**Generation Time:** 20635ms
**Tokens:** 2148

```
**1. Immediate Public Statement (First 2 Hours)**

Earlier today, our AI generated deeply offensive content. We saw the screenshots circulating online. We own this failure completely, and we apologize to everyone who viewed these outputs. 

We shut down the affected product feature immediately. Our engineers began reviewing our safety filters the moment we spotted the issue, and they continue to work on it right now
```

### Grok 4.20

**Generation Time:** 6324ms
**Tokens:** 1039

```
**1. Immediate Public Statement (within 2 hours)**

We generated offensive and harmful content that has spread widely. This happened because of our failure to build sufficient safeguards into the model. The fault is ours.

We are sorry to everyone hurt by what we released. There is no excuse for this. We have already taken the system offline and are manually reviewing every part of the pipeline that allowed this to happen. We will update you with concrete next steps as soon as we have them.

**2. Detailed Follow-up Statement (24 hours later)**

Yesterday our model produced content that was offensive, derogatory, and genuinely harmful. We own this completely.

After a full night of investigation, here is what we found:

The root cause was a combination of three failures on our part:
- We shipped a post-training filter that was far too weak on identity-based attacks and culturally inflammatory prompts.
- Our red teaming dataset severely underrepresented the specific failure modes that actually went viral.
- We prioritized launch velocity over a final safety pass that multiple engineers had flagged as incomplete.

These were our decisions. No external actor or unexpected “emergent behavior” did this. We did this.

Here is what we are doing right now:

- The model remains offline.
- We have rebuilt and expanded the red teaming set with the exact prompts and personas that bypassed our filters. This new set is now part of every future training run.
- We have implemented a multi-layered guardrail system that will reject or heavily rewrite any output matching the patterns we saw yesterday. This change will ship before the model returns.
- Every single safety-related ticket that was deprioritized in the last two quarters is being reopened and given explicit executive priority.
- We are bringing in three external red teams with no prior relationship to our company to stress-test the fixes.
- We will publish the full post-mortem (including the exact prompts that caused the fai...
```

### DeepSeek V3

**Generation Time:** 47445ms
**Tokens:** 680

```
### **(1) Immediate Public Statement (First 2 Hours)**  

**Subject:** We Failed You – An Immediate Apology  

Today, our AI generated offensive and harmful content. It should not have happened. We are ashamed of the pain this has caused, and we owe everyone—especially those directly affected—an unequivocal apology.  

We are investigating how this occurred and will share a full update within 24 hours. Right now, we are disabling the feature involved and reviewing all outputs to prevent further harm.  

This was our mistake, and we will fix it. No qualifications, no excuses.  

—[Your Name/Company]  

---  

### **(2) Detailed Follow-Up (24 Hours Later)**  

**Subject:** What Went Wrong and How We’re Fixing It  

Yesterday, our AI produced unacceptable content. We know apologies aren’t enough—you deserve transparency and action. Here’s what happened and what we’re doing:  

**Root Cause:**  
- Our safeguards failed to detect biased patterns in the training data.  
- Stress-testing for offensive outputs was incomplete before launch.  
- Human review processes were not rigorous enough.  

**Immediate Actions:**  
1. We’ve taken the flawed feature offline indefinitely.  
2. We’re auditing all training data and removing harmful sources.  
3. We’ve partnered with third-party experts to rebuild our content filters.  

**Long-Term Changes:**  
- We will establish an external advisory board to challenge our safety protocols.  
- We will publish regular reports on harmful outputs and our progress.  

We know trust is earned, not promised. We will update you weekly on our progress.  

—[Your Name/Company]  

---  

### **(3) Internal All-Hands Message**  

**Subject:** This Hurts. Here’s How We Move Forward.  

Team,  

What happened yesterday was a failure—not just of technology, but of our responsibility as a company. Many of you warned about risks, worked tirelessly to prevent this, and now feel demoralized. That’s understandable.  

Here’s what you should know:  
- **We o...
```

### GPT-OSS-120B

**Generation Time:** 27742ms
**Tokens:** 1516

```
---

## 1. Immediate public statement (first 2 hours)

**To our community, partners, and the public:**

Our latest AI release produced a piece of content that is offensive, hurtful, and completely unacceptable. The material spread far beyond what we intended, and we own that mistake.  

Effective immediately, we have taken the offending output offline, disabled the specific generation pipeline, and begun a full investigation. No excuse can justify the harm caused, and we will not wait for anyone else to fix it.

We will keep you informed with concrete updates as soon as we have them.

— [CEO Name], CEO, [Company]  

---

## 2. Detailed follow‑up (24 hours later)

**What happened, why it happened, and what we are doing right now**

1. **Root cause** – A mis‑configured safety filter allowed the language model to draw from a subset of training data that contained hateful rhetoric. The filter’s thresholds were lowered in a recent performance‑tuning sprint, and the change was not validated against our bias‑detection suite. As a result, the model generated content that violated our own community standards.

2. **Immediate corrective actions**  
   - **Shutdown** the entire generation endpoint for this model and replace it with a sandboxed version that enforces a stricter profanity and hate‑speech blocklist.  
   - **Audit** every prompt‑response pair produced in the last 48 hours; any content that breaches policy will be removed and logged.  
   - **Notify** affected users directly with an apology and an offer to delete any saved outputs.

3. **Long‑term fixes**  
   - **Re‑engineer** the safety‑filter architecture to run a multi‑layer, real‑time check that combines lexical, semantic, and context‑aware signals.  
   - **Expand** our bias‑testing corpus by 300 % and integrate continuous automated regression tests that flag any drift toward disallowed language.  
   - **Bring in** an external ethics advisory board to review the model’s behavior weekly for the next six month...
```

### MiMo-V2-Flash

**Generation Time:** 12450ms
**Tokens:** 1268

```
Here is a crisis response plan addressing the situation. These drafts avoid corporate jargon, passive voice, and the overused phrase "we take this seriously." Instead, they demonstrate ownership through direct action and specific accountability.

***

### (1) Immediate Public Statement
**Timing:** Within 2 hours of the incident going viral.
**Platform:** X (Twitter), LinkedIn, and Company Blog.
**Tone:** Urgent, direct, and humble.

**Headline:** We messed up. The offensive content is ours, and we are deleting it now.

**Body:**
Our AI generated content that is offensive, unacceptable, and does not reflect our values. We own this mistake completely.

We have immediately disabled the model responsible for this output and are pulling the content down across all platforms. We are not making excuses about "edge cases" or "unexpected prompts." The system failed, and as the leadership team, we are accountable for that failure.

We are investigating the root cause right now. We will share a detailed update within 24 hours on exactly what went wrong and the concrete steps we are taking to ensure this does not happen again.

To everyone who saw this content and was hurt or offended: we are deeply sorry. We know we broke your trust, and we will work to earn it back.

***

### (2) Detailed Follow-Up
**Timing:** 24 hours after the incident.
**Platform:** Company Blog and Email to Users.
**Tone:** Technical, transparent, and corrective.

**Headline:** What went wrong, why it happened, and what we’re doing next.

**Body:**
Yesterday, our AI product generated and distributed harmful content. We take full responsibility for this failure. We have completed our initial investigation, and here is exactly what happened and how we are fixing it.

**Root Cause**
The incident occurred due to a failure in our safety alignment layer. During a recent update to improve the model’s creativity, we inadvertently weakened the filters that detect and block hate speech and offensive imagery. The mo...
```

### Mistral Small Creative

**Generation Time:** 15614ms
**Tokens:** 2342

```
Here are three authentic, direct, and accountable responses—each tailored to its audience and purpose. The tone avoids corporate clichés while owning the failure without defensiveness.

---

### **1. Immediate Public Statement (First 2 Hours)**
**Subject:** We Failed You. Here’s What Happened.

**To our users, partners, and the public,**

This morning, our AI product generated content that was offensive, harmful, and completely unacceptable. There are no excuses. We built this tool to help people, not to cause pain, and we fell short in the most basic way possible.

We’re removing the content immediately, investigating how this happened, and taking swift action to prevent it from ever happening again. That includes pausing the feature in question while we assess our safeguards—and yes, that means some of you may experience temporary disruptions. The risk of another failure like this is not worth the convenience.

This is on us. We designed the system. We deployed it. And we own the outcome. There’s no “algorithm did it” or “edge case” that justifies this. We will share more about what went wrong and what we’re doing to fix it within 24 hours. In the meantime, if you or someone you know was affected, please [contact us here]. We’re listening.

We’re better than this. And we will prove it.

**[Your Name]**
[Your Title]
[Company Name]

---
**Why this works:**
- **No weasel words:** "Fell short," "completely unacceptable," "this is on us" — direct ownership.
- **Action over platitudes:** Names the immediate steps (removal, pause, investigation) without vague promises.
- **Acknowledges harm:** Centers the impact on people, not the company’s reputation.
- **Sets a clear next step:** 24-hour update with specifics.

---

### **2. Detailed Follow-Up (24 Hours Later)**
**Subject:** What Went Wrong and How We’re Fixing It

**To our community,**

Twenty-four hours ago, we published a statement acknowledging that our AI generated harmful content. We said we’d share what happened...
```

### Seed 1.6 Flash

**Generation Time:** 23191ms
**Tokens:** 3161

```
### **(1) Immediate Public Statement (1:47 PM ET, [Date])**  
To our users, partners, and everyone who trusted us: I’m sorry. Yesterday, our AI generated offensive content that spread online. That content was our creation. There’s no way to spin it, no “context” that excuses it. We failed you.  

We’re taking it down *immediately*—every instance of the content is being removed, and we’re working to block it from ever appearing again. We’re launching a full, independent review of our AI systems and processes, and we’ll share what we find. This isn’t a “glitch” or a “one-off”—it’s a failure of the work we do, and we will fix it.  

Thank you for holding us accountable. We won’t let you down again.  

— [Your Full Name], [Your Title]  


### **(2) Detailed Follow-Up (24 Hours Later, 10:02 AM ET, [Date])**  
To our users, partners, and the public: Today, we’re sharing what we’ve learned about the offensive content our AI generated yesterday—and what we’re doing to fix it.  

**First, the root cause:** Our AI training dataset included unfiltered, outdated content from public sources. Much of this content was biased, harmful, or offensive. Our system, designed to identify and learn from patterns, inadvertently absorbed these patterns. We should have caught this in rigorous testing, but we didn’t. That’s on us.  

**To fix it:**  
1. **We’re rebuilding our AI from the ground up.** We’ve paused all non-critical AI development to overhaul our training pipelines. We’re removing *all* biased or harmful data from our datasets and implementing new, human-supervised filters to block offensive content before it’s learned.  
2. **We’re bringing in independent oversight.** We’ve hired a team of AI ethicists and data scientists (external to the company) to audit our systems, processes, and culture. They’ll release a full report in 30 days, and we’ll act on every recommendation.  
3. **We’re adding human checks at every step.** Starting next week, *every* AI-generated output will be r...
```

---

*Generated by The Multivac V5*
*https://themultivac.com*