import socket

# Define family and type: IPv4 + TCP
srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Allow port reuse after restart
srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Associate to an IP and port
srv.bind(("0.0.0.0", 9000))

srv.listen()
print("Listening on port 9000")

# Wait client
conn, addr = srv.accept()

print("Connected:", addr)


data = conn.recv(1024)
print("Received:", data)

conn.sendall(b"Hello, I received: " + data)

# Close connection and server
conn.close()
srv.close()
