
import threading
from werkzeug.serving import make_server
from flask import Flask, jsonify

from network import *
from client.utilization import *

app = Flask(__name__)

@app.route("/")
def get_data():
    data = get_all()
    return jsonify(data)

class Flask_Thread(threading.Thread):
    def __init__(self, Fstop_event):
        super().__init__()
        self.stop_event = Fstop_event
        self.server = make_server("0.0.0.0", 5000, app)
        self.ctx = app.app_context()
        self.ctx.push()

    def run(self):
        print("Flask Server started")
        while not self.stop_event.is_set():
            self.server.handle_request()
        print("Flask Server terminated")

    def shutdown(self):
        print("Terminating flask server...")
        self.stop_event.set()

def on_message(data="", addr=""):
    ip, port = addr
    print(f"Message: {data}")
    print(f"From {ip} on port {port}")
    pr_thread.start()

last_ping_time = 0
def handle_ping(ts):
    global last_ping_time
    last_ping_time = ts

stop_event = threading.Event()
flask_thread = Flask_Thread(stop_event)
pr_thread = threading.Thread(target=ping_responder, args=(stop_event,), kwargs={"on_ping": handle_ping})

start_listener("0.0.0.0", 5005, on_message, True)
flask_thread.start()

while True:
    if not last_ping_time == 0:
        elapsed = time.time() - last_ping_time
        if elapsed > 12:
            print("Lost connection with Pi. Terminating program...")
            flask_thread.shutdown()
            stop_event.set()
            pr_thread.join()
            flask_thread.join()
            break
        elif elapsed > 7:
            print(f"Possible Pi disconnect, waiting... ({round(elapsed,0)})")
    time.sleep(1)
