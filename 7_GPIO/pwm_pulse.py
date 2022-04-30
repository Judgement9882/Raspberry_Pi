from gpiozero import PWMLED
from signal import pause

led = PWMLED(18)

led.pulse()

pause()
