
import platform, os
import subprocess

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
