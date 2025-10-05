# main.py
from client import server
from client.utilization import get_cpu

if __name__ == "__main__":
    server.data = get_cpu()
    server.app.run(host="0.0.0.0", port=5000)
