
import requests
import threading
import sys
from queue import Queue, Empty
from pi.eink_driver import EInkDisplay
from pi.renderer import Renderer
from config import *
from network import *

def on_message(data="", addr=""):
    ip, port = addr
    if data == "MISSMATCH":
        raise ValueError("Config Values Do Not Match Client's")
    elif data == "SUCCESS":
        print("Config values match client's")

def run_display(data_queue: Queue, stop_event):
    display = EInkDisplay()
    width, height = display.get_dimensions()
    dis_renderer = Renderer()

    while not stop_event.is_set():
        try:
            data = data_queue.get(timeout=DATA_TIMEOUT)
        except Empty:
            continue

        dis_renderer.give_data(data)
        display.clear()
        display.show_image(image=dis_renderer.render_img((width, height)))
        display.sleep()

def run_pi():
    config_vals = UDP_PORT, PING_PORT, DATA_PORT

    CLIENT_IP = get_client_ip()

    state = read_state()
    last = state

    data_queue = Queue()

    while True:
        cur = read_state()
        if cur == "1":
            print("USB Up, Connected")
            send_message(CLIENT_IP, UDP_PORT, ("MSG","connected"))
            break
        time.sleep(1)

    print("Sending Message...")
    send_message(CLIENT_IP, UDP_PORT, ("DATA", config_vals))
    print(f"Client IP: {CLIENT_IP}")
    print(f"UDP Port: {UDP_PORT}")
    start_listener("0.0.0.0", 5007, on_message, 1) # Port is not configurable as it always must be the same as client

    stop_event = threading.Event()
    display_thread = threading.Thread(target=run_display, args=(data_queue, stop_event), daemon=True)
    display_thread.start()

    # Main loop
    i = 0
    try:
        while True:
            time.sleep(POLLING_RATE)
            if not ping(CLIENT_IP, PING_PORT):
                print("No reply, trying to connect")
                if not ping(CLIENT_IP, PING_PORT, 5):
                    print(f"Client ({CLIENT_IP}) disconnected, terminating program")
                    stop_event.set()
                    display_thread.join(timeout=1)
                    return
            data = requests.get(f"http://{CLIENT_IP}:{DATA_PORT}").json()
            for x, y in data["cpu"].items():
                print(f"{x}: {y}")

            if i == 0:
                data_queue.put(data)
            i += 1
    except KeyboardInterrupt:
        print("Program stopped by Keyboard Interrupt")
        stop_event.set()
        display_thread.join(timeout=1)
        sys.exit()