# Tested with Pico
from ili934xnew import ILI9341, color565
from machine import Pin, SPI
import tt24
import time
import utime

from ds1302 import DS1302

import freesansbold64


# Einige Farben from https://www.hobbyelektroniker.ch/resources/PytEsp20.zip
RED = const(0XF800)  # (255, 0, 0)
GREEN = const(0X07E0)  # (0, 255, 0)
BLUE = const(0X001F)  # (0, 0, 255)
YELLOW = const(0XFFE0)  # (255, 255, 0)
FUCHSIA = const(0XF81F)  # (255, 0, 255)
AQUA = const(0X07FF)  # (0, 255, 255)
MAROON = const(0X8000)  # (128, 0, 0)
DARKGREEN = const(0X0400)  # (0, 128, 0)
NAVY = const(0X0010)  # (0, 0, 128)
TEAL = const(0X0410)  # (0, 128, 128)
PURPLE = const(0X8010)  # (128, 0, 128)
OLIVE = const(0X8400)  # (128, 128, 0)
ORANGE = const(0XFC00)  # (255, 128, 0)
DEEP_PINK = const(0XF810)  # (255, 0, 128)
CHARTREUSE = const(0X87E0)  # (128, 255, 0)
SPRING_GREEN = const(0X07F0)  # (0, 255, 128)
INDIGO = const(0X801F)  # (128, 0, 255)
DODGER_BLUE = const(0X041F)  # (0, 128, 255)
CYAN = const(0X87FF)  # (128, 255, 255)
PINK = const(0XFC1F)  # (255, 128, 255)
LIGHT_YELLOW = const(0XFFF0)  # (255, 255, 128)
LIGHT_CORAL = const(0XFC10)  # (255, 128, 128)
LIGHT_GREEN = const(0X87F0)  # (128, 255, 128)
LIGHT_SLATE_BLUE = const(0X841F)  # (128, 128, 255)
WHITE = const(0XFFFF)  # (255, 255, 255)
BLACK = const(0)

led = Pin(25, Pin.OUT)
led(1)

#UTC offset time of state/country in hrs, mins stored in dictionary
time_zones={       
0:["JUNEAU",-9,0],
1:["LOS ANGELES",-8,0],
2:["MEXICO CITY",-6,0],
3:["MIAMI",-5,0],
4:["SANTIAGO",-3,0],
5:["NEW YORK",-5,0],
6:["RIO",-3,0],
7:["NUUK",-3,0],
8:["ACCRA",0,0],
9:["LISBON",0,0],
10:["LONDON",0,0],
11:["PARIS",1,0],
12:["MOSCOW",3,0],
13:["DUBAI",4,0],
14:["KARACHI",5,0],
15:["NEW DELHI",5,30],
16:["COLOMBO",5,30],
17:["DHAKA",6,0],
18:["BANGKOK",7,0],
19:["BEIJING",8,0],
20:["SINGAPORE",8,0],
21:["HONGKONG",8,0],
22:["TOKYO",9,0],
23:["SYDNEY",11,0],
24:["AUCKLAND",13,0],
}

week=["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]

month=["Jan","Feb","Mar","Apr","May","Jun","Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


#TFT

spi = SPI(0, baudrate=40000000, sck=Pin(18), mosi=Pin(19)) #SPI(2, baudrate=20000000, miso=Pin(19),mosi=Pin(23), sck=Pin(18))
display = ILI9341(spi, cs=Pin(17), dc=Pin(15), rst=Pin(14), w=320, h=240, r=2)

#RTC module
#CLK - GP6, DN/DT - GP7, RST - GP3

ds = DS1302(Pin(6),Pin(7),Pin(3))


#display.erase()
display.fill_rectangle(0, 0, 240, 320, BLUE)
display.set_color(CHARTREUSE,BLUE)

offset_sec=time_zones[10][1]*60*60+ time_zones[10][2]*60  # convert UTC offset to seconds

#print (utime.localtime())

#ds.date_time(utime.localtime())

curr_time=utime.localtime(offset_sec+utime.time())

"""
ds.year(curr_time[0])
ds.month(curr_time[1])
ds.day(curr_time[2])
ds.weekday(curr_time[6])
ds.hour(curr_time[3])
ds.minute(curr_time[4])
ds.second(curr_time[5])
"""

print("from RTC : %s" % (ds.date_time()))

#ds.date_time([2001, 5, 21, 0, 21, 30, 0, 0]) # set datetime

while True:
    
    #ds.date_time() # returns the current datetime
    #print(ds.date_time())
    
    #curr_time=utime.localtime(offset_sec+utime.time())     # provides day,date and time from epoch time
    
    #ds.date_time(utime.localtime(offset_sec+utime.time()))
    
    #print(utime.localtime(offset_sec+utime.time()))
    
    #curr_time=ds.date_time()     # provides day,date and time from epoch time
    
    #print(curr_time)
        
    #curr_date=str(curr_time[2])+" / "+str(curr_time[1])+" / "+str(curr_time[0])
    
    display.set_color(YELLOW,BLUE)
    display.set_font(freesansbold64)
    
    (Hr,Min,Sec)=(ds.hour(),ds.minute(),ds.second())      # obtain current hour,min of the city/state
    
    display.set_pos(85,80)

    hr = str("%02d:" % (Hr,))
    display.print(hr)   # display hour
    
    display.set_pos(85,140)
    display.print(str("%02d" % (Min,)))   # display minute
    
    display.set_font(tt24)
    
    display.set_pos(85,190)
    display.print("-----------")   # display blip
    
    #display.set_font(tt24)
    display.set_color(CHARTREUSE,BLUE)
    
    day = week[ds.weekday()]
    
    display.set_pos(50,265)
    display.print(day)
    
    dd = ds.day()
        
    i = dd if (dd < 20) else (dd % 10)
    if i == 1:
      suffix = 'st'
    elif i == 2:
      suffix = 'nd'
    elif i == 3:
      suffix = 'rd'
    elif dd < 100:
      suffix = 'th'
      
    dt = str("%s%s, %s %s" % (ds.day(), suffix, month[ds.month()-1], ds.year()))
    
    display.set_pos(50,290)
    display.print(dt)

    
    time.sleep(0.5)

    
led(0)