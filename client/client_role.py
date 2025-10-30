
import time
import config
from network import start_listener, send_message
from client.flask_handler import FlaskThread
from client.ping_handler import PingHandler

def on_message(data="", addr=""):
    ip, port = addr
    typ, content = data
    if typ == "MSG":
        print(f"Ping from {ip}:{port} - {data}")
    elif typ == "DATA":
        piUDP, piPING, piDATA = content
        if not (config.UDP_PORT == piUDP and config.PING_PORT == piPING and config.DATA_PORT == piDATA):
            if config.RESOLVE_MISSMATCH:
                config.UDP_PORT, config.PING_PORT, config.DATA_PORT = piUDP, piPING, piDATA
            else:
                send_message(ip, port, "MISSMATCH")
                raise ValueError("Config Values Do Not Match Pi's")

def run_client():
    ping = PingHandler()
    flask_thread = None

    start_listener("0.0.0.0", config.UDP_PORT, on_message, 2)
    # Script is blocked until listener stops

    ping.start()

    while True:
        elapsed = ping.time_since_last_ping()

        if elapsed is None:
            time.sleep(1)
            continue

        if flask_thread is None:
            print("Pi connected - starting Flask server")
            flask_thread = FlaskThread(ping.stop_event)
            flask_thread.start()

        if elapsed > 12:
            print("Lost connection. Terminating program...")
            flask_thread.shutdown()
            ping.stop()
            flask_thread.join()
            break
        elif elapsed > 7:
            print(f"Possible Pi disconnect, waiting... ({round(elapsed, 0)})")
            time.sleep(1)