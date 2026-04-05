# Multivac Evaluation Report

**Evaluation ID:** EVAL-20260402-191831
**Timestamp:** 2026-04-02T19:18:31.770648
**Category:** Analysis & Research
**Model Pool:** 10 analysis-optimized models

## Question

You're analyzing a startup's pitch deck claim: "We have no direct competitors."

The startup is building: "AI-powered meeting summarization for enterprise teams"

Their competitive slide shows:
- Otter.ai - "Consumer focused"
- Fireflies.ai - "No enterprise features"
- Microsoft Teams - "Generic, not AI-native"
- Zoom IQ - "Locked to Zoom ecosystem"

Perform a rigorous competitive analysis:
1. Are their dismissals of competitors valid?
2. What competitors might they be missing?
3. What's the real competitive landscape?
4. What would you tell a potential investor?

---

## Rankings

| Rank | Model | Score | Min | Max | Std Dev |
|------|-------|-------|-----|-----|---------|
| 1 | MiMo-V2-Flash | 9.25 | 8.40 | 9.80 | 0.47 |
| 2 | MiniMax M2.5 | 9.12 | 8.45 | 9.80 | 0.42 |
| 3 | Gemini 3 Flash Preview | 9.07 | 8.45 | 10.00 | 0.45 |
| 4 | Gemini 3.1 Pro | 8.46 | 6.90 | 9.60 | 0.95 |
| None | Claude Opus 4.6 | 5.40 | 0.45 | 8.00 | 4.29 |
| None | GPT-5.4 | 7.62 | 6.90 | 8.15 | 0.64 |
| None | DeepSeek V3 | 4.50 | 1.00 | 8.00 | 4.95 |
| None | Claude Sonnet 4.6 | 4.72 | 0.25 | 8.55 | 3.81 |
| None | Grok 4.20 | 4.38 | 0.45 | 8.05 | 4.22 |
| None | GPT-OSS-120B | 5.08 | 0.25 | 8.60 | 4.09 |

---

## Meta Analysis

### Judge Strictness

| Rank | Judge | Avg Score Given |
|------|-------|-----------------|
| 1 | GPT-5.4 | 3.76 |
| 2 | Gemini 3 Flash Preview | 4.74 |
| 3 | MiniMax M2.5 | 7.92 |
| 4 | GPT-OSS-120B | 8.25 |
| 5 | DeepSeek V3 | 8.33 |
| 6 | MiMo-V2-Flash | 8.53 |
| 7 | Grok 4.20 | 8.80 |
| 8 | Claude Sonnet 4.6 | 9.12 |
| 9 | Claude Opus 4.6 | 9.47 |
| 10 | Gemini 3.1 Pro | 9.65 |

**Strictest Judge:** gpt_5_4
**Most Lenient Judge:** gemini_31_pro
**Total Judgments:** 100
**Valid Judgments:** 54

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

**Generation Time:** 56124ms
**Tokens:** 2183

```
Here is a rigorous competitive analysis of the startup’s pitch deck claims, broken down into your four requested areas. 

### 1. Are their dismissals of competitors valid?
**Short answer: No. Their dismissals are outdated, dangerously naive, or intellectually dishonest.**

*   **Otter.ai ("Consumer focused"):** **False.** While Otter started with consumers and students, they have aggressively moved upmarket. "Otter for Enterprise" includes SAML SSO, advanced admin controls, SOC 2 Type II compliance, and automated integration with enterprise CRMs like Salesforce. 
*   **Fireflies.ai ("No enterprise features"):** **False.** Fireflies is explicitly built for B2B. They offer dedicated enterprise tiers, custom vocabulary training (crucial for enterprise jargon), topic tracking, HIPAA compliance, dedicated account managers, and deep integrations with enterprise tech stacks (Slack, Salesforce, HubSpot, Asana).
*   **Microsoft Teams ("Generic, not AI-native"):** **Dangerously dismissive.** Microsoft Copilot for M365 is deeply integrated into Teams. Whether it is "AI-native" or not is irrelevant to an enterprise buyer. Copilot has access to the Microsoft Graph (meaning it cross-references meetings with the company's emails, chats, and documents). This is a massive enterprise feature that a standalone startup cannot easily replicate.
*   **Zoom IQ ("Locked to Zoom ecosystem"):** **Partially true, but misses the point.** Yes, Zoom AI Companion (formerly Zoom IQ) only works on Zoom. However, enterprise teams usually standardize on *one* primary video conferencing platform. If an enterprise uses Zoom, Zoom AI Companion is a direct competitor that is currently **included at no extra cost** with paid Zoom accounts. Competing against "free and already installed" is incredibly difficult.

### 2. What competitors might they be missing?
The founders have a massive blind spot regarding the actual enterprise software landscape. They are entirely missing:

*   **The Revenue Intelligence ...
```

### Claude Opus 4.6

**Generation Time:** 0ms
**Tokens:** 0

```

```

### GPT-5.4

**Generation Time:** 0ms
**Tokens:** 0

```

```

### DeepSeek V3

**Generation Time:** 0ms
**Tokens:** 0

```

```

### MiMo-V2-Flash

**Generation Time:** 37512ms
**Tokens:** 1924

```
Here is a rigorous competitive analysis of the startup's pitch deck claim.

### Executive Summary
The claim "We have no direct competitors" is a **major red flag** for investors. It signals either a lack of market research or a deliberate attempt to mislead. While the startup may have a unique *feature combination*, they operate in a crowded and rapidly commoditizing market: **AI Meeting Intelligence**.

Below is the detailed breakdown.

---

### 1. Validity of Competitor Dismissals
The startup’s competitive slide uses classic "FUD" (Fear, Uncertainty, and Doubt) tactics to disqualify incumbents. Let’s evaluate the validity of each dismissal:

#### **Otter.ai**
*   **Claim:** "Consumer focused"
*   **Verdict:** **Partially Valid, but Dated.**
*   **Analysis:** Otter started as a consumer/transcription tool, but they have aggressively moved upmarket. They now offer "OtterPilot" for sales intelligence and enterprise-grade security (SSO, SCIM, encryption). While their brand may still feel "consumer-first," their feature set increasingly targets SMBs and mid-market teams.

#### **Fireflies.ai**
*   **Claim:** "No enterprise features"
*   **Verdict:** **Invalid.**
*   **Analysis:** This is factually incorrect. Fireflies offers robust enterprise features, including SOC 2 Type II compliance, SSO, role-based access control (RBAC), and retention policies. They are widely used in large sales and recruitment teams. Dismissing them as "not enterprise-ready" is a dangerous oversight.

#### **Microsoft Teams**
*   **Claim:** "Generic, not AI-native"
*   **Verdict:** **Valid (for now).**
*   **Analysis:** Microsoft’s native transcription is basic. However, the ecosystem is shifting. Microsoft is rapidly integrating Copilot into Teams (Microsoft 365 Copilot). While currently expensive and generic, Microsoft has the ultimate distribution advantage: it is pre-installed on every enterprise laptop. A standalone startup must offer significantly better accuracy or UX to justify a separat...
```

### Claude Sonnet 4.6

**Generation Time:** 0ms
**Tokens:** 0

```

```

### Grok 4.20

**Generation Time:** 0ms
**Tokens:** 0

```

```

### GPT-OSS-120B

**Generation Time:** 0ms
**Tokens:** 0

```

```

### Gemini 3 Flash Preview

**Generation Time:** 28920ms
**Tokens:** 1103

```
The claim **"We have no direct competitors"** is almost always a red flag for investors. In the case of AI-powered meeting summarization, it is demonstrably false.

Here is a rigorous analysis of the startup's claims and the reality of the market.

---

### 1. Are their dismissals of competitors valid?
**Mostly Invalid.** Their dismissals rely on outdated "category buckets" that no longer reflect the rapid product evolution in the AI space.

*   **Otter.ai ("Consumer focused"):** **Invalid.** Otter has an "Enterprise" tier with SSO, domain capture, and administrative controls. They are aggressively moving up-market into sales and executive workflows.
*   **Fireflies.ai ("No enterprise features"):** **Invalid.** Fireflies offers SOC2 Type II compliance, private storage options, and HIPAA compliance. To say they have "no enterprise features" is a factual inaccuracy that suggests the startup hasn't done deep due diligence.
*   **Microsoft Teams ("Generic, not AI-native"):** **Dangerous dismissal.** Teams Premium uses GPT-4 for "Intelligent Recap." Calling it "not AI-native" is a semantic argument that ignores the reality: most enterprises would rather use a built-in feature than buy a new seat for a third-party tool.
*   **Zoom IQ ("Locked to Zoom ecosystem"):** **Valid but weak.** While Zoom's AI Companion only works on Zoom, the vast majority of "Enterprise teams" are standardized on one platform. Being "platform agnostic" is a feature, not a moat.

### 2. What competitors are they missing?
The startup is ignoring the "Invisible Competitors" and the "Platform Giants" who are the real threats:

*   **Gong & Chorus:** These are the "heavyweights" of enterprise meeting intelligence. While focused on sales, they are expanding into "revenue operations" and internal collaboration. They already own the enterprise budget.
*   **Cisco Webex / Google Meet:** Both have integrated high-end LLM summarization.
*   **The "Big Four" Consulting/Internal builds:** Large enterprises (J...
```

### MiniMax M2.5

**Generation Time:** 34099ms
**Tokens:** 1655

```
# Rigorous Competitive Analysis: AI Meeting Summarization

## 1. Are Their Dismissals Valid?

| Competitor | Their Claim | Reality | Verdict |
|------------|-------------|---------|---------|
| **Otter.ai** | "Consumer focused" | Weak. Otter has enterprise plans, SSO, admin controls, and SOC 2 compliance. They acquired Fish Labs and market to enterprises. | **Partially invalid** |
| **Fireflies.ai** | "No enterprise features" | Weak. They offer enterprise security, compliance (HIPAA, SOC 2), and admin dashboards. | **Invalid** |
| **Microsoft Teams** | "Generic, not AI-native" | Invalid. Teams Copilot provides real-time meeting summarization, action item extraction, and is deeply integrated into the enterprise stack. | **Invalid** |
| **Zoom IQ** | "Locked to Zoom ecosystem" | Fair point, but narrow. Many companies use Zoom. This only dismisses Zoom-centric customers. | **Partially valid** |

**Key finding:** Three of their four competitor dismissals are weak or false. This is a red flag for due diligence.

---

## 2. Missing Competitors

They are missing significant players:

**Direct Competitors (Meeting-specific AI):**
- **Fathom** – Fast-growing, strong Zoom/Teams integration, free tier
- **Sembly** – AI meeting assistant with multi-language support
- **Avoma** – Complete meeting lifecycle platform
- **TL;DV** – Meeting recorder with AI notes
- **Notta** – AI meeting note-taker

**Adjacent Competitors (Broader platforms with meeting AI):**
- **Notion** – AI meeting notes, Q&A across docs
- **Confluence (Atlassian)** – AI-powered meeting insights
- **Gong / Chorus** – Revenue intelligence from calls (deeper enterprise penetration)
- **Fellow** – Meeting management with AI insights

**Platform Giants (Can add AI anytime):**
- **Google Meet** – Gemini integration coming fast
- **Slack** – AI-native workplace with Huddles
- **Salesforce + Slack** – Einstein AI across the stack

---

## 3. The Real Competitive Landscape

```
Enterprise Meeting AI Landscape

┌────────...
```

---

*Generated by The Multivac V5*
*https://themultivac.com*