from machine import Pin
import time
import neopixel
import random

np = neopixel.NeoPixel(Pin(14), 45)

photodiodes = [
    Pin(4, Pin.IN, Pin.PULL_UP),   # Photodiode 1
    Pin(5, Pin.IN, Pin.PULL_UP),   # Photodiode 2
    Pin(12, Pin.IN, Pin.PULL_UP),  # Photodiode 3
    Pin(13, Pin.IN, Pin.PULL_UP),  # Photodiode 4
    Pin(15, Pin.IN, Pin.PULL_UP),  # Photodiode 5
    Pin(16, Pin.IN, Pin.PULL_UP),  # Photodiode 6
    Pin(17, Pin.IN, Pin.PULL_UP),  # Photodiode 7
    Pin(18, Pin.IN, Pin.PULL_UP),  # Photodiode 8
    Pin(19, Pin.IN, Pin.PULL_UP)   # Photodiode 9
]

buzzer = Pin(25, Pin.OUT)

# Map each photodiode index to 3 NeoPixels
led_groups = {

    0: [42, 43, 44],
    1: [36, 37, 38],
    2: [30, 31, 32],
    3: [27, 28, 29],
    4: [21, 22, 23],
    5: [15, 16, 17],
    6: [12, 13, 14],
    7: [6, 7, 8],
    8: [0, 1, 2]
}

point = 0

def ran():
    return random.randint(0, 8)  # Choose one photodiode randomly

def beep():
    buzzer.value(1)
    time.sleep(0.1)
    buzzer.value(0)

while True:
    t = time.time()
    target = ran()
    pixels = led_groups[target]

    # Light up target LEDs
    for i in pixels:
        np[i] = (255, 255, 255)
    np.write()

    # Wait for hit or timeout
    while time.time() - t < 5:
        if photodiodes[target].value() == 0:
            point += 1 #giving a point if the target is hit
            print("Hit! Score:", point)
            beep() #activating the buzzer to inidicate scoring of a point
            break #immediately swapping targets as soon as a target is hit

    # Turn off target LEDs
    for i in pixels:
        np[i] = (0, 0, 0)
    np.write()

    time.sleep(0.1)
