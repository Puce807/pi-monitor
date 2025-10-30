
import platform, os
import subprocess

from config import AUTO_CORRECT_CONFIG

def bytes_gigabytes(byte):
    return byte // 1000000000

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

def validate_value(value, default, valid_options=None, valid_range=None):
    if valid_options is not None:
        if value not in valid_options:
            if AUTO_CORRECT_CONFIG:
                print(f"Reverting value {value} to default {default}")
                return default
            else:
                raise ValueError(f"Value {value} must be one of {valid_options}")
    elif valid_range is not None:
        range1, range2 = valid_range
        if not (range1 <= value <= range2):
            if AUTO_CORRECT_CONFIG:
                print(f"Reverting value {value} to default {default}")
                return default
            else:
                raise ValueError(f"Value {value} must be in the range {range1}-{range2}")
    return value

def validate_config(ROLE, POLLING_RATE, TIMEOUT):
    # General
    ROLE = validate_value(ROLE, "auto", valid_options=("pi", "client", "auto"))
    # Pi
    POLLING_RATE = validate_value(POLLING_RATE, 3, valid_range=(2, 60))
    # Client
    TIMEOUT = validate_value(TIMEOUT, 12, valid_range=(6, 61))
    print("Config Validated Successfully")
    return ROLE, POLLING_RATE, TIMEOUT

