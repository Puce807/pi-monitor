
from PIL import Image, ImageDraw, ImageFont
from pi.layout import Layout
from config import *
from client.utilization import get_all
from utils import bytes_gigabytes, bytes_megabytes

class Renderer:
    def __init__(self):
        self.layout = Layout()
        self.font = ImageFont.truetype(FONT_PATH, 14)
        self.small_font = ImageFont.truetype(FONT_PATH, 14)

        self.cpu = None
        self.ram = None
        self.sent = None
        self.recv = None
        self.disk_used = None
        self.disk_total = None

    def draw_centered_text(self, draw, position, text, font=None, fill=0):
        if font is None:
            font = self.small_font
        bbox = draw.textbbox((0, 0), text, font=font)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
        x, y = position
        draw.text((x - tw / 2, y - th / 2), text, font=font, fill=fill)

    def give_data(self, data):
        self.cpu = data["cpu"]["percent"]
        self.ram = data["ram"]["percent"]
        self.sent = round(bytes_megabytes(data["net"]["bytes_sent"]), 1)
        self.recv = round(bytes_megabytes(data["net"]["bytes_recv"]), 1)
        self.disk_used = round(bytes_gigabytes(data["disk"]["d_used"]), 1)
        self.disk_total = round(bytes_gigabytes(data["disk"]["d_total"]))

        disk_decimal = int(self.disk_used) / int(self.disk_total)
        disk_len = round(disk_decimal * 236)
        self.layout.disk_fill_coords = [(7, 54), (7+disk_len, 60)]

    def render_img(self, size):
        img = Image.new('1', size, 255)
        draw = ImageDraw.Draw(img)

        if self.cpu is not None:
            draw.text(self.layout.cpu_label, f"CPU:  {self.cpu}%", font=self.font, fill=0)
            draw.text(self.layout.ram_label, f"RAM:  {self.ram}%", font=self.font, fill=0)
            draw.text(self.layout.sent_label, f"Sent: {self.sent}MB", font=self.font, fill=0)
            draw.text(self.layout.recv_label, f"Recv: {self.recv}MB", font=self.font, fill=0)
            draw.text(self.layout.disk_label, f"Disk: {self.disk_used}GB/{self.disk_total}GB", font=self.font, fill=0)

            draw.rectangle(self.layout.disk_full_coords, fill=0)
            draw.rectangle(self.layout.disk_clear_coords, fill=255)
            draw.rectangle(self.layout.disk_fill_coords, fill=0)

            draw.rectangle(self.layout.graph_full_coords, fill=0)
            draw.rectangle(self.layout.graph_clear_coords, fill=255)
        else:
            self.draw_centered_text(draw, self.layout.warning_text, "Warning: Data not found")
            draw.polygon(self.layout.warn_out_coords, fill=0)
            draw.polygon(self.layout.warn_clear_coords, fill=255)
            draw.rectangle(self.layout.warn_line_coords, fill=0)
            draw.rectangle(self.layout.warn_dot_coords, fill=0)

        return img