
def bytes_gigabytes(byte):
    return byte // 1000000000

def get_client_ip(interface="usb0"):
    import subprocess
    result = subprocess.run(["arp", "-i", interface, "-n"], capture_output=True, text=True)
    for line in result.stdout.splitlines():
        if "ether" in line and interface in line:
            parts = line.split()
            if len(parts) >= 1 and parts[0].startswith("10."):
                return parts[0]
    return None