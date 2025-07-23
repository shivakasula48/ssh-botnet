# test_server.py - Run this on your target machine
import socket
import threading
import time
from datetime import datetime

def handle_client(client_socket, addr):
    try:
        client_socket.settimeout(5)
        data = client_socket.recv(1024)
        print(f"[{datetime.now()}] Connection from {addr}: {len(data)} bytes")
        client_socket.close()
    except:
        pass

def start_server(port=80):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('0.0.0.0', port))
    server.listen(100)
    print(f"Test server listening on port {port}")
    
    while True:
        try:
            client, addr = server.accept()
            thread = threading.Thread(target=handle_client, args=(client, addr))
            thread.start()
        except KeyboardInterrupt:
            break
    
    server.close()

if __name__ == "__main__":
    start_server(8080)  # Use port 8080 for testing
