import board,busio
import terminalio
import time
from time import sleep
from adafruit_st7735r import ST7735R
import displayio
from adafruit_display_text import label
from adafruit_display_shapes.rect import Rect

mosi_pin = board.IO35
clk_pin = board.IO36
reset_pin = board.IO38
cs_pin = board.IO34
dc_pin = board.IO37

def calculate_pi(n):
    """
    Calculate the value of pi using the Bailey–Borwein–Plouffe formula.
    """
    pi = 0
    k = 0
    while k < n:
        pi += (1 / (16 ** k)) * ((4 / (8 * k + 1)) - (2 / (8 * k + 4)) - (1 / (8 * k + 5)) - (1 / (8 * k + 6)))
        k += 1
        if k%50 == 0:
            drawPercent(k/n)
    return pi

def drawTitle():
    text = "Pi Benchmark"
    text_area = label.Label(terminalio.FONT, text=text, color=0x0000FF, x=30, y=14)
    splash.append(text_area)
    
def drawResult(pi):
    text = f"Result: {pi}"
    text_area = label.Label(terminalio.FONT, text=text, color=0x00ffff, x=20, y=120)
    splash.append(text_area)
    
def drawTime(time):
    text = f"Time: {time} sec"
    text_area = label.Label(terminalio.FONT, text=text, color=0x00ffff, x=20, y=140)
    splash.append(text_area)
    
def drawPercent(percent):
    progressBar = Rect(4, 60, int(120*percent), 20, fill=0x00ffff)
    if percent > 0.1:
        splash.pop()
    splash.append(progressBar)
    
def drawEmptyProgressBar():
    progressBar = Rect(4, 60, 120, 20, outline=0x00ffff, stroke=3)
    splash.append(progressBar)
    
def displaySplashScreen(group):
    bitmap = displayio.OnDiskBitmap("/splash.bmp")
    tile_grid = displayio.TileGrid(bitmap, pixel_shader=bitmap.pixel_shader)
    group.append(tile_grid)
    sleep(2)
    

displayio.release_displays()

spi = busio.SPI(clock=clk_pin, MOSI=mosi_pin)

display_bus = displayio.FourWire(spi, command=dc_pin, chip_select=cs_pin, reset=reset_pin)

display = ST7735R(display_bus, width=128, height=160)

# Make the display context
splash = displayio.Group()
display.show(splash)

displaySplashScreen(splash)

color_bitmap = displayio.Bitmap(128, 160, 1)
color_palette = displayio.Palette(1)
color_palette[0] = 0x000000 

bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
splash.append(bg_sprite)

drawEmptyProgressBar()

drawTitle()
start_time = time.monotonic()
pi = calculate_pi(1500)
end_time = time.monotonic()
execution_time = round(end_time - start_time,4)

drawResult(pi)

drawTime(execution_time)

while True:
    pass