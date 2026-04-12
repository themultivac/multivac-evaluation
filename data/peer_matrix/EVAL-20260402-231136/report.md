# Multivac Evaluation Report

**Evaluation ID:** EVAL-20260402-231136
**Timestamp:** 2026-04-02T23:11:36.179335
**Category:** Communication & Writing
**Model Pool:** 10 communication-optimized models

## Question

Explain how HTTPS works to someone who only knows that 'the lock icon means secure.' Cover: (1) What actually happens when you type https://example.com, (2) Why you need certificates, (3) What a man-in-the-middle attack is, (4) Why public WiFi is risky even with HTTPS. Use analogies only — no technical terms (no 'encryption,' 'certificate,' 'handshake'). Max 400 words.

---

## Rankings

| Rank | Model | Score | Min | Max | Std Dev |
|------|-------|-------|-----|-----|---------|
| 1 | Claude Opus 4.6 | 9.00 | 8.25 | 9.80 | 0.49 |
| 2 | GPT-5.4 | 8.75 | 8.00 | 9.80 | 0.58 |
| 3 | Claude Sonnet 4.6 | 8.70 | 8.00 | 9.45 | 0.54 |
| 4 | Grok 4.20 | 8.69 | 8.15 | 9.45 | 0.43 |
| 5 | GPT-OSS-120B | 8.38 | 7.35 | 9.60 | 0.70 |
| 6 | DeepSeek V3 | 8.08 | 6.55 | 9.00 | 0.74 |
| 7 | MiMo-V2-Flash | 8.02 | 6.55 | 9.45 | 0.87 |
| 8 | Gemini 3.1 Pro | 7.41 | 5.85 | 8.80 | 1.18 |
| 9 | Mistral Small Creative | 7.31 | 4.80 | 9.00 | 1.33 |
| 10 | Seed 1.6 Flash | 6.80 | 4.15 | 8.80 | 1.83 |

---

## Meta Analysis

### Judge Strictness

| Rank | Judge | Avg Score Given |
|------|-------|-----------------|
| 1 | Claude Opus 4.6 | 7.43 |
| 2 | Gemini 3.1 Pro | 7.44 |
| 3 | Claude Sonnet 4.6 | 7.47 |
| 4 | GPT-5.4 | 7.64 |
| 5 | Grok 4.20 | 7.73 |
| 6 | Seed 1.6 Flash | 7.96 |
| 7 | GPT-OSS-120B | 8.19 |
| 8 | DeepSeek V3 | 8.80 |
| 9 | MiMo-V2-Flash | 8.96 |
| 10 | Mistral Small Creative | 9.27 |

**Strictest Judge:** claude_opus_46
**Most Lenient Judge:** mistral_small_creative
**Total Judgments:** 100
**Valid Judgments:** 87

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

**Generation Time:** 17303ms
**Tokens:** 663

```
# How That Little Lock Actually Protects You

## What Happens When You Visit a Site

Imagine you want to pass secret notes to your friend across a crowded room. Before sending anything private, you both agree on a secret language only you two understand. So first, your friend sends you a special decoder ring that only *they* made. You use it to scramble your messages so that even if someone grabs the note mid-air, it looks like pure gibberish. Your friend unscrambles it on their end. That back-and-forth "let's agree on our secret language" moment happens invisibly every time you see that lock icon.

## Why You Need Proof of Identity

Here's the problem: how do you *know* the decoder ring actually came from your friend and not some imposter? So your friend gets a trusted teacher to sign a permission slip that says, "I verified this really is who they claim to be." Your browser checks that permission slip every time. If it's missing, expired, or signed by someone nobody trusts, your browser throws up a big warning — like a bouncer checking IDs at the door.

## The Imposter in the Middle

Now imagine someone sneaky sits between you and your friend. They intercept your friend's decoder ring, replace it with their own, and hand *that* to you. You think you're talking to your friend, but you're actually sharing secrets with the imposter — who reads everything, then passes it along to your friend so nobody notices. This is why that signed permission slip matters so much. Without it, you'd never know someone swapped the decoder ring. The imposter gets caught because they can't forge the teacher's signature.

## Why Coffee-Shop WiFi Is Still Risky

"But if I have the lock, I'm safe on public WiFi, right?" Mostly — but not completely. Think of public WiFi as passing notes through a room full of strangers. Your secret language protects the *contents* of your notes, yes. But everyone in the room can still see *who* you're passing notes to, *how often*, and *how thick the envelo...
```

### GPT-5.4

**Generation Time:** 12694ms
**Tokens:** 559

```
Think of visiting a website like going to a business in a huge city where many buildings look alike.

When you type **https://example.com**, your browser first tries to find the right building. Then, before saying anything private, it asks: **“How do I know you’re really Example?”**  
The site responds by showing an official-looking **proof of identity**—like a business license in a frame. Your browser doesn’t just glance at it. It checks whether the license was vouched for by a trusted office it already knows, and whether the name on the license matches the place you meant to visit.

If everything checks out, your browser and the site agree on a **secret way of talking**—like deciding to speak in a made-up language that only the two of them understand. After that, the messages traveling between them look like nonsense to anyone else watching the road. That’s what the **lock icon** really means: your browser believes it reached the right place and is now speaking privately with it.

Why do you need that proof of identity? Because without it, anyone could hang up a sign saying “Example” and trick you into walking into the wrong building. The proof stops random impostors from pretending to be the real site.

A **man-in-the-middle attack** is like a con artist standing between you and the real business. Imagine you hand your note to someone who says, “I’ll pass this along.” They read it, maybe change it, then pass it on—while pretending to each side that they’re just helping. If your browser doesn’t properly confirm who it’s talking to, that middle person can spy, alter messages, or steal what you send.

Why is **public Wi‑Fi** risky even with HTTPS? Because public Wi‑Fi is like shouting your room number and messages through a crowded café run by strangers. The lock helps protect what you say to the real site, but the café owner can still see **where you’re going**, when you go, and sometimes trick you into the wrong place with fake signs or fake doorways. Also, not ev...
```

### Claude Sonnet 4.6

**Generation Time:** 15189ms
**Tokens:** 661

```
# The Lock Icon, Explained

## 1. What Actually Happens

Imagine you want to pass secret notes with a stranger across a crowded room. Before you start, you both agree on a **secret language** — one only the two of you will ever know. You shout the agreement across the room publicly, but it's done in such a clever way that even people listening can't figure out the final language you landed on.

From that point forward, every note you pass looks like gibberish to anyone who intercepts it. Only you and the website can read them. That negotiation — agreeing on the secret language — happens in milliseconds when you type `https://`.

---

## 2. Why You Need Certificates

Here's the problem: how do you know the stranger across the room is actually your bank, and not someone *pretending* to be your bank?

This is where a **trusted referee** comes in. Imagine a notary public that everyone in the world agrees to trust. Your bank went to that notary, proved their identity, and got a signed letter saying *"This is genuinely Bank of America."*

When you connect, the website shows you that letter. Your browser checks it against a list of trusted notaries it was born with. If the letter is genuine and unaltered, you get the lock. If someone faked the letter, your browser screams a warning instead.

---

## 3. Man-in-the-Middle Attack

Imagine your secret notes have to pass through a mail carrier. A dishonest carrier could stand between you and your bank, pretending to *be* the bank when talking to you, and pretending to *be* you when talking to the bank. They read everything, change things, and pass it along. Both sides think they're talking directly to each other.

The notary letter system stops this — a fake carrier can't produce a genuine letter from a trusted notary.

---

## 4. Why Public WiFi Is Still Risky

The lock protects the *contents* of your notes. But it doesn't hide *who you're writing to*.

On public WiFi, the café owner can see every address on every envelope you...
```

### Gemini 3.1 Pro

**Generation Time:** 28316ms
**Tokens:** 2140

```
Imagine sending a secret letter to a store. 

**(1) Making the connection:**
Normally, letters are written on postcards; any delivery driver can read them. To get that "lock icon," you ask the store for an open padlock. You put your letter inside a metal box, snap the store's padlock shut, and send it back. Only the store has the key to that padlock, so nobody along the delivery route can peek inside your box.

**(2) Proving identity:**
But how do you know the open padlock *actually* came from the store and not a scammer? The store’s padlock arrives with a special wax seal stamped by a universally trusted Mayor. You already know what the Mayor's seal looks like. If the seal is perfectly intact, you trust the padlock genuinely belongs to the store. 

**(3) The middleman trick:**
Imagine a sneaky delivery driver. When you ask the store for a padlock, the driver intercepts the message. The driver sends you *their own* padlock instead, hoping you won't notice the missing Mayor's seal. If you lock your box with it, the driver intercepts your package, opens it with their own key, reads your secrets, and repackages your letter in a *new* box locked with the *real* store's padlock. Neither you nor the store realizes the driver read everything. 

**(4) The risk of public spaces:**
Using a coffee shop's free delivery service is risky. Even if you use the Mayor-approved padlocks so nobody can read the *inside* of your boxes, everyone in the cafe can still see the *outside*. They can watch exactly which banks
```

### Grok 4.20

**Generation Time:** 3016ms
**Tokens:** 705

```
**How HTTPS Keeps Your Browsing Safe (Like a Locked Briefcase)**

Imagine you want to send a valuable gift to a friend across town. You type **https://example.com** — that's like deciding to use a special armored delivery service instead of regular mail.

### 1. What actually happens when you type the address
You tell the delivery company: “I want to send this gift to example.com.”  
The company first asks the shop to prove it really is the real example.com store. The shop shows a special tamper-proof ID card that only it possesses. Once you see the real ID, you and the shop quickly agree on a secret way to lock the briefcase that only the two of you know. From then on, every gift travels inside that locked briefcase. The lock icon appears because you’ve both confirmed you’re talking to the real store and you now have a private locking method.

### 2. Why you need that ID card (the “certificate”)
Without the special ID card, anyone could open a fake shop with the same name, claim to be example.com, and you’d hand them your gift by mistake. The ID card proves the shop is the genuine one, not an impostor.

### 3. What a man-in-the-middle attack is
Picture a sneaky neighbor standing between your house and the real shop. If there’s no ID card and no secret locking method, he can intercept your briefcase, open it, look at or change the gift, then re-wrap it and send it on. You and the shop would never know. The special ID and secret lock stop him from being able to open or fake the delivery.

### 4. Why public WiFi is still risky even with the lock icon
On public WiFi, that sneaky neighbor is sitting right on the same network. Even though your briefcase is locked with the secret method, he can still see the *address* on the outside of every briefcase you send (he knows you’re visiting example.com). Sometimes he can also see how big the gift is or mess with the delivery in other sneaky ways. The lock protects the *contents*, but it doesn’t hide the fact that you’re sendin...
```

### DeepSeek V3

**Generation Time:** 11284ms
**Tokens:** 504

```
Imagine you’re mailing a secret letter to a friend. Normally, anyone handling the mail could peek inside (like HTTP). But with HTTPS, it’s like putting your letter in a locked box. Here’s how it works:

1. **Visiting a Website (the Locked Box):**  
When you type `https://example.com`, your computer asks the website for its special "lock." The site sends back a unique lock only it can open. Your computer checks if this lock is trustworthy (like verifying a signature from someone you trust). If it is, your computer sends a secret code only that lock can use. Now, all messages between you and the site are scrambled like a secret language—safe from eavesdroppers.  

2. **Why Trust the Lock (Certificates):**  
That "lock" is like a passport. A trusted authority (like a government) stamps it to prove the website is who it claims to be. Without this stamp, a fake site could pretend to be your bank and trick you into handing over secrets.  

3. **The Spy in the Middle (Man-in-the-Middle Attack):**  
Imagine a shady post worker who intercepts your locked box, replaces the website’s lock with their own, and tricks you into using it. Now they can read all your "secret" messages. HTTPS stops this by ensuring only the real website’s lock works.  

4. **Public WiFi’s Hidden Danger:**  
Even with HTTPS, public WiFi is like a crowded park where someone could watch you hand the locked box to a courier. They can’t open it, but they might see who you’re talking to or trick you into using a fake lock (like a phishing site). Always double-check the sender (website URL) and avoid sharing sensitive info on public networks.  

HTTPS is like a trusted courier service: it keeps your letters private and ensures they reach the right hands. The lock icon means your secrets stay secret.
```

### GPT-OSS-120B

**Generation Time:** 13835ms
**Tokens:** 922

```
**1. What happens when you type https://example.com**  
Imagine you want to send a private note to a friend who lives far away. First you look up the friend’s address in a phone book, then you call a trusted courier service and ask it to deliver the note. The courier doesn’t just shout the note across the street; it puts the note in a sturdy, sealed box that only your friend can open. When the box reaches the friend’s house, the friend checks the seal, opens the box, reads the note, and writes a reply in another sealed box that only you can open. This back‑and‑forth of sealed boxes is what happens every time you visit a secure web page.

**2. Why you need a “badge of trust”**  
Before the courier trusts that the box really belongs to your friend, it asks to see a special badge that only the friend’s building can issue. That badge proves the building is really the one it claims to be, not a look‑alike set up by a stranger. The badge is like a government‑issued ID for the website: it tells the courier (and you) that the box is being delivered to the right place, not to an impostor’s workshop.

**3. What a “middle‑person” trick looks like**  
A sneaky trickster might set up a fake shop right in the hallway between you and the courier. He watches the sealed box, copies the note, and then sends his own box onward, hoping you won’t notice the difference. Because the fake shop can’t show the proper badge, the courier refuses to hand over the box—unless you’re not checking the badge carefully. That sneaky trick is the “middle‑person” attack.

**4. Why public Wi‑Fi can still be dicey**  
Using a public coffee‑shop Wi‑Fi is like shouting your conversation across a crowded café. Even though the boxes are sealed, a nosy bystander can see the timing, the size of the boxes, and sometimes even the address of the shop you’re sending to. If the bystander manages to slip a fake badge into the mix, he could convince the courier to hand over a box to his own shop. So, while the sealed‑...
```

### MiMo-V2-Flash

**Generation Time:** 6179ms
**Tokens:** 540

```
Think of the internet as a town square where everyone whispers. You see a lock, which means you’re speaking privately with a specific shopkeeper, not just shouting across the square.

(1) When you type https://example.com, you walk to that shop’s door. Before you say anything, you ask for its ID. The shopkeeper shows a special card that proves they are the real owner of that shop. You check the card with a trusted notary in town who keeps a list of who owns which shop. Only when the card matches do you open a private booth inside the shop to talk. Your conversation happens inside that booth, not on the street.

(2) You need these cards because the town is full of strangers. Without a card, anyone could pretend to be the shopkeeper and trick you. The card is hard to fake because the notary only gives one after checking the shopkeeper’s real paperwork. The card also has a secret code that only the real shopkeeper knows, so you can be sure you’re talking to the right person.

(3) A man-in-the-middle attack is like someone dressing up as the shopkeeper and standing outside the door. They show you a fake card, take your message, copy it, and then run into the real shop to pass it along. They stay in the middle, reading everything and even changing it. The card system stops this because the fake card won’t match the notary’s records, and you won’t open the booth.

(4) Public WiFi is risky because the town square is crowded and noisy. Even with the booth, someone might try to jam the door or block the notary so you can’t check the card. If you can’t reach the notary, you might be forced to talk to the impostor. Also, if the shop’s card is old or the notary list is out of date, you could be fooled. So on public WiFi, wait until the booth opens and the card checks out before sharing anything sensitive.
```

### Mistral Small Creative

**Generation Time:** 6345ms
**Tokens:** 1058

```
Imagine you’re sending a **secret letter** to a friend, but instead of mailing it, you’re handing it to a chain of strangers—some trustworthy, some shady—who pass it along until it reaches your friend. That’s basically what happens when you type *https://example.com*, but with a few clever tricks to keep your letter private.

---

### **1. What Happens When You Type the Address?**
You’re at a **busy café**, and you ask the waiter (your browser) to deliver a message to *Example Café* (the website). The waiter doesn’t know the café’s exact location, so they check a **giant phone book** (the DNS system) to find the right address. But here’s the catch: *anyone in the café could be eavesdropping*—maybe that guy in the corner is writing down every request you make!

Once the waiter finds the café, they knock on the door (connect to the website). But before the café lets them in, they do a **secret handshake**:
- The café shows the waiter a **golden key** (the website’s certificate) that proves they’re the *real* Example Café, not an imposter.
- The waiter checks the key with a **trusted bouncer** (a *Certificate Authority*, like a security company) to make sure it’s not a fake.
- Only then do the waiter and the café agree on a **secret code** (HTTPS) to whisper back and forth—so even if someone listens in, they’ll only hear gibberish.

Now, your message (like your credit card number) is wrapped in a **locked box** that only the café can open.

---

### **2. Why Do You Need the Golden Key (Certificates)?**
Imagine the café’s door has a **sign that says “Example Café”**, but anyone could slap that sign on their own fake café down the street. How would you know which one is real?

The **golden key** is like a **notarized ID**—it proves the café is who they claim to be. Without it, you might accidentally give your secret letter to a **fake café** (a scammer) who steals your message. The key is issued by a **trusted judge** (Certificate Authority) who checks that the café is l...
```

### Seed 1.6 Flash

**Generation Time:** 7463ms
**Tokens:** 953

```
Imagine typing “https://example.com” as a sealed envelope with a gold wax stamp. Normally, you’d drop letters in a mailbox—anyone could peek. But this stamp means a *trusted courier* takes it. The courier ensures the envelope reaches *exactly* example.com, not a faker.  


The stamp isn’t random. Before the courier takes your letter, example.com must prove it’s real—like a notary stamping a document to confirm the signer is who they say. The “certificate” is this stamp. The notary (a trusted group) checks example.com’s “ID” (like a business card) and stamps the envelope so *you* know it’s not a thief in disguise.  


A man-in-the-middle is a thief who sets up a fake mailbox next to the real one. When you drop your sealed letter, the thief swaps it for their own sealed (but *fake*) envelope. They read it, then send *their* sealed letter to example.com. You never notice—you think the courier’s real, and the stamp is valid.  


Even with a sealed envelope, public WiFi is a crowded post office. Thieves set up fake mailboxes that look identical to the real ones. They grab your letter, read it, then send their own version to example.com. The “stamp” might look real, but it’s from the thief. Your private info (like a password) goes to *them*, not example.com.  


The lock icon is your guarantee the courier, stamp, and path are real. Without it, you’re mailing letters in a crowded, unsafe lobby.
```

---

*Generated by The Multivac V5*
*https://themultivac.com*