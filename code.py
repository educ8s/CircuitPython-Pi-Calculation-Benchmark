# CircuitPython PI Benchmark Latest Version for all boards

import board, busio, os, time, terminalio, displayio, microcontroller
from adafruit_st7735r import ST7735R
from adafruit_display_text import label
from adafruit_display_shapes.rect import Rect

board_type = os.uname().machine
print(f"Board: {board_type}")
print(f"Cpu Frequency: {microcontroller.cpu.frequency/1000000} MHz")


if 'Pico' in board_type:
    clk_pin, mosi_pin, reset_pin, dc_pin, cs_pin = board.GP18, board.GP19, board.GP16, board.GP20, board.GP17
elif 'ESP32-S2' in board_type:
    mosi_pin, clk_pin, reset_pin, cs_pin, dc_pin = board.IO35, board.IO36, board.IO38, board.IO34, board.IO37    
else:
    mosi_pin, clk_pin, reset_pin, cs_pin, dc_pin = board.GP11, board.GP10, board.GP17, board.GP18, board.GP16
    print("This board is not supported. Change the pin definitions above.")

def calculate_pi(n):
    """
    Calculate the value of pi using the Bailey–Borwein–Plouffe formula.
    """
    pi = 0
    k = 0
    for k in range(n):
        pi += (1 / 16.**k) * ((4 / (8 * k + 1)) - (2 / (8 * k + 4)) - (1 / (8 * k + 5)) - (1 / (8 * k + 6)))
        k += 1
        if k%50 == 0:
            drawPercent(k/n)
    return pi

def drawTitle():
    text = "Pi Benchmark"
    text_area = label.Label(terminalio.FONT, text=text, color=0x0000FF, x=30, y=14)
    splash.insert(3, text_area)
    
def drawResult(pi):
    text = f"Result: {pi}"
    text_area = label.Label(terminalio.FONT, text=text, color=0x00ffff, x=20, y=120)
    splash.insert(4, text_area)
    
def drawTime(time):
    text = f"Time: {time} sec"
    text_area = label.Label(terminalio.FONT, text=text, color=0x00ffff, x=20, y=140)
    splash.insert(5, text_area)
    
def drawPercent(percent):
    progressBar = Rect(4, 60, int(120*percent), 20, fill=0x00ffff)
    splash[2] = progressBar
    
def drawEmptyProgressBar():
    empty_progress_bar = Rect(4, 60, 120, 20, outline=0x00ffff, stroke=3)
    splash.insert(1,empty_progress_bar)
    progressBar = Rect(4, 60, 0, 20, fill=0x00ffff)
    splash.insert(2, progressBar)

displayio.release_displays()

spi = busio.SPI(clock=clk_pin, MOSI=mosi_pin)

display_bus = displayio.FourWire(spi, command=dc_pin, chip_select=cs_pin, reset=reset_pin)

display = ST7735R(display_bus, width=128, height=160)

# Make the display context
splash = displayio.Group()
display.show(splash)

color_bitmap = displayio.Bitmap(128, 160, 1)
color_palette = displayio.Palette(1)
color_palette[0] = 0x000000 

bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
splash.insert(0, bg_sprite)
drawEmptyProgressBar()

drawTitle()

start_time = time.monotonic()
pi = calculate_pi(60000)
end_time = time.monotonic()
execution_time = round(end_time - start_time,4)

drawResult(pi)
drawTime(execution_time)

while True:
    pass