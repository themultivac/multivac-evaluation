# Multivac Evaluation Report

**Evaluation ID:** EVAL-20260402-175350
**Timestamp:** 2026-04-02T17:53:50.687216
**Category:** Reasoning & Logic
**Model Pool:** 10 reasoning-optimized models

## Question

Achilles gives a tortoise a 100-meter head start. Achilles runs at 10 m/s, the tortoise at 1 m/s. Zeno argues Achilles can never catch the tortoise because he must first reach where the tortoise was, but by then the tortoise has moved. (1) Resolve the paradox using limits. (2) Resolve it without calculus — using only physical reasoning. (3) Is there a version of Zeno's paradox that modern physics cannot fully resolve? (Hint: consider Planck length.)

---

## Rankings

| Rank | Model | Score | Min | Max | Std Dev |
|------|-------|-------|-----|-----|---------|
| 1 | GPT-OSS-120B | 9.38 | 8.65 | 10.00 | 0.45 |
| 2 | Claude Sonnet 4.6 | 9.29 | 8.45 | 10.00 | 0.62 |
| 3 | MiMo-V2-Flash | 9.19 | 8.55 | 10.00 | 0.53 |
| 4 | Claude Opus 4.6 | 9.10 | 8.50 | 9.85 | 0.48 |
| 5 | GPT-5.4 | 8.99 | 8.45 | 10.00 | 0.47 |
| 6 | Gemini 2.5 Flash | 8.90 | 8.40 | 9.65 | 0.42 |
| 7 | Grok 4.20 | 8.89 | 8.45 | 9.20 | 0.32 |
| 8 | DeepSeek V3 | 8.80 | 8.00 | 9.65 | 0.45 |
| 9 | Gemini 3.1 Pro | 6.71 | 3.65 | 8.25 | 1.63 |
| 10 | MiniMax M2.5 | 4.29 | 1.55 | 8.45 | 2.68 |

---

## Meta Analysis

### Judge Strictness

| Rank | Judge | Avg Score Given |
|------|-------|-----------------|
| 1 | GPT-5.4 | 7.38 |
| 2 | Grok 4.20 | 7.97 |
| 3 | Claude Opus 4.6 | 8.08 |
| 4 | Claude Sonnet 4.6 | 8.22 |
| 5 | GPT-OSS-120B | 8.25 |
| 6 | MiniMax M2.5 | 8.71 |
| 7 | Gemini 3.1 Pro | 8.73 |
| 8 | Gemini 2.5 Flash | 8.91 |
| 9 | MiMo-V2-Flash | 8.99 |
| 10 | DeepSeek V3 | 9.02 |

**Strictest Judge:** gpt_5_4
**Most Lenient Judge:** deepseek_v4
**Total Judgments:** 100
**Valid Judgments:** 88

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

**Generation Time:** 29042ms
**Tokens:** 2155

```
Here is the resolution to Zeno's paradox in three parts, ranging from mathematics to classical physics, and finally to the frontiers of modern quantum mechanics.

### 1. Resolving the Paradox Using Limits (Calculus/Mathematics)
Zeno’s argument relies on a mathematical trick: he breaks a finite distance into an infinite number of increasingly smaller steps. The paradox assumes that an infinite number of steps must take an infinite amount of time to complete. Calculus, specifically the concept of infinite series and limits, proves this assumption false.

Let's calculate the time it takes for Achilles to complete each step Zeno describes:
*   **Step 1:** Achilles runs the 100 m head start. At 10 m/s, this takes **10 seconds**. (In this time, the tortoise moves 10 m).
*   **Step 2:** Achilles runs that 10 m. This takes **1 second**. (The tortoise moves 1 m).
*   **Step 3:** Achilles runs that 1 m. This takes **0.1 seconds**. (The tortoise moves 0.1 m).

The total time $T$ it takes for Achilles to catch the tortoise is the sum of these times:
$T = 10 + 1 + 0.1 + 0.01 + 0.001 + \dots$

This is a geometric series. The formula for the sum of an infinite geometric series is $S = \frac{a}{1 - r}$, where $a$ is the first term (10) and $r$ is the common ratio (0.1). 
$T = \frac{10}{1 - 0.1} = \frac{10}{0.9} = \frac{100}{9} \approx 11.11 \text{ seconds.}$

Using limits, we mathematically prove that an infinite number of decreasing time intervals converges to a strictly finite number. Achilles catches the tortoise at exactly 11.11 seconds, at the 111.11-meter mark.

### 2. Resolving the Paradox Without Calculus (Physical Reasoning)
Zeno’s paradox is ultimately an optical illusion of language; it forces you to look at the race from an unnatural, distorted frame of reference. We can resolve it using basic, continuous physical kinematics
```

### DeepSeek V3

**Generation Time:** 26642ms
**Tokens:** 1376

```
### (1) Resolving the Paradox Using Limits

**Understanding the Paradox:**
Zeno's paradox of Achilles and the tortoise presents a scenario where Achilles, despite being faster, can never overtake the tortoise because he must first reach the point where the tortoise started, by which time the tortoise has moved forward. This process repeats indefinitely, suggesting Achilles never catches up.

**Mathematical Setup:**
- Initial head start for the tortoise: 100 meters.
- Achilles' speed: 10 m/s.
- Tortoise's speed: 1 m/s.

**Relative Speed Approach:**
Achilles gains on the tortoise at a rate equal to the difference in their speeds:
Relative speed = Achilles' speed - Tortoise's speed = 10 m/s - 1 m/s = 9 m/s.

Time taken to catch up:
Time = Distance / Relative speed = 100 m / 9 m/s ≈ 11.11 seconds.

Distance Achilles covers in this time:
Distance = Speed × Time = 10 m/s × 11.11 s ≈ 111.11 meters.

So, Achilles catches the tortoise after running approximately 111.11 meters, which takes about 11.11 seconds.

**Limit Approach:**
Zeno's argument breaks the race into an infinite series of steps where Achilles reaches the tortoise's previous position:

1. Achilles runs 100 m to where the tortoise started. Time: 100 m / 10 m/s = 10 s. Tortoise moves: 1 m/s × 10 s = 10 m. New distance: 10 m.
2. Achilles runs 10 m. Time: 10 m / 10 m/s = 1 s. Tortoise moves: 1 m/s × 1 s = 1 m. New distance: 1 m.
3. Achilles runs 1 m. Time: 1 m / 10 m/s = 0.1 s. Tortoise moves: 1 m/s × 0.1 s = 0.1 m. New distance: 0.1 m.
... and so on.

Total time taken is the sum of this infinite series:
10 + 1 + 0.1 + 0.01 + ... seconds.

This is a geometric series: S = a / (1 - r), where a = 10, r = 0.1.
S = 10 / (1 - 0.1) = 10 / 0.9 ≈ 11.11 seconds.

Total distance Achilles runs is similarly:
100 + 10 + 1 + 0.1 + ... meters.
This is 100 / (1 - 0.1) ≈ 111.11 meters.

**Conclusion:**
The infinite series converges to a finite sum, meaning Achilles catches the tortoise in finite time and distance. The paradox arise...
```

### Claude Opus 4.6

**Generation Time:** 40477ms
**Tokens:** 2100

```
# Resolving Zeno's Paradox

## Part 1: Resolution Using Limits

Zeno constructs an infinite sequence of "catch-up" events:

| Stage | Achilles reaches... | Tortoise has moved to... | Distance remaining |
|-------|-------------------|--------------------------|-------------------|
| 1 | 100 m | 110 m | 10 m |
| 2 | 110 m | 111 m | 1 m |
| 3 | 111 m | 111.1 m | 0.1 m |
| n | ... | ... | 100/(10ⁿ⁻¹) m |

**The distance Achilles must cover across all stages:**

$$S = 100 + 10 + 1 + 0.1 + \cdots = \sum_{n=0}^{\infty} 100 \cdot \left(\frac{1}{10}\right)^n$$

This is a geometric series with ratio $r = \frac{1}{10}$:

$$S = \frac{100}{1 - \frac{1}{10}} = \frac{100}{\frac{9}{10}} = \frac{1000}{9} \approx 111.11 \text{ m}$$

**The time elapsed across all stages:**

$$T = 10 + 1 + 0.1 + \cdots = \sum_{n=0}^{\infty} 10 \cdot \left(\frac{1}{10}\right)^n = \frac{10}{1 - \frac{1}{10}} = \frac{100}{9} \approx 11.11 \text{ s}$$

**The core resolution:** Zeno's error is the implicit assumption that *an infinite sum of positive terms must be infinite*. The rigorous definition of a limit shows:

$$\lim_{N \to \infty} \sum_{n=0}^{N} ar^n = \frac{a}{1-r} \quad \text{for } |r| < 1$$

An infinite number of steps can sum to a **finite** quantity. Achilles catches the tortoise at exactly $\frac{1000}{9}$ meters in exactly $\frac{100}{9}$ seconds.

**Verification by direct algebra:**
Position of Achilles: $x_A(t) = 10t$
Position of tortoise: $x_T(t) = 100 + t$

Setting equal: $10t = 100 + t \implies t = \frac{100}{9}$ s, at position $\frac{1000}{9}$ m. ✓

---

## Part 2: Resolution Without Calculus — Pure Physical Reasoning

No infinite series or limits are needed. The resolution is almost embarrassingly direct:

**The frame-shift argument:**
Stand in Achilles' reference frame. From his perspective, forget the ground entirely. He sees a tortoise 100 meters ahead, and that tortoise is *approaching him* at a relative speed of:

$$v_{\text{rel}} = 10 - 1 = 9 \text{ m/s}$$

A gap of 100 m closing...
```

### GPT-5.4

**Generation Time:** 18367ms
**Tokens:** 1055

```
1) Using limits

Let \(t=0\) when Achilles starts and the tortoise is 100 m ahead.

- Achilles’ position:  
  \[
  x_A(t)=10t
  \]
- Tortoise’s position:  
  \[
  x_T(t)=100+1t
  \]

Achilles catches the tortoise when \(x_A=x_T\):
\[
10t=100+t
\]
\[
9t=100
\]
\[
t=\frac{100}{9}\text{ s}\approx 11.11\text{ s}
\]

So Achilles does catch the tortoise.

Zeno’s step-by-step argument can also be written as an infinite series:

- Time for Achilles to reach the tortoise’s starting point:
  \[
  100/10=10\text{ s}
  \]
- In that time the tortoise moves 10 m more.
- Time to cover those 10 m:
  \[
  10/10=1\text{ s}
  \]
- Then the tortoise moves 1 m more.
- Time to cover that:
  \[
  1/10=0.1\text{ s}
  \]
- etc.

Total time:
\[
10+1+0.1+0.01+\cdots
\]

This is a geometric series with ratio \(1/10\), so
\[
10+1+0.1+\cdots = \frac{10}{1-1/10}=\frac{10}{9/10}=\frac{100}{9}
\]

Thus infinitely many “tasks” can have a finite total duration. That is the mathematical resolution: the limit of the partial sums exists and is finite.

---

2) Without calculus — physical reasoning only

The key physical fact is relative speed.

Achilles gains on the tortoise at:
\[
10-1=9\text{ m/s}
\]

The tortoise starts 100 m ahead. If Achilles closes the gap by 9 meters every second, then the time needed is:

\[
\frac{100}{9}\text{ s}
\]

No paradox remains. Zeno’s mistake is treating “there are infinitely many smaller catch-up stages” as if that means “it takes infinite time.” Physically, that does not follow. The stages get shorter and shorter in both distance and time.

A simple analogy: to walk across a room, you can describe the trip as first half the room, then half the remainder, then half again, and so on forever. That does not mean you never reach the other side. It just means one motion can be subdivided into endlessly many conceptual parts.

So physically:

- Achilles is faster.
- The distance between them shrinks steadily.
- Once the shrinking distance reaches zero, Achilles catches the ...
```

### Grok 4.20

**Generation Time:** 4856ms
**Tokens:** 1014

```
**1. Resolution using limits (calculus)**

Achilles closes the gap in an infinite series of ever-smaller intervals, but the sum of the series is finite.

- Time for Achilles to reach tortoise’s starting point: 100 m / 10 m/s = 10 s. In that time the tortoise has moved 10 m.
- Time to cover the new 10 m gap: 10 m / 10 m/s = 1 s. Tortoise moves 1 m further.
- Time for next 1 m gap: 0.1 s, tortoise moves 0.1 m, and so on.

The total time is the infinite geometric series:

t = 10 + 1 + 0.1 + 0.01 + … = 10 × (1 + 0.1 + 0.01 + …) = 10 × (1 / (1 − 0.1)) = 10 / 0.9 ≈ 11.111… s

The sum converges to a finite value. After ≈11.11 s Achilles has run exactly 111.11… m and catches the tortoise at the 111.11… m mark. The infinite number of “tasks” takes only a finite time because the time intervals shrink proportionally.

**2. Resolution without calculus — using only physical reasoning**

The paradox assumes that completing an infinite number of tasks must take an infinite amount of time. This assumption is false.

Achilles and the tortoise are both moving continuously through space at constant speeds. At every instant there is a well-defined distance between them that is steadily decreasing. There is no physical law that forbids a faster object from overtaking a slower one; we observe it constantly (a car passing a bicycle, a dog catching a rabbit, etc.).

The supposed “infinite tasks” are an arbitrary mental subdivision of a single continuous motion. Nature does not perform the tasks one after another like a computer executing a loop; the motion is seamless. The moment Achilles has covered the initial 100 m, the tortoise has moved 10 m; by the time Achilles covers that extra 10 m the tortoise has moved 1 m; and so on. All of these “stages” happen simultaneously in the single continuous interval of time. The infinite subdivision exists only in the description, not in the physical event. Therefore the conclusion that Achilles can never catch the tortoise is an artifact of the desc...
```

### Claude Sonnet 4.6

**Generation Time:** 30472ms
**Tokens:** 1660

```
# Zeno's Paradox: Three Resolutions

## Part 1: Resolution via Limits (Calculus)

### Setting Up the Infinite Series

Zeno's argument constructs an infinite sequence of "stages":

| Stage | Achilles runs | Time elapsed | Tortoise position |
|-------|--------------|--------------|-------------------|
| 1 | 100 m | 10 s | 110 m |
| 2 | 10 m | 1 s | 111 m |
| 3 | 1 m | 0.1 s | 111.1 m |
| n | $100/10^{n-1}$ m | $10/10^{n-1}$ s | ... |

The total time for infinitely many stages:

$$T = 10 + 1 + 0.1 + 0.01 + \cdots = \sum_{n=0}^{\infty} \frac{10}{10^n} = \frac{10}{1 - \frac{1}{10}} = \frac{100}{9} \approx 11.\overline{1} \text{ s}$$

### The Key Mathematical Insight

$$\lim_{N \to \infty} \sum_{n=0}^{N} \frac{10}{10^n} = \frac{100}{9} < \infty$$

**An infinite number of intervals can sum to a finite value.**

Verification: Position of Achilles at $t = 100/9$ s:
$$x_A = 10 \times \frac{100}{9} = \frac{1000}{9} \approx 111.\overline{1} \text{ m}$$
$$x_T = 100 + 1 \times \frac{100}{9} = \frac{1000}{9} \approx 111.\overline{1} \text{ m} \checkmark$$

### Where Zeno's Logic Fails

> Zeno conflates **"infinitely many steps"** with **"infinite time"**
> The logical error: *more steps ≠ more time*, if the steps shrink fast enough

---

## Part 2: Resolution Without Calculus (Physical Reasoning)

### The Direct Argument

Set up two equations and solve directly — **no infinite series needed**:

$$\text{Achilles: } x = 10t$$
$$\text{Tortoise: } x = 100 + t$$

Setting equal:
$$10t = 100 + t \implies t = \frac{100}{9} \text{ s}, \quad x = \frac{1000}{9} \text{ m}$$

**Done.** Achilles catches the tortoise in finite time by elementary algebra.

### The Deeper Physical Argument

Zeno's paradox is a **description of motion, not a constraint on it**. Consider:

- Zeno's stages are a *mathematical labeling* we impose on a continuous physical process
- Nature does not "wait" for Achilles to complete each logical stage before proceeding
- **The stages are not causally sequential** — they ar...
```

### MiMo-V2-Flash

**Generation Time:** 34334ms
**Tokens:** 1732

```
Here is the resolution of Zeno’s paradox in three parts, addressing the mathematical, physical, and philosophical aspects.

### (1) Resolution Using Limits (Calculus)

Zeno’s paradox relies on the assumption that because there are infinite steps, the total time must be infinite. Calculus resolves this by demonstrating that an infinite sum of finite terms can converge to a finite limit.

**The Setup:**
*   **Achilles' speed ($v_A$):** 10 m/s
*   **Tortoise's speed ($v_T$):** 1 m/s
*   **Head start ($d_0$):** 100 meters

**The Geometric Series:**
To catch the tortoise, Achilles must traverse the initial 100 meters. While he does this, the tortoise moves forward.
1.  **Step 1:** Achilles runs 100 m. Time taken: $t_1 = \frac{100}{10} = 10$ seconds. In this time, the tortoise moves 10 m ($1 \text{ m/s} \times 10 \text{ s}$).
2.  **Step 2:** Achilles runs the new gap of 10 m. Time taken: $t_2 = \frac{10}{10} = 1$ second. The tortoise moves 1 m.
3.  **Step 3:** Achilles runs 1 m. Time taken: $t_3 = \frac{1}{10} = 0.1$ second. The tortoise moves 0.1 m.

This creates an infinite geometric series of time intervals:
$$T_{total} = 10 + 1 + 0.1 + 0.01 + \dots$$

**The Sum:**
This series has a first term $a = 10$ and a common ratio $r = 0.1$ (since each subsequent time interval is 1/10th of the previous one).

The sum of an infinite geometric series is given by:
$$S = \frac{a}{1 - r}$$

Substituting our values:
$$T_{total} = \frac{10}{1 - 0.1} = \frac{10}{0.9} = \frac{100}{9} \approx 11.11 \text{ seconds}$$

**Conclusion:**
While there are infinitely many steps, the duration of each step decreases rapidly enough that the total time converges to a finite value ($11.11$ seconds). At this time, Achilles has traveled $10 \times 11.11 = 111.11$ meters, exactly catching the tortoise.

***

### (2) Resolution Without Calculus (Physical Reasoning)

We can resolve this using simple algebra and the concept of relative motion, avoiding the abstraction of infinite sums.

**Relative Velocity:...
```

### GPT-OSS-120B

**Generation Time:** 68368ms
**Tokens:** 2469

```
Below are three separate “answers’’ – one that uses the language of limits, one that stays completely within elementary physics, and one that points out a version of Zeno’s puzzle that still sits on the edge of what our present‑day theories can settle.

---

## 1.  Resolution with limits (the usual “calculus’’ answer)

Let  

* \(v_A = 10\;{\rm m\,s^{-1}}\) – Achilles’ speed,  
* \(v_T = 1\;{\rm m\,s^{-1}}\) – the tortoise’s speed,  
* \(d_0 = 100\;{\rm m}\) – the initial head‑start.

The distance between them at any instant \(t\) is  

\[
d(t)=d_0-(v_A-v_T)t .
\]

When \(d(t)=0\) the two meet. Solving for \(t\),

\[
t_{\rm catch}= \frac{d_0}{v_A-v_T}= \frac{100}{10-1}= \frac{100}{9}\;{\rm s}
          \approx 11.111\;{\rm s}.
\]

Zeno’s “infinite‑step’’ description can be written as an infinite series of time‑intervals:

* Step 1 – Achilles runs to the tortoise’s **initial** position (100 m).  
  \[
  t_1 = \frac{100}{10}=10\;{\rm s}
  \]

* During those 10 s the tortoise has moved \(10\;{\rm m}\) ahead.  
  Step 2 – Achilles now runs that extra 10 m.
  \[
  t_2 = \frac{10}{10}=1\;{\rm s}
  \]

* In that second he gains another 1 m, so Step 3 lasts \(0.1\) s, etc.

The total time is therefore the sum of a geometric series

\[
\begin{aligned}
T &= t_1 + t_2 + t_3 + \dots \\
  &= 10\;+\;1\;+\;0.1\;+\;0.01\;+\dots \\
  &= 10\sum_{n=0}^{\infty}\!\left(\frac{1}{10}\right)^{\!n}
   = 10\;\frac{1}{1-\frac{1}{10}}
   = \frac{10}{0.9}
   = \frac{100}{9}\;{\rm s}.
\end{aligned}
\]

The infinite series converges to a **finite** number.  In the language of limits,

\[
\lim_{N\to\infty}\sum_{n=0}^{N}10\left(\frac{1}{10}\right)^{n}= \frac{100}{9}\;{\rm s}.
\]

Thus Zeno’s “never‑catch‑up’’ conclusion comes from ignoring the fact that an infinite sum of ever‑smaller positive numbers can have a finite limit.

---

## 2.  Resolution without calculus – pure physical reasoning

### (a) Relative‑velocity argument

From the point of view of the tortoise, Achilles approaches with a **re...
```

### Gemini 2.5 Flash

**Generation Time:** 13336ms
**Tokens:** 2158

```
Let's break down Zeno's paradox of Achilles and the Tortoise.

## 1. Resolving the Paradox Using Limits (Calculus)

Zeno's paradox highlights the infinite divisibility of space and time, but it doesn't prevent Achilles from catching the tortoise. Calculus, specifically the concept of limits, beautifully resolves this.

Let:
* $d_A(t)$ be the distance Achilles has run at time $t$.
* $d_T(t)$ be the distance the Tortoise has run at time $t$.
* $v_A = 10 \text{ m/s}$ (Achilles' speed)
* $v_T = 1 \text{ m/s}$ (Tortoise's speed)
* $H = 100 \text{ m}$ (Head start)

Achilles' position: $P_A(t) = v_A \cdot t$
Tortoise's position: $P_T(t) = H + v_T \cdot t$

Achilles catches the tortoise when their positions are equal:
$P_A(t) = P_T(t)$
$v_A \cdot t = H + v_T \cdot t$
$10t = 100 + 1t$
$9t = 100$
$t = \frac{100}{9} \text{ seconds} \approx 11.11 \text{ seconds}$

Now, let's look at Zeno's argument as a series of steps:

*   **Step 1:** Achilles reaches the tortoise's initial starting point (100 m).
    *   Time taken: $t_1 = \frac{100 \text{ m}}{10 \text{ m/s}} = 10 \text{ s}$
    *   During this time, the tortoise moves: $d_{T1} = 1 \text{ m/s} \times 10 \text{ s} = 10 \text{ m}$
    *   New gap: 10 m

*   **Step 2:** Achilles reaches the tortoise's new position (100 m + 10 m = 110 m).
    *   Time taken: $t_2 = \frac{10 \text{ m}}{10 \text{ m/s}} = 1 \text{ s}$
    *   During this time, the tortoise moves: $d_{T2} = 1 \text{ m/s} \times 1 \text{ s} = 1 \text{ m}$
    *   New gap: 1 m

*   **Step 3:** Achilles reaches the tortoise's new position (110 m + 1 m = 111 m).
    *   Time taken: $t_3 = \frac{1 \text{ m}}{10 \text{ m/s}} = 0.1 \text{ s}$
    *   During this time, the tortoise moves: $d_{T3} = 1 \text{ m/s} \times 0.1 \text{ s} = 0.1 \text{ m}$
    *   New gap: 0.1 m

This forms an infinite series for the total time Achilles takes to catch the tortoise:
$T_{total} = t_1 + t_2 + t_3 + \dots$
$T_{total} = 10 + 1 + 0.1 + 0.01 + \dots$

This is a geometric series with:
*  ...
```

### MiniMax M2.5

**Generation Time:** 36471ms
**Tokens:** 2189

```
**The set‑up**

- Achilles starts at \(x=0\) and runs with constant speed \(v_A=10\;\text{m/s}\).  
- The tortoise starts \(100\;\text{m}\) ahead and crawls at \(v_T=1\;\text{m/s}\).  
- At \(t=0\) the separation is \(\Delta_0=100\;\text{m}\).

Zeno’s “ Achilles never catches the tortoise ” argument is that Achilles must first cover the 100 m, then the 10 m the tortoise moved while Achilles was doing that, then the 1 m the tortoise moved in the next interval, and so on – an infinite list of tasks.  

Below we resolve the paradox in three ways and then ask whether a modern‑physics version still
```

---

*Generated by The Multivac V5*
*https://themultivac.com*