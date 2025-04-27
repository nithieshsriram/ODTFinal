from machine import Pin
import time

# Your original GPIO pins
photodiodes = [
    Pin(4, Pin.IN, Pin.PULL_UP),   # Photodiode 1
    Pin(5, Pin.IN, Pin.PULL_UP),   # Photodiode 2
    Pin(12, Pin.IN, Pin.PULL_UP),  # Photodiode 3
    Pin(22, Pin.IN, Pin.PULL_UP),  # Photodiode 4
    Pin(15, Pin.IN, Pin.PULL_UP),  # Photodiode 5
    Pin(16, Pin.IN, Pin.PULL_UP),  # Photodiode 6
    Pin(17, Pin.IN, Pin.PULL_UP),  # Photodiode 7
    Pin(18, Pin.IN, Pin.PULL_UP),  # Photodiode 8
    Pin(19, Pin.IN, Pin.PULL_UP)   # Photodiode 9
]

print("Ready to detect triggers...")

while True:
    for i, pd in enumerate(photodiodes):
        if pd.value() == 0:  # Triggered (light or interruption)
            print("Photodiode", i + 1, "was triggered!")
            time.sleep(0.3)  # small delay to avoid spamming
# Write your code here :-)
