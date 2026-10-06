# raw-tcp-server

A TCP server built from raw sockets in Python, with no frameworks, to understand
what happens underneath tools like uvicorn, FastAPI and nginx.

## Why

I use FastAPI behind nginx in Docker every day, but I wanted to understand the
layer below: how a process listens on a port, how the kernel handles
connections, and how a server deals with multiple clients.

## Run it

```bash
python server.py
```

In another terminal:

```bash
nc localhost 9000
```

Type a message and press Enter. The server echoes it back.

## Stages

- [x] **1. Blocking echo server**: one client at a time, multiple messages per connection
- [ ] **2. Thread per client**: handle several clients concurrently
- [ ] **3. Event loop with `selectors`**: one thread, many clients, using epoll
- [ ] **4. `asyncio` version**: the same model uvicorn uses
- [ ] **5. Minimal HTTP**: parse raw HTTP requests and respond to `curl` and a browser

## What I learned

- The `socket` module is a thin wrapper over Linux syscalls:
  `socket`, `setsockopt`, `bind`, `listen`, `accept4`, `recv`, `send`.
- TCP is implemented by the kernel, not by my program. The kernel completes the
  handshake and queues connections; `accept()` just takes one from the queue.
- `accept()` and `recv()` block because the kernel puts the thread to sleep
  until there is something to return. No CPU is used while waiting.
- A socket is a file descriptor, visible in `/proc/<pid>/fd`.
- `recv()` returning `b""` means the client closed the connection.
- `SO_REUSEADDR` avoids "Address already in use" caused by `TIME_WAIT`
  when restarting the server.
- Binding to `0.0.0.0` vs `127.0.0.1` matters, especially inside Docker.

## Useful commands

```bash
ss -tlnp | grep 9000                           # listening socket, PID and fd
ss -tnp | grep 9000                            # active connections
strace -e trace=network python server.py       # syscalls in real time
```
