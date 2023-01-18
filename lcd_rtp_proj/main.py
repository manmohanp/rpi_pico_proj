# Tested with Pico
from ili934xnew import ILI9341, color565
from machine import Pin, SPI
import tt24
import time
import utime
#https://github.com/Guitarman9119/Raspberry-Pi-Pico-/tree/main/DS1302%20RTC
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
GREY = const(141414)

led = Pin(25, Pin.OUT)
led(1)

#UTC offset time of state/country in hrs, mins stored in dictionary
time_zones={       
0:["HAWAII",-10,0],
1:["LOS ANGELES",-8,0],
2:["MEXICO CITY",-6,0],
3:["MIAMI",-5,0],
4:["SANTIAGO",-3,0],
5:["CARACAS",-4,0],
6:["NEW YORK",-5,0],
7:["RIO DE JANIERO",-3,0],
8:["LONDON",0,0],
9:["PARIS",1,0],
10:["MOSCOW",3,0],
11:["DUBAI",4,0],
12:["DELHI",5,30],
13:["DHAKA",6,0],
14:["BANGKOK",7,0],
15:["BEIJING",8,0],
16:["SINGAPORE",8,0],
17:["TOKYO",9,0],
18:["SYDNEY",11,0],
19:["AUCKLAND",13,0],
}

week=["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]

month=["Jan","Feb","Mar","Apr","May","Jun","Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


#TFT

spi = SPI(0, baudrate=40000000, sck=Pin(18), mosi=Pin(19)) #SPI(2, baudrate=20000000, miso=Pin(19),mosi=Pin(23), sck=Pin(18))
display = ILI9341(spi, cs=Pin(17), dc=Pin(15), rst=Pin(14), w=320, h=240, r=2)

#RTC module
#CLK - GP6, DN/DT - GP7, RST - GP3

ds = DS1302(Pin(6),Pin(7),Pin(3))

#buttons
green_button = Pin(10, Pin.IN)
red_button = Pin(2, Pin.IN)

#display.erase()
display.fill_rectangle(0, 0, 240, 320,WHITE) #top part

time_zone_counter = 8

ds.date_time()

# [year,month,day,weekday,hour,minute,second]
#ds.date_time([2023, 1, 17, 0, 23, 04, 00])

offset_sec=time_zones[time_zone_counter][1]*60*60+ time_zones[time_zone_counter][2]*60  # convert to UTC offset to seconds, for London

#curr_time=utime.localtime(offset_sec+utime.time())

curr_time=utime.localtime(offset_sec + utime.mktime([ds.year(),ds.month(),ds.day(),ds.hour(),ds.minute(),ds.second(),ds.weekday(),"0"]))

#ds.date_time([curr_time[0],curr_time[1],curr_time[2],curr_time[6],curr_time[3],curr_time[4],curr_time[5]]) ##update to RTC

flag = 1

green_pressed_count = 0
red_pressed_count = 0

background_flag = 0


display.set_color(BLACK, WHITE)
display.set_font(tt24)
display.set_pos(5,5)
display.print(time_zones[time_zone_counter][0]) #display London

while True:
    
    #ds.date_time() # returns the current datetime
    #print(ds.date_time())
    
    #curr_time=utime.localtime(offset_sec+utime.time())     # provides day,date and time from epoch time
    
    #ds.date_time(utime.localtime(offset_sec+utime.time()))
    
    #print(utime.localtime(offset_sec+utime.time()))
    
    #curr_time=ds.date_time()     # provides day,date and time from epoch time
    
    #print(curr_time)
        
    #curr_date=str(curr_time[2])+" / "+str(curr_time[1])+" / "+str(curr_time[0])

    #print(button.value())
    
    
    if green_button.value()==1:
        green_pressed_count = green_pressed_count+1
    else:
        green_pressed_count = 0
        
    if red_button.value()==1:
        red_pressed_count = red_pressed_count+1
    else:
        red_pressed_count = 0
        
    if green_pressed_count > 2:
        #ds.date_time([2018, 9, 5, 2, 8, 45, 0, 0]) # set datetime
        print(time_zone_counter)
        if time_zone_counter == 18:
            time_zone_counter = 0
        else:
            time_zone_counter = time_zone_counter+1
        display.erase()
        offset_sec=time_zones[time_zone_counter][1]*60*60+ time_zones[time_zone_counter][2]*60  # convert UTC offset to seconds
        curr_time=utime.localtime(offset_sec + utime.mktime([ds.year(),ds.month(),ds.day(),ds.hour(),ds.minute(),ds.second(),ds.weekday(),"0"]))
        #ds.date_time([curr_time[0],curr_time[1],curr_time[2],curr_time[6],curr_time[3],curr_time[4],curr_time[5]]) ##update to RTC
        display.set_font(tt24)
        display.set_pos(5,5)
        display.print(time_zones[time_zone_counter][0]) #display London
        
    
    if red_pressed_count > 2:
        
        if background_flag == 0:
            background_flag = 1
            display.fill_rectangle(0, 0, 240, 320, GREY)
            
        display.set_color(WHITE,GREY)
        display.set_font(tt24)
        display.set_pos(5,5)
        display.print(time_zones[time_zone_counter][0]) #display London
    else:
        if background_flag == 1:
            background_flag = 0
            display.fill_rectangle(0, 0, 240, 320, WHITE)
        display.set_color(BLACK, WHITE)
        display.set_font(tt24)
        display.set_pos(5,5)
        display.print(time_zones[time_zone_counter][0]) #display London
        
        
    display.set_font(freesansbold64)
    
    (Hr,Min,Sec)=(curr_time[3],curr_time[4],curr_time[5])      # obtain current hour,min of the city/state
    
    display.set_pos(85,80)

    hr = str("%02d:" % (Hr,))
    display.print(hr)   # display hour
    
    display.set_pos(85,140)
    display.print(str("%02d" % (Min,)))   # display minute
    
    display.set_font(tt24)
    
    
    if flag:
        display.set_pos(85,195)
        display.print("-----------")   # display blip
        flag = 0
    else:
        if red_pressed_count > 2:
            display.set_color(GREY,GREY)
        else:
            display.set_color(WHITE,WHITE)
                
        display.set_pos(85,195)
        display.print("-----------")   # display blip
        flag = 1

    
    #display.set_font(tt24)
    
    if red_pressed_count > 2:
        display.set_color(WHITE,GREY)
    else:
        display.set_color(BLACK,WHITE)
    
    day = week[curr_time[6]]
    
    display.set_pos(50,265)
    display.print(day)
    
    dd = curr_time[2]
        
    i = dd if (dd < 20) else (dd % 10)
    if i == 1:
      suffix = 'st'
    elif i == 2:
      suffix = 'nd'
    elif i == 3:
      suffix = 'rd'
    elif dd < 100:
      suffix = 'th'
      
    dt = str("%s%s, %s %s" % (curr_time[2], suffix, month[curr_time[1]-1], curr_time[0]))
    
    display.set_pos(50,290)
    display.print(dt)

    
    time.sleep(0.5)

    
led(0)