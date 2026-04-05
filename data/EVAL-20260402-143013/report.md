# Multivac Evaluation Report

**Evaluation ID:** EVAL-20260402-143013
**Timestamp:** 2026-04-02T14:30:13.046531
**Category:** Code Generation
**Model Pool:** 10 code-optimized models

## Question

Implement an HTTP/1.1 server from raw TCP sockets in Python (no http.server, no frameworks). Support: GET and POST methods, proper header parsing, chunked transfer encoding, keep-alive connections, static file serving, and a 404 handler. Handle malformed requests gracefully.

---

## Rankings

| Rank | Model | Score | Min | Max | Std Dev |
|------|-------|-------|-----|-----|---------|
| 1 | MiniMax M2.5 | 8.29 | 6.75 | 9.55 | 1.08 |
| 2 | Gemini 3 Flash Preview | 7.69 | 6.75 | 8.60 | 0.64 |
| 3 | GPT-5.4 | 7.41 | 4.95 | 9.15 | 1.48 |
| 4 | Grok 4.20 | 7.30 | 4.95 | 9.15 | 1.25 |
| 5 | DeepSeek V3 | 7.15 | 5.40 | 9.15 | 1.26 |
| 6 | Claude Sonnet 4.6 | 6.61 | 2.65 | 8.80 | 2.28 |
| 7 | GPT-OSS-120B | 6.48 | 3.25 | 8.80 | 2.01 |
| 8 | MiMo-V2-Flash | 5.96 | 3.25 | 8.80 | 2.02 |
| 9 | Claude Opus 4.6 | 5.63 | 2.25 | 8.00 | 1.69 |
| 10 | Gemini 3.1 Pro | 3.53 | 1.15 | 8.20 | 2.84 |

---

## Meta Analysis

### Judge Strictness

| Rank | Judge | Avg Score Given |
|------|-------|-----------------|
| 1 | GPT-5.4 | 4.18 |
| 2 | Gemini 3.1 Pro | 5.87 |
| 3 | GPT-OSS-120B | 5.93 |
| 4 | Claude Opus 4.6 | 6.01 |
| 5 | Grok 4.20 | 6.34 |
| 6 | Claude Sonnet 4.6 | 6.68 |
| 7 | MiniMax M2.5 | 6.69 |
| 8 | MiMo-V2-Flash | 7.99 |
| 9 | Gemini 3 Flash Preview | 8.13 |
| 10 | DeepSeek V3 | 8.60 |

**Strictest Judge:** gpt_5_4
**Most Lenient Judge:** deepseek_v4
**Total Judgments:** 100
**Valid Judgments:** 86

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

**Generation Time:** 23829ms
**Tokens:** 2112

```
Below is a complete, minimal HTTP/1.1 server implemented directly on raw TCP sockets in Python.

It supports:

- `GET`
- `POST`
- HTTP/1.1 request line + header parsing
- `Transfer-Encoding: chunked` request bodies
- `Content-Length` request bodies
- keep-alive connections
- static file serving
- 404 responses
- graceful handling of malformed requests

No `http.server`, no frameworks.

---

## Full implementation

```python
import os
import socket
import threading
import mimetypes
from urllib.parse import unquote, urlparse

HOST = "127.0.0.1"
PORT = 8080
DOCUMENT_ROOT = "./www"
SERVER_NAME = "RawPythonHTTP/1.1"
MAX_HEADER_SIZE = 64 * 1024
MAX_BODY_SIZE = 10 * 1024 * 1024
SOCKET_TIMEOUT = 10


STATUS_MESSAGES = {
    200: "OK",
    201: "Created",
    400: "Bad Request",
    404: "Not Found",
    405: "Method Not Allowed",
    411: "Length Required",
    413: "Payload Too Large",
    500: "Internal Server Error",
    501: "Not Implemented",
}


class HTTPError(Exception):
    def __init__(self, status_code, message=None):
        self.status_code = status_code
        self.message = message or STATUS_MESSAGES.get(status_code, "Error")
        super().__init__(self.message)


class BufferedSocketReader:
    def __init__(self, conn):
        self.conn = conn
        self.buffer = b""

    def recv_until(self, delimiter, max_bytes):
        while delimiter not in self.buffer:
            chunk = self.conn.recv(4096)
            if not chunk:
                break
            self.buffer += chunk
            if len(self.buffer) > max_bytes:
                raise HTTPError(400, "Request too large")
        idx = self.buffer.find(delimiter)
        if idx == -1:
            return None
        result = self.buffer[:idx + len(delimiter)]
        self.buffer = self.buffer[idx + len(delimiter):]
        return result

    def read_exact(self, n):
        while len(self.buffer) < n:
            chunk = self.conn.recv(4096)
            if not chunk:
                raise HTTPEr...
```

### Claude Opus 4.6

**Generation Time:** 224821ms
**Tokens:** 2120

```


# HTTP/1.1 Server from Raw TCP Sockets

## Implementation

```python
#!/usr/bin/env python3
"""
HTTP/1.1 Server built from raw TCP sockets.
Supports: GET, POST, header parsing, chunked transfer encoding,
keep-alive connections, static file serving, and 404 handling.
"""

import socket
import threading
import os
import mimetypes
import json
import logging
import time
import signal
import sys
from dataclasses import dataclass, field
from typing import Optional, Callable
from urllib.parse import unquote, urlparse, parse_qs
from pathlib import Path
from datetime import datetime, timezone

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(threadName)s] %(levelname)s %(message)s",
)
logger = logging.getLogger("httpserver")

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
CRLF = b"\r\n"
HEADER_END = b"\r\n\r\n"
MAX_REQUEST_LINE = 8192
MAX_HEADERS = 100
MAX_HEADER_SIZE = 65536
MAX_BODY_SIZE = 10 * 1024 * 1024  # 10 MB
DEFAULT_KEEP_ALIVE_TIMEOUT = 15  # seconds
DEFAULT_MAX_REQUESTS_PER_CONN = 100
RECV_CHUNK = 4096

# Standard HTTP status phrases
STATUS_PHRASES = {
    200: "OK",
    201: "Created",
    204: "No Content",
    301: "Moved Permanently",
    304: "Not Modified",
    400: "Bad Request",
    403: "Forbidden",
    404: "Not Found",
    405: "Method Not Allowed",
    408: "Request Timeout",
    411: "Length Required",
    413: "Payload Too Large",
    414: "URI Too Long",
    500: "Internal Server Error",
    501: "Not Implemented",
    505: "HTTP Version Not Supported",
}


# ---------------------------------------------------------------------------
# Exceptions
# ---------------------------------------------------------------------------
class HTTPError(Excep...
```

### Gemini 3.1 Pro

**Generation Time:** 23984ms
**Tokens:** 2106

```
Here is a complete, robust implementation of an HTTP/1.1 server using only Python's built-in `socket` and `threading` modules. 

It fulfills all your requirements: GET/POST handling, chunked transfer encoding parsing, keep-alive connections, static file serving with directory traversal protection, a 404 handler, and graceful error handling.

### Directory Setup

```

### Claude Sonnet 4.6

**Generation Time:** 25742ms
**Tokens:** 2120

```
# HTTP/1.1 Server from Raw TCP Sockets

```python
#!/usr/bin/env python3
"""
HTTP/1.1 server implemented from raw TCP sockets.
Supports: GET/POST, header parsing, chunked transfer encoding,
keep-alive connections, static file serving, and 404 handling.
"""

import socket
import threading
import os
import sys
import logging
import mimetypes
import time
import signal
from pathlib import Path
from datetime import datetime, timezone
from typing import Optional

# ─────────────────────────────────────────────────────────────────────────────
# Configuration
# ─────────────────────────────────────────────────────────────────────────────
HOST = "0.0.0.0"
PORT = 8080
STATIC_ROOT = Path("./static")          # directory to serve files from
KEEP_ALIVE_TIMEOUT = 30                  # seconds before idle connection closes
MAX_REQUEST_SIZE = 8 * 1024 * 1024      # 8 MB body limit
RECV_BUFFER = 4096
SERVER_NAME = "RawPy/1.0"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger("http_server")


# ─────────────────────────────────────────────────────────────────────────────
# HTTP Status Codes
# ─────────────────────────────────────────────────────────────────────────────
STATUS = {
    200: "OK",
    201: "Created",
    204: "No Content",
    301: "Moved Permanently",
    304: "Not Modified",
    400: "Bad Request",
    403: "Forbidden",
    404: "Not Found",
    405: "Method Not Allowed",
    408: "Request Timeout",
    411: "Length Required",
    413: "Payload Too Large",
    500: "Internal Server Error",
    501: "Not Implemented",
    505: "HTTP Version Not Supported",
}


# ─────────────────────────────────────────────────────────────────────────────
# HTTP Request / Response Data Classes
# ─────────────────────────────────────────────────────────────────────────────
class HTTPRequest:
    """Parsed HTTP request."""

    __slots__ = ("method", "path", "query", "version", "h...
```

### Grok 4.20

**Generation Time:** 10587ms
**Tokens:** 2227

```
**Here's a complete, clean HTTP/1.1 server implemented from raw TCP sockets in Python:**

```python
import socket
import os
import mimetypes
import datetime
import sys
from urllib.parse import unquote_plus
from typing import Dict, Tuple, Optional

class HTTPServer:
    def __init__(self, host: str = '0.0.0.0', port: int = 8080, root_dir: str = './public'):
        self.host = host
        self.port = port
        self.root_dir = os.path.abspath(root_dir)
        self.server_socket = None
        self.keep_alive = True
        self.chunk_size = 8192

        # Ensure root directory exists
        os.makedirs(self.root_dir, exist_ok=True)

    def start(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        
        print(f"HTTP/1.1 Server running on http://{self.host}:{self.port}")
        print(f"Serving files from: {self.root_dir}")

        try:
            while True:
                client_socket, addr = self.server_socket.accept()
                self.handle_client(client_socket)
        except KeyboardInterrupt:
            print("\nShutting down server...")
        finally:
            if self.server_socket:
                self.server_socket.close()

    def handle_client(self, client_socket: socket.socket):
        try:
            while True:  # Support keep-alive
                request = self.parse_request(client_socket)
                if not request:
                    break

                method, path, headers, body = request
                
                # Handle keep-alive
                connection = headers.get('connection', '').lower()
                should_close = connection == 'close' or not self.keep_alive

                if method == 'GET':
                    self.handle_get(client_socket, path, headers, should_close)
      ...
```

### DeepSeek V3

**Generation Time:** 104548ms
**Tokens:** 2486

```
# HTTP/1.1 Server Implementation

Here's a complete implementation of an HTTP/1.1 server using raw TCP sockets in Python:

```python
import socket
import os
import mimetypes
from threading import Thread
import time
from urllib.parse import unquote, urlparse, parse_qs

class HTTPServer:
    def __init__(self, host='0.0.0.0', port=8080):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.static_dir = 'static'  # Directory for static files
        self.routes = {}  # For potential route handling
        
        # Ensure static directory exists
        if not os.path.exists(self.static_dir):
            os.makedirs(self.static_dir)

    def start(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"Server running on http://{self.host}:{self.port}")
        
        try:
            while True:
                client_socket, client_address = self.server_socket.accept()
                print(f"Connection from {client_address}")
                thread = Thread(target=self.handle_client, args=(client_socket,))
                thread.daemon = True
                thread.start()
        except KeyboardInterrupt:
            print("\nShutting down server...")
            self.server_socket.close()

    def handle_client(self, client_socket):
        try:
            while True:
                request = self.receive_all(client_socket)
                if not request:
                    break  # Connection closed by client

                try:
                    method, path, headers, body = self.parse_request(request)
                    response = self.handle_request(method, path, headers, body)
                except Exception as e:
                    print(f"Error handling request: {e}")
                    response = self.error_response(4...
```

### GPT-OSS-120B

**Generation Time:** 17096ms
**Tokens:** 2171

```
Below is a **complete, self‑contained HTTP/1.1 server** that is written only with the Python standard library (no `http.server`, no external frameworks).  

It demonstrates how to:

* Accept raw TCP connections (`socket`)
* Parse the request line and headers (case‑insensitive)
* Read a request body that can be either **Content‑Length** or **chunked transfer‑encoding**
* Keep the connection alive when the client asks for it (the default for HTTP/1.1)
* Serve static files from a configurable document‑root
* Return a proper **404 Not Found** page
* Gracefully handle malformed requests (400 Bad Request) and unexpected errors (500 Internal Server Error)

The code is deliberately kept in a single file (`http_server.py`) so you can copy‑paste it, run it, and start experimenting.

---

## 1. How the server works (high‑level overview)

```
┌─────────────────────┐          ┌───────────────────────┐
│   Listening socket  │  accept  │  New client socket (TCP)│
└─────────┬───────────┘ ───────► └─────────────┬────────────┘
          │                                   │
          │   spawn a thread → handle_client()│
          │                                   │
          ▼                                   ▼
   ┌─────────────────────┐          ┌───────────────────────┐
   │   handle_client()   │  loop   │   read request line   │
   │  (keep‑alive loop)  │ ◄─────── │   read headers        │
   └───────┬─────────────┘          │   read body (if any) │
           │                        │   → build Request    │
           │                        └─────────────┬─────────┘
           │                                      │
           ▼                                      ▼
   ┌─────────────────────┐          ┌───────────────────────┐
   │  route_request()    │          │   build Response      │
   │   (GET/POST)        │ ◄─────── │   (status line, hdrs)│
   └───────┬─────────────┘          │   send body           │
           │                        └─────────────┬─────────┘
 ...
```

### Gemini 3 Flash Preview

**Generation Time:** 13338ms
**Tokens:** 2106

```
This implementation uses Python’s `socket` module to build a multi-threaded HTTP/1.1 server from the ground up. It handles manual byte-stream parsing, chunked decoding, and connection persistence.

### The Implementation (`server.py`)

```python
import socket
import threading
import os
import urllib.parse

# Configuration
HOST = '127.0.0.1'
PORT = 8080
BUFFER_SIZE = 4096
WEB_ROOT = './www'

class HTTPRequest:
    def __init__(self):
        self.method = ""
        self.path = ""
        self.version = ""
        self.headers = {}
        self.body = b""

class HTTPServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        if not os.path.exists(WEB_ROOT):
            os.makedirs(WEB_ROOT)

    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((self.host, self.port))
            s.listen(5)
            print(f"[*] Server listening on {self.host}:{self.port}")
            
            while True:
                conn, addr = s.accept()
                client_thread = threading.Thread(target=self.handle_client, args=(conn, addr))
                client_thread.start()

    def handle_client(self, conn, addr):
        conn.settimeout(10)  # Keep-alive timeout
        try:
            while True:
                request = self.parse_request(conn)
                if not request:
                    break

                response = self.process_request(request)
                conn.sendall(response)

                # Connection: keep-alive logic
                if request.headers.get('connection', '').lower() == 'close':
                    break
        except (socket.timeout, ConnectionResetError, BrokenPipeError):
            pass
        finally:
            conn.close()

    def read_until(self, conn, delimiter):
        """Helper to read from socket until a specific byte sequence (e.g., CRLF)."""
      ...
```

### MiniMax M2.5

**Generation Time:** 41149ms
**Tokens:** 4426

```
Here is a complete, single-file Python implementation of an HTTP/1.1 server using raw TCP sockets. It meets all your requirements, including chunked transfer encoding, keep-alive, and static file serving.

### The Python Code

Save this code as `server.py` and run it. It will serve files from a folder named `www` in the same directory.

```python
import socket
import os
import sys
import threading
import mimetypes

# Configuration
HOST = '0.0.0.0'
PORT = 8080
BUFFER_SIZE = 4096
ROOT_DIR = 'www'  # Make sure this directory exists

class RawHTTPServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        # Ensure root directory exists
        if not os.path.exists(ROOT_DIR):
            os.makedirs(ROOT_DIR)
            # Create a dummy index
            with open(os.path.join(ROOT_DIR, 'index.html'), 'w') as f:
                f.write("<h1>It Works!</h1><p>This is served by a raw Python socket.</p>")

    def start(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"Server listening on {self.host}:{self.port}")

        try:
            while True:
                client_socket, client_address = self.server_socket.accept()
                print(f"Connection from {client_address}")
                # Handle each client in a new thread to support concurrency
                # (Keep-alive is handled within the thread)
                client_thread = threading.Thread(target=self.handle_client, args=(client_socket,))
                client_thread.daemon = True
                client_thread.start()
        except KeyboardInterrupt:
            print("\nShutting down...")
        finally:
            self.server_socket.close()

    def handle_client(self, client_socket):
        """
        Handles the lif...
```

### MiMo-V2-Flash

**Generation Time:** 18700ms
**Tokens:** 2145

```
Here is a complete implementation of an HTTP/1.1 server using only Python's built-in `socket` and `os` libraries.

### Key Features Implemented:
1.  **Raw TCP Sockets**: Uses `socket.socket` and `select` (via `threading`) for concurrency.
2.  **HTTP/1.1 Protocol**:
    *   Parses Request Line and Headers.
    *   Handles `Connection: keep-alive` and closes connections on `Connection: close`.
    *   Returns standard HTTP status codes and headers.
3.  **Method Support**:
    *   **GET**: Serves static files (checks `index.html`) and handles 404s.
    *   **POST**: Reads the request body and echoes it back in the response.
4.  **Transfer Encoding**:
    *   **Chunked**: Parses incoming `Transfer-Encoding: chunked` bodies (Client -> Server).
    *   **Content-Length**: Used for standard non-chunked bodies.
5.  **Robustness**:
    *   Handles malformed requests (returns 400 Bad Request).
    *   Handles missing files (returns 404 Not Found).
    *   Thread-safe file serving.

### The Code

Save this code as `server.py` and run it with `python server.py`. Create an `index.html` file in the same directory to test the file serving.

```python
import socket
import threading
import os
import mimetypes

# Configuration
HOST = '0.0.0.0'
PORT = 8080
MAX_CONNECTIONS = 10
DOCUMENT_ROOT = os.getcwd()

class HTTPRequest:
    """Represents a parsed HTTP Request."""
    def __init__(self):
        self.method = None
        self.path = None
        self.version = None
        self.headers = {}
        self.body = b''
        self.keep_alive = True
        self.content_length = 0
        self.chunked = False

class HTTPServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.running = True

    def start(self):
        try:
            self.server_socket.bind((self.host, self.po...
```

---

*Generated by The Multivac V5*
*https://themultivac.com*