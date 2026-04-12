# Multivac Evaluation Report

**Evaluation ID:** EVAL-20260402-201915
**Timestamp:** 2026-04-02T20:19:15.812289
**Category:** Analysis & Research
**Model Pool:** 10 analysis-optimized models

## Question

Estimate the total energy cost and carbon footprint of training a frontier AI model (like GPT-5). Include: GPU hours, electricity cost, cooling overhead, water usage, and embodied carbon of hardware. (1) Compare to: one year of Netflix streaming for all users, one transatlantic flight, and one Bitcoin transaction. (2) Inference costs are growing faster than training costs. Why? (3) What changes would reduce AI's environmental impact by 10x?

---

## Rankings

| Rank | Model | Score | Min | Max | Std Dev |
|------|-------|-------|-----|-----|---------|
| 1 | Grok 4.20 | 8.62 | 8.15 | 9.55 | 0.47 |
| 2 | Gemini 3 Flash Preview | 8.24 | 7.50 | 9.65 | 0.77 |
| 3 | MiMo-V2-Flash | 8.02 | 6.95 | 9.00 | 0.78 |
| 4 | MiniMax M2.5 | 7.91 | 6.55 | 9.00 | 0.84 |
| 5 | GPT-5.4 | 7.58 | 5.85 | 9.20 | 1.21 |
| 6 | Claude Opus 4.6 | 7.21 | 5.00 | 9.00 | 1.29 |
| 7 | Claude Sonnet 4.6 | 6.93 | 4.45 | 8.45 | 1.26 |
| 8 | DeepSeek V3 | 6.43 | 4.55 | 8.30 | 1.35 |
| 9 | GPT-OSS-120B | 6.03 | 2.60 | 8.55 | 2.06 |
| 10 | Gemini 3.1 Pro | 2.93 | 0.65 | 6.20 | 1.97 |

---

## Meta Analysis

### Judge Strictness

| Rank | Judge | Avg Score Given |
|------|-------|-----------------|
| 1 | GPT-5.4 | 5.35 |
| 2 | GPT-OSS-120B | 6.33 |
| 3 | Claude Opus 4.6 | 6.42 |
| 4 | Grok 4.20 | 6.44 |
| 5 | Gemini 3.1 Pro | 6.86 |
| 6 | MiniMax M2.5 | 6.87 |
| 7 | Claude Sonnet 4.6 | 7.31 |
| 8 | MiMo-V2-Flash | 7.88 |
| 9 | Gemini 3 Flash Preview | 7.97 |
| 10 | DeepSeek V3 | 8.42 |

**Strictest Judge:** gpt_5_4
**Most Lenient Judge:** deepseek_v4
**Total Judgments:** 100
**Valid Judgments:** 89

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

**Generation Time:** 21738ms
**Tokens:** 2140

```
Estimating the energy cost and carbon footprint of a frontier AI model (like a hypothetical GPT-5) requires projecting current trends in AI hardware scaling. While companies like OpenAI and Google do not publish exact specifications, we can make highly educated estimates based on the hardware required to achieve the next leap in capabilities.

Here is a comprehensive breakdown of the estimated environmental impact of training a frontier AI model, followed
```

### Claude Opus 4.6

**Generation Time:** 49815ms
**Tokens:** 2156

```
# The Full Environmental Cost of Training a Frontier AI Model

## Part 1: Estimating the Total Cost of Training a GPT-5-Class Model

### Establishing the Baseline

We need to work from what's publicly known and make principled extrapolations. GPT-4 reportedly used ~2.15e25 FLOPs across ~25,000 A100 GPUs over roughly 90-100 days. Frontier models currently in training (GPT-5 class, circa 2024-2025) are estimated at 5-10x that compute budget, using newer H100/B200 hardware.

**I'll estimate for a model requiring ~1e26 FLOPs trained on ~30,000 H100 GPUs.**

---

### GPU Hours

```
GPUs:                    ~30,000 H100s (a realistic 2024-25 cluster)
Training duration:       ~90-120 days
GPU-hours:               30,000 × 100 days × 24 hrs = ~72 million GPU-hours
Effective utilization:   ~40-50% MFU (model FLOP utilization)
Total calendar time:     ~3-4 months of continuous operation
```

Note: "72 million GPU-hours" sounds enormous, but low MFU means a significant fraction is spent on communication overhead, pipeline bubbles, and checkpointing. The *useful* compute is perhaps 35-40 million GPU-hours equivalent.

---

### Electricity: Direct Compute

```
H100 TDP:                         700W per GPU
Actual average draw under training: ~600-650W (not always at peak)
Compute power draw:               30,000 × 625W = 18.75 MW
Duration:                         100 days = 2,400 hours
Direct compute energy:            18.75 MW × 2,400 hrs = 45,000 MWh
```

But GPUs aren't the only load. Networking (InfiniBand switches, ~3-5% overhead), CPU hosts, storage I/O, and other infrastructure add roughly 10-15%:

```
Total IT load:                    ~50,000-52,000 MWh
```

---

### Cooling Overhead (PUE)

Power Usage Effectiveness (PUE) captures total facility energy divided by IT energy. Hyperscaler data centers achieve PUE of 1.1-1.3. GPU-dense training clusters run hotter and often land at the higher end.

```
Assumed PUE:                      1.25 (realistic for a dense GPU cluster...
```

### GPT-5.4

**Generation Time:** 34962ms
**Tokens:** 2151

```
Below is a **reasoned estimate** for a **frontier AI model** in the “GPT-5-class” range. Since exact numbers are not public, I’ll give **credible ranges**, show the assumptions, and compare them to other familiar activities.

---

## Executive summary

A plausible training run for a frontier model today might involve:

- **Compute:** about **10–100 million GPU-hours**
- **Electricity use:** about **10–150 GWh**
- **Electricity cost:** about **$1M–$15M** for power alone
- **Cooling overhead (via PUE):** adds roughly **10–40%**
- **Water use:** about **10–200 million liters**, depending heavily on data center design and climate
- **Operational CO2e:** about **5,000–70,000 tCO2e**, depending mostly on grid cleanliness
- **Embodied carbon of hardware used for the run:** about **1,000–10,000 tCO2e** attributable to the training cluster/run

A central estimate for one major frontier training run is roughly:

- **25 million GPU-hours**
- **~35 GWh total electricity**
- **~$3–5M electricity**
- **~20 million liters water**
- **~10,000–20,000 tCO2e total**, including hardware share

That is **huge**, but often still smaller than the cumulative footprint of serving billions of inference requests over time.

---

# 1) Estimate the total energy cost and carbon footprint of training a frontier AI model

## A. GPU-hours

A frontier run could plausibly use:

- **10,000–50,000 GPUs**
- for **30–120 days**

So GPU-hours are roughly:

- Low: 10,000 × 24 × 45 days = **10.8 million GPU-hours**
- Mid: 25,000 × 24 × 60 days = **36 million GPU-hours**
- High: 50,000 × 24 × 90 days = **108 million GPU-hours**

### Plausible range:
**10–100 million GPU-hours**

That is the right order of magnitude for a frontier model training campaign.

---

## B. Electricity use

Assume modern AI accelerators draw roughly:

- **0.5–1.2 kW per GPU** in real training conditions
- plus CPU, networking, storage, etc.
- plus cooling/data-center overhead

A useful way is to estimate full-system power per GPU-eq...
```

### DeepSeek V3

**Generation Time:** 69323ms
**Tokens:** 1039

```
### **Estimating the Energy Cost and Carbon Footprint of Training a Frontier AI Model (e.g., GPT-5)**  

Training large AI models like GPT-5 requires massive computational resources, leading to significant energy consumption and carbon emissions. Here’s a breakdown:

#### **1. Training Costs**  
- **GPU Hours**: Estimates suggest GPT-3 (~175B params) required ~3.14 × 10²³ FLOPs (~1,000 petaFLOP-days). GPT-5 (~10x larger?) could require **~10,000 petaFLOP-days** (~3.65 × 10²⁴ FLOPs).  
  - Assuming NVIDIA H100 GPUs (~4,000 FLOPs/W efficiency), training could take **~100M GPU hours**.  
- **Electricity Cost**:  
  - Power draw: ~6W per petaFLOP → ~6 × 10¹⁵ J (~1.67M kWh).  
  - At $0.10/kWh → **~$167M in electricity**.  
- **Cooling Overhead**: Data centers add ~40% energy overhead → **~2.34M kWh**.  
- **Water Usage**: Cooling consumes ~0.5L per kWh → **~1.17M liters**.  
- **Embodied Carbon (Hardware)**: Manufacturing GPUs emits ~250kg CO₂ per GPU → **~25,000 tons CO₂** (assuming 100,000 GPUs).  
- **Total Carbon Footprint**:  
  - Electricity: ~1.67M kWh × 0.4 kg CO₂/kWh (global avg.) → **~670 tons CO₂**.  
  - Including embodied carbon → **~25,670 tons CO₂**.  

*(Note: Estimates vary widely; some suggest GPT-3 emitted ~500 tons CO₂, while GPT-5 could be 10-100x higher.)*  

#### **Comparisons**  
| Activity                  | Energy/Carbon Cost             |
|---------------------------|---------------------------------|
| **GPT-5 Training**        | ~25,670 tons CO₂               |
| **Netflix (1 year, all users)** | ~1.2B kWh (~480,000 tons CO₂) |
| **Transatlantic Flight**  | ~1 ton CO₂ per passenger       |
| **Bitcoin Transaction**   | ~500 kWh (~200 kg CO₂)         |

**Key Insight**:  
- Training GPT-5 emits **~25,000x a flight**, **~0.05x Netflix yearly**, and **~128,350x a Bitcoin transaction**.  
- However, inference costs dominate long-term (see below).  

---

### **2. Why Are Inference Costs Growing Faster Than Training?**  
- **Scale of Deployment**...
```

### MiMo-V2-Flash

**Generation Time:** 17702ms
**Tokens:** 2185

```
Here is an estimation of the environmental and energy costs of training a frontier AI model (e.g., GPT-5 class), followed by comparisons, an analysis of inference growth, and strategies for reduction.

***

### 1. Estimation: Training a Frontier AI Model

Training a frontier model (e.g., 1–2 trillion parameters, trained on 10–20 trillion tokens) requires massive compute clusters. Below are estimates based on current hardware (NVIDIA H100/H200 GPUs) and public data from sources like Epoch AI, the IEA, and academic papers on LLM scaling.

#### A. GPU Hours & Compute
*   **Hardware:** ~10,000–25,000 NVIDIA H100 GPUs.
*   **Duration:** ~90–180 days (2,160–4,320 hours).
*   **Total GPU Hours:** **~40 million GPU hours** (assuming 15,000 GPUs for 90 days).
*   **Energy Consumption:** H100s draw ~700W peak (including server overhead). Total power draw for the cluster is ~10–15 MW.
*   **Total Electricity:** **~60–70 GWh** (Gigawatt-hours).

#### B. Electricity Cost
*   **Commercial Rate:** ~$0.10–$0.15 per kWh (varies by region/data center).
*   **Total Cost:** **$6M – $10.5M** for electricity alone.
*   *Note: Total training cost (including labor, R&D, and infrastructure) is often 3–5x higher, estimated at $50M–$100M.*

#### C. Cooling Overhead (PUE)
*   **PUE (Power Usage Effectiveness):** Modern hyperscale data centers have a PUE of ~1.1–1.2 (meaning for every 1 kW of compute, 1.1–1.2 kW is used total, including cooling and power distribution).
*   **Cooling Energy:** **~6–14 GWh** (additional to compute load).
*   **Water Usage:** Cooling towers evaporate water to reject heat.
    *   *Water Consumption Intensity:* ~1.8 L per kWh of IT load.
    *   *Total Water:* **~110–130 million liters** (roughly 45 Olympic swimming pools).
    *   *Note: This is "consumption," not just withdrawal. Water stress in the local region (e.g., Iowa vs. Arizona) drastically changes the impact.*

#### D. Embodied Carbon of Hardware
Hardware doesn’t just run on electricity; it is manufactur...
```

### Claude Sonnet 4.6

**Generation Time:** 40976ms
**Tokens:** 2155

```
# AI's Environmental Footprint: A Rigorous Estimate

## Upfront Epistemics

**Confidence levels vary dramatically here.** Companies don't publish training details, so I'm working from: leaked information, research papers, energy pricing data, and scaling laws. I'll flag where I'm extrapolating versus where I have solid grounding. Some numbers will be wrong by 2-3x — that's the honest state of knowledge.

---

## Part 0: Establishing the Baseline — What Does Training a Frontier Model Cost?

### What We Actually Know

| Model | Compute (FLOPs) | Source |
|-------|-----------------|--------|
| GPT-3 (175B) | ~3.1 × 10²³ | OpenAI paper |
| PaLM (540B) | ~2.5 × 10²⁴ | Google paper |
| GPT-4 (est.) | ~2-8 × 10²⁴ | Leaked/estimated |
| Llama 3 405B | ~3.8 × 10²⁵ | Meta paper (tokens × params) |
| Frontier 2025 model | **~10²⁵ - 10²⁶** | Extrapolation |

I'll use **10²⁵ FLOPs** as my working estimate for a current frontier model — roughly GPT-4 scale. This is probably conservative for the most capable 2025 models.

### GPU Hours

```
H100 GPU: ~2 × 10¹⁵ FLOPs/second (BF16, theoretical)
Achievable utilization: ~35-45% (memory bandwidth, communication overhead)
Effective throughput: ~7 × 10¹⁴ FLOPs/second

GPU-seconds = 10²⁵ / (7 × 10¹⁴) = 1.43 × 10¹⁰ seconds
GPU-hours = ~4 × 10⁶ GPU-hours = 4 million GPU-hours

At scale (10,000 H100s running in parallel):
Wall-clock time = 400,000 hours / 10,000 GPUs = 40 hours... 

Wait, that's wrong. Let me redo this properly.
```

**Corrected calculation:**

```
4 million GPU-hours / 10,000 GPUs = 400 hours wall-clock ≈ 17 days

This is plausible for a single training run, but frontier models:
- Run multiple experiments/ablations (10-50x the final run)
- Have failed runs, restarts, hyperparameter sweeps
- Do RLHF/fine-tuning on top

Realistic total GPU-hours including all overhead: 
20-100 million GPU-hours
```

**Working estimate: ~50 million H100 GPU-hours for full training pipeline**

*This feels high but aligns with reports that GPT-4...
```

### Grok 4.20

**Generation Time:** 9868ms
**Tokens:** 1776

```
**Estimated Environmental Cost of Training a Frontier AI Model (like GPT-5)**

These are informed estimates based on scaling trends from GPT-4 (2023), Llama 3 405B, and early 2025 frontier systems. A "GPT-5 class" model is assumed to be in the 3–10× compute scale of GPT-4 (which itself was roughly 2–3× GPT-3 in effective training compute).

### Best-estimate numbers for one full training run (mid-2025 hardware)

- **Training compute**: ~3 × 10²⁶ FLOPs (roughly 5–8× GPT-4)
- **GPU/Accelerator hours**: 8–15 million H100-equivalent GPU-hours  
  (Equates to ~25,000–40,000 H100s running for 3–5 months)
- **Electricity consumption (direct IT load)**: 60–110 GWh
- **Total electricity with cooling & overhead (PUE 1.25–1.35 typical for new AI clusters)**: **90–150 GWh**
- **Electricity cost** (at $0.08–0.12/kWh, common for hyperscalers with power purchase agreements): **$8–16 million**
- **Water usage (cooling)**: 1.5–3.5 million gallons (5,700–13,000 m³) for a single training run, assuming evaporative cooling in a mid-sized data center. This is highly variable — some facilities use dry cooling or direct liquid cooling with far lower water use.
- **Embodied carbon of hardware**: Very high. Training one frontier model typically requires the equivalent of 15,000–30,000 H100 GPUs (plus networking, servers, etc.).  
  Embodied carbon per H100 is ~2,000–3,500 kg CO₂e (manufacturing + shipping).  
  **Total embodied carbon**: ~40,000–90,000 tCO₂e (metric tons), depending on whether you amortize across many training runs or count the full hardware as dedicated to this model.

**Total carbon footprint (operational + embodied)**: **60,000–140,000 tCO₂e**  
(Assumes average U.S. grid intensity of ~400 gCO₂e/kWh or better regional grids ~250–350 gCO₂e/kWh used by Microsoft/Google. If run on coal-heavy grids, this can double.)

These numbers are in the same ballpark as independent estimates from Epoch AI, Hugging Face, and academic papers published 2024–2025.

### (1) Comparisons

- **...
```

### GPT-OSS-120B

**Generation Time:** 8351ms
**Tokens:** 2212

```
## 1.  What does it take to train a “frontier” model (e.g., a GPT‑5‑class, ~1 trillion‑parameter transformer)?

| Item | Typical value for a GPT‑5‑scale run | How the number is obtained |
|------|------------------------------------|----------------------------|
| **Model size** | 1 × 10¹² parameters (≈ 4 TB FP16 weights) | Public speculation on next‑generation LLMs |
| **Training tokens** | 5 × 10¹³ (≈ 500 B tokens) | 10 × the token count used for GPT‑4 (≈ 100 B) |
| **GPU type** | NVIDIA H100 (40 GB) – 500 W TDP (average 350 W under load) | H100 is the current flagship for large‑scale training |
| **Number of GPUs** | 1 200 (≈ 12 pods of 100 GPUs each) | Roughly the size of the “Azure AI super‑cluster” used for GPT‑4 |
| **Training duration** | 90 days (≈ 2 160 h) of continuous operation | 3 months is the typical window for a full‑scale run |
| **Total GPU‑hours** | 1 200 × 2 160 h = 2.59 × 10⁶ GPU‑h | Direct multiplication |
| **Energy per GPU‑hour** | 0.35 kWh (350 W × 1 h) | Avg. power draw under training load |
| **Raw compute energy** | 2.59 × 10⁶ GPU‑h × 0.35 kWh ≈ 9.1 × 10⁵ kWh | 0.91 GWh |
| **PUE (Power‑Usage‑Effectiveness)** | 1.25 (typical for modern hyperscale data centers) | 1.0 = no overhead; 1.25 = 25 % extra for cooling, power‑distribution, etc. |
| **Total facility electricity** | 0.91 GWh × 1.25 ≈ 1.14 GWh | Includes cooling & ancillary loads |
| **Electricity cost** | $0.10 /kWh (average US/Europe wholesale price) | Approx. price for large‑scale contracts |
| **Total electricity bill** | 1.14 GWh × $0.10 ≈ $114 M | 1 GWh = 10⁶ kWh |
| **Water used for cooling** | ≈ 0.5 L /kWh (evaporative/adsorption cooling) | Industry average for water‑cooled data centers |
| **Total water consumption** | 1.14 GWh × 0.5 L/kWh ≈ 5.7 × 10⁵ L (≈ 570 m³) | Rough but useful for comparison |
| **CO₂e from electricity** | 0.45 kg CO₂/kWh (global average grid mix) | IEA 2023 average; lower if renewable‑heavy region |
| **CO₂e from compute** | 1.14 GWh × 0.45 ≈ 5.1 × 10...
```

### Gemini 3 Flash Preview

**Generation Time:** 7824ms
**Tokens:** 1154

```
Estimating the footprint of a "frontier model" (GPT-5 class) requires extrapolating from known data about GPT-4 and Llama-3 (405B). While exact figures are proprietary, industry consensus suggests a ~10x scaling factor from the previous generation.

### 1. Estimated Impact of Training a Frontier Model

| Metric | Estimated Value | Notes |
| :--- | :--- | :--- |
| **GPU Hours** | ~50–100 Million H100 hours | Based on clusters of 50k–100k GPUs running for months. |
| **Electricity Consumption** | ~200–400 GWh | Includes compute + data center overhead. |
| **Electricity Cost** | ~$20M – $40M | Based on industrial rates (~$0.10/kWh). |
| **Cooling Overhead (PUE)** | 1.1 to 1.5 | Modern AI DCs are efficient (1.1), but older ones lag. |
| **Water Usage** | ~150–300 Million Liters | Combined direct cooling + offsite power generation water. |
| **Carbon Footprint** | ~50,000 – 100,000 tCO2e | Highly dependent on the grid (e.g., Iowa vs. Virginia). |
| **Embodied Carbon** | ~20,000 – 40,000 tCO2e | The carbon cost of manufacturing 50k+ H100 GPUs and servers. |

#### Comparative Context:
*   **One Transatlantic Flight:** ~1 tonne CO2e per passenger. Training one frontier model equals roughly **75,000 passenger flights** from NYC to London.
*   **One Bitcoin Transaction:** ~400–700 kg CO2e. Training one model equals roughly **150,000 Bitcoin transactions**.
*   **Netflix Global Streaming (1 Year):** Netflix consumes ~11,000 GWh annually across its operations and delivery. Training one frontier model is roughly **2–4% of Netflix's entire annual global energy footprint.**

---

### 2. Why Inference Costs are Outpacing Training Costs

While training a model is a massive "one-time" energy spike, inference (the daily use of the model) is cumulative and growing exponentially for three reasons:

1.  **Scale of Adoption:** Training happens once. Inference happens every time a user types a prompt. With hundreds of millions of daily active users across ChatGPT, Gemini, and Copilot, the ...
```

### MiniMax M2.5

**Generation Time:** 57709ms
**Tokens:** 2181

```
Excellent and important questions. Estimating the impact of frontier AI models involves significant uncertainty due to proprietary data, but we can use industry benchmarks and known scaling trends to provide reasonable estimates.

Here is a detailed breakdown and analysis.

### **1. Estimated Training Cost & Carbon Footprint for a Frontier Model (e.g., GPT-5)**

We will assume a next-generation model trained with ~5x the compute of GPT-4, using the most advanced hardware (NVIDIA H100 GPUs).

*   **Hardware Scale:** 50,000 GPUs (H100) running for ~120 days.
*   **GPU Hours:** 50,000 GPUs * 24 hours * 120 days = **144 million GPU-hours**.
*   **Electricity Cost:**
    *   Each H100 consumes ~700W under load.
    *   Total power: 50,000 * 0.7 kW = 35,000 kW = 35 MW.
    *   Energy: 35 MW * 24 hours * 120 days = **100,800 MWh** (100.8 GWh).
    *   At $0.10/kWh (average US industrial rate), electricity cost: **~ $10 million**.
*   **Cooling & Facility Overhead:** Data center PUE (Power Usage Effectiveness) is typically 1.1-1.4. Using an average PUE of 1.2, total facility energy is 100,800 MWh * 1.2 = **120,960 MWh**. The added cost for cooling is the difference (~20,160 MWh), costing an additional **~$2 million**.
*   **Water Usage:** Evaporative cooling for a 35 MW facility uses ~1-2 gallons per kWh. Estimated water usage: 120,960 MWh * 1.5 gallons/kWh ≈ **181 million gallons** (~686 million liters), enough to fill ~275 Olympic swimming pools.
*   **Embodied Carbon of Hardware:**
    *   Each H100 GPU has an estimated embodied carbon of ~400-600 kg CO2e.
    *   50,000 GPUs = 50,000 * 500 kg = **25,000 tonnes CO2e**.
    *   This is amortized over the hardware's ~5-year lifespan, but for training a single model, we can attribute a large fraction (e.g., 50%) during the training period: **~12,500 tonnes CO2e**.

**Total Estimated Training Footprint:**
*   **Electricity (Facility):** 120,960 MWh
*   **Carbon Emissions:** ~50,000 - 70,000 tonnes CO2e (depending on grid car...
```

---

*Generated by The Multivac V5*
*https://themultivac.com*