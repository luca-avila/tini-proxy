import socket

# Define family and type: IPv4 + TCP
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as srv:

    # Allow port reuse after restart
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Associate to an IP and port
    srv.bind(("0.0.0.0", 9000))

    srv.listen()
    print("Listening on port 9000")
    
    while True:
        # Wait client
        conn, addr = srv.accept()
        print("Connected:", addr)
        
        while True:

            data = conn.recv(1024)

            if not data:
                break

            print("Received:", data)

            conn.sendall(b"Hello, I received: " + data)

            # Close connection and serve r
        conn.close()
        print("Disconnected from:", addr)
