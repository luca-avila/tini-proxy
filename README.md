# tini-proxy

A TCP server built from raw sockets in Python, with no frameworks, that grows
step by step into an HTTP server and finally a toy reverse proxy / load
balancer. The goal is to understand what happens underneath tools like
uvicorn, FastAPI and nginx.

## Why

I use FastAPI behind nginx in Docker every day, but I wanted to understand the
layer below: how a process listens on a port, how the kernel handles
connections, how a server deals with multiple clients, and what a reverse
proxy actually does with the bytes in between.

## Run it

```bash
python server.py
```

In another terminal:

```bash
nc localhost 9000
```

Type a message and press Enter. The server echoes it back.

## Roadmap

### 1. TCP echo server

`bind`, `listen`, `accept`, `recv`/`send`. This is where it becomes clear that
TCP is a byte stream, not a sequence of messages, and framing becomes a problem.

- [x] Blocking echo server, multiple messages per connection
- [ ] Explore framing: partial reads, several messages in one `recv()`
- [ ] Implement a framing strategy (delimiter or length prefix)

### 2. HTTP/1.1 server from scratch

- [ ] Parse the request line and headers
- [ ] Read the body using `Content-Length`
- [ ] Keep-alive: several requests over one connection
- [ ] Serve static files
- [ ] Test with `curl -v` and a browser

### 3. Concurrency

The progression that ends up explaining what uvicorn does underneath FastAPI.

- [ ] One thread per connection
- [ ] Hand-written event loop with `selectors` (epoll)
- [ ] `asyncio` version

### 4. Mini reverse proxy / load balancer

A toy nginx.

- [ ] Forward requests to a backend
- [ ] Round-robin between two backends
- [ ] Health checks
- [ ] Timeouts

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
