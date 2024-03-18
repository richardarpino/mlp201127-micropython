# MLP201127 MicroPython driver based on RPI Pico
Python driver for Mottram Labs MLP201127 LED and 4x7 Segment Display based on MAX7219

You can find more about this driver from the [maker](https://www.mottramlabs.com/): [Round LED Bar Graph Power Display - RED - Arduino - ESP8266 - MLP201127](https://www.ebay.co.uk/itm/133752718757)

Based on the MAX7219, the first 4 registers are for the 4x7 digit LED dispay and the following 3 are for the surrounding LEDs, one for each colour. There is a super simple implementation for the onboard speaker too.

Implementation inherits from [micropython-MAX7219](https://github.com/JennaSys/micropython-max7219/) which provides excellent support for the LED digits and I added an additional methods to initialise using specific Pins, set the leds using an integer and reset.

![RPi Pico with the ML201127 Display](https://github.com/richardarpino/mlp201127-micropython/blob/main/MLP201127%20with%20RPi%20Pico.jpg)

## Example Implementation
| Board       | GPIO        | RPI Pin     |
| ----------- | ----------- | ----------- |
| din         | gpio3       | 5           |
| cs          | gpio5       | 7           |
| clk         | gpio2       | 4           |
| spkr        | gpio7       | 10          |

```
# Import MicroPython libraries of PIN and SPI
from mlp201127 import PowerDisplay
from machine import SPI, Pin
from time import sleep

# Intialize the Pins
spi_bus = SPI(0, baudrate=10000000, polarity=1, phase=1, sck=Pin(2), mosi=Pin(3))
cs = Pin(5, Pin.OUT)
speaker = Pin(7, Pin.OUT)

display = PowerDisplay(cs, spi_bus, speaker)

# Handy python version of Arduino map function
def map_range(x, in_min, in_max, out_min, out_max):
  return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min

# Python implementation of soak test from Mottram Labs - https://github.com/Mottramlabs/MAX7219-LED-Bar-Graph-Power-Display/blob/master/Firmware/Power_Display_Soak_Round_Type_Version_1/Power_Display_Soak_Round_Type_Version_1.ino
for yy in range(5):
    zz = 0.0
    display.tone()
    while zz < 100.1:
        sleep(0.001)
        display.number(zz)
        xx = int(zz)
        xx = map_range(xx, 0, 100, 0, 24)
        display.set_power(xx)
        zz += 0.1
```

## Dependencies
[micropython-MAX7219](https://github.com/JennaSys/micropython-max7219/) - provides base support for LED digits
