
import time
import config
from config import TIMEOUT, AUTO_RECONNECT
from network import start_listener, send_message
from client.flask_handler import FlaskThread
from client.ping_handler import PingHandler

def on_message(data="", addr=""):
    ip, port = addr
    typ, content = data
    if typ == "MSG":
        print(f"Ping from {ip}:{port} - {data}")
    elif typ == "DATA":
        # Validate Config
        piUDP, piPING, piDATA = content
        if not (config.UDP_PORT == piUDP and config.PING_PORT == piPING and config.DATA_PORT == piDATA):
            if config.RESOLVE_MISSMATCH:
                config.UDP_PORT, config.PING_PORT, config.DATA_PORT = piUDP, piPING, piDATA
                print("Config missmatch resolved")
            else:
                send_message(ip, 5007, "MISSMATCH")
                raise ValueError("Config Values Do Not Match Pi's")
        else:
            print("Config matches pi")
            send_message(ip, 5007, "SUCCESS")

def run_client():
    while True:
        ping = PingHandler()
        flask_thread = None

        start_listener("0.0.0.0", config.UDP_PORT, on_message, 2)
        # Script is blocked until listener stops

        ping.start()

        connected = True
        while connected:
            elapsed = ping.time_since_last_ping()

            if elapsed is None:
                time.sleep(1)
                continue

            if flask_thread is None:
                print("Pi connected - starting Flask server")
                flask_thread = FlaskThread(ping.stop_event)
                flask_thread.start()

            if elapsed > TIMEOUT:
                print("Lost connection. Terminating program...")
                connected = False
            elif elapsed > 7:
                print(f"Possible Pi disconnect, waiting... ({round(elapsed, 0)})")
                time.sleep(1)

        flask_thread.shutdown()
        ping.stop()
        flask_thread.join()

        if not AUTO_RECONNECT:
            break