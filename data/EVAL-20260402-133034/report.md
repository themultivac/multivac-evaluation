# Multivac Evaluation Report

**Evaluation ID:** EVAL-20260402-133034
**Timestamp:** 2026-04-02T13:30:34.106135
**Category:** Code Generation
**Model Pool:** 10 code-optimized models

## Question

Build a production-ready WebSocket chat server in Python using asyncio. Requirements: support multiple rooms, handle disconnections gracefully, implement message history (last 100 messages per room), rate limiting (5 messages/second per user), and heartbeat/keepalive. Include error handling for malformed messages.

---

## Rankings

| Rank | Model | Score | Min | Max | Std Dev |
|------|-------|-------|-----|-----|---------|
| 1 | Grok 4.20 | 8.49 | 7.15 | 9.60 | 0.81 |
| 2 | Gemini 3 Flash Preview | 8.47 | 6.75 | 9.55 | 0.79 |
| 3 | DeepSeek V3 | 7.72 | 6.25 | 9.00 | 0.84 |
| 4 | GPT-OSS-120B | 7.66 | 4.45 | 9.35 | 1.60 |
| 5 | GPT-5.4 | 7.41 | 5.95 | 8.80 | 1.01 |
| 6 | MiMo-V2-Flash | 7.41 | 5.40 | 9.15 | 1.21 |
| 7 | Claude Opus 4.6 | 6.94 | 4.70 | 9.00 | 1.64 |
| 8 | Claude Sonnet 4.6 | 6.74 | 5.05 | 9.00 | 1.56 |
| 9 | MiniMax M2.5 | 5.24 | 2.05 | 8.80 | 2.26 |
| 10 | Gemini 3.1 Pro | 4.57 | 1.65 | 8.60 | 2.16 |

---

## Meta Analysis

### Judge Strictness

| Rank | Judge | Avg Score Given |
|------|-------|-----------------|
| 1 | GPT-5.4 | 4.96 |
| 2 | Claude Opus 4.6 | 6.12 |
| 3 | Gemini 3.1 Pro | 6.47 |
| 4 | GPT-OSS-120B | 6.70 |
| 5 | MiniMax M2.5 | 6.84 |
| 6 | Grok 4.20 | 6.85 |
| 7 | Claude Sonnet 4.6 | 7.15 |
| 8 | MiMo-V2-Flash | 8.08 |
| 9 | Gemini 3 Flash Preview | 8.47 |
| 10 | DeepSeek V3 | 8.93 |

**Strictest Judge:** gpt_5_4
**Most Lenient Judge:** deepseek_v4
**Total Judgments:** 100
**Valid Judgments:** 88

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

**Generation Time:** 24926ms
**Tokens:** 2112

```
Below is a production-ready asyncio WebSocket chat server in Python using `websockets`. It supports:

- Multiple rooms
- Graceful disconnections
- Message history: last 100 messages per room
- Rate limiting: 5 messages/second per user
- Heartbeat / keepalive
- Error handling for malformed messages

It’s designed to be clean, extensible, and safe for real use.

---

## Features and protocol

### Client → Server message format
All client messages must be JSON objects.

Supported actions:

#### Join a room
```json
{
  "action": "join",
  "room": "general",
  "username": "alice"
}
```

#### Send a chat message
```json
{
  "action": "message",
  "room": "general",
  "content": "Hello everyone"
}
```

#### Leave a room
```json
{
  "action": "leave",
  "room": "general"
}
```

#### Ping
```json
{
  "action": "ping"
}
```

---

### Server → Client message examples

#### Joined room
```json
{
  "type": "joined",
  "room": "general",
  "username": "alice",
  "history": [...]
}
```

#### Chat message
```json
{
  "type": "message",
  "room": "general",
  "username": "alice",
  "content": "Hello everyone",
  "timestamp": "2026-04-02T12:00:00.000000Z"
}
```

#### Error
```json
{
  "type": "error",
  "error": "Malformed JSON"
}
```

#### Rate limit exceeded
```json
{
  "type": "error",
  "error": "Rate limit exceeded: max 5 messages per second"
}
```

#### Pong
```json
{
  "type": "pong",
  "timestamp": "2026-04-02T12:00:00.000000Z"
}
```

---

## Install dependency

```bash
pip install websockets
```

---

## Full server implementation

```python
import asyncio
import json
import logging
import signal
import time
from collections import defaultdict, deque
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict, Set, Optional

import websockets
from websockets.exceptions import ConnectionClosed

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s"
)
logger = logging.getLogger("chat...
```

### Claude Opus 4.6

**Generation Time:** 28398ms
**Tokens:** 2121

```


# Production-Ready WebSocket Chat Server

## Project Structure

```
websocket_chat/
├── server.py          # Main server entry point
├── models.py          # Data models
├── room_manager.py    # Room and message management
├── rate_limiter.py    # Token bucket rate limiter
├── connection.py      # Connection handler
├── protocol.py        # Message protocol definitions
├── config.py          # Configuration
├── exceptions.py      # Custom exceptions
└── tests/
    └── test_server.py # Integration tests
```

## config.py

```python
"""Server configuration with sensible defaults."""

from dataclasses import dataclass, field
from typing import Optional


@dataclass(frozen=True)
class ServerConfig:
    host: str = "0.0.0.0"
    port: int = 8765

    # Room settings
    max_history_per_room: int = 100
    max_rooms: int = 50
    max_room_name_length: int = 64

    # Rate limiting (token bucket)
    rate_limit_messages: float = 5.0   # messages per second
    rate_limit_burst: int = 10         # max burst size

    # Heartbeat / keepalive
    heartbeat_interval: float = 30.0   # seconds between pings
    heartbeat_timeout: float = 10.0    # seconds to wait for pong

    # Connection limits
    max_message_size: int = 4096       # bytes
    max_username_length: int = 32
    max_connections_per_ip: int = 5

    # Logging
    log_level: str = "INFO"
```

## exceptions.py

```python
"""Custom exception hierarchy for the chat server."""


class ChatError(Exception):
    """Base exception for chat server errors."""

    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message
        super().__init__(message)


class MalformedMessageError(ChatError):
    """Raised when a message cannot be parsed or is structurally invalid."""

    def __init__(self, message: str = "Malformed message"):
        super().__init__("MALFORMED_MESSAGE", message)


class RateLimitError(ChatError):
    """Raised when a user exceeds the rate limit."""

    d...
```

### Gemini 3.1 Pro

**Generation Time:** 27344ms
**Tokens:** 2106

```
Here is a fully functional, production-ready WebSocket chat server in Python. 

It uses the highly performant `websockets` library and `asyncio`. It utilizes a class-based architecture to manage state, implements a sliding-window rate limiter, uses `collections.deque` for efficient history management, and includes proper OS signal handling for graceful shutdowns.

### Prerequisites
Install the required library:
```bash
pip install websockets
```

### The Server Code (`server.py`)

```python
import asyncio
import json
import logging
import signal
import time
from collections import deque
from typing import Dict, Set, Optional

import websockets
from websockets.exceptions import ConnectionClosed
from websockets.server import WebSocketServerProtocol

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    
```

### Claude Sonnet 4.6

**Generation Time:** 24152ms
**Tokens:** 2121

```
# Production-Ready WebSocket Chat Server

## Architecture Overview

```
┌─────────────────────────────────────────────────────┐
│                   Chat Server                        │
│  ┌─────────────┐  ┌──────────────┐  ┌────────────┐ │
│  │ Room Manager│  │ Rate Limiter │  │  Heartbeat │ │
│  │ (History)   │  │ (Token Bucket│  │  Manager   │ │
│  └─────────────┘  └──────────────┘  └────────────┘ │
│  ┌─────────────────────────────────────────────────┐ │
│  │           Connection Handler                     │ │
│  │  (Auth → Join Room → Message Loop → Cleanup)    │ │
│  └─────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────┘
```

## File Structure

```
chat_server/
├── server.py          # Main entry point
├── handlers.py        # WebSocket connection handlers
├── room_manager.py    # Room and message history management
├── rate_limiter.py    # Token bucket rate limiting
├── heartbeat.py       # Keepalive management
├── models.py          # Data models and message schemas
├── exceptions.py      # Custom exceptions
└── config.py          # Configuration
```

## Implementation

### `config.py`
```python
from dataclasses import dataclass
from typing import Optional
import os


@dataclass
class ServerConfig:
    host: str = "0.0.0.0"
    port: int = 8765
    
    # Rate limiting
    rate_limit_messages: int = 5        # messages per window
    rate_limit_window: float = 1.0      # seconds
    rate_limit_burst: int = 10          # max burst size
    
    # History
    max_history_per_room: int = 100
    
    # Heartbeat
    heartbeat_interval: float = 30.0    # seconds
    heartbeat_timeout: float = 10.0     # seconds to wait for pong
    
    # Rooms
    max_rooms: int = 1000
    max_users_per_room: int = 500
    max_message_length: int = 4096
    max_username_length: int = 32
    max_room_name_length: int = 64
    
    # Connection
    max_connections: int = 10000
    
    @classmethod
    def from_env(cls) -> "S...
```

### Grok 4.20

**Generation Time:** 8339ms
**Tokens:** 2067

```
**Production-ready WebSocket Chat Server with asyncio**

```python
import asyncio
import json
import time
from collections import defaultdict, deque
from typing import Dict, Set, Deque, Optional
from dataclasses import dataclass, asdict
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Query
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from pydantic import BaseModel, ValidationError

# ====================== Models ======================

class Message(BaseModel):
    type: str
    room: str
    content: Optional[str] = None
    username: Optional[str] = None


@dataclass
class ChatMessage:
    username: str
    content: str
    timestamp: float
    message_id: int


# ====================== Server State ======================

class ChatServer:
    def __init__(self):
        self.rooms: Dict[str, Set[WebSocket]] = defaultdict(set)
        self.history: Dict[str, Deque[ChatMessage]] = defaultdict(
            lambda: deque(maxlen=100)
        )
        self.user_rooms: Dict[WebSocket, str] = {}
        self.user_rate_limit: Dict[WebSocket, Dict] = {}
        self.message_counter = 0
        self.heartbeat_interval = 30  # seconds
        self._lock = asyncio.Lock()

    async def connect(self, websocket: WebSocket, room: str = "general"):
        await websocket.accept()
        
        async with self._lock:
            self.rooms[room].add(websocket)
            self.user_rooms[websocket] = room
            self.user_rate_limit[websocket] = {
                "timestamps": deque(maxlen=5),
                "last_heartbeat": time.time()
            }

        # Send history to new user
        await self._send_history(websocket, room)
        
        # Broadcast join message
        await self.broadcast(
            room=room,
            message_type="system",
            content=f"User joined the room",
            exclude=websocket
        )

    async def disconnect(self, websocket: WebSocket):
        room = self.user_rooms.get...
```

### DeepSeek V3

**Generation Time:** 67159ms
**Tokens:** 2112

```
# Production-Ready WebSocket Chat Server with asyncio

Here's a complete implementation of a WebSocket chat server that meets all your requirements:

```python
import asyncio
import json
import time
from collections import defaultdict, deque
from typing import Dict, Deque, Set

from websockets import serve, WebSocketServerProtocol
from websockets.exceptions import ConnectionClosed

# Constants
MAX_MESSAGES_PER_ROOM = 100
MESSAGE_RATE_LIMIT = 5  # messages per second
HEARTBEAT_INTERVAL = 30  # seconds
HEARTBEAT_TIMEOUT = 10  # seconds


class ChatServer:
    def __init__(self):
        # Room data structures
        self.rooms: Dict[str, Set[WebSocketServerProtocol]] = defaultdict(set)
        self.message_history: Dict[str, Deque[Dict]] = defaultdict(deque)
        
        # User tracking
        self.user_rooms: Dict[WebSocketServerProtocol, str] = {}
        self.user_message_counts: Dict[WebSocketServerProtocol, Deque[float]] = defaultdict(deque)
        self.user_last_heartbeat: Dict[WebSocketServerProtocol, float] = {}

    async def handle_connection(self, websocket: WebSocketServerProtocol, path: str):
        """Handle a new WebSocket connection."""
        try:
            # Extract room from path (format: /<room_name>)
            room_name = path.strip('/')
            if not room_name:
                await websocket.close(code=4000, reason="Room name required")
                return

            # Register user
            self.rooms[room_name].add(websocket)
            self.user_rooms[websocket] = room_name
            self.user_last_heartbeat[websocket] = time.time()

            try:
                # Send connection confirmation
                await websocket.send(json.dumps({
                    'type': 'system',
                    'message': f'Connected to room: {room_name}'
                }))

                # Send message history
                history = list(self.message_history.get(room_name, deque()))
                await websocket.s...
```

### GPT-OSS-120B

**Generation Time:** 53194ms
**Tokens:** 2160

```
Below is a **complete, production‑ready WebSocket chat server** written with **Python 3.11+**, **asyncio**, and the **`websockets`** library.  
It satisfies every requirement you listed:

| Feature | Implementation |
|---------|----------------|
| **Multiple rooms** | `Room` objects stored in a global registry (`rooms`). |
| **Graceful disconnections** | `Client` cleanup in `finally` block & `on_close` callbacks. |
| **Message history (last 100 per room)** | `deque(maxlen=100)` per `Room`. |
| **Rate limiting – 5 msg/s per user** | Token‑bucket `RateLimiter` per `Client`. |
| **Heartbeat / keep‑alive** | WebSocket ping/pong + server‑side `asyncio.wait_for` timeout. |
| **Malformed‑message handling** | JSON schema validation and explicit error messages. |
| **Production‑grade touches** | Structured logging, configurable settings, graceful shutdown, TLS support, Dockerfile, health‑check endpoint. |

> **TL;DR** – Copy the code, `pip install -r requirements.txt`, run `python -m chat_server`, and you have a ready‑to‑deploy chat service.

---

## 1. Project Layout

```
chat_server/
│
├─ chat_server/
│   ├─ __init__.py
│   ├─ server.py          # entry point, starts the WS server
│   ├─ router.py          # message routing & validation
│   ├─ client.py          # per‑connection state & rate limiting
│   ├─ room.py            # room management & message history
│   └─ config.py          # runtime configuration (env vars)
│
├─ requirements.txt
├─ Dockerfile
└─ README.md
```

All files are shown below; you can also copy‑paste the **single‑file version** at the end of this answer if you prefer a minimal prototype.

---

## 2. Core Concepts

### 2.1 Message Protocol (JSON)

Every client‑to‑server message **must** be a JSON object with at least a `type` field.

| `type` | Required fields | Meaning |
|--------|----------------|---------|
| `join` | `room` (str) | Join (or create) a chat room. |
| `leave`| `room` (str) | Leave a room. |
| `msg`  | `room` (str), `text` (str) | Bro...
```

### Gemini 3 Flash Preview

**Generation Time:** 12496ms
**Tokens:** 2105

```
To build a production-ready WebSocket server in Python, the `websockets` library is the industry standard for `asyncio` integration.

Below is a robust implementation. To run this, you will need to install the library:
`pip install websockets`

### The Implementation

```python
import asyncio
import json
import logging
import time
from collections import deque, defaultdict
from dataclasses import dataclass, field
from typing import Dict, Set, List

# Configuration
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
logger = logging.getLogger(__name__)

import websockets
from websockets.exceptions import ConnectionClosedError, ConnectionClosedOK

@dataclass
class User:
    websocket: any
    remote_address: str
    last_messages: deque = field(default_factory=lambda: deque(maxlen=5)) # For rate limiting

class ChatServer:
    def __init__(self):
        # room_id -> set of User objects
        self.rooms: Dict[str, Set[User]] = defaultdict(set)
        # room_id -> deque of message dicts
        self.history: Dict[str, deque] = defaultdict(lambda: deque(maxlen=100))
        self.rate_limit_window = 1.0  # seconds
        self.max_msgs_per_window = 5

    async def send_to_user(self, user: User, message: dict):
        """Safe wrapper to send JSON to a specific user."""
        try:
            await user.websocket.send(json.dumps(message))
        except Exception:
            pass

    async def broadcast(self, room_id: str, message: dict, exclude_user: User = None):
        """Broadcasts a message to all users in a specific room."""
        if room_id not in self.rooms:
            return

        message_json = json.dumps(message)
        dead_users = set()
        
        # Create tasks for parallel sending
        tasks = []
        for user in self.rooms[room_id]:
            if user != exclude_user:
                tasks.append(self._safe_send(user, message_json, dead_users))
        
        if ...
```

### MiniMax M2.5

**Generation Time:** 77559ms
**Tokens:** 2144

```
Here is a complete, production-ready implementation using Python 3.10+, `asyncio`, and the industry-standard `websockets` library.

### Prerequisites

You will need to install the `websockets` library:

```bash
pip install websockets
```

### The Server Implementation

This solution uses a class-based structure to manage state, locks for thread safety (in an async context), and robust error handling.

```python
import asyncio
import json
import logging
import time
from collections import defaultdict, deque
from dataclasses import dataclass, field
from typing import Any, Dict, Set

import websockets
from websockets.server import WebSocketServerProtocol

# --- Configuration ---
HOST = "0.0.0.0"
PORT = 8765
MAX_HISTORY = 100
RATE_LIMIT_COUNT = 5  # Messages
RATE_LIMIT_WINDOW = 1.0  # Seconds
PING_INTERVAL = 20  # Seconds (Heartbeat)

# --- Logging Setup ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("chat_server")


# --- Data Structures ---
@dataclass
class User:
    websocket: WebSocketServerProtocol
    user_id: str
    room: str
    message_timestamps: deque = field(default_factory=lambda: deque(maxlen=RATE_LIMIT_COUNT))


class ChatServer:
    def __init__(self):
        # Room ID -> Deque of message dicts
        self.rooms: Dict[str, deque] = defaultdict(lambda: deque(maxlen=MAX_HISTORY))
        
        # Websocket Connection -> User Object
        self.active_connections: Dict[WebSocketServerProtocol, User] = {}
        
        # Lock to prevent race conditions on shared state
        self.lock = asyncio.Lock()

    async def broadcast(self, room: str, message: Dict[str, Any], exclude_ws: WebSocketServerProtocol = None):
        """Broadcasts a message to all users in a specific room."""
        if room not in self.rooms:
            return

        # Prepare the JSON payload
        payload = json.dumps(message)

        # Create a set of tasks to send messages concurrentl...
```

### MiMo-V2-Flash

**Generation Time:** 14630ms
**Tokens:** 2144

```
Here is a production-ready WebSocket chat server built with Python's `asyncio` and the `websockets` library.

### Prerequisites

You will need to install the `websockets` library:

```bash
pip install websockets
```

### Implementation

This solution uses a class-based architecture to manage state, ensuring thread-safety (via `asyncio.Lock`) and efficient memory management.

```python
import asyncio
import json
import logging
import signal
import time
import uuid
from collections import deque
from dataclasses import dataclass, field
from typing import Set, Dict, Optional, Deque, Any

import websockets
from websockets.server import ServerProtocol
from websockets.exceptions import ConnectionClosedOK, ConnectionClosedError

# --- Configuration ---
HOST = "0.0.0.0"
PORT = 8765
HEARTBEAT_INTERVAL = 20  # Seconds
RATE_LIMIT_MESSAGES = 5  # Max messages
RATE_LIMIT_WINDOW = 1    # Per second
MAX_MESSAGE_SIZE = 1024  # Bytes
MAX_HISTORY = 100        # Messages per room

# --- Logging Setup ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger("ChatServer")

# --- Data Models ---

@dataclass
class Message:
    """Represents a chat message."""
    sender: str
    content: str
    timestamp: float = field(default_factory=time.time)
    msg_type: str = "message"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": self.msg_type,
            "sender": self.sender,
            "content": self.content,
            "timestamp": self.timestamp
        }

@dataclass
class RateLimiter:
    """Simple token bucket implementation for rate limiting."""
    tokens: float = RATE_LIMIT_MESSAGES
    last_refill: float = field(default_factory=time.time)

    def allow_request(self) -> bool:
        now = time.time()
        elapsed = now - self.last_refill
        self.tokens = min(RATE_LIMIT_MESSAGES, self.tokens + elapsed * RATE_LIMIT_MESSAGES)
        self.l...
```

---

*Generated by The Multivac V5*
*https://themultivac.com*