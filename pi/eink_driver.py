
try:
    import epaper
except ImportError as e:
    print("Import failed: ", e)
from PIL import Image

class EInkDisplay:
    def __init__(self):
        self.epd = epaper.epaper("epd2in13_V4").EPD()
        self.epd.init()

    def show_image(self, image):
        self.epd.display(self.epd.getbuffer(image))

    def get_dimensions(self):
        return self.epd.height, self.epd.width

    def clear(self):
        self.epd.clear(0xFF)

    def sleep(self):
        self.epd.sleep()