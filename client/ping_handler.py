
from config import UDP_PORT
from network import ping_responder, start_listener
import threading
import time

class PingHandler:
    def __init__(self):
        self.last_ping = 0
        self.stop_event = threading.Event()
        self.ping_thread = threading.Thread(
            target = ping_responder,
            args = (self.stop_event,),
            kwargs = {"on_ping": self.handle_ping},
            daemon = True
        )

    def handle_ping(self, ts):
        self.last_ping = ts

    def start(self):
        self.ping_thread.start()

    def time_since_last_ping(self):
        if not self.last_ping:
            return None
        return time.time() - self.last_ping

    def stop(self):
        self.stop_event.set()
        self.ping_thread.join()