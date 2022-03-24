# <Embedded Communication System>
# Mission : Making Alarm Timer
# This timer include weather mode, alarm mode.
# You can show six cities' weather, temperature, humidity.
# You can set up alarm time and show the time.
# If the alarm time comes, music comes out.
# You can also stop the music.

import pifacecad
from   pifacecad.tools.scanf import LCDScanf
from pyowm.owm import OWM
from datetime import datetime
import time 
from omxplayer.player import OMXPlayer

# initialization
cad = pifacecad.PiFaceCAD()
cad.lcd.backlight_on()
cad.lcd.clear()

# weather information initialization
mykey = '8fd58d9e5f18ac1a88bdfb70c3052dbf'
owm = OWM(mykey)
mgr = owm.weather_manager()
reg = owm.city_id_registry()

city = ['Incheon,KR', 'Seoul,KR', 'Busan,KR', 'Ulsan,KR', 'Daegu,KR', 'Daejeon,KR']
wea = []
tem = []
hum = []

# Kelvin To Celcius
K2C = lambda k : k - 273.15

for i in range(6):
  observation = mgr.weather_at_place(city[i])
  weather = observation.weather
  wea.append(weather.status)

  temp = weather.temperature()
  tem.append(K2C(temp['temp_min']))

  city_name = city[i].split(",")[0]
  country_name = city[i].split(",")[1]
  list_of_locations = reg.locations_for(city_name, country = country_name)
  lat_city = list_of_locations[0].lat
  lon_city = list_of_locations[0].lon
  one_call = mgr.one_call(lat = lat_city, lon = lon_city)
  hum.append(one_call.current.humidity)

# alarm time variable
alarm_time = [-1, -1, "inu"]

# show time until press 4
while not cad.switches[4].value:
  now = datetime.now()
  cad.lcd.set_cursor(0,1)
  cad.lcd.write(now.strftime("%m/%d %I:%M:%S%p"))

  # ring alarm lava.mp3
  if alarm_time[0] == int(now.strftime("%I")) and \
     alarm_time[1] == int(now.strftime("%M")) and \
     alarm_time[2] == now.strftime("%p") and \
     int(now.strftime("%S")) == 0: 
    time.sleep(1)
    alarm_player = OMXPlayer("/home/pi/practice/lava.mp3")

  # press 5 stop alarm
  if cad.switches[5].value:
    alarm_player.quit()

  # press 0 show weather
  if cad.switches[0].value:
    index = 0
    cad.lcd.clear()

    # show weather until press 1
    while not cad.switches[1].value:

      cad.lcd.set_cursor(0,0)
      cad.lcd.write(city[index])
      cad.lcd.write(" ")
      cad.lcd.write(wea[index])
      cad.lcd.set_cursor(0,1)
      cad.lcd.write(str(tem[index]))
      cad.lcd.write("'C ")
      cad.lcd.write(str(hum[index]))
      cad.lcd.write("%")

      #press 6, go left
      if cad.switches[6].value:
        if index == 0:
          index = 6
        index = index - 1
        cad.lcd.clear()

      #press 7, go right
      if cad.switches[7].value:
        index = (index + 1) % 6
        cad.lcd.clear()

      # escape
      if cad.switches[1].value:
        cad.lcd.clear()

  # press 2 set alarm
  if cad.switches[2].value:
    cad.lcd.clear()
    scanner = LCDScanf("Alarm %2i:%2i %m%r",custom_values=('AM', 'PM'))
    alarm_time = scanner.scan()
    cad.lcd.clear()
    cad.lcd.write("Alarm set")
    cad.lcd.set_cursor(0,1)
    cad.lcd.write(f'at {alarm_time[0]:02d}:{alarm_time[1]:02d} {alarm_time[2]}')
    time.sleep(3)
    cad.lcd.clear()

  # press 3 show alarm time
  if cad.switches[3].value:
    cad.lcd.clear()
    cad.lcd.set_cursor(0,1)
    cad.lcd.write(f'at {alarm_time[0]:02d}:{alarm_time[1]:02d} {alarm_time[2]}')
    time.sleep(2)
    cad.lcd.clear()
