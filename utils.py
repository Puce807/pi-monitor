
import time
import platform, os
import subprocess

from config import AUTO_CORRECT_CONFIG

def bytes_gigabytes(byte):
    return byte // 1000000000

def bytes_megabytes(byte):
    return byte // 1000000

def is_pi():
    path = os.path.exists("/sys/firmware/devicetree/base/model")
    return ("raspberrypi" in platform.uname().node.lower()
        or path), path

def update_git():
    try:
        subprocess.run(["git", "fetch"], check=True)
    except subprocess.CalledProcessError:
        print("Github fetch failed")
        return

    result = subprocess.run(
        ["git", "rev-list", "--count", "HEAD...@{upstream}"],
        capture_output=True,
        text=True,
        check=True )

    commits_behind = int(result.stdout.strip())

    if commits_behind > 0:
        print(f"Local repo is {commits_behind} commits behind. Updating...")
        try: subprocess.run(["git", "pull"], check=True)
        except subprocess.CalledProcessError:
            print("Pull failed")
            return
        print("Pull complete")
    else:
        print("Local repo up-to-date")

    time.sleep(1)

def validate_value(value, default, valid_options=None, valid_range=None, custom_msg=None):
    if valid_options is not None:
        if value not in valid_options:
            if AUTO_CORRECT_CONFIG:
                print(f"Reverting value {value} to default {default}")
                return default
            else:
                if custom_msg is not None:
                    print(f"Value {value} disallowed: {custom_msg}")
                raise ValueError(f"Value {value} must be one of {valid_options}")
    elif valid_range is not None:
        range1, range2 = valid_range
        if not (range1 <= value <= range2):
            if AUTO_CORRECT_CONFIG:
                print(f"Reverting value {value} to default {default}")
                return default
            else:
                if custom_msg is not None:
                    print(f"Value {value} disallowed: {custom_msg}")
                raise ValueError(f"Value {value} must be in the range {range1}-{range2}")
    return value

def validate_config(ROLE, POLLING_RATE, TIMEOUT_LIM, TIMEOUT_THRESH):
    # General
    ROLE = validate_value(ROLE, "auto", valid_options=("pi", "client", "auto"))
    # Pi
    POLLING_RATE = validate_value(POLLING_RATE, 3, valid_range=(2, 60))
    # Client
    TIMEOUT_LIM = validate_value(TIMEOUT_LIM, 25, valid_range=(6, 61))
    TIMEOUT_THRESH = validate_value(TIMEOUT_THRESH, 16, valid_range=(POLLING_RATE+1, TIMEOUT_LIM-1),
                                    custom_msg=f"Must be greater than POLLING_RATE ({POLLING_RATE}) and less than TIMEOUT_LIM ({TIMEOUT_LIM-1})")
    print("Config Validated Successfully")
    return ROLE, POLLING_RATE, TIMEOUT_LIM, TIMEOUT_THRESH

