# Python Redis-Like Server (RESP Redis Clone)

A lightweight, experimental Redis-style key-value store written in Python.  
This project is currently **on hold** but already includes a functional command parser, a custom Redis-protocol-parser for the RESP protocol implementation, and several Redis-inspired commands.

The goal of the project is to explore how Redis works internally — networking, serialization, command dispatching, and data structures — while building a small, educational clone.

---

## Project Status

- **Not production-ready**
- **Project currently on hold**
- Docker support **planned**
- Reverse proxy **planned**
- Volatile Memory 
- Uses raw TCP sockets + a custom version of the **RESP protocol**
- Streams support is **work-in-progress**

---

## RESP — Redis Serialization Protocol (Custom Implementation)

The server communicates over TCP sockets using a custom-built RESP parser, inspired by Redis' own protocol but adapted for this implementation.

RESP is responsible for converting raw socket bytes into structured command arrays that the server executes.

Implementation file:  
`RPP.py`

---

## Implemented Commands

Each command exists in its own Python file.

### **String Commands**
- `SET`
- `GET`
- `ECHO`
- `TYPE`

### **List Commands**
- `LPUSH`
- `RPUSH`
- `LPOP`
- `BLPOP`
- `LLEN`
- `LRANGE`

### **Connection / Misc**
- `PONG`

### **Streams (WIP)**
- `XADD`

### Command Files

- BLPOP.py
- ECHO.py
- GET.py
- LLEN.py
- LPOP.py
- LPUSH.py
- LRANGE.py
- Pong.py
- RESP.py
- RPUSH.py
- SET.py
- TYPE.py
- XADD.py

---

## Data Storage

Data is stored in a "complex" python dict

## Networking

The server:

- uses Python sockets  
- receives raw bytes  
- decodes them with the custom RESP parser  
- uses a Method to map command String to fitting command file

---

## Testing

A `tests/` directory includes unit tests for most implemented commands.  
These tests help ensure Redis-like behavior and internal consistency.

---

## Planned Features

- Docker image & docker-compose setup  
- Reverse proxy support  
- Full stream support (`XREAD`, `XRANGE`, `XDEL`, ...)  
- More Redis commands  
- Configurable persistence layer  
- Official CLI client  
- Configuration file  

---

## Getting Started

```bash
# Clone the repository
git clone <https://github.com/Jeffnicht/Python-Redis.git>

# Run the server
python main.py
