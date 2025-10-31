
from eink import EInkDisplay
from PIL import Image, ImageDraw, ImageFont
from layout import Layout
from config import *

class Renderer:
    def __init__(self):
        self.layout = Layout()
        self.font = ImageFont.truetype(FONT_PATH, 14)

    def render(self):
        img = Image.new('1', (250, 122), 255)
        draw = ImageDraw.Draw(img)

        draw.text(self.layout.hello_label, "Hello World!", font=self.font, fill=0)

        return img

if __name__ == "__main__":
    display = EInkDisplay()
    renderer = Renderer
    display.show_image(image=renderer.render)
    display.sleep()
    try: pass
    except KeyboardInterrupt:
        display.clear()