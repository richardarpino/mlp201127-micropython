from machine import Pin, SPI
import time
import max7219

class PowerDisplay(max7219.SevenSegment):

    Bar_1 = [0, 128, 192, 224, 240, 248, 252, 254, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255]
    Bar_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 128, 192, 224, 240, 248, 252, 254, 255, 255, 255, 255, 255, 255, 255, 255, 255]
    Bar_3 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 128, 192, 224, 240, 248, 252, 254, 255]

    SCAN_LIMIT = 7

    # Init Class with pins that MLP201127 is connected to
    def __init__(self, cs: Pin, spi_bus: Pin, speaker: Pin=None):
        
        #cs: Clock Pin e.g. cs = Pin(5, Pin.OUT)
        #spi_bus: SPI Bus e.g SPI(0, baudrate=10000000, polarity=1, phase=1, sck=Pin(2), mosi=Pin(3))
        #speaker: Speaker Pin e.g Pin(7, Pin.OUT)
        
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

    # reset - reset all the registers on the board or just the leds (you can use the base classes 'clear' for just the digits)
    def reset(self, led_only:bool = False):
        for register in range(5, 8):
             self._write([register, 0x0])
        if not led_only:
            super(PowerDisplay, self).clear(True)

    # set_power - sets the number of leds to illuminate (0-24). Any values over 24 will be treated as 24 and no error will be thrown
    def set_power(self, value):
        setting = value
        if setting >= len(PowerDisplay.Bar_1):
            setting = len(PowerDisplay.Bar_1) - 1
        if setting < 0:
            setting = 0
        self._write(bytearray([5, PowerDisplay.Bar_1[setting]]))
        self._write(bytearray([6, PowerDisplay.Bar_2[setting]]))
        self._write(bytearray([7, PowerDisplay.Bar_3[setting]]))

    # tone - emit a 300ms tone from the onboard speaker (if Pin is provided)
    def tone(self):
        if self._speaker:
            self._speaker.on()
            time.sleep_ms(350)
            self._speaker.off()
    
    # test - illuminate everything as a display test
    def test(self):
        self._write([max7219.MAX7219_REG_DISPLAYTEST, 0x1])
