
from PIL import Image, ImageDraw, ImageFont
from pi.layout import Layout

class Renderer:
    def __init__(self):
        self.layout = Layout()
        self.font = ImageFont.truetype("../assets/Monocraft.ttc", 16)
        self.small_font = ImageFont.truetype("../assets/Monocraft.ttc", 14)

    def draw_centered_text(self, draw, position, text, fill=0):
        bbox = draw.textbbox((0, 0), text, font=self.small_font)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
        x, y = position
        draw.text((x - tw / 2, y - th / 2), text, font=self.small_font, fill=fill)

    def render_img(self, size):
        img = Image.new('1', size, 255)
        draw = ImageDraw.Draw(img)

        success = False

        if success:
            draw.text(self.layout.cpu_label, f"CPU:  50%", font=self.font, fill=0)
            draw.text(self.layout.ram_label, f"RAM:  90%", font=self.font, fill=0)
            draw.text(self.layout.sent_label, f"Sent: 10mb", font=self.font, fill=0)
            draw.text(self.layout.recv_label, f"Recv: 15mb", font=self.font, fill=0)
            draw.text(self.layout.disk_label, f"Disk: 20mb/15GB", font=self.font, fill=0)

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

render = Renderer()
image = render.render_img((250, 122))
image.save("preview.png")