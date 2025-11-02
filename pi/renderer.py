
from PIL import Image, ImageDraw, ImageFont
from pi.layout import Layout
from config import *
from client.utilization import get_all
from utils import bytes_gigabytes, bytes_megabytes

class Renderer:
    def __init__(self):
        self.layout = Layout()
        self.font = ImageFont.truetype(FONT_PATH, 14)

        self.cpu = None
        self.ram = None
        self.sent = None
        self.recv = None
        self.disk_used = None
        self.disk_total = None

    def get_data(self):
        data = get_all()
        self.cpu = data["cpu"]["percent"]
        self.ram = data["ram"]["percent"]
        self.sent = round(bytes_gigabytes(data["net"]["bytes_sent"]), 1)
        self.recv = round(bytes_gigabytes(data["net"]["bytes_recv"]), 1)
        self.disk_used = bytes_gigabytes(data["disk"]["d_used"])
        self.disk_total = bytes_gigabytes(data["disk"]["d_total"])

    def render_img(self, size):
        img = Image.new('1', size, 255)
        draw = ImageDraw.Draw(img)

        self.get_data()

        draw.text(self.layout.cpu_label, f"CPU:  {self.cpu}%", font=self.font, fill=0)
        draw.text(self.layout.ram_label, f"RAM:  {self.ram}%", font=self.font, fill=0)
        draw.text(self.layout.sent_label, f"Sent: {self.sent}GB", font=self.font, fill=0)
        draw.text(self.layout.recv_label, f"Recv: {self.recv}GB", font=self.font, fill=0)
        draw.text(self.layout.disk_label, f"Disk: {self.disk_used}GB/{self.disk_total}GB", font=self.font, fill=0)

        draw.rectangle(self.layout.disk_full_coords, fill=0)
        draw.rectangle(self.layout.disk_clear_coords, fill=255)
        draw.rectangle(self.layout.disk_fill_coords, fill=0)

        draw.rectangle(self.layout.graph_full_coords, fill=0)
        draw.rectangle(self.layout.graph_clear_coords, fill=255)

        return img