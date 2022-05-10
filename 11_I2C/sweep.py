from RPLCD.i2c import CharLCD
import time

# LCD initialization
lcd = CharLCD('PCF8574', 0x3f)

lcd.clear()
while True:

    # print 1st line
    for i in range(16):
        lcd.cursor_pos = (0, i)
        lcd.write_string(format(i, 'X'))
        time.sleep(0.1)
        lcd.clear()

    # print 2nd line
    for i in range(15, -1, -1):
        lcd.cursor_pos = (1, i)
        lcd.write_string(format(i, 'X'))
        time.sleep(0.1)
        lcd.clear()
