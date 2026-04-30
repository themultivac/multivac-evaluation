# Multivac Evaluation Report

**Evaluation ID:** EVAL-20260318-163203
**Timestamp:** 2026-03-18T16:32:03.732869
**Category:** Project MiniMax
**Model Pool:** 9 minimax-optimized models

## Question

You must choose between three investments. Investment A returns 10% with 90% probability, -50% with 10% probability. Investment B returns 5% with certainty. Investment C returns 100% with 20% probability, 0% with 80% probability. (1) Rank them by expected value. (2) Rank them by the Kelly criterion. (3) You have $10,000 your entire savings. Does this change your answer? Why? (4) Now you have $10,000,000. Does it change again? Derive the general principle.

---

## Rankings

| Rank | Model | Score | Min | Max | Std Dev |
|------|-------|-------|-----|-----|---------|
| 1 | GPT-5.4 | 9.71 | 8.80 | 10.00 | 0.41 |
| 2 | Claude Sonnet 4.6 | 9.42 | 7.60 | 10.00 | 0.92 |
| 3 | MiniMax-01 | 7.24 | 4.35 | 9.10 | 1.73 |

---

## Meta Analysis

### Judge Strictness

| Rank | Judge | Avg Score Given |
|------|-------|-----------------|
| 1 | GPT-5.4 | 5.97 |
| 2 | Claude Sonnet 4.6 | 7.33 |
| 3 | MiniMax M1 | 8.78 |
| 4 | MiniMax M2.5 | 9.05 |
| 5 | MiniMax-01 | 9.30 |
| 6 | MiniMax M2 | 9.42 |
| 7 | MiniMax M2.1 | 9.60 |
| 8 | MiniMax M2.7 | 9.63 |

**Strictest Judge:** judge_gpt54
**Most Lenient Judge:** minimax_m27
**Total Judgments:** 72
**Valid Judgments:** 21

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

**Generation Time:** 47681ms
**Tokens:** 2211

```

```

### MiniMax M2.5

**Generation Time:** 41754ms
**Tokens:** 2208

```

```

### MiniMax M2.1

**Generation Time:** 64662ms
**Tokens:** 2211

```

```

### MiniMax M2

**Generation Time:** 39154ms
**Tokens:** 2209

```

```

### MiniMax M1

**Generation Time:** 42386ms
**Tokens:** 2616

```

```

### MiniMax-01

**Generation Time:** 30003ms
**Tokens:** 2131

```
### (1) **Ranking by Expected Value**

To rank the investments by expected value, we need to calculate the expected return for each investment.

#### Investment A:
- **Return of 10% with 90% probability**: \( 0.10 \times 0.90 = 0.09 \)
- **Return of -50% with 10% probability**: \( -0.50 \times 0.10 = -0.05 \)
- **Expected return**: \( 0.09 + (-0.05) = 0.04 \) or 4%.

#### Investment B:
- **Return of 5% with certainty**: \( 0.05 \times 1.00 = 0.05 \) or 5%.

#### Investment C:
- **Return of 100% with 20% probability**: \( 1.00 \times 0.20 = 0.20 \)
- **Return of 0% with 80% probability**: \( 0.00 \times 0.80 = 0.00 \)
- **Expected return**: \( 0.20 + 0.00 = 0.20 \) or 20%.

**Ranking by Expected Value**:
1. **Investment C**: 20%
2. **Investment B**: 5%
3. **Investment A**: 4%

---

### (2) **Ranking by the Kelly Criterion**

The Kelly criterion helps determine the optimal fraction of capital to invest in a given opportunity to maximize the long-term growth rate of capital. The formula for the Kelly criterion is:

\[
f^* = \frac{p \cdot b - q}{b}
\]

where:
- \( f^* \) is the fraction of capital to invest.
- \( p \) is the probability of winning.
- \( q \) is the probability of losing (\( q = 1 - p \)).
- \( b \) is the net odds received on the bet (\( b = \text{return if win} - 1 \)).

#### Investment A:
- \( p = 0.90 \), \( q = 0.10 \)
- \( b = 0.10 - (-0.50) = 0.60 \) (since a 10% return means \( 1.10 \) times the original investment, and a -50% return means \( 0.50 \) times the original investment)
- \( f^* = \frac{0.90 \times 0.60 - 0.10}{0.60} = \frac{0.54 - 0.10}{0.60} = \frac{0.44}{0.60} \approx 0.733 \)
- **Kelly fraction**: \( 73.3\% \)

#### Investment B:
- \( p = 1.00 \), \( q = 0.00 \)
- \( b = 0.05 \) (since a 5% return means \( 1.05 \) times the original investment)
- \( f^* = \frac{1.00 \times 0.05 - 0.00}{0.05} = \frac{0.05}{0.05} = 1.00 \)
- **Kelly fraction**: \( 100\% \)

#### Investment C:
- \( p = 0.20 \), \( q = 0.80 \)
- \( b = 1.00 \) (since a...
```

### Claude Sonnet 4.6

**Generation Time:** 40802ms
**Tokens:** 2181

```
# Investment Analysis: Expected Value vs. Kelly Criterion

## (1) Ranking by Expected Value

Expected Value = Σ(probability × return)

**Investment A:**
E[A] = (0.90)(0.10) + (0.10)(−0.50) = 0.09 − 0.05 = **+4%**

**Investment B:**
E[B] = (1.00)(0.05) = **+5%**

**Investment C:**
E[C] = (0.20)(1.00) + (0.80)(0.00) = 0.20 + 0 = **+20%**

### EV Ranking: **C > B > A**

---

## (2) Ranking by Kelly Criterion

The Kelly criterion maximizes the **expected logarithm of wealth** (geometric growth rate), which accounts for the asymmetry between gains and losses.

### The Kelly Formula

For a bet with probability p of winning return b and probability q of losing fraction l:

$$f^* = \frac{p \cdot b - q \cdot l}{b \cdot l}$$

More precisely, Kelly maximizes:

$$G(f) = p \cdot \ln(1 + fb) + q \cdot \ln(1 - fl)$$

---

### Investment A

Two outcomes: +10% (p=0.90), −50% (q=0.10)

$$G(f) = 0.90\ln(1 + 0.10f) + 0.10\ln(1 - 0.50f)$$

Taking derivative and setting to zero:

$$\frac{dG}{df} = \frac{0.90(0.10)}{1+0.10f} + \frac{0.10(-0.50)}{1-0.50f} = 0$$

$$\frac{0.09}{1+0.10f} = \frac{0.05}{1-0.50f}$$

$$0.09(1-0.50f) = 0.05(1+0.10f)$$

$$0.09 - 0.045f = 0.05 + 0.005f$$

$$0.04 = 0.050f$$

$$f^* = 0.80 = \textbf{80\%}$$

**Growth rate:** G = 0.90·ln(1.08) + 0.10·ln(0.60) = 0.0693 − 0.0511 = **+1.82% per period**

---

### Investment B

Certain 5% return → Kelly says invest **100%** (no risk of ruin)

$$G = \ln(1.05) = \textbf{+4.88\% per period}$$

---

### Investment C

Two outcomes: +100% (p=0.20), 0% (q=0.80)

$$G(f) = 0.20\ln(1 + f) + 0.80\ln(1)$$

Since ln(1) = 0:

$$G(f) = 0.20\ln(1+f)$$

This is **monotonically increasing in f** — Kelly says invest **100%**

$$G = 0.20\ln(2) + 0.80\ln(1) = 0.20(0.693) = \textbf{+13.86\% per period}$$

> **Note:** Investment C has no ruin risk (worst case: 0% return, not negative), so Kelly prescribes full investment. This is a critical structural feature.

### Kelly Ranking: **C > B > A**

| Investment | Kelly f* | Growth Rate |
|-----------...
```

### GPT-5.4

**Generation Time:** 29095ms
**Tokens:** 1522

```
Let wealth be \(W\), and suppose you put **all** your money into one investment for one period.

## 1) Rank by expected value

Compute expected return:

- **A**:  
  \[
  0.9(0.10)+0.1(-0.50)=0.09-0.05=0.04
  \]
  So \(E[r_A]=4\%\).

- **B**:  
  \[
  E[r_B]=5\%
  \]

- **C**:  
  \[
  0.2(1.00)+0.8(0)=0.20
  \]
  So \(E[r_C]=20\%\).

### Expected value ranking:
\[
\boxed{C > B > A}
\]

---

## 2) Rank by Kelly criterion

Kelly ranks by **expected log wealth growth**, not expected return.

For each all-in choice, maximize:
\[
E[\log(1+r)]
\]

### A
\[
E[\log(1+r_A)] = 0.9\log(1.1)+0.1\log(0.5)
\]
Using natural logs:
\[
0.9(0.09531)+0.1(-0.69315)=0.08578-0.06932=0.01647
\]

### B
\[
E[\log(1.05)] = \log(1.05)\approx 0.04879
\]

### C
\[
E[\log(1+r_C)] = 0.2\log(2)+0.8\log(1)=0.2\log(2)\approx 0.13863
\]

### Kelly ranking:
\[
\boxed{C > B > A}
\]

So with the assumption “choose one and go all-in,” Kelly gives the same ranking as expected value here.

---

## 3) You have \$10,000, your entire savings. Does this change the answer? Why?

**Yes, in practice it should.**

If this is your **entire wealth**, then the decision is not just about one-period expected return or asymptotic log growth. You also care about **survival**, liquidity, and inability to recover from bad outcomes.

### Key issue
- **A** has a 10% chance of cutting your wealth in half immediately.
- **C** has an 80% chance of no gain at all.
- **B** gives a sure gain.

Even though **C** has the highest expected value and highest expected log growth, if this money is all you have, real-world constraints matter:
- bills,
- emergencies,
- inability to withstand drawdowns,
- human risk tolerance,
- no guarantee of repeated independent opportunities.

If this \$10,000 is truly all your wealth, many people would rationally choose:
\[
\boxed{B}
\]
because certainty has high utility when wealth is near a subsistence or highly valuable threshold.

### Why Kelly alone is not enough
Full Kelly is derived for:
- repea...
```

---

*Generated by The Multivac V5*
*https://themultivac.com*