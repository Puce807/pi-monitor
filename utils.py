
import platform, os

def bytes_gigabytes(byte):
    return byte // 1000000000

def is_pi():
    return (
        "raspberrypi" in platform.uname().node.lower()
        or os.path.exists("/sys/firmware/devicetree/base/model")
    )