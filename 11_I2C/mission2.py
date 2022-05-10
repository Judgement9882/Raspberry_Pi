from RPLCD.i2c import CharLCD
import numpy as np
import random
import math
import time

# LCD initialization
lcd = CharLCD('PCF8574', 0x3f)

# time set
time_slice = np.linspace(0, 2*np.pi, 50)

# Pixel data
pd0 = (0b00000, 0b00000, 0b00000, 0b00000, 0b00000, 0b00000, 0b00000, 0b00000)
pd1 = (0b10000, 0b10000, 0b10000, 0b10000, 0b10000, 0b10000, 0b10000, 0b10000)
pd2 = (0b11000, 0b11000, 0b11000, 0b11000, 0b11000, 0b11000, 0b11000, 0b11000)
pd3 = (0b11100, 0b11100, 0b11100, 0b11100, 0b11100, 0b11100, 0b11100, 0b11100)
pd4 = (0b11110, 0b11110, 0b11110, 0b11110, 0b11110, 0b11110, 0b11110, 0b11110)
pd5 = (0b11111, 0b11111, 0b11111, 0b11111, 0b11111, 0b11111, 0b11111, 0b11111)

lcd.create_char(0, pd0)
lcd.create_char(1, pd1)
lcd.create_char(2, pd2)
lcd.create_char(3, pd3)
lcd.create_char(4, pd4)
lcd.create_char(5, pd5)

def ren(r):
    if r == 1:
        lcd.write_string('\x01') # 20%
    elif r == 2:
        lcd.write_string('\x02') # 40%
    elif r == 3:
        lcd.write_string('\x03') # 60%
    elif r == 4:
        lcd.write_string('\x04') # 80%


"""
q = quotient
r = remainder
line -> 0 or 1
S = Start position
LCD = Last Div Value
"""

def draw(q, r, line, S, LDV):
    lcd.cursor_pos = (line, S)
    if q > LDV:
        for i in range(0, q - LDV):
            lcd.cursor_pos = (line, S)
            lcd.write_string('\x05') # 100%
            S += 1

        if r != 0:
            lcd.cursor_pos = (line, S)
            ren(r)

    elif LDV >= q:
        for i in range(0, LDV - q):
            lcd.write_string('\x00') # 0%
            S -= 1
            lcd.cursor_pos = (line, S)

        if r != 0:
            ren(r)

    return S

# Last Div Value Initialization
LDV_one = 0
LDV_two = 0

# Start position initialization
S_one = 0
S_two = 0

while True:
    for t in time_slice:

        # Random number (0~1)
        n = random.random()

        # Channel data
        ch_one = int(40 + 20*math.cos(t) + 30*n)
        ch_two = int(40 + 20*math.sin(t) + 30*n)

        # Range limit
        if ch_one > 80:
            ch_one = 80
        if ch_two > 80:
            ch_two = 80

        
        # Calculate quotient & remainder
        q_one = int(ch_one / 5)
        r_one = ch_one % 5
        q_two = int(ch_two / 5)
        r_two = ch_two % 5

        # 1st
        lcd.cursor_pos = (0, S_one)
        pos_one = draw(q_one, r_one, 0, S_one, LDV_one)

        # 2nd
        lcd.cursor_pos = (1, S_two)
        pos_two = draw(q_two, r_two, 1, S_two, LDV_two)

        # Update value
        S_one = pos_one
        LDV_one = q_one
        S_two = pos_two
        LDV_two = q_two

        # Wait 0.01s
        time.sleep(0.01)
