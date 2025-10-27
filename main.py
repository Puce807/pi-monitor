
from config import *
from utils import is_pi
from client.client_role import run_client
from pi.pi_role import run_pi

if __name__ == "__main__":
    if ROLE == "auto":
        if is_pi():
            ROLE = "pi"
        else:
            ROLE = "client"
    elif ROLE != "pi":
        if ROLE != "client":
            raise ValueError("Role should be pi, client or auto")

    print(f"ROLE: {ROLE}")
    if ROLE == "pi":
        run_pi()
    else:
        run_client()