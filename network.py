
import os
import socket
import time

def read_state(IFACE="usb0"):
    try:
        with open(f"/sys/class/net/{IFACE}/carrier") as f:
            return f.read().strip()
    except FileNotFoundError:
        return "0"

def send_message(IP, PORT, MESSAGE):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        if isinstance(MESSAGE, str):
            MESSAGE = MESSAGE.encode()
        sock.sendto(MESSAGE, (IP, PORT))
    finally:
        sock.close()

def start_listener(ip, port, callback, stop):
    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((ip, port))
    print(f"Listening on {ip}:{port}...")
    while True:
        data, addr = sock.recvfrom(1024)
        callback(data.decode(), addr)
        if stop:
            break

def ping(ip, port, timeout=2):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(timeout)
    try:
        sock.sendto(b"ping", (ip, port))
        data, addr = sock.recvfrom(1024)
        if data == b"pong":
            print("Client Connected")
            return True
    except socket.timeout:
        print("No reply, possible client disconnect")
        return False
    finally:
        sock.close()

def ping_responder(stop_event, ip="0.0.0.0", port=5006, on_ping=None):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((ip, port))
    sock.settimeout(1)
    print(f"Listening for pings on {ip}:{port}")
    while not stop_event.is_set():
        try:
            data, addr = sock.recvfrom(1024)
            if data == b"ping":
                sock.sendto(b"pong", addr)
                print(f"Replied to ping from {addr[0]}")
        except socket.timeout:
            continue
        if on_ping:
            on_ping(time.time())

    sock.close()