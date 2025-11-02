
import psutil

def get_cpu():
    # Returns CPU usage %, number of cores and CPU frequency in a dictionary
    return dict(percent=psutil.cpu_percent(interval=1), cores=psutil.cpu_count(logical=False), freq=psutil.cpu_freq())

def get_memory():
    # Returns RAM usage %, total RAM, used RAM and free RAM in a dictionary - Bytes
    mem = psutil.virtual_memory()
    return dict(percent=mem.percent, total=mem.total, used=mem.used, free=mem.free)

def get_disk():
    # Returns total disk usage %, total disk, used disk space, free disk space in a dictionary - Bytes
    disk = psutil.disk_usage("/")
    return dict(percent=disk.percent, disk_total=disk.total, disk_used=disk.used, free=disk.free)

def get_network():
    # Returns bytes sent, bytes received, incoming packets dropped and outgoing packets dropped in a dictionary
    net = psutil.net_io_counters()
    return dict(bytes_sent=net.bytes_sent, bytes_recv=net.bytes_recv, dropin=net.dropin, dropout=net.dropout)

def get_all():
    # Returns CPU, Memory, Disk and Network utilization stats
    return dict(cpu=get_cpu(), ram=get_memory(), disk=get_disk(), net=get_network())