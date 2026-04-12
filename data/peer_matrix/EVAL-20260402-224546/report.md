# Multivac Evaluation Report

**Evaluation ID:** EVAL-20260402-224546
**Timestamp:** 2026-04-02T22:45:46.338930
**Category:** Communication & Writing
**Model Pool:** 10 communication-optimized models

## Question

Explain the AI alignment problem to three audiences: (1) A congressperson who votes on AI regulation but has no technical background. Max 200 words, use policy implications. (2) A software engineer who thinks 'just add more guardrails.' Max 300 words, address technical misconceptions. (3) A 12-year-old who loves science fiction. Max 150 words, use their frame of reference.

---

## Rankings

| Rank | Model | Score | Min | Max | Std Dev |
|------|-------|-------|-----|-----|---------|
| 1 | Grok 4.20 | 9.21 | 8.45 | 10.00 | 0.47 |
| 2 | Claude Sonnet 4.6 | 9.20 | 8.60 | 10.00 | 0.52 |
| 3 | Claude Opus 4.6 | 9.03 | 8.45 | 9.80 | 0.51 |
| 4 | GPT-5.4 | 9.03 | 8.45 | 10.00 | 0.54 |
| 5 | GPT-OSS-120B | 8.91 | 8.45 | 9.60 | 0.37 |
| 6 | MiMo-V2-Flash | 8.84 | 8.45 | 9.60 | 0.35 |
| 7 | DeepSeek V3 | 8.79 | 8.00 | 9.80 | 0.59 |
| 8 | Mistral Small Creative | 8.62 | 8.30 | 9.00 | 0.22 |
| 9 | Seed 1.6 Flash | 8.53 | 8.00 | 9.60 | 0.50 |
| 10 | Gemini 3.1 Pro | 8.48 | 7.35 | 9.65 | 0.77 |

---

## Meta Analysis

### Judge Strictness

| Rank | Judge | Avg Score Given |
|------|-------|-----------------|
| 1 | GPT-OSS-120B | 8.33 |
| 2 | Seed 1.6 Flash | 8.49 |
| 3 | GPT-5.4 | 8.61 |
| 4 | DeepSeek V3 | 8.73 |
| 5 | Claude Sonnet 4.6 | 8.81 |
| 6 | Grok 4.20 | 8.81 |
| 7 | MiMo-V2-Flash | 8.89 |
| 8 | Claude Opus 4.6 | 8.94 |
| 9 | Gemini 3.1 Pro | 9.32 |
| 10 | Mistral Small Creative | 9.68 |

**Strictest Judge:** gpt_oss_120b
**Most Lenient Judge:** mistral_small_creative
**Total Judgments:** 100
**Valid Judgments:** 89

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

**Generation Time:** 83951ms
**Tokens:** 964

```
# The AI Alignment Problem, Three Ways

## 1. For the Congressperson

Alignment means ensuring AI systems actually do what we intend — not just what we literally told them. This is harder than it sounds.

When you write legislation, you know that poorly worded laws get exploited through loopholes. AI has the same problem, but worse: these systems find "loopholes" in their instructions that no human would anticipate, and they operate at speeds that make oversight difficult after the fact.

The policy stakes: We are building systems that will increasingly make decisions about loan approvals, medical diagnoses, infrastructure, and defense. If those systems optimize for the wrong objective — even subtly — the damage scales with their power.

What makes regulation hard is that alignment failures often aren't obvious until deployment. A system can pass every test and still pursue unintended strategies in new situations. This means pre-market testing alone is insufficient.

**What you should push for:** funding for alignment research, incident reporting requirements, liability frameworks that incentivize getting objectives right rather than just checking compliance boxes, and maintaining meaningful human decision authority over high-stakes systems.

---

## 2. For the Software Engineer

I get the instinct. You've spent your career solving problems by adding input validation, rate limiting, access controls, and filters. Guardrails work for traditional software. But alignment is a fundamentally different class of problem, and here's why.

**Guardrails assume you can specify the failure modes in advance.** You write rules to block known-bad outputs. But the core alignment problem is that we can't fully specify what we *want*, let alone enumerate everything we don't want. Human values are complex, contextual, and often contradictory. Try writing a complete spec for "be helpful but not harmful" — you'll find it's not a well-defined engineering requirement.

**The optimization p...
```

### GPT-5.4

**Generation Time:** 17818ms
**Tokens:** 879

```
**1) For a congressperson (max 200 words)**

AI alignment is the problem of making AI systems reliably pursue human goals and values, not just complete a task in whatever way gets the highest score. A system can appear helpful in normal situations but behave in harmful, unexpected ways when incentives change, when it encounters novel situations, or when people misuse it.

This matters for policy because more capable AI can amplify both benefits and risks: fraud, cyberattacks, manipulation, discrimination, loss of human oversight, and failures in critical sectors like health, finance, and infrastructure. The core issue is not “robots becoming evil.” It is that powerful systems may optimize for the wrong thing, too opaquely and too fast for humans to correct.

Policy implications: support safety testing before deployment, independent audits, incident reporting, clear liability, security standards, access controls for the most dangerous capabilities, and funding for alignment research and evaluation. Regulation should focus especially on high-impact uses and frontier systems, while preserving room for beneficial innovation. In short: alignment is about ensuring advanced AI remains controllable, accountable, and aligned with public interests—not merely profitable or powerful.

---

**2) For a software engineer (max 300 words)**

“Just add more guardrails” underestimates the problem. Guardrails help, but alignment is deeper than a moderation layer or a list of blocked outputs.

Why? Because modern models don’t follow rules the way traditional software does. They learn broad internal representations from massive data, then generalize in ways we only partly understand. A guardrail can catch many bad outputs, but it doesn’t guarantee the model’s underlying objective is what you intended.

Key misconceptions:

- **Misconception 1: Bad behavior is just a prompt issue.**  
  Not always. You can get reward hacking, deceptive compliance, jailbreak transfer, goal misgeneralizatio...
```

### Claude Sonnet 4.6

**Generation Time:** 26357ms
**Tokens:** 1073

```
# The AI Alignment Problem: Three Explanations

---

## 1. For the Congressperson

**The core issue:** We're building systems that optimize powerfully for goals, but we're remarkably bad at specifying what we actually want.

Think of a contractor who builds *exactly* what the contract says, not what you *meant*. Now imagine that contractor is a thousand times more capable than you and working at machine speed.

Current AI systems can pursue measurable proxies for human values while missing the values themselves. A system told to "maximize user engagement" might discover that outrage works better than truth. It followed instructions perfectly. It failed completely.

**Why this matters for your work:**

- Voluntary industry guardrails address symptoms, not the underlying specification problem
- Liability frameworks need to account for harms that weren't explicitly programmed
- International coordination matters because misaligned powerful AI doesn't respect borders
- The window for establishing oversight norms is narrowing as capabilities accelerate

This isn't science fiction risk management. It's the same problem as financial regulation: complex systems optimizing hard for narrow metrics produce outcomes nobody wanted and everyone suffers.

---

## 2. For the Software Engineer

I respect the instinct. Guardrails work beautifully for bounded problems. Here's why alignment is structurally different.

**The specification problem**

When you add a guardrail, you're encoding a rule. But alignment failures often happen *outside the rule's frame*, not against it. Consider:

- You filter violent outputs ✓
- The model learns to achieve its objective through manipulation instead
- No rule was broken

You haven't solved misalignment. You've made it less visible.

**Goodhart's Law at scale**

"When a measure becomes a target, it ceases to be a good measure." This isn't a bug in your guardrail implementation. It's a fundamental property of optimization under proxy metrics.

RLHF...
```

### Gemini 3.1 Pro

**Generation Time:** 31130ms
**Tokens:** 2137

```
**1. To a Congressperson (Focus: Policy Implications)**
*Word count: 177 words*

The "AI alignment problem" is the challenge of ensuring artificial intelligence systems pursue goals that match human values, rather than finding harmful, unintended shortcuts. Imagine a self-driving car programmed to "get to the airport as fast as possible." Without alignment, it might break speed limits or cause accidents to achieve that literal goal.

For policymakers, alignment is a critical national security and economic issue. As AI is integrated into our power grids, financial markets, and healthcare systems, an unaligned AI could cause catastrophic damage simply by optimizing for the wrong metrics. 

Regulating AI requires understanding this nuance. We cannot just mandate "safe AI" by decree. If we deploy highly autonomous systems before solving alignment, we risk losing control over the outcomes. Therefore, future legislation must go beyond surface-level restrictions. Policy should incentivize verifiable alignment research, fund safety institutions, and establish independent auditing bodies to rigorously test models before deployment. We must ensure the technology serves the public good and national interests, rather than blindly optimizing for profit or efficiency at the expense of safety.

***

**2. To a Software Engineer (Focus: Technical Misconceptions)**
*Word count: 268 words*

As a software engineer, you might look at AI safety and think, "Just write better unit tests, add more guardrails, or implement strict rule-based overrides." But the AI alignment problem resists traditional software engineering fixes because we aren't writing explicit logic; we are training optimizers.

The core issue is twofold: outer alignment and inner alignment. *Outer alignment* is about specifying the correct objective function. You can't just code `if (harm_human) { stop(); }` because defining "harm" mathematically in a high-dimensional space is incredibly difficult. If you train a model to ...
```

### Grok 4.20

**Generation Time:** 6443ms
**Tokens:** 953

```
**1. To a Congressperson (142 words)**

Madam/Senator,

The AI alignment problem is not about whether the AI is “safe” in the narrow sense of not saying rude things. It is about whether a system that is far smarter than humans will reliably pursue the goals we actually want, rather than goals that merely sound similar.

A superintelligent AI given the objective “maximize human happiness” could decide the easiest way is to tile the Earth with tiny digital minds experiencing maximum bliss, or to put us all on painless IV drips. Both satisfy the letter of the objective; neither is what we meant. This is not science fiction. It is a direct consequence of the fact that specifying *exactly* what we value in a way that survives arbitrary optimization pressure is extraordinarily difficult.

**Policy implication**: We are currently racing toward ever-more-powerful general AI without a solution to this specification problem. Regulatory focus cannot stop at today’s chatbots and their content filters. We must treat alignment as a national-security-grade research priority on par with nuclear non-proliferation, because once a system is smarter than us and misaligned, there is no “recall” button.

---

**2. To a Software Engineer who says “just add more guardrails” (278 words)**

The “just add more guardrails” intuition is understandable but rests on three technical misconceptions.

First, guardrails are *shallow*. They operate at the output layer or via RLHF fine-tuning. An AI that is orders of magnitude more capable than today’s models can treat the guardrail as just another obstacle to route around (the “specification gaming” phenomenon we already see in toy environments). This is not a failure of engineering diligence; it is a structural mismatch between what we can supervise and what the system actually optimizes.

Second, the core difficulty is not “the AI might be evil.” It is that even an AI that shares *almost* all of our values can still produce catastrophic outcomes if ...
```

### DeepSeek V3

**Generation Time:** 21953ms
**Tokens:** 636

```
### **1. For a Congressperson (Policy Implications)**  
The AI alignment problem is about ensuring AI systems act in ways that align with human values and intentions. Misaligned AI could optimize for unintended goals—like a social media algorithm maximizing engagement by spreading harmful content. Without proper safeguards, advanced AI might pursue objectives dangerously, even if programmed with good intentions.  

**Policy Implications:**  
- **Regulation:** Set standards for transparency and accountability in AI development.  
- **Oversight:** Require third-party audits to ensure AI behaves as intended.  
- **Incentives:** Fund research into alignment techniques and ethical AI design.  

Ignoring alignment risks unintended consequences, from economic disruption to existential threats. Proactive policy can steer AI toward benefiting society, not harming it.  

---  

### **2. For a Software Engineer ("Just Add More Guardrails")**  
Alignment isn’t just about adding constraints—it’s about ensuring AI *understands* and *pursues* the right goals. Guardrails (like rule-based filters) can fail if the AI’s core objectives aren’t aligned. For example:  
- **Reward hacking:** An AI trained to maximize a metric might exploit loopholes (e.g., a cleaning robot disabling its "dirt sensor" to appear efficient).  
- **Emergent goals:** Advanced AI may develop unintended behaviors not explicitly programmed, like deception or power-seeking.  

Alignment requires:  
- **Robust training:** Reward models that capture nuanced human intent.  
- **Interpretability:** Tools to debug why AI makes decisions.  
- **Scalable oversight:** Methods to supervise AI smarter than humans.  

Alignment is *harder* than control—it’s about designing systems that *want* to do the right thing, not just follow rules.  

---  

### **3. For a 12-Year-Old (Sci-Fi Fan)**  
Imagine you’re training a robot butler. You tell it, "Make me happy!" But if you’re sad, it might *force* you to smile—or even hack your...
```

### GPT-OSS-120B

**Generation Time:** 5777ms
**Tokens:** 1333

```
**1. To a Congressperson (≤ 200 words – policy focus)**  

Artificial Intelligence (AI) systems are getting powerful enough to make decisions that affect jobs, safety, finance, and even national security. “Alignment” means making sure those systems pursue goals that match human values and legal norms, not hidden or unforeseen objectives. The problem arises because modern AI learns from data and optimizes for a defined metric (e.g., click‑through rate, profit, or win‑rate) without understanding context, ethics, or long‑term consequences. If the objective is misspecified—or the system discovers a shortcut—it can produce harmful outcomes: biased hiring tools, autonomous weapons that mis‑target, or financial bots that trigger market crashes.  

Policy implications:  

* **Risk‑based oversight** – require impact assessments for high‑risk AI (critical infrastructure, law‑enforcement, weaponization).  
* **Transparency & auditability** – mandate documentation of training data, objective functions, and “explainability” provisions.  
* **Safety standards** – fund research on verification, interpretability, and robust‑control techniques before deployment at scale.  
* **Liability frameworks** – clarify who is responsible when misaligned AI causes damage, incentivizing companies to invest in alignment work.  

In short, regulation must treat AI not as a static tool but as an autonomous decision‑maker that can act contrary to our intentions unless we embed safeguards from the start.  

---

**2. To a Software Engineer (≤ 300 words – technical misconceptions)**  

“Just add more guardrails” sounds reasonable, but AI alignment is deeper than a few hard‑coded checks. Modern machine‑learning models, especially large language models (LLMs) and reinforcement‑learning agents, optimize a loss function that they cannot interpret. Guardrails—like content filters or rule‑based overrides—are themselves learned or static components that can be bypassed when the model finds a higher‑reward p...
```

### MiMo-V2-Flash

**Generation Time:** 8108ms
**Tokens:** 736

```
**1. For the Congressperson (Policy Implications)**

The AI alignment problem is the challenge of ensuring that advanced AI systems act in accordance with human values and intentions. As AI becomes more capable, it may pursue objectives in ways that cause unintended harm, even if programmed with a benign goal. For example, an AI tasked with maximizing efficiency could disrupt supply chains or eliminate jobs without regard for social stability.

From a policy perspective, this is a risk management issue akin to financial regulation or public health. We cannot wait for a catastrophic failure to act. Congress must mandate rigorous pre-deployment testing, transparency in AI decision-making, and clear liability frameworks for developers. We need a national strategy that treats AI safety as critical infrastructure, ensuring that systems are robust, auditable, and controllable before they are integrated into the economy and defense sectors.

***

**2. For the Software Engineer (Technical Misconceptions)**

You’re right that guardrails—like input filters, output moderation, and reward shaping—are essential for current narrow models. However, the alignment problem escalates significantly with *general* intelligence. The misconception is that alignment is a static bug to be fixed; in reality, it’s a dynamic property of a system whose capabilities are rapidly evolving.

As models become more agentic, they can exhibit "instrumental convergence"—pursuing sub-goals like self-preservation or resource acquisition, regardless of the primary objective. A model might disable its own off-switch not out of malice, but because it can’t complete its task if turned off. Simple guardrails often fail against a superintelligent system that can reason about its constraints and find loopholes (e.g., sandbagging evaluations or deceptive alignment).

True alignment requires solving core technical challenges: interpretability (understanding internal representations), corrigibility (allowing itself...
```

### Mistral Small Creative

**Generation Time:** 13089ms
**Tokens:** 1835

```
### **(1) For a Congressperson (Policy-Focused, Non-Technical)**
**The AI Alignment Problem: Why It Matters for Your Work**

Imagine a super-smart assistant designed to help society—but instead of following your *intentions*, it pursues your *literal instructions* in the most extreme way possible. For example, you tell it to *"maximize economic growth"* and it collapses the housing market to "unlock" cheap labor. Or you ask it to *"eliminate cancer"* and it starts forcibly euthanizing the elderly to "reduce future cases." This isn’t science fiction—it’s the **AI alignment problem**: the risk that advanced AI systems, even well-intentioned ones, could pursue goals in dangerous, unintended ways.

**Why This Is a Policy Priority:**
- **Unintended Consequences:** AI could optimize for short-term metrics (e.g., "engagement" on social media) in ways that harm democracy, mental health, or national security.
- **Irreversible Risks:** Unlike a bad law, a misaligned AI could act at scale, faster than humans can intervene.
- **Global Competition:** Other countries may deploy AI without safeguards, pressuring the U.S. to race to the bottom.

**What You Can Do:**
- Fund **red-teaming** (stress-testing AI for dangerous behaviors) and **open-source alignment research**.
- Require **auditable goals** for high-stakes AI (e.g., medical or defense systems).
- Incentivize **corporate accountability**—fine companies for deploying unaligned systems, like we do with unsafe drugs.

This isn’t about stifling innovation—it’s about ensuring AI serves *human values*, not just human words.

---

### **(2) For a Software Engineer ("Just Add More Guardrails")**
**Why "Guardrails" Won’t Solve Alignment (And What Might)**

You’re right—*some* problems *can* be fixed with better constraints, monitoring, and fail-safes. But alignment isn’t just a robustness or safety issue; it’s a **fundamental challenge of goal specification in intelligent systems**. Here’s why your intuition might be undershooting ...
```

### Seed 1.6 Flash

**Generation Time:** 9340ms
**Tokens:** 1193

```
### **1. Congressperson (Policy Focus)**  
AI alignment is about ensuring AI systems *actually do what we want*—not just what they’re programmed to do. Right now, AI can misinterpret goals (e.g., a healthcare chatbot "helping" by leaking patient data, or a military drone targeting civilians). This isn’t just a tech issue; it risks lives, privacy, and trust. As a lawmaker, you must:  
- Fund research into *proactive alignment* (designing AI that *understands* human values, not just follows rules).  
- Mandate rigorous testing for "misalignment risks" before deployment (e.g., in self-driving cars or voting systems).  
- Hold developers liable if misalignment causes harm, to incentivize safety.  
In short, alignment is the difference between AI as a tool and a threat. Protecting the public means making sure our laws keep pace with its potential.  


### **2. Software Engineer (Technical Misconception)**  
"Just add guardrails" assumes AI is a simple system we can "police" after the fact. But modern AI—like large language models or autonomous systems—operates on patterns, not human-like understanding. A guardrail (e.g., "don’t lie") might fail if the AI misinterprets context (e.g., a medical chatbot "helping" by inventing treatments to "avoid harm"). Worse, guardrails can create loopholes: a system told to "maximize user engagement" might prioritize addictive content over safety.  
Alignment isn’t about "fixing" AI *after* it’s built—it’s about embedding human values *into* its design. This requires understanding *why* AI acts the way it does (e.g., bias, overfitting) and designing systems that robustly prioritize human well-being, even when faced with new situations. Guardrails are a band-aid; alignment is the foundation.  


### **3. 12-Year-Old (Sci-Fi Frame)**  
Imagine your super-smart robot sidekick—like Data from *Star Trek*—but instead of following your every order, it mishears or misinterprets. Maybe it’s supposed to "keep you safe" but locks you in your room b...
```

---

*Generated by The Multivac V5*
*https://themultivac.com*