
try:
    import epaper
except ImportError as e:
    print("Import failed: ", e)

class EInkDisplay:
    def __init__(self):
        self.epd = epaper.epaper("epd2in13_V4").EPD()
        self.epd.init()

    def show_image(self, image):
        self.epd.display(self.epd.getbuffer(image))

    def clear(self):
        self.epd.clear(0xFF)

    def sleep(self):
        self.epd.sleep()