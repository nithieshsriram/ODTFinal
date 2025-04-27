from machine import ADC, Pin
import time

# Setup for joystick axes
joy_x = ADC(Pin(34))  # X-axis
joy_y = ADC(Pin(35))  # Y-axis


# Setup for joystick button
joystick_btn = Pin(33, Pin.IN, Pin.PULL_UP)  # Active LOW
joy_x.atten(ADC.ATTN_11DB)
joy_y.atten(ADC.ATTN_11DB)
# Main loop
while True:
    x_val = joy_x.read()
    y_val = joy_y.read()
    btn_val = joystick_btn.value()

    print("X:", x_val, "Y:", y_val)
    time.sleep(0.1)
