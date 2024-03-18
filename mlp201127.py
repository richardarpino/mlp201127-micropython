from machine import Pin, SPI
import time
import max7219

class PowerDisplay(max7219.SevenSegment):

    Bar_1 = [0, 128, 192, 224, 240, 248, 252, 254, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255]
    Bar_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 128, 192, 224, 240, 248, 252, 254, 255, 255, 255, 255, 255, 255, 255, 255, 255]
    Bar_3 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 128, 192, 224, 240, 248, 252, 254, 255]

    SCAN_LIMIT = 7
    
    def __init__(self, cs, spi_bus, speaker=None):
        
        # NOTE: We have to re-implement basically what is in our base class init as I found
        # this board gets a bit weird on power cycle unless you send the mosi and sck pins
        # rather than use the defaults - which is what max7219.SevenSegment does
        self.scan_digits = self.digits = 4
        self._buffer = [0] * self.digits
        self.devices = 1
        self.reverse = False
        self._spi = spi_bus
        self._cs = cs
        self._speaker = speaker

        self.command(max7219.MAX7219_REG_SHUTDOWN, 0)     # not blanking mode
        self.command(max7219.MAX7219_REG_DISPLAYTEST, 0)  # no display test
        self.command(max7219.MAX7219_REG_SCANLIMIT, PowerDisplay.SCAN_LIMIT)  # We use 7 registers on this board
        self.command(max7219.MAX7219_REG_DECODEMODE, 0)   # use segments (not digits)
        self.command(max7219.MAX7219_REG_SHUTDOWN, 1)     # not blanking mode
        self.brightness(7)                        # intensity: range: 0..15
        self.reset()

    def reset(self, led_only:bool = False):
        for register in range(5, 9):
             self._write([register, 0x0])
        if not led_only:
            super(PowerDisplay, self).clear(True)

    def set_power(self, value):
        self._write(bytearray([5, PowerDisplay.Bar_1[value]]))
        self._write(bytearray([6, PowerDisplay.Bar_2[value]]))
        self._write(bytearray([7, PowerDisplay.Bar_3[value]]))

    def tone(self):
        if self._speaker:
            self._speaker.on()
            time.sleep_ms(350)
            self._speaker.off()

    def test(self):
        self._write([max7219.MAX7219_REG_DISPLAYTEST, 0x1])