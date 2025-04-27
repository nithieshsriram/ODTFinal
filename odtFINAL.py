import time
from machine import I2C, Pin, ADC

# PCA9685 class to control servo motor via I2C
class PCA9685:
    def __init__(self, i2c, address=0x40):
        self.i2c = i2c
        self.address = address
        self.reset()
        self.set_pwm_freq(50)  # 50Hz for servos

    def reset(self):
        self.i2c.writeto_mem(self.address, 0x00, bytes([0x00]))

    def set_pwm_freq(self, freq_hz):
        prescale_val = int(25000000.0 / (4096 * freq_hz) - 1)
        old_mode = self.i2c.readfrom_mem(self.address, 0x00, 1)[0]
        new_mode = (old_mode & 0x7F) | 0x10
        self.i2c.writeto_mem(self.address, 0x00, bytes([new_mode]))
        self.i2c.writeto_mem(self.address, 0xFE, bytes([prescale_val]))
        self.i2c.writeto_mem(self.address, 0x00, bytes([old_mode]))
        time.sleep_ms(5)
        self.i2c.writeto_mem(self.address, 0x00, bytes([old_mode | 0xa1]))

    def set_pwm(self, channel, on, off):
        reg = 0x06 + 4 * channel
        data = bytearray([
            on & 0xFF,
            on >> 8,
            off & 0xFF,
            off >> 8
        ])
        self.i2c.writeto_mem(self.address, reg, data)

    def set_servo_angle(self, channel, angle):
        angle = max(0, min(180, angle))  # Clamp angle
        pulse_min = 102  # 0 degrees
        pulse_max = 512  # 180 degrees
        pulse = int(pulse_min + (pulse_max - pulse_min) * angle / 180)
        self.set_pwm(channel, 0, pulse)

# Setup I2C and PCA9685
i2c = I2C(0, scl=Pin(22), sda=Pin(21))
pca = PCA9685(i2c)

# Joystick setup
joy_x = ADC(Pin(34))  # X-axis
joy_y = ADC(Pin(35))  # Y-axis
joy_x.atten(ADC.ATTN_11DB) #enasures maximum volatage range is supplid to the joystick
joy_y.atten(ADC.ATTN_11DB)
joystick_btn = Pin(33, Pin.IN, Pin.PULL_UP)  #

# Laser pin
laser = Pin(25, Pin.OUT)

# Start at center
x_angle = 90
y_angle = 90
pca.set_servo_angle(0, x_angle)
pca.set_servo_angle(1, y_angle)

# Movement parameters
step = 1  #this variable determines how quickly the turret changes angle with respect to joystick movement
dead_zone = 250  #This is a deadzone at the center of the joystick.
#The default center values of the joystick are not exactly 2048(joystick values range from 0 to 4095)
#So there needs to be a small deadzone around the center where user input does not affect movement to avoid accidental or automatic movement of the servos

# Helper to smooth analog input (simple moving average)
def smooth_adc(adc_pin, samples=5):
    return sum(adc_pin.read() for _ in range(samples)) // samples

# Main loop
while True:
    x_val = smooth_adc(joy_x)
    y_val = smooth_adc(joy_y)

    # X-axis movement (left/right)
    if x_val < 2048 - dead_zone:
        x_angle = min(180, x_angle + step)#increaseing the angle of the servo by the step variable defined earleir until it reaches 180 degrees
    elif x_val > 2048 + dead_zone:
        x_angle = max(0, x_angle - step)#decreasing the angle of the servo by the step variable defined earleir until it reaches 0 degrees

    # Y-axis movement (up/down)
    if y_val < 2048 - dead_zone:
        y_angle = max(0, y_angle - step)
    elif y_val > 2048 + dead_zone:
        y_angle = min(180, y_angle + step)

    # Update servos
    pca.set_servo_angle(0, x_angle)
    pca.set_servo_angle(1, y_angle)


    time.sleep(0.05)
