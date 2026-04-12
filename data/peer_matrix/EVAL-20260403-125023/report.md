# Multivac Evaluation Report

**Evaluation ID:** EVAL-20260403-125023
**Timestamp:** 2026-04-03T12:50:23.250876
**Category:** Code Generation
**Model Pool:** 10 code-optimized models

## Question

Given these hex dumps of network packets and their known meanings, reverse-engineer the binary protocol format and write a parser.

Packet 1 (Login): 4d 56 01 00 0c 68 65 6c 6c 6f 5f 77 6f 72 6c 64 00 00 00 05 61 64 6d 69 6e
Known: username="hello_world", password="admin"

Packet 2 (Login): 4d 56 01 00 08 74 65 73 74 75 73 65 72 00 00 00 04 70 61 73 73
Known: username="testuser", password="pass"

Packet 3 (Message): 4d 56 02 00 05 68 65 6c 6c 6f 00 00 00 01
Known: message="hello", room_id=1

Write the protocol specification and a Python parser/serializer.

---

## Rankings

| Rank | Model | Score | Min | Max | Std Dev |
|------|-------|-------|-----|-----|---------|
| 1 | GPT-OSS-120B | 9.38 | 7.50 | 10.00 | 0.76 |
| 2 | GPT-5.4 | 9.08 | 8.80 | 10.00 | 0.43 |
| 3 | Gemini 3 Flash Preview | 7.37 | 4.20 | 9.00 | 1.90 |
| 4 | Grok 4.20 | 7.29 | 2.95 | 10.00 | 2.80 |
| 5 | MiMo-V2-Flash | 6.81 | 4.20 | 10.00 | 2.32 |
| 6 | DeepSeek V3 | 5.46 | 3.75 | 8.60 | 1.72 |
| 7 | Claude Sonnet 4.6 | 4.62 | 2.25 | 6.85 | 1.48 |
| 8 | Claude Opus 4.6 | 4.32 | 1.85 | 6.75 | 1.81 |
| 9 | Gemini 3.1 Pro | 1.35 | 0.45 | 2.85 | 0.80 |

---

## Meta Analysis

### Judge Strictness

| Rank | Judge | Avg Score Given |
|------|-------|-----------------|
| 1 | GPT-5.4 | 3.58 |
| 2 | GPT-OSS-120B | 4.26 |
| 3 | Claude Opus 4.6 | 5.67 |
| 4 | Gemini 3.1 Pro | 6.01 |
| 5 | Grok 4.20 | 6.07 |
| 6 | Claude Sonnet 4.6 | 6.66 |
| 7 | MiniMax M2.5 | 6.73 |
| 8 | MiMo-V2-Flash | 7.57 |
| 9 | DeepSeek V3 | 7.66 |
| 10 | Gemini 3 Flash Preview | 7.98 |

**Strictest Judge:** gpt_5_4
**Most Lenient Judge:** gemini_3_flash
**Total Judgments:** 100
**Valid Judgments:** 76

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

**Generation Time:** 24528ms
**Tokens:** 2278

```
Here’s a clean reverse-engineering of the protocol from the samples.

## Protocol format

All packets begin with:

- `magic`: 2 bytes = `4d 56` = ASCII `"MV"`
- `type`: 1 byte
  - `0x01` = Login
  - `0x02` = Message

After that, payload depends on packet type.

---

## Integer encoding

From the examples:

- `00 0c` = 12
- `00 08` = 8
- `00 00 00 05` = 5
- `00 00 00 01` = 1

So integers are **big-endian**.

---

## Packet type 1: Login

Example:

`4d 56 01 00 0c 68 65 6c 6c 6f 5f 77 6f 72 6c 64 00 00 00 05 61 64 6d 69 6e`

Breakdown:

- `4d 56` = magic `"MV"`
- `01` = type Login
- `00 0c` = username length = 12
- next 12 bytes = `hello_world`
- `00 00 00 05` = password length = 5
- next 5 bytes = `admin`

### Login packet structure

| Field | Size | Type | Notes |
|---|---:|---|---|
| magic | 2 bytes | bytes | must be `b"MV"` |
| type | 1 byte | uint8 | `0x01` |
| username_len | 2 bytes | uint16 BE | length of username |
| username | variable | bytes/UTF-8 | username data |
| password_len | 4 bytes | uint32 BE | length of password |
| password | variable | bytes/UTF-8 | password data |

---

## Packet type 2: Message

Example:

`4d 56 02 00 05 68 65 6c 6c 6f 00 00 00 01`

Breakdown:

- `4d 56` = magic `"MV"`
- `02` = type Message
- `00 05` = message length = 5
- next 5 bytes = `hello`
- `00 00 00 01` = room_id = 1

### Message packet structure

| Field | Size | Type | Notes |
|---|---:|---|---|
| magic | 2 bytes | bytes | must be `b"MV"` |
| type | 1 byte | uint8 | `0x02` |
| message_len | 2 bytes | uint16 BE | length of message |
| message | variable | bytes/UTF-8 | message data |
| room_id | 4 bytes | uint32 BE | room identifier |

---

# Protocol specification

## Common header
```text
offset  size  field
0       2     magic = "MV"
2       1     packet_type
```

## Login packet (`packet_type = 0x01`)
```text
offset  size    field
0       2       magic = "MV"
2       1       packet_type = 0x01
3       2       username_len (uint16, big-endian)
5       N       usern...
```

### Claude Opus 4.6

**Generation Time:** 37726ms
**Tokens:** 2291

```


# Binary Protocol Reverse Engineering

## Step 1: Analysis

Let me work through each byte systematically.

### Packet 1 Analysis
```
4d 56 01 00 0c 68 65 6c 6c 6f 5f 77 6f 72 6c 64 00 00 00 05 61 64 6d 69 6e
```

| Bytes | Hex | Interpretation |
|-------|-----|----------------|
| 0-1 | `4d 56` | "MV" — magic bytes (ASCII) |
| 2 | `01` | Packet type: 0x01 = Login |
| 3 | `00` | Flags / reserved byte |
| 4 | `0c` | Length of next field = 12 (but "hello_world" = 11 chars...) |

Wait — let me recount. `hello_world` = h-e-l-l-o-\_-w-o-r-l-d = **11 chars**. But byte 4 is `0c` = **12**.

Let me re-examine: maybe byte 4 is `0c` and it's a **total remaining length** or the username length includes a null terminator? Let me check the raw ASCII:

```
68 65 6c 6c 6f 5f 77 6f 72 6c 64 = "hello_world" (11 bytes)
```

So `0c` (12) ≠ 11. Let me reconsider — maybe bytes 3-4 form a **16-bit big-endian** field:

`00 0c` = 12... still doesn't match 11.

**But wait** — what if it's the length of the *username field including a null terminator*? No, there's no null after the username before `00 00 00 05`.

Let me try: bytes 3-4 = `00 0c` = 12 as a **total payload length for the first field section**, or maybe it's the **username length** and I miscounted.

Recounting the ASCII: `68 65 6c 6c 6f 5f 77 6f 72 6c 64` — that's positions 5 through 15 = **11 bytes**.

Let me try the alternative: byte 3 alone is something, and bytes 4-5 are a 16-bit length:

```
Byte 3: 00 (version minor? flags?)
Byte 4-5: 0c 68 — no, 0x0c68 = 3176, too large
```

Let me revisit with the **second packet** for cross-reference:

### Packet 2 Analysis
```
4d 56 01 00 08 74 65 73 74 75 73 65 72 00 00 00 04 70 61 73 73
```

- `74 65 73 74 75 73 65 72` = "testuser" = **8 bytes**
- Byte 4 = `08` = **8** ✓ — matches username length!

So for Packet 1, byte 4 = `0c` = 12, but "hello_world" = 11. Let me recount the hex very carefully:

```
Position:  0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 2...
```

### Gemini 3.1 Pro

**Generation Time:** 29317ms
**Tokens:** 2319

```
 (2)
                    Type: `01` (1)
                    Username length: `00 0c` (2 bytes BE? 12). But the hex is `01 00 0c`. That's 3 bytes.
                    Wait.
                    Packet 1: `4d 56` | `01`
```

### Claude Sonnet 4.6

**Generation Time:** 34778ms
**Tokens:** 2291

```
## Protocol Reverse Engineering

### Analysis

Let me work through the hex dumps systematically:

**Packet 1:** `4d 56 01 00 0c 68 65 6c 6c 6f 5f 77 6f 72 6c 64 00 00 00 05 61 64 6d 69 6e`

```
4d 56        → Magic bytes "MV"
01           → Packet type (1 = Login)
00 0c        → Username length (12)
68 65 6c 6c 6f 5f 77 6f 72 6c 64  → "hello_world" (11 chars... wait)
```

Let me recount: `00 0c` = 12, but "hello_world" = 11 chars. Rechecking:

```
4d 56        → Magic "MV"
01           → Type: Login
00           → ??? 
0c           → Username length (12)... but "hello_world" = 11
```

Actually: `4d 56 01 00` then `0c` = 12... "hello_world" is 11. Let me try `00 0b`:

Re-examining: positions matter. Let me try a different field layout:

```
4d 56     → Magic "MV"  
01        → Type
00        → Version or flags
0c        → username_len = 12? No, hello_world = 11
```

Trying: `0c` might include a null terminator, or the length field is 2 bytes `00 0b` = 11. Let me reparse:

```
Byte 0-1:  4d 56       → Magic "MV"
Byte 2:    01          → Packet type
Byte 3-4:  00 0b       → username_len = 11
Byte 5-15: hello_world → username (11 bytes)
Byte 16-19: 00 00 00 05 → password_len = 5
Byte 20-24: 61 64 6d 69 6e → "admin"
```

But byte 3 is `00` and byte 4 is `0c`=12, not 11. Unless length is 1 byte at position 4: `0c`=12 with a null terminator included? Let me verify with Packet 2:

**Packet 2:** `4d 56 01 00 08 74 65 73 74 75 73 65 72 00 00 00 04 70 61 73 73`
- `08` = 8, "testuser" = 8 ✓
- So `00 08` at bytes 3-4 → 2-byte length field = 8

Back to Packet 1: `00 0b` would be bytes 3-4, but byte 4 is `0c`=12, not 11.

**Wait** — let me recount "hello_world": h-e-l-l-o-_-w-o-r-l-d = 11 chars. Byte 4 = `0c` = 12. Off by one suggests the length **includes a null terminator**.

Packet 2 check: `08` = 8, "testuser" = 8, so no null terminator there. Contradiction.

**Alternative**: Maybe byte 3 is a separate field (flags/version = 0), and username length is 1 byte:

```
Packet 1: 4d...
```

### Grok 4.20

**Generation Time:** 5204ms
**Tokens:** 1619

```
**Protocol Specification**

**Magic**: `4D 56` ("MV")  
**Version**: `01` (uint8, always 1)  
**Type**: `01` = Login, `02` = Message (uint8)  
**Length**: `uint16` (big-endian) — length of the *payload* that follows (excluding header)

### Payload formats

**Type 1 — Login**
```
uint16     username_length
byte[]     username (ASCII, no null terminator)
uint16     password_length
byte[]     password (ASCII, no null terminator)
```

**Type 2 — Message**
```
uint16     message_length
byte[]     message (ASCII)
uint32     room_id (big-endian)
```

Total header size = 5 bytes (`MV` + version + type + length).

---

**Python Parser / Serializer**

```python
from dataclasses import dataclass
from typing import Union
import struct


class PacketType:
    LOGIN = 1
    MESSAGE = 2


@dataclass
class LoginPacket:
    username: str
    password: str
    packet_type: int = PacketType.LOGIN


@dataclass
class MessagePacket:
    message: str
    room_id: int
    packet_type: int = PacketType.MESSAGE


Packet = Union[LoginPacket, MessagePacket]


class MVProtocol:
    MAGIC = b'MV'
    VERSION = 1
    HEADER_FMT = '>BBH'          # Magic is checked manually, then version + type + length
    HEADER_SIZE = 5

    @staticmethod
    def parse(data: bytes) -> Packet:
        if len(data) < MVProtocol.HEADER_SIZE:
            raise ValueError("Data too short for header")

        magic = data[0:2]
        if magic != MVProtocol.MAGIC:
            raise ValueError(f"Bad magic: {magic.hex()}")

        version, pkt_type, length = struct.unpack(
            MVProtocol.HEADER_FMT, data[2:5]
        )

        if version != MVProtocol.VERSION:
            raise ValueError(f"Unsupported version: {version}")

        if len(data) - MVProtocol.HEADER_SIZE < length:
            raise ValueError("Packet truncated")

        payload = data[MVProtocol.HEADER_SIZE:MVProtocol.HEADER_SIZE + length]

        if pkt_type == PacketType.LOGIN:
            return MVProtocol._parse_login(payload)
        el...
```

### DeepSeek V3

**Generation Time:** 29301ms
**Tokens:** 1389

```
# Binary Protocol Specification

Based on the provided hex dumps, here's the reverse-engineered protocol specification:

## Packet Structure
All packets follow this general format:
```
[Magic Bytes (2)] [Packet Type (1)] [Flags (1)] [Variable Length Field] [Fixed Length Field]
```

### Fields:
1. **Magic Bytes**: `4d 56` (ASCII "MV") - identifies the start of a packet
2. **Packet Type**:
   - `01`: Login packet
   - `02`: Message packet
3. **Flags**: Currently unused (always `00` in examples)
4. **Variable Length Field**:
   - For Login packets: username (null-terminated string)
   - For Message packets: message content (null-terminated string)
5. **Fixed Length Field**:
   - For Login packets: password (4-byte string)
   - For Message packets: room_id (4-byte integer, little-endian)

## Python Parser/Serializer

```python
import struct
from typing import Union, Tuple

class ProtocolParser:
    MAGIC = b'MV'
    
    @staticmethod
    def parse(packet: bytes) -> Union[Tuple[str, str], Tuple[str, int]]:
        """Parse a binary packet into its components."""
        if len(packet) < 4:
            raise ValueError("Packet too short")
        
        # Check magic bytes
        if packet[0:2] != ProtocolParser.MAGIC:
            raise ValueError("Invalid magic bytes")
        
        packet_type = packet[2]
        flags = packet[3]
        
        if packet_type == 0x01:  # Login packet
            # Find null terminator for username
            null_pos = packet.find(b'\x00', 4)
            if null_pos == -1:
                raise ValueError("Missing null terminator for username")
            
            username = packet[4:null_pos].decode('ascii')
            password_start = null_pos + 1
            password = packet[password_start:password_start+4].decode('ascii')
            
            return ('login', username, password)
        
        elif packet_type == 0x02:  # Message packet
            # Find null terminator for message
            null_pos = pac...
```

### GPT-OSS-120B

**Generation Time:** 77437ms
**Tokens:** 3509

```
## 1️⃣  Protocol specification (binary “MV” protocol)

| Offset (bytes) | Size | Meaning | Details |
|----------------|------|---------|---------|
| 0‑1            | 2    | **Magic** | ASCII “M V” → `0x4D 0x56`. All packets start with these two bytes. |
| 2              | 1    | **Message‑type** | `0x01` = *Login*<br>`0x02` = *Chat‑Message* (future types can be added). |
| 3              | 1    | **Reserved / Flags** | Currently always `0x00`. Reserved for future use. |
| **Login packet (type 0x01)** |
| 4              | 1    | **Username‑length** | Unsigned 8‑bit integer (`N`). |
| 5 … 5+N‑1     | N    | **Username** | UTF‑8 bytes, **no terminating NUL**. |
| 5+N … 5+N+3   | 4    | **Password‑length** | Unsigned 32‑bit **big‑endian** integer (`M`). |
| 5+N+4 … 5+N+3+M | M | **Password** | UTF‑8 bytes, **no terminating NUL**. |
| **Message packet (type 0x02)** |
| 4              | 1    | **Message‑length** | Unsigned 8‑bit integer (`L`). |
| 5 … 5+L‑1     | L    | **Message text** | UTF‑8 bytes, **no terminating NUL**. |
| 5+L … 5+L+3   | 4    | **Room‑ID** | Unsigned 32‑bit **big‑endian** integer. |
| **End of packet** | – | No extra trailer, checksum, or padding. |

*All multi‑byte integer fields are big‑endian (network byte order).  
All strings are raw UTF‑8 bytes; length fields tell the parser how many bytes to read.*

---

## 2️⃣  Python implementation  

Below is a **self‑contained** Python 3 module that can

* parse a raw `bytes` buffer into a high‑level packet object,
* serialize a packet object back into the binary representation,
* and expose a tiny public API (`parse_packet`, `LoginPacket`, `MessagePacket`).

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
MV binary protocol parser / serializer.

Supported packet types:
    0x01 – LoginPacket
    0x02 – MessagePacket

The wire format follows the specification described in the module docstring.
"""

import struct
from dataclasses import dataclass
from typing import Union, Tuple

MAGIC = b"MV...
```

### Gemini 3 Flash Preview

**Generation Time:** 12462ms
**Tokens:** 1753

```
Based on the provided hex dumps, here is the reverse-engineered protocol specification and a corresponding Python implementation.

### Protocol Specification: "MV" Protocol

The protocol uses a binary format with a fixed header followed by variable-length fields. All multi-byte integers appear to be **Big-Endian**.

#### 1. Header (4 bytes)
| Offset | Size | Field | Description |
| :--- | :--- | :--- | :--- |
| 0 | 2 | Magic Number | Constant `0x4d 56` (ASCII "MV") |
| 2 | 1 | Packet Type | `0x01` = Login, `0x02` = Message |
| 3 | 1 | Reserved | Always `0x00` in examples |

#### 2. Packet Body Structures

**Type 0x01: Login**
| Field | Size | Description |
| :--- | :--- | :--- |
| Username Length | 4 bytes | Big-endian integer |
| Username | N bytes | UTF-8 String |
| Password Length | 4 bytes | Big-endian integer |
| Password | N bytes | UTF-8 String |

**Type 0x02: Message**
| Field | Size | Description |
| :--- | :--- | :--- |
| Message Length | 4 bytes | Big-endian integer |
| Message | N bytes | UTF-8 String |
| Room ID | 4 bytes | Big-endian integer |

---

### Python Implementation

This implementation uses the `struct` module for memory-efficient binary parsing and serialization.

```python
import struct

class MVProtocol:
    MAGIC = b'MV'
    TYPE_LOGIN = 1
    TYPE_MESSAGE = 2

    @staticmethod
    def serialize_login(username, password):
        u_bytes = username.encode('utf-8')
        p_bytes = password.encode('utf-8')
        
        # Header: Magic(2), Type(1), Reserved(1)
        header = struct.pack(">2sBB", MVProtocol.MAGIC, MVProtocol.TYPE_LOGIN, 0)
        # Body: Len(4), Data, Len(4), Data
        body = struct.pack(">I", len(u_bytes)) + u_bytes + struct.pack(">I", len(p_bytes)) + p_bytes
        return header + body

    @staticmethod
    def serialize_message(message, room_id):
        m_bytes = message.encode('utf-8')
        
        header = struct.pack(">2sBB", MVProtocol.MAGIC, MVProtocol.TYPE_MESSAGE, 0)
        # Body: Len(4), Data,...
```

### MiniMax M2.5

**Generation Time:** 41735ms
**Tokens:** 2310

```

```

### MiMo-V2-Flash

**Generation Time:** 13452ms
**Tokens:** 2354

```
Based on the provided hex dumps and known meanings, here is the reverse-engineered protocol specification and a Python implementation.

### Protocol Specification

The protocol is a binary, length-prefixed format. It consists of a static header followed by variable-length payload fields.

**1. Packet Structure**

| Field | Size (bytes) | Description |
| :--- | :--- | :--- |
| **Magic** | 2 | Constant identifier: `0x4D 0x56` ("MV") |
| **Type** | 1 | Packet type ID (e.g., `0x01` = Login, `0x02` = Message) |
| **Reserved** | 1 | Unused/Padding (Always `0x00` in these examples) |
| **Payload** | Variable | One or more fields, depending on the Type. |

**2. Field Structure (within Payload)**

All data fields (strings, integers) in the payload are encoded using a **Length-Prefix** scheme.

| Field | Size (bytes) | Description |
| :--- | :--- | :--- |
| **Length** | 4 | Unsigned 32-bit Little-Endian integer representing the size of the data in bytes. |
| **Data** | *Length* | The actual data bytes. |

**3. Packet Definitions**

**A. Login Packet (Type `0x01`)**
*   **Payload Fields (in order):**
    1.  **Username** (String)
    2.  **Password** (String)

**B. Message Packet (Type `0x02`)**
*   **Payload Fields (in order):**
    1.  **Message** (String)
    2.  **Room ID** (Integer)
    *   *Note:* Integers are stored as their ASCII string representation (e.g., the integer `1` is stored as the string `"1"`).

---

### Python Parser/Serializer

This Python script includes a `BinaryProtocol` class that can parse raw bytes into dictionaries and serialize dictionaries back into raw bytes according to the specification derived above.

```python
import struct
from typing import Dict, Any, List, Union

class BinaryProtocol:
    """
    Parser and Serializer for the reverse-engineered binary protocol.
    Protocol: [Magic: 2][Type: 1][Reserved: 1][Payload: N]
    Payload Fields: [Length: 4][Data: N] (repeated)
    """

    MAGIC = b'MV'
    HEADER_FORMAT = '>2sBB'  # Big-endian: ...
```

---

*Generated by The Multivac V5*
*https://themultivac.com*