
from config import *
from utils import *
from client.client_role import run_client
from pi.pi_role import run_pi

if __name__ == "__main__":

    if update_git(): update_git()
    ROLE, POLLING_RATE, TIMEOUT = validate_config(ROLE, POLLING_RATE, TIMEOUT)

    if ROLE == "auto":
        val, path = is_pi()
        if val:
            ROLE = "pi"
            if path:
                with open('/sys/firmware/devicetree/base/model', 'r') as file:
                    content = file.read()
                    if not "Raspberry Pi Zero" in content:
                        print("WARNING: It is recommended to use a RPi Zero")
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