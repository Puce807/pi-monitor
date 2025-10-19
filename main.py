# main.py
from client import server
from client.utilization import *

if __name__ == "__main__":
    server.app.run(host="0.0.0.0", port=5000)
