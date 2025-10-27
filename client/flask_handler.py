import threading
import requests
from wsgiref.simple_server import make_server
from flask import Flask, jsonify

from config import DATA_PORT
from client.utilization import *

class FlaskThread(threading.Thread):
    def __init__(self, Fstop_event):
        super().__init__(daemon=True)
        self.stop_event = Fstop_event
        self.app = Flask(__name__)
        self.server = make_server("0.0.0.0", DATA_PORT, self.app)
        self.ctx = self.app.app_context()
        self.ctx.push()

    def setup(self):
        @self.app.route("/")
        def get_data():
            return jsonify(get_all())

    def run(self):
        print("Flask Server Started")
        while not self.stop_event.is_set():
            self.server.handle_request()
        print("Flask Server Terminated")

    def shutdown(self):
        print("Terminating flask server...")
        self.stop_event.set()
        try:
            requests.get(f"http://127.0.0.1:{DATA_PORT}")
        except requests.RequestException as e:
            print(f"Could not send unblock request - {e}")
        else:
            print("Unblock request sent successfully")
