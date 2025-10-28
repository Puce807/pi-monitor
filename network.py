
import os
import socket
import time
import json

def read_state(IFACE="usb0"):
    try:
        with open(f"/sys/class/net/{IFACE}/carrier") as f:
            return f.read().strip()
    except FileNotFoundError:
        return "0"

def send_message(IP, PORT, MESSAGE):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        if not isinstance(MESSAGE, (bytes, bytearray)):
            MESSAGE = json.dumps(MESSAGE).encode('utf-8')
        sock.sendto(MESSAGE, (IP, PORT))
    finally:
        sock.close()

def start_listener(ip, port, callback, stop):
    # Stop = amount of time script will loop until terminating
    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((ip, port))
    print(f"Listening on {ip}:{port}...")
    i = 0
    while i < stop:
        data, addr = sock.recvfrom(1024)
        decoded = json.loads(data.decode())
        callback(data.decode(), addr)
        i += 1

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
    print(f"\nListening for pings on {ip}:{port}")
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

def get_client_ip(interface="usb0"):
    import subprocess
    result = subprocess.run(["arp", "-i", interface, "-n"], capture_output=True, text=True)
    for line in result.stdout.splitlines():
        if "ether" in line and interface in line:
            parts = line.split()
            if len(parts) >= 1 and parts[0].startswith("10."):
                return parts[0]
    return None