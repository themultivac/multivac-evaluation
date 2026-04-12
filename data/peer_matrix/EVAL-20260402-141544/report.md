# Multivac Evaluation Report

**Evaluation ID:** EVAL-20260402-141544
**Timestamp:** 2026-04-02T14:15:44.483051
**Category:** Code Generation
**Model Pool:** 10 code-optimized models

## Question

Implement the OAuth 2.0 Authorization Code flow with PKCE (Proof Key for Code Exchange) from scratch in Python. Include: code verifier/challenge generation, authorization URL construction, token exchange, token refresh, and secure token storage. Explain why PKCE prevents authorization code interception attacks.

---

## Rankings

| Rank | Model | Score | Min | Max | Std Dev |
|------|-------|-------|-----|-----|---------|
| 1 | Grok 4.20 | 8.90 | 8.00 | 9.80 | 0.78 |
| 2 | Gemini 3 Flash Preview | 8.24 | 7.45 | 8.80 | 0.49 |
| 3 | GPT-5.4 | 7.75 | 5.25 | 8.80 | 1.17 |
| 4 | DeepSeek V3 | 7.58 | 6.50 | 9.40 | 0.95 |
| 5 | GPT-OSS-120B | 7.57 | 5.45 | 8.60 | 1.15 |
| 6 | MiniMax M2.5 | 7.53 | 3.85 | 9.40 | 1.66 |
| 7 | MiMo-V2-Flash | 7.39 | 4.80 | 9.40 | 1.53 |
| 8 | Claude Sonnet 4.6 | 7.14 | 4.10 | 9.00 | 1.62 |
| 9 | Claude Opus 4.6 | 6.62 | 2.85 | 9.25 | 2.11 |
| 10 | Gemini 3.1 Pro | 5.47 | 2.30 | 8.80 | 2.15 |

---

## Meta Analysis

### Judge Strictness

| Rank | Judge | Avg Score Given |
|------|-------|-----------------|
| 1 | GPT-5.4 | 5.11 |
| 2 | MiniMax M2.5 | 6.68 |
| 3 | Gemini 3.1 Pro | 6.74 |
| 4 | Claude Opus 4.6 | 7.01 |
| 5 | GPT-OSS-120B | 7.03 |
| 6 | Claude Sonnet 4.6 | 7.29 |
| 7 | Grok 4.20 | 7.71 |
| 8 | MiMo-V2-Flash | 8.69 |
| 9 | DeepSeek V3 | 8.72 |
| 10 | Gemini 3 Flash Preview | 9.04 |

**Strictest Judge:** gpt_5_4
**Most Lenient Judge:** gemini_3_flash
**Total Judgments:** 100
**Valid Judgments:** 89

---

## Model Pool

Models selected for **Code Generation** evaluation:

1. **GPT-5.4** (openrouter)
2. **Claude Opus 4.6** (openrouter)
3. **Gemini 3.1 Pro** (openrouter)
4. **Claude Sonnet 4.6** (openrouter)
5. **Grok 4.20** (openrouter)
6. **DeepSeek V3** (openrouter)
7. **GPT-OSS-120B** (openrouter)
8. **Gemini 3 Flash Preview** (openrouter)
9. **MiniMax M2.5** (openrouter)
10. **MiMo-V2-Flash** (openrouter)

---

## Model Responses

### GPT-5.4

**Generation Time:** 24165ms
**Tokens:** 2112

```
Below is a from-scratch implementation of OAuth 2.0 Authorization Code flow with PKCE in Python, along with an explanation of why PKCE protects against authorization code interception.

I’ll keep it framework-agnostic and use only standard Python libraries plus `requests` for HTTP.

---

# Overview

We’ll implement:

1. **PKCE code verifier generation**
2. **PKCE code challenge generation**
3. **Authorization URL construction**
4. **Local callback handler to receive the authorization code**
5. **Token exchange**
6. **Refresh token flow**
7. **Secure-ish token storage**
8. **Explanation of how PKCE prevents interception attacks**

---

# Important notes before you use this

- This example is suitable for:
  - CLI apps
  - Desktop apps
  - Local development
- For production:
  - Use provider-specific details from their OAuth docs
  - Prefer OS keychain / secret manager for token storage
  - Validate ID tokens if using OpenID Connect
  - Use HTTPS redirect URIs where applicable
  - Protect against CSRF with `state`
- PKCE is most important for **public clients** that cannot safely store a client secret.

---

# OAuth + PKCE flow in plain English

1. App generates:
   - `code_verifier`: random secret string
   - `code_challenge`: derived from the verifier
2. App sends user to the authorization endpoint with the `code_challenge`
3. User logs in and authorizes
4. Authorization server redirects back with an authorization `code`
5. App exchanges the `code` for tokens, sending the original `code_verifier`
6. Server checks:
   - Does `BASE64URL(SHA256(code_verifier)) == code_challenge`?
   - If yes, issue tokens
   - If no, reject

This means a stolen authorization code alone is not enough.

---

# Full example

## Dependencies

```bash
pip install requests
```

---

## Complete Python code

```python
import base64
import hashlib
import json
import os
import secrets
import threading
import time
import webbrowser
from dataclasses import dataclass, asdict
from http.server impor...
```

### Claude Opus 4.6

**Generation Time:** 37134ms
**Tokens:** 2121

```


# OAuth 2.0 Authorization Code Flow with PKCE — Complete Implementation

## Why PKCE Exists and How It Prevents Attacks

Before diving into code, let's understand the threat model:

```
WITHOUT PKCE (Vulnerable):
═══════════════════════════

  Legitimate App                    Authorization Server
       │                                    │
       │──── Authorization Request ────────>│
       │                                    │
       │<─── Authorization Code ────────────│
       │         ▲                          │
       │         │ INTERCEPTED!             │
       │    Malicious App                   │
       │         │                          │
       │         │── Token Request ────────>│
       │         │   (with stolen code)     │
       │         │<── Access Token ─────────│
       │         │   ATTACK SUCCEEDS!       │


WITH PKCE (Secure):
═══════════════════

  Legitimate App                    Authorization Server
       │                                    │
       │ generates code_verifier            │
       │ computes code_challenge            │
       │     = SHA256(code_verifier)        │
       │                                    │
       │── Auth Request + challenge ───────>│
       │                                    │  Server stores
       │<── Authorization Code ─────────────│  challenge
       │         ▲                          │
       │         │ INTERCEPTED!             │
       │    Malicious App                   │
       │         │                          │
       │         │── Token Request ────────>│
       │         │   (code, but NO          │
       │         │    code_verifier!)       │
       │         │<── REJECTED ─────────────│
       │         │   ATTACK FAILS!          │
       │                                    │
       │── Token Request ─────────────────>│
       │   (code + code_verifier)          │
       │                                   │  Server verifies:
       │                                ...
```

### Gemini 3.1 Pro

**Generation Time:** 17204ms
**Tokens:** 2103

```
Here is a complete, from-scratch implementation of the OAuth 2.0 Authorization Code flow with PKCE in Python. It uses standard library modules for the cryptographic requirements and the popular `requests` library for HTTP calls.

### Part 1: Why PKCE Prevents Authorization Code Interception

**The Vulnerability (Without PKCE):**
In native/mobile or Single Page Applications (Public Clients), the app cannot securely store a `client_secret`. When a user logs in, the Authorization Server redirects the user back to the app using a custom URI scheme (e.g., `myapp://callback?code=12345`). 
A malicious app installed on the same device can register the same URI scheme (`myapp://`). If the OS routes the redirect to the malicious app, the attacker intercepts the `code`. Because there is no `client_secret`, the malicious app can just send the `code` to the server and get an Access Token.

**The PKCE Solution:**
PKCE (Proof Key for Code Exchange) fixes this by dynamically creating a one-time secret for every single login attempt.
1. **Creation:** The app generates a random string (`code_verifier`)
```

### Claude Sonnet 4.6

**Generation Time:** 27728ms
**Tokens:** 2121

```
# OAuth 2.0 Authorization Code Flow with PKCE in Python

## Why PKCE Prevents Authorization Code Interception Attacks

```
Traditional OAuth 2.0 (vulnerable):
1. Client requests auth code
2. Server redirects with code → ATTACKER intercepts code!
3. Attacker exchanges code for tokens ✗

PKCE Protection:
1. Client generates random code_verifier (secret)
2. Client sends code_challenge = SHA256(code_verifier) with auth request
3. Server stores code_challenge
4. Even if attacker intercepts auth code, they need code_verifier
5. Attacker can't reverse SHA256(code_verifier) → can't get tokens ✓
```

---

## Implementation

```python
# oauth_pkce.py
import hashlib
import hmac
import json
import os
import secrets
import time
import urllib.parse
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Optional
import base64
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ============================================================
# SECTION 1: PKCE Core Cryptography
# ============================================================

class PKCEGenerator:
    """
    Implements RFC 7636 - Proof Key for Code Exchange
    
    Security guarantees:
    - code_verifier: 32 bytes of cryptographic randomness (256 bits)
    - code_challenge: SHA-256 of verifier, base64url-encoded
    - One-way: SHA-256 cannot be reversed to recover verifier
    """
    
    MIN_VERIFIER_LENGTH = 43   # RFC 7636 minimum
    MAX_VERIFIER_LENGTH = 128  # RFC 7636 maximum
    VERIFIER_BYTES = 32        # 32 bytes = 43 base64url chars (within range)
    
    @staticmethod
    def generate_code_verifier() -> str:
        """
        Generate cryptographically secure code verifier.
        Uses os.urandom() → /dev/urandom on Unix, CryptGenRandom on Windows.
        
        Returns: base64url-encoded random string (no padding)
        """
        # Generate 32 random bytes = 256 bits of entropy
        random_bytes = secrets.toke...
```

### Grok 4.20

**Generation Time:** 13130ms
**Tokens:** 2228

```
**✅ OAuth 2.0 Authorization Code Flow with PKCE – Complete Python Implementation**

### 1. Full Implementation

```python
import secrets
import hashlib
import base64
import webbrowser
import requests
from urllib.parse import urlencode, urlparse, parse_qs
import json
from pathlib import Path
import time
from typing import Dict, Optional
import os


class OAuth2PKCEClient:
    def __init__(self, 
                 client_id: str,
                 redirect_uri: str,
                 authorization_endpoint: str,
                 token_endpoint: str,
                 scopes: list = None):
        
        self.client_id = client_id
        self.redirect_uri = redirect_uri
        self.auth_endpoint = authorization_endpoint
        self.token_endpoint = token_endpoint
        self.scopes = scopes or ["openid", "profile", "email"]
        
        self.token_file = Path(".tokens.json")
        self._tokens = None

    # ===================== PKCE GENERATION =====================

    @staticmethod
    def generate_code_verifier(length: int = 128) -> str:
        """Generate a high-entropy cryptographic random string."""
        if length < 43 or length > 128:
            raise ValueError("Code verifier must be between 43 and 128 characters")
        
        # Generate random bytes and encode as URL-safe base64
        token = secrets.token_bytes(96)
        verifier = base64.urlsafe_b64encode(token).decode('utf-8').rstrip('=')
        return verifier[:length]

    @staticmethod
    def generate_code_challenge(verifier: str) -> str:
        """Create a SHA256 hash of the code verifier and base64-url-encode it."""
        digest = hashlib.sha256(verifier.encode('utf-8')).digest()
        challenge = base64.urlsafe_b64encode(digest).decode('utf-8').rstrip('=')
        return challenge

    # ===================== AUTHORIZATION =====================

    def get_authorization_url(self, state: Optional[str] = None) -> tuple:
        """Generate authorization URL and PKCE values...
```

### DeepSeek V3

**Generation Time:** 118758ms
**Tokens:** 2111

```
# OAuth 2.0 Authorization Code Flow with PKCE in Python

Here's a complete implementation of the OAuth 2.0 Authorization Code flow with PKCE in Python:

```python
import os
import base64
import hashlib
import secrets
import requests
import json
from urllib.parse import urlencode, parse_qs, urlparse
from datetime import datetime, timedelta
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
from threading import Thread
import time

class OAuthPKCE:
    def __init__(self, client_id, redirect_uri, auth_url, token_url, scopes):
        self.client_id = client_id
        self.redirect_uri = redirect_uri
        self.auth_url = auth_url
        self.token_url = token_url
        self.scopes = scopes
        self.tokens = None
        self.code_verifier = None
        
    def generate_code_verifier(self):
        """Generate a code verifier for PKCE"""
        self.code_verifier = secrets.token_urlsafe(96)[:128]
        return self.code_verifier
    
    def generate_code_challenge(self):
        """Generate the code challenge from the verifier"""
        if not self.code_verifier:
            raise ValueError("Code verifier not generated")
        
        # SHA-256 hash of the code verifier, then base64url encode
        digest = hashlib.sha256(self.code_verifier.encode('ascii')).digest()
        challenge = base64.urlsafe_b64encode(digest).decode('ascii').replace('=', '')
        return challenge
    
    def get_authorization_url(self):
        """Generate the authorization URL with PKCE parameters"""
        self.generate_code_verifier()
        challenge = self.generate_code_challenge()
        
        params = {
            'response_type': 'code',
            'client_id': self.client_id,
            'redirect_uri': self.redirect_uri,
            'scope': ' '.join(self.scopes),
            'code_challenge': challenge,
            'code_challenge_method': 'S256',
            'state': secrets.token_urlsafe(16)
        }
        
        retu...
```

### GPT-OSS-120B

**Generation Time:** 33102ms
**Tokens:** 2160

```
Below is a **complete, from‑scratch implementation of the OAuth 2.0 Authorization‑Code flow with PKCE** in plain Python (no external OAuth libraries).  
It covers every step you asked for:

| Step | What the code does | Where in the code |
|------|-------------------|-------------------|
| **1. Code verifier & code challenge** | Generates a high‑entropy random string (`code_verifier`) and its SHA‑256‑based `code_challenge` (Base64‑URL‑encoded). | `PKCE.generate_verifier()` / `PKCE.generate_challenge()` |
| **2. Authorization URL** | Builds the URL you must open in a browser (or embed in a UI) so the user can consent. | `OAuth2Client.get_authorization_url()` |
| **3. Token exchange** | After the user is redirected back with an *authorization code*, the client exchanges it for an access‑token (and optionally a refresh‑token). | `OAuth2Client.exchange_code_for_token()` |
| **4. Token refresh** | Uses the refresh‑token to obtain a fresh access‑token when the old one expires. | `OAuth2Client.refresh_token()` |
| **5. Secure token storage** | Stores the token set encrypted on disk (AES‑GCM) using a key derived from a user‑provided passphrase (or you can swap it for `keyring`). | `TokenStore.save()` / `TokenStore.load()` |
| **6. PKCE security rationale** | Explained after the code. | — |

---

## 1.  PKCE Helper (code verifier / challenge)

```python
import os
import secrets
import hashlib
import base64

class PKCE:
    """Utility class for generating PKCE code verifier & code challenge."""

    @staticmethod
    def _base64url_encode(data: bytes) -> str:
        """Base64‑URL encode without padding (RFC 7636 requirement)."""
        return base64.urlsafe_b64encode(data).rstrip(b'=').decode('ascii')

    @staticmethod
    def generate_verifier(length: int = 64) -> str:
        """
        Generate a high‑entropy `code_verifier`.

        RFC 7636 recommends 43‑128 characters from the unreserved URL set.
        64 bytes → 86 characters after base64url‑encoding, comfortabl...
```

### Gemini 3 Flash Preview

**Generation Time:** 11887ms
**Tokens:** 1632

```
This implementation uses standard Python libraries (`hashlib`, `secrets`, `base64`) to demonstrate the PKCE flow. We will use `requests` for the HTTP calls.

### Why PKCE Prevents Interception Attacks
In the standard Authorization Code flow, an attacker on a shared device or a malicious app on a mobile OS could intercept the `code` sent via the redirect URI. If the client is a "public client" (like a SPA or Mobile App) that doesn't have a client secret, the attacker can exchange that code for an access token.

**PKCE solves this by adding a "secret" created on the fly:**
1.  **Code Verifier:** A high-entropy random string generated by the client.
2.  **Code Challenge:** A SHA256 hash of the verifier, sent with the initial authorization request.
3.  **The Binding:** The Authorization Server stores the challenge. When the client later exchanges the code for a token, it must provide the original **Verifier**. The server hashes it and compares it to the stored challenge. 

Even if an attacker steals the `code`, they cannot exchange it because they don't know the original `Code Verifier` used to generate the challenge.

---

### Python Implementation

#### 1. PKCE Helper Functions
These generate the cryptographically secure strings required.

```python
import hashlib
import secrets
import base64
import requests
import json

def generate_pkce_pair():
    # 1. Create Code Verifier: Random string (43-128 chars)
    # Using URL-safe base64 encoding without padding
    verifier = secrets.token_urlsafe(64)
    
    # 2. Create Code Challenge: SHA256(verifier) -> Base64URL encoded
    sha256_hash = hashlib.sha256(verifier.encode('utf-8')).digest()
    challenge = base64.urlsafe_b64encode(sha256_hash).decode('utf-8').replace('=', '')
    
    return verifier, challenge
```

#### 2. The OAuth Client Class
This handles the URL construction, token exchange, and refresh logic.

```python
class OAuthClient:
    def __init__(self, client_id, auth_endpoint, token_endpoint, redirect_uri...
```

### MiniMax M2.5

**Generation Time:** 55147ms
**Tokens:** 2144

```
Below is a **self‑contained, educational implementation** of the OAuth 2.0 Authorization‑Code grant with PKCE (Proof Key for Code Exchange).  
It shows how to:

1. **Generate** a `code_verifier` and its `code_challenge`.
2. **Build** the authorization URL that you send the user to.
3. **Exchange** the authorization code for access / refresh tokens.
4. **Refresh** an access token when it expires.
5. **Store** tokens securely (using the OS keyring – e.g. Windows Credential Manager, macOS Keychain, or Linux libsecret).

> **⚠️ Production warning** – This code is meant for learning/demo purposes. In a real app you should use a well‑maintained library (e.g. **Authlib**, **django-oauth-toolkit**, **Flask-OAuthlib**, …) that handles edge‑cases, proper TLS, revocation, PKCE‑related security checks, and token lifecycle management.

---

## 1. PKCE – code_verifier & code_challenge

```python
import secrets
import hashlib
import base64
import re
from urllib.parse import quote, urlencode

def generate_code_verifier(length: int = 128) -> str:
    """
    Return a random, URL‑safe string (43‑128 characters) that will be used
    as the *code_verifier* in PKCE.
    """
    if length < 43 or length > 128:
        raise ValueError("Length must be between 43 and 128 characters.")
    # Each byte → two base64url characters, so we need length/3*4 ≈ length bytes
    random_bytes = secrets.token_bytes(length)
    # Make it URL‑safe (replace '+' with '-', '/' with '_', strip padding '=')
    verifier = base64.urlsafe_b64encode(random_bytes).decode('utf-8')
    # Trim to exact length (the spec allows any length in range, but we keep it exact)
    verifier = verifier[:length]
    # Ensure it only contains [A‑Z, a‑z, 0‑9, -, _, ., ~]
    if not re.fullmatch(r'[A-Za-z0-9\-._~]+', verifier):
        # If we accidentally got a non‑allowed char, regenerate (very unlikely)
        return generate_code_verifier(length)
    return verifier


def generate_code_challenge(verifier: str) -> str:
    ""...
```

### MiMo-V2-Flash

**Generation Time:** 17795ms
**Tokens:** 2143

```
Here is a complete implementation of the OAuth 2.0 Authorization Code flow with PKCE from scratch in Python using only standard libraries (`hashlib`, `secrets`, `base64`, `urllib`, `http.server`, and `json`).

No external dependencies (like `requests` or `authlib`) are used, ensuring you see exactly how the cryptography and HTTP requests are constructed.

### Prerequisites

To test this code, you need OAuth credentials from an Identity Provider (IdP) like **Auth0**, **Google**, or **Okta**.

**Note:** You must configure your IdP to allow the loopback address `http://127.0.0.1:8080/callback` as a valid Redirect URI.

### The Python Implementation

Save this code as `oauth_pkce.py`.

```python
import hashlib
import base64
import secrets
import json
import sys
from urllib.parse import urlencode, parse_qs, urlparse
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
import time

# ==========================================
# 1. Configuration
# ==========================================
# Replace these with your actual OAuth provider details
CLIENT_ID = "YOUR_CLIENT_ID"
CLIENT_SECRET = "YOUR_CLIENT_SECRET"  # Optional for Public Clients, required for Confidential
REDIRECT_URI = "http://127.0.0.1:8080/callback"
AUTHORIZATION_ENDPOINT = "https://YOUR_DOMAIN/authorize"  # e.g., https://dev-xyz.us.auth0.com/authorize
TOKEN_ENDPOINT = "https://YOUR_DOMAIN/oauth/token"        # e.g., https://dev-xyz.us.auth0.com/oauth/token
SCOPES = "openid profile email"

# ==========================================
# 2. PKCE Cryptography Helpers
# ==========================================

def generate_code_verifier() -> str:
    """
    Generates a high-entropy cryptographically random string.
    Length: 43-128 characters (recommended 43-45).
    """
    return secrets.token_urlsafe(96)[:128]  # Generate and trim to safe length

def generate_code_challenge(verifier: str) -> str:
    """
    Creates a S256 code challenge from the verifier.
    Method: BASE64URL(SHA2...
```

---

*Generated by The Multivac V5*
*https://themultivac.com*