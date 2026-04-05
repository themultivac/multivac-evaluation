# Multivac Evaluation Report

**Evaluation ID:** EVAL-20260402-133517
**Timestamp:** 2026-04-02T13:35:17.096053
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
| 1 | GPT-5.4 | 9.19 | 8.30 | 10.00 | 0.56 |
| 2 | MiMo-V2-Flash | 6.87 | 3.95 | 9.00 | 2.03 |
| 3 | DeepSeek V3 | 6.81 | 4.35 | 10.00 | 2.01 |
| 4 | Grok 4.20 | 6.64 | 3.35 | 9.55 | 2.24 |
| 5 | Gemini 3 Flash Preview | 6.54 | 4.20 | 8.80 | 1.85 |
| 6 | MiniMax M2.5 | 6.33 | 3.25 | 8.95 | 2.15 |
| 7 | Claude Opus 4.6 | 4.84 | 2.25 | 7.35 | 1.67 |
| 8 | Gemini 3.1 Pro | 2.77 | 0.65 | 5.00 | 1.56 |
| None | Claude Sonnet 4.6 | 4.26 | 1.45 | 8.20 | 2.39 |

---

## Meta Analysis

### Judge Strictness

| Rank | Judge | Avg Score Given |
|------|-------|-----------------|
| 1 | GPT-5.4 | 3.05 |
| 2 | GPT-OSS-120B | 4.84 |
| 3 | Grok 4.20 | 5.71 |
| 4 | Gemini 3.1 Pro | 5.81 |
| 5 | Claude Sonnet 4.6 | 5.93 |
| 6 | Claude Opus 4.6 | 5.96 |
| 7 | MiniMax M2.5 | 6.84 |
| 8 | MiMo-V2-Flash | 7.82 |
| 9 | DeepSeek V3 | 7.86 |
| 10 | Gemini 3 Flash Preview | 7.86 |

**Strictest Judge:** gpt_5_4
**Most Lenient Judge:** gemini_3_flash
**Total Judgments:** 100
**Valid Judgments:** 71

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

**Generation Time:** 24908ms
**Tokens:** 2191

```
Here’s a reasonable reverse-engineering of the protocol from the samples.

## Observed structure

All packets begin with:

- `4d 56` → ASCII `"MV"` magic/header
- `01` or `02` → packet type

Then packet-specific fields follow.

---

## Reverse-engineered protocol spec

### Common header

| Offset | Size | Type   | Meaning |
|--------|------|--------|---------|
| 0      | 2    | bytes  | Magic = `"MV"` (`0x4d 0x56`) |
| 2      | 1    | uint8  | Packet type |

Packet types seen:

- `0x01` = Login
- `0x02` = Message

Integers appear to be **big-endian**.

Strings appear to be encoded as:

- 1-byte length for some string fields
- followed by raw ASCII/UTF-8 bytes

---

## Packet type `0x01`: Login

Example:

`4d 56 01 00 0c 68 65 6c 6c 6f 5f 77 6f 72 6c 64 00 00 00 05 61 64 6d 69 6e`

Breakdown:

- `4d 56` = magic
- `01` = login
- `00 0c` = username length = 12
- `68 65 6c 6c 6f 5f 77 6f 72 6c 64` = `"hello_world"`
- `00 00 00 05` = password length = 5
- `61 64 6d 69 6e` = `"admin"`

So login packet format is:

| Field | Size | Type |
|-------|------|------|
| magic | 2    | bytes (`"MV"`) |
| type  | 1    | uint8 (`0x01`) |
| username_len | 2 | uint16 BE |
| username | variable | bytes |
| password_len | 4 | uint32 BE |
| password | variable | bytes |

---

## Packet type `0x02`: Message

Example:

`4d 56 02 00 05 68 65 6c 6c 6f 00 00 00 01`

Breakdown:

- `4d 56` = magic
- `02` = message
- `00 05` = message length = 5
- `68 65 6c 6c 6f` = `"hello"`
- `00 00 00 01` = room_id = 1

So message packet format is:

| Field | Size | Type |
|-------|------|------|
| magic | 2    | bytes (`"MV"`) |
| type  | 1    | uint8 (`0x02`) |
| message_len | 2 | uint16 BE |
| message | variable | bytes |
| room_id | 4 | uint32 BE |

---

# Python parser/serializer

```python
from dataclasses import dataclass
import struct
from typing import Union


MAGIC = b"MV"
TYPE_LOGIN = 0x01
TYPE_MESSAGE = 0x02


class ProtocolError(ValueError):
    pass


@dataclass
class LoginPacket:
    username: ...
```

### Claude Opus 4.6

**Generation Time:** 48242ms
**Tokens:** 2290

```


# Binary Protocol Reverse Engineering & Implementation

## Step 1: Reverse Engineering Analysis

Let me work through each packet byte-by-byte to deduce the protocol format.

### Packet 1 Analysis
```
4d 56 01 00 0c 68 65 6c 6c 6f 5f 77 6f 72 6c 64 00 00 00 05 61 64 6d 69 6e
```

```
4d 56       = "MV" in ASCII → Magic bytes (protocol identifier)
01          = 0x01 → Message type (1 = Login)
00 0c       = 12 as uint16 big-endian? No... 0x000c = 12, but "hello_world" = 11 chars
            Wait: 0x00 then 0x0c separately?
            Let's try: 00 = flags/version?, 0c = length of username?
            0x0c = 12... but "hello_world" is 11 chars.

Let me re-examine. Maybe 00 is padding and 0c (12) includes a null terminator?
No — let me look at the raw bytes more carefully:

68 65 6c 6c 6f 5f 77 6f 72 6c 64 = "hello_world" (11 bytes)

So if the length field is just the single byte 0x0c = 12, that doesn't match 11.
But wait — what if 00 is a separate field and 0c is NOT the length?

Let me try: the byte BEFORE the string is the length.
Position 3 = 00, Position 4 = 0c = 12. "hello_world" = 11 chars.

Hmm. Let me re-examine with Packet 2:
4d 56 01 00 08 74 65 73 74 75 73 65 72 00 00 00 04 70 61 73 73
"testuser" = 8 chars. Byte at position 4 = 08 = 8. ✓ MATCH!

So for Packet 1, byte at position 4 = 0c = 12. But "hello_world" = 11.
Unless... let me recount: h-e-l-l-o-_-w-o-r-l-d = 11. 

Wait, let me recount the hex bytes after 0c:
68 65 6c 6c 6f 5f 77 6f 72 6c 64 = 11 bytes, then 00
That's 12 bytes if we INCLUDE the null terminator 00!

So: length byte includes a null terminator? Let me verify with Packet 2:
After 08: 74 65 73 74 75 73 65 72 = 8 bytes = "testuser", then 00
That's 8 bytes of string + 00 = 9 bytes, but length says 8.

CONTRADICTION. Let me re-examine.
```

Let me re-approach systematically by aligning both packets:

### Side-by-Side Alignment

```
Packet 1: 4d 56 | 01 | 00 | 0c | 68 65 6c 6c 6f 5f 77 6f 72 6c 64 00 | 00 00 05 | 61 64 6d 69 6e
Packet 2: 4d 5...
```

### Gemini 3.1 Pro

**Generation Time:** 19515ms
**Tokens:** 2318

```
Based on the hex dumps provided, we can reverse-engineer the structure of this binary protocol. 

### Step 1: Reverse-Engineering the Protocol

Let's break down the packets byte-by-byte to identify the patterns.

**Packet 1 (Login):**
`4d 56 01 00 0c 68 65
```

### Claude Sonnet 4.6

**Generation Time:** 36799ms
**Tokens:** 2291

```
## Protocol Analysis

Let me work through the hex dumps systematically.

### Reverse Engineering Packet 1 (Login)
```
4d 56          → Magic bytes "MV"
01             → Packet type (1 = Login)
00             → Flags/padding?
0c             → 12 decimal → length of "hello_world" = 11... wait, 0x0c = 12
               → Actually: username length = 12? "hello_world" = 11 chars
               → Let me re-examine...

4d 56 01 00 | 0c | 68 65 6c 6c 6f 5f 77 6f 72 6c 64 | 00 00 00 05 | 61 64 6d 69 6e
             ^12   ^"hello_world" (11 bytes)            ^5            ^"admin" (5 bytes)

Hmm, 0x0c=12 but "hello_world" is 11 bytes. Let me recount:
h=68 e=65 l=6c l=6c o=6f _=5f w=77 o=6f r=72 l=6c d=64 → 11 bytes

So username length field = 0x0c = 12... but string is 11.
Wait — maybe it's a Pascal-style string where length INCLUDES the null terminator?
Or maybe the length field is 2 bytes: 00 0c = 12... no that doesn't work either.

Let me re-parse with 2-byte length:
4d 56 | 01 | 00 | 00 0c | 68..64 (12 bytes?) 

h e l l o _ w o r l d = 11 bytes, not 12.

Back to 1-byte: field=0x0c=12, but "hello_world"=11. 
Check packet 2: 4d 56 01 00 | 08 | 74 65 73 74 75 73 65 72 | 00 00 00 04 | 70 61 73 73
"testuser" = 8 bytes, field=0x08=8 ✓
"pass" = 4 bytes, field=0x04=4 ✓

So packet 2 works with 1-byte username length. Back to packet 1:
0c = 12, but "hello_world" = 11. Unless there's a null terminator included!
"hello_world\x00" = 12 bytes — YES! Null-terminated, length includes null.

Packet 2 check: "testuser" = 8, no null? field=8. Inconsistent...
OR: username length is 2 bytes in packet 1: [00][0c] but packet 2 would be [00][08].

Let me try: magic(2) + type(1) + flags(1) + username_len(2) + username + password_len(4) + password
Packet1: 4d56 | 01 | 00 | 000c → 12? still 12 ≠ 11
Packet2: 4d56 | 01 | 00 | 0008 → 8 = "testuser" ✓ but packet1 still off

FINAL interpretation: username_len is 1 byte, "hello_world" has implicit null terminator read separately:
4d 56 | 01 | 00 | 0c=12....
```

### Grok 4.20

**Generation Time:** 7058ms
**Tokens:** 1587

```
**Protocol Specification**

**Magic**: `4D 56` ("MV")  
**Version**: `01` (1 byte, currently always 1)  
**Type**: 1 byte  
- `01` = Login  
- `02` = Message  

**Login packet (Type 1)**:
```
MV 01 01 <u16-be username_len> <username> <u16-be password_len> <password>
```

**Message packet (Type 2)**:
```
MV 01 02 <u16-be message_len> <message> <u32-be room_id>
```

**Notes**:
- All length fields and the room_id are **big-endian**.
- Strings are raw bytes (no encoding assumed, but in the examples they are ASCII).
- No padding, no null terminators in the strings themselves (the lengths tell exactly how many bytes to read).

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

    def to_bytes(self) -> bytes:
        username_bytes = self.username.encode('utf-8')
        password_bytes = self.password.encode('utf-8')
        
        return (
            b'MV\x01' +
            bytes([PacketType.LOGIN]) +
            struct.pack('>H', len(username_bytes)) + username_bytes +
            struct.pack('>H', len(password_bytes)) + password_bytes
        )


@dataclass
class MessagePacket:
    message: str
    room_id: int

    def to_bytes(self) -> bytes:
        msg_bytes = self.message.encode('utf-8')
        
        return (
            b'MV\x01' +
            bytes([PacketType.MESSAGE]) +
            struct.pack('>H', len(msg_bytes)) + msg_bytes +
            struct.pack('>I', self.room_id)
        )


Packet = Union[LoginPacket, MessagePacket]


class MVProtocol:
    MAGIC = b'MV'
    VERSION = 1

    @staticmethod
    def parse(data: bytes) -> Packet:
        if len(data) < 4:
            raise ValueError("Packet too short")

        magic = data[0:2]
        version = data[2]
        pkt_type = data[3]

        if magic != MVProtocol.MAGIC:
            raise ValueError("Invalid magic"...
```

### DeepSeek V3

**Generation Time:** 89595ms
**Tokens:** 1656

```
# Binary Protocol Specification

Based on the provided hex dumps and their meanings, here's the reverse-engineered protocol specification:

## Header Format (all packets)
- Bytes 0-1: Magic number `0x4d56` (ASCII "MV")
- Byte 2: Packet type
  - `0x01` = Login
  - `0x02` = Message
- Byte 3: Reserved (always `0x00` in examples)

## Login Packet (Type 0x01)
- Bytes 4-5: Length of username (little-endian)
- Bytes 6-N: Username (ASCII string)
- Padding: Null bytes to align to 4-byte boundary
- Next 4 bytes: Length of password (little-endian)
- Following bytes: Password (ASCII string)

## Message Packet (Type 0x02)
- Bytes 4-5: Length of message (little-endian)
- Bytes 6-N: Message (ASCII string)
- Padding: Null bytes to align to 4-byte boundary
- Next 4 bytes: Room ID (little-endian)

# Python Parser/Serializer

```python
import struct
from typing import Union, Tuple, Dict

class ProtocolParser:
    MAGIC = b'MV'
    
    @staticmethod
    def _align_to_4(length: int) -> int:
        """Calculate padding needed to align to 4-byte boundary"""
        return (4 - (length % 4)) % 4
    
    @staticmethod
    def parse_packet(data: bytes) -> Union[Dict, None]:
        """Parse a binary packet into a dictionary"""
        if len(data) < 4 or data[:2] != ProtocolParser.MAGIC:
            return None
            
        packet_type = data[2]
        reserved = data[3]
        
        if packet_type == 0x01:  # Login packet
            username_len = struct.unpack('<H', data[4:6])[0]
            username = data[6:6+username_len].decode('ascii')
            
            password_offset = 6 + username_len + ProtocolParser._align_to_4(username_len)
            password_len = struct.unpack('<I', data[password_offset:password_offset+4])[0]
            password = data[password_offset+4:password_offset+4+password_len].decode('ascii')
            
            return {
                'type': 'login',
                'username': username,
                'password': password
          ...
```

### GPT-OSS-120B

**Generation Time:** 59523ms
**Tokens:** 2326

```

```

### Gemini 3 Flash Preview

**Generation Time:** 10701ms
**Tokens:** 1713

```
### Protocol Analysis

By comparing the provided hex dumps, we can break down the binary structure:

| Offset | Size | Type | Description |
| :--- | :--- | :--- | :--- |
| 0 | 2 | Bytes | **Magic Number**: Always `4d 56` ("MV") |
| 2 | 1 | Byte | **Command ID**: `01` for Login, `02` for Message |
| 3 | 1 | Byte | **Reserved**: Always `00` |
| 4 | 4 | Int32 (BE) | **Length 1**: Length of the first string (Username or Message) |
| 8 | N | String | **Data 1**: UTF-8 string content |
| 8+N | 4 | Int32 (BE) | **Length 2 / Value**: Length of second string (Password) OR Integer (Room ID) |
| 12+N | M | String | **Data 2**: (Only for Login) Password content |

#### Breakdown of Packet 1 (Login):
`4d 56` (Magic) | `01` (Login) | `00` | `00 0c` (Len=12) | `68 65 6c 6c 6f 5f 77 6f 72 6c 64` ("hello_world") | `00 00 00 05` (Len=5) | `61 64 6d 69 6e` ("admin")

#### Breakdown of Packet 3 (Message):
`4d 56` (Magic) | `02` (Msg) | `00` | `00 05` (Len=5) | `68 65 6c 6c 6f` ("hello") | `00 00 00 01` (Room ID=1)

---

### Python Implementation

```python
import struct

class MVProtocol:
    MAGIC = b'MV'
    CMD_LOGIN = 1
    CMD_MESSAGE = 2

    @staticmethod
    def serialize_login(username, password):
        u_bytes = username.encode('utf-8')
        p_bytes = password.encode('utf-8')
        # Format: Magic(2s), Cmd(B), Res(B), Len1(I), Str1, Len2(I), Str2
        # Note: Using Big-Endian (>) for lengths
        header = struct.pack(">2sBB I", MVProtocol.MAGIC, MVProtocol.CMD_LOGIN, 0, len(u_bytes))
        footer = struct.pack(">I", len(p_bytes))
        return header + u_bytes + footer + p_bytes

    @staticmethod
    def serialize_message(message, room_id):
        m_bytes = message.encode('utf-8')
        header = struct.pack(">2sBB I", MVProtocol.MAGIC, MVProtocol.CMD_MESSAGE, 0, len(m_bytes))
        footer = struct.pack(">I", room_id)
        return header + m_bytes + footer

    @classmethod
    def parse(cls, data):
        if len(data) < 8:
            raise ValueError...
```

### MiniMax M2.5

**Generation Time:** 20067ms
**Tokens:** 2310

```
## 1.  Protocol specification  

| Offset | Size | Field | Remarks |
|--------|------|-------|---------|
| 0      | 2 B   | **Magic** | Fixed bytes `0x4D 0x56` (ASCII “MV”) – identifies the start of a packet. |
| 2      | 2 B   | **Command** | Little‑endian `uint16`. Currently defined: <br>• `0x0001` – **LOGIN** <br>• `0x0002` – **MESSAGE** |
| 4      | *payload* | **Payload** | Command‑specific data (see below). All integers are little‑endian. |

### 1.1 LOGIN (command = 1)

| Offset (relative to payload start) | Size | Field |
|------------------------------------|------|-------|
| 0 | 1 B | **username length** (`uint8`) |
| 1 | *N* | **username** (ASCII, *N* = username length) |
| 1 + N | 4 B | **password length** (`uint32`) |
| 5 + N | *M* | **password** (ASCII, *M* = password length) |

### 1.2 MESSAGE (command = 2)

| Offset (relative to payload start) | Size | Field |
|------------------------------------|------|-------|
| 0 | 1 B | **message length** (`uint8`) |
| 1 | *N* | **message** (ASCII, *N* = message length) |
| 1 + N | 4 B | **room_id** (`uint32`) |

*All strings are plain ASCII (no terminating `0x00`). The maximum length that can be stored in a 1‑byte length field is 255 characters.*

---

## 2.  Python implementation  

```python
#!/usr/bin/env python3
"""
Binary protocol parser/serializer for the “MV” protocol used in the
given examples.

The module provides:
* `parse_packet(data: bytes) -> Packet` – decode a complete packet.
* `login(username: str, password: str) -> bytes` – build a LOGIN packet.
* `message(text: str, room_id: int) -> bytes` – build a MESSAGE packet.
"""

import struct
from dataclasses import dataclass
from typing import Union

# -------------------------------------------------------------------------
# Constants
# -------------------------------------------------------------------------
MAGIC = b"MV"
LOGIN_CMD = 1
MSG_CMD = 2

# -------------------------------------------------------------------------
# Packet data‑classes
# --...
```

### MiMo-V2-Flash

**Generation Time:** 19643ms
**Tokens:** 2354

```
Excellent! This is a classic reverse-engineering problem. Let's break down the hex dumps step-by-step to deduce the protocol structure.

### Reverse-Engineering Analysis

We'll analyze the packets byte by byte, using the known meanings as a guide.

#### Packet 1 (Login): `hello_world` / `admin`

`4d 56 01 00 0c 68 65 6c 6c 6f 5f 77 6f 72 6c 64 00 00 00 05 61 64 6d 69 6e`

Let's break it into logical chunks.

1.  `4d 56` -> ASCII for "MV". This looks like a **Magic Number** or **Protocol Signature** to identify the protocol.
2.  `01` -> This is the **Packet Type**. We can confirm this when we see Packet 3.
3.  `00` -> This could be **Flags** or a version sub-field. For now, we'll label it **Flags**.
4.  `0c` -> This is `12` in decimal. The next 12 bytes are `68 65 6c 6c 6f 5f 77 6f 72 6c 64`, which is the ASCII for `hello_world`. So, this is the **Username Length**.
5.  `68 65 6c 6c 6f 5f 77 6f 72 6c 64` -> ASCII for `hello_world`. This is the **Username Data**.
6.  `00 00 00 05` -> This is `5` in big-endian integer format. The next 5 bytes are `61 64 6d 69 6e`, which is `admin`. This is the **Password Length**.
7.  `61 64 6d 69 6e` -> ASCII for `admin`. This is the **Password Data**.

So, the Login packet format seems to be:
`[Magic][Type][Flags][Username Length][Username Data][Password Length][Password Data]`

---

#### Packet 2 (Login): `testuser` / `pass`

`4d 56 01 00 08 74 65 73 74 75 73 65 72 00 00 00 04 70 61 73 73`

Let's verify our hypothesis.

1.  `4d 56` -> "MV". Matches.
2.  `01` -> Packet Type `0x01`. Matches.
3.  `00` -> Flags. Matches.
4.  `08` -> `8` in decimal. The next 8 bytes are `testuser`. Matches.
5.  `74 65 73 74 75 73 65 72` -> `testuser`. Matches.
6.  `00 00 00 04` -> `4` in big-endian. The next 4 bytes are `pass`. Matches.
7.  `70 61 73 73` -> `pass`. Matches.

This confirms our initial structure for the Login packet.

---

#### Packet 3 (Message): `hello` / `room_id=1`

`4d 56 02 00 05 68 65 6c 6c 6f 00 00 00 01`

Now let's apply our struc...
```

---

*Generated by The Multivac V5*
*https://themultivac.com*