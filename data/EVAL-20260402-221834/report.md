# Multivac Evaluation Report

**Evaluation ID:** EVAL-20260402-221834
**Timestamp:** 2026-04-02T22:18:34.746140
**Category:** Communication & Writing
**Model Pool:** 10 communication-optimized models

## Question

Explain the CAP theorem to someone who:
1. Has never studied computer science
2. Needs to understand why they can't have "everything" in their distributed database
3. Has to make a real architectural decision this week

Use concrete analogies. No jargon. Under 300 words.

---

## Rankings

| Rank | Model | Score | Min | Max | Std Dev |
|------|-------|-------|-----|-----|---------|
| 1 | Claude Opus 4.6 | 8.98 | 8.25 | 9.80 | 0.50 |
| 2 | GPT-5.4 | 8.95 | 8.40 | 9.80 | 0.48 |
| 3 | GPT-OSS-120B | 8.95 | 8.35 | 9.60 | 0.39 |
| 4 | Claude Sonnet 4.6 | 8.94 | 8.25 | 9.60 | 0.46 |
| 5 | MiMo-V2-Flash | 8.85 | 8.60 | 9.80 | 0.48 |
| 6 | Grok 4.20 | 8.83 | 7.80 | 9.80 | 0.60 |
| 7 | Gemini 3.1 Pro | 8.82 | 8.35 | 9.60 | 0.41 |
| 8 | DeepSeek V3 | 8.63 | 7.90 | 9.60 | 0.51 |
| 9 | Mistral Small Creative | 8.59 | 7.40 | 9.60 | 0.71 |
| 10 | Seed 1.6 Flash | 7.01 | 3.25 | 9.60 | 2.13 |

---

## Meta Analysis

### Judge Strictness

| Rank | Judge | Avg Score Given |
|------|-------|-----------------|
| 1 | Claude Opus 4.6 | 8.18 |
| 2 | GPT-OSS-120B | 8.34 |
| 3 | GPT-5.4 | 8.36 |
| 4 | Claude Sonnet 4.6 | 8.44 |
| 5 | Grok 4.20 | 8.49 |
| 6 | Gemini 3.1 Pro | 8.55 |
| 7 | Seed 1.6 Flash | 8.55 |
| 8 | DeepSeek V3 | 8.94 |
| 9 | MiMo-V2-Flash | 9.06 |
| 10 | Mistral Small Creative | 9.58 |

**Strictest Judge:** claude_opus_46
**Most Lenient Judge:** mistral_small_creative
**Total Judgments:** 100
**Valid Judgments:** 88

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

**Generation Time:** 14841ms
**Tokens:** 516

```
# The CAP Theorem: Pick Two, Not Three

Imagine you run a chain of three coffee shops, and you keep track of how many loyalty stamps each customer has **in a notebook at each location**.

You want three things:

**Consistency** — Every location has the *same* number of stamps for each customer, always. A customer can't have 5 stamps at the downtown shop and 3 stamps at the airport shop.

**Availability** — Every shop can always look up and update stamps, no matter what. No one ever says "sorry, the system is down."

**Partition tolerance** — The shops keep working even when the phone line between them goes dead (and in the real world, it *will* go dead sometimes).

## The brutal truth

**You can only reliably have two.**

Here's why. The phone line between shops goes down. A customer walks in and wants to add a stamp. Now you face a choice:

- **Update the notebook anyway** (stay available) — but now the shops disagree, and you've lost consistency.
- **Refuse to update until the phone line is back** (stay consistent) — but now you've told a customer "sorry, come back later," and you've lost availability.

There is no third option. This isn't a technology limitation. It's a logical impossibility, like being in two cities at once.

## What this means for your decision

You're really choosing what **hurts less when things break**:

- **Choose consistency** (like a bank) — "I'd rather be temporarily down than show wrong data."
- **Choose availability** (like a social media feed) — "I'd rather show slightly stale data than go offline."

Most systems aren't purely one or the other — you tune the dial. But you need to know **which direction you're leaning**, because your engineers will build very different systems depending on your answer.

So: when the network hiccups, do you want **wrong answers** or **no answers**?
```

### GPT-5.4

**Generation Time:** 9669ms
**Tokens:** 430

```
Think of a distributed database like **several cash registers in different stores** that all need to agree on how many TVs are left.

You want 3 things:

1. **Every register shows the same number**  
   If one says “2 left,” they all should say “2 left.”

2. **The system always answers quickly**  
   Even if something is going wrong, a register should still let you do something.

3. **It keeps working even if stores can’t talk to each other**  
   Maybe the network link between stores is down.

The CAP theorem says:

**When stores can’t talk to each other, you must choose between:**
- **Same answer everywhere**
- **Always answering**

You cannot guarantee both.

### Analogy
Imagine two stores get disconnected.

- If you choose **same answer everywhere**, each store may need to **pause sales** until they can talk again. That avoids selling the same last TV twice.
- If you choose **always answering**, each store keeps selling. But now both might sell the “last TV,” and you must clean up the mistake later.

### So what does this mean for your decision?
Ask:

- **Is it worse to be wrong, or to be unavailable?**

Choose **correctness first** if:
- You handle money
- Inventory must be exact
- Double-booking is unacceptable

Choose **always available first** if:
- Speed matters most
- Small temporary mistakes are okay
- You can fix conflicts later

### The practical truth
You’re not choosing what happens on a normal day.  
You’re choosing what happens **during a network failure**.

That’s why you can’t have “everything”: in a split, the system must either **wait** or **risk disagreement**.
```

### Claude Sonnet 4.6

**Generation Time:** 11970ms
**Tokens:** 479

```
# Why Your Database Can't Do Everything: The CAP Problem

## The Bank Branch Analogy

Imagine a bank with branches in New York and London. They share customer account information.

Now a storm cuts the cable between them. What happens when someone tries to withdraw money in London?

**You're forced to choose:**

**Option A: Refuse the transaction.**
"Sorry, we can't reach New York to verify your balance. Come back later."
→ The system is *accurate* but *unavailable*.

**Option B: Allow the transaction.**
"We'll process it and sync later."
→ The system *stays open* but might let someone overdraw if they're withdrawing in both cities simultaneously.

**There is no Option C.** The cable is cut. You cannot be both perfectly accurate *and* always available when branches can't talk to each other.

---

## That's CAP

Three things you want. You only get two.

- **Consistency** — Every user sees the same, correct data
- **Availability** — The system always responds
- **Partition tolerance** — The system survives network failures

**The hard truth:** Network failures *will* happen. So partition tolerance isn't optional. That means you're *always* choosing between consistency and availability when things go wrong.

---

## Your Actual Decision This Week

**Choose Consistency** (banks, inventory, anything where wrong data causes real damage)
> "We'd rather show an error than show a lie."

**Choose Availability** (social feeds, analytics, shopping carts, anything where being slightly stale is fine)
> "We'd rather show approximate data than nothing."

---

**Ask yourself one question:**

*What's worse — showing users an error, or showing them wrong information?*

Your answer tells you which database to pick.
```

### Gemini 3.1 Pro

**Generation Time:** 20312ms
**Tokens:** 1552

```
Imagine you run a bakery with two cashiers, Alice and Bob. They both take orders for your famous, limited-edition cake. To keep track of inventory, they use walkie-talkies to update each other every time a cake is sold. 

This setup is your "distributed database."

Now, imagine the walkie-talkies break. Alice and Bob can no longer talk. In the real world, internet cables get cut or power goes out. **Communication breaks will inevitably happen.**

Because they can't communicate, you must force Alice and Bob to make a hard choice:

**Option 1: Choose Accuracy (Consistency)**
Alice and Bob stop selling the cake entirely until the walkie-talkies are fixed. 
* *The Benefit:* You guarantee you never accidentally sell the same cake twice. 
* *The Trade-off:* Customers are turned away and get frustrated, even though you might still have cake in the back.

**Option 2: Choose Responsiveness (Availability)**
Alice and Bob keep taking orders, guessing what inventory is left.
* *The Benefit:* Every customer gets served immediately. You never turn away a buyer!
* *The Trade-off:* Alice and Bob might both sell the *last* cake to two different people. You’ll have to apologize and issue a refund later.

**The CAP Theorem simply says:** When communication breaks across your system, you *cannot* have both Accuracy and Responsiveness. You must pick one. 

**For your decision this week:**
Look at your product. If you are handling bank balances, financial transactions, or medical records, choose Accuracy (Option 1). It's better to be temporarily unavailable than wrong. 

If you are running a social media feed, a shopping catalog, or a video streaming site, choose Responsiveness (Option 2). It is better to show slightly outdated information than to show a blank screen.
```

### Grok 4.20

**Generation Time:** 2977ms
**Tokens:** 554

```
**The CAP Theorem, explained like you're choosing a party venue**

Imagine you’re organizing a huge wedding reception across three cities at the same time. You have three things you desperately want:

- **Consistency** – Every guest must see the exact same wedding schedule and seating chart at the exact same moment.
- **Availability** – No matter which city a guest walks into, the doors are open and someone immediately hands them the schedule.
- **Partition tolerance** – If a storm knocks out the phone lines between two cities, the party must still go on in the other cities.

The CAP theorem says: **You can only fully guarantee two of these three at the same time.**

### Real-life analogies for your decision this week:

**Option A – “The Strict Wedding Planner” (CP system)**  
You wait until every city has exactly the same schedule before anyone is allowed to see it. If the phone lines are down, guests in the disconnected city get nothing.  
→ Your app will sometimes say “Sorry, can’t help you right now.” (bad user experience, but data is always correct)

**Option B – “The Party Must Go On” (AP system)**  
Even if the cities can’t talk, every venue keeps handing out schedules. If the lines come back later and the schedules don’t match, you’ll fix it tomorrow.  
→ Users are never blocked, but they might briefly see different answers depending on which city they’re in.

### Your real decision this week
Ask yourself:  
“If two parts of my system can’t talk for a few minutes, would I rather show users **wrong data** or show them **nothing**?”

Pick one. You literally cannot have both perfect accuracy *and* perfect uptime when the network gets flaky — and networks get flaky.

Choose your pain now, or the system will choose it for you later.
```

### DeepSeek V3

**Generation Time:** 15352ms
**Tokens:** 397

```
Imagine you're running a pizza delivery service with three key promises: **Speed** (deliver fast), **Accuracy** (never mess up orders), and **Availability** (always take orders, even during a storm).  

The CAP Theorem says you can only **fully guarantee two of these at once** in a distributed system (like multiple pizza shops sharing orders):  

1. **Consistency (Accuracy)**  
   - Every customer gets the same correct info. If one shop runs out of pepperoni, all others know instantly.  
   - *But*: If the shops can’t communicate (e.g., phone lines down), some must stop taking orders to avoid mistakes.  

2. **Availability (Always Open)**  
   - Every shop takes orders 24/7, even if communication breaks.  
   - *But*: Customers might get stale info (“Sorry, we’re actually out of pepperoni!”).  

3. **Partition Tolerance (Storm Mode)**  
   - The system keeps working even if shops can’t talk (e.g., a storm knocks out phones).  
   - *But*: You must choose between Consistency (stop orders to avoid mistakes) or Availability (keep taking orders but risk errors).  

**Real Decision This Week?**  
- **Banking app?** Pick Consistency + Partition Tolerance—correct balances matter more than 24/7 access.  
- **Social media?** Pick Availability + Partition Tolerance—better to show old posts than error messages.  

You can’t have all three. Choose based on what your system **must** prioritize when things go wrong.
```

### GPT-OSS-120B

**Generation Time:** 2889ms
**Tokens:** 834

```
**The three promises a distributed system can try to keep**

Imagine you run a chain of coffee shops that all share the same menu and price list. Every shop must decide which promises it can keep at the same time.

| Promise | What it means for the coffee shop |
|--------|-----------------------------------|
| **All‑the‑same (Consistency)** | If a new price is set in one shop, every other shop shows that exact price instantly. |
| **Always‑open (Availability)** | No matter what, each shop can take orders and serve coffee. |
| **No‑break‑the‑road (Partition tolerance)** | Even if the phone lines or internet between shops break, each shop can still run on its own. |

The **CAP theorem** says that when the connection between shops sometimes breaks (which almost always happens in the real world), you can only guarantee two of the three promises at once.

---

### What the trade‑offs look like

1. **Consistency + Availability (but not Partition tolerance)**  
   *Analogy*: All shops stay perfectly in sync, but if the network goes down they all shut down until they can talk again.  
   *Result*: Customers may see “service unavailable” during outages.

2. **Consistency + Partition tolerance (but not Availability)**  
   *Analogy*: When the network breaks, a shop refuses to take orders until it can confirm the latest price list with the others.  
   *Result*: The system never shows conflicting prices, but some customers may be turned away temporarily.

3. **Availability + Partition tolerance (but not Consistency)**  
   *Analogy*: Each shop keeps serving coffee even when isolated, but during a break the two shops might show different prices for the same drink.  
   *Result*: Customers always get service, but they may see inconsistent data.

---

### Why you can’t have “everything”

Network glitches are inevitable—think of a bad Wi‑Fi spot, a cloud‑provider outage, or a data‑center fire. When those happen, the system must choose: either stop serving (lose availability) or ri...
```

### MiMo-V2-Flash

**Generation Time:** 4105ms
**Tokens:** 383

```
Think of your database as a **bank with three branches**. You want three things:

1.  **Consistency:** Every branch shows the exact same balance instantly.
2.  **Availability:** Every branch is always open for withdrawals.
3.  **Partition Tolerance:** The branches keep working even if the phone lines connecting them go down.

**The Problem:**  
In a single branch, you can have all three. But if you open three branches across town, the phone lines *will* eventually fail (a storm cuts the wires). This is **Partition Tolerance**—you must accept that branches will lose contact.

**The Choice:**  
When the wires are cut, you can only pick two:

*   **Option A (CP):** You keep balances consistent but lock the doors.  
    *If the branches can’t sync, you stop withdrawals to avoid errors. The system is accurate but unavailable.*
*   **Option B (AP):** You keep the doors open but accept mistakes.  
    *If the branches can’t sync, you let people withdraw anyway. The system is always open, but balances might get out of sync.*

**The Decision:**  
You cannot have all three. If you need **instant data accuracy** (like tracking money), choose Option A. If you need **unstoppable uptime** (like a social media feed), choose Option B.
```

### Mistral Small Creative

**Generation Time:** 4172ms
**Tokens:** 648

```
Imagine you’re running a **global pizza delivery empire**, and you need to keep track of orders across 100 restaurants. Here’s the problem: you can’t have all three of these things at once—pick **two**:

1. **Always Correct (Consistency)**
   *Every restaurant’s order board shows the exact same, up-to-date list of pizzas—no mistakes, ever.*
   - *Example:* If New York’s board says "5 Margheritas left," Tokyo’s *must* say the same instantly. No "oops, we sold out" surprises.
   - *Trade-off:* If the internet lag between cities makes updates slow, the system **freezes** until it’s sure everyone’s in sync. (Like waiting for 100 chefs to confirm a recipe change before taking any orders.)

2. **Always Available (Availability)**
   *Every restaurant can take orders 24/7, no matter what.*
   - *Example:* Even if the New York office burns down, Tokyo and London keep delivering. Customers never get "try again later."
   - *Trade-off:* Sometimes, a restaurant might show "3 Margheritas left" when New York *just* sold the last one. (Like a chef guessing stock levels during a power outage.)

3. **Tolerates Chaos (Partition Tolerance)**
   *Your system survives disasters—cable cuts, cyberattacks, zombie apocalypses.*
   - *Example:* If a hurricane severs the link between Europe and America, the system **keeps running** (even if Europe’s data gets slightly out of sync for a while).
   - *Trade-off:* You *must* sacrifice one of the other two. (Either let some orders get lost in the chaos *or* pause deliveries until the storm passes.)

---
**Why you can’t have all three:**
- If you prioritize **correctness + availability**, a disaster (partition) will **break everything** (e.g., restaurants argue over who has the last pizza).
- If you prioritize **correctness + chaos tolerance**, the system **stalls** during outages (e.g., no orders until the internet’s fixed).
- If you prioritize **availability + chaos tolerance**, you’ll get **temporary lies** (e.g., "Out of pizza!" when it’s not—...
```

### Seed 1.6 Flash

**Generation Time:** 7323ms
**Tokens:** 924

```
### To a Non-CS Person:  
Think of your phone and a friend’s laptop both accessing a shared to-do list. If the list lives *only* on your phone, it’s always up-to-date (consistent) but if your phone dies, you can’t edit it (unavailable). If you copy the list to both phones, it never goes down (available) but you might see different versions (not consistent). You can’t have *both*—the copy is the trade-off.  


### Why You Can’t Have “Everything”  
In the to-do list example, suppose you want *always* to see the latest version *and* never have either phone fail. But if you and your friend edit the list at the same time, both can’t save their changes without chaos. So you have to pick: wait for one to save (consistent, but a phone might fail), or let both save (available, but versions differ). You can’t have all three. Distributed databases are the same—they can’t be *both* fully available *and* fully consistent at all times.  


### For Your Architectural Decision This Week  
Imagine building a app where users check their bank balance (critical) or just see if the app is working (less critical). For the balance: use a single database—if it’s down, users panic. It might be slow (consistent) but never unavailable. For the app status: use two databases (one in NY, one in LA). If one crashes, the other works—users see the app is up (available), even if the balance is a minute old. Choose *consistency* for critical tasks, *availability* for non-critical ones. You can’t have both.  


That’s it—no jargon, just real choices. Pick your trade-off.
```

---

*Generated by The Multivac V5*
*https://themultivac.com*