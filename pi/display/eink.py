
try:
    from waveshare_epd import epd2in13
except ImportError:
    epd2in13 = None
from PIL import Image

class EInkDisplay:
    def __init__(self):
        self.epd = epd2in13.EPD()
        self.epd.init()

    def show_image(self, image):
        self.epd.display(self.epd.getbuffer(image))

    def clear(self):
        self.epd.clear(0xFF)

    def sleep(self):
        self.epd.sleep()