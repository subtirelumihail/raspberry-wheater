#!/usr/bin/python
import RPi.GPIO as GPIO
import time
import os
import pywapi
import string

LCD_RS = 25
LCD_E  = 24
LCD_D4 = 23
LCD_D5 = 17
LCD_D6 = 18
LCD_D7 = 22


LCD_WIDTH = 16
LCD_CHR = True
LCD_CMD = False

LCD_LINE_1 = 0x80
LCD_LINE_2 = 0xC0

E_PULSE = 0.00005
E_DELAY = 0.00005

def main():

  GPIO.setmode(GPIO.BCM)
  GPIO.setup(LCD_E, GPIO.OUT)
  GPIO.setup(LCD_RS, GPIO.OUT)
  GPIO.setup(LCD_D4, GPIO.OUT)
  GPIO.setup(LCD_D5, GPIO.OUT)
  GPIO.setup(LCD_D6, GPIO.OUT)
  GPIO.setup(LCD_D7, GPIO.OUT)

  lcd_init() #initiatie the lcd
  set_leds() #initiate the leds

  loading() #show loading

  #yahoo_result = pywapi.get_weather_from_yahoo('ROXX0003')
  get_weather("Bucharest", "ROXX0003")


def get_weather(location, code):
  yahoo_result = pywapi.get_weather_from_yahoo(code)

  conditionCode = int(yahoo_result['condition']['code'])
  
  if conditionCode in [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,23,22,35,37,38,39,40,41,42,43,45,46,47]:
    light_leds(3) #Vreme ura/foarte urata
  elif conditionCode in [20,21,24,25,26,27,28,36,3200]:
    light_leds(1) #Vremea este improbabila
  elif conditionCode in [31,32,33,34,44,29,30,44]:
    light_leds(2) #Vremea este buna


  while(True):
    temp_display(location,yahoo_result)
    time.sleep(10)
    today_weather_text_display(yahoo_result)
    time.sleep(10)
    low_high_temp_display(yahoo_result)
    time.sleep(10)
    sunset_sunrise_display(yahoo_result)
    time.sleep(10)


def temp_display(location,yahoo_result):
	line_1 = location
	line_2 = "Temp:" + yahoo_result['condition']['temp'] + "C"
	led_display(line_1,line_2,2)

def today_weather_text_display(yahoo_result):
	line_1 = "Today"
	line_2 = yahoo_result['forecasts'][0]['text']
	led_display(line_1,line_2,2)

def low_high_temp_display(yahoo_result):
	line_1 = "Low:" + yahoo_result['forecasts'][0]['low'] + "C"
	line_2 = "Max:" +  yahoo_result['forecasts'][0]['high'] + "C"
	led_display(line_1,line_2,1)

def sunset_sunrise_display(yahoo_result):
	sunrise = yahoo_result['astronomy']['sunrise']
	sunset = yahoo_result['astronomy']['sunset']
	line_1 = "Sunrise: " + sunrise
	line_2 = "Sunset: " + sunset
	led_display(line_1,line_2,2)


def loading():
	led_display("Loading...","",2)
 
def light_leds(led):
  if led==1: #blue
     GPIO.output(9, True)
     GPIO.output(10, False)
     GPIO.output(11, False )
  elif led==2: #green
     GPIO.output(9,  False)
     GPIO.output(10, True)
     GPIO.output(11, False)
  elif led==3:#red
     GPIO.output(9,  False)
     GPIO.output(10, False)
     GPIO.output(11, True)

def test_leds():
  GPIO.output(9, True)
  GPIO.output(10, False)
  GPIO.output(11, False)
  time.sleep(1)
  GPIO.output(9, False)
  GPIO.output(10, True)
  GPIO.output(11, False)
  time.sleep(1)
  GPIO.output(9, False)
  GPIO.output(10, False)
  GPIO.output(11, True )
  time.sleep(1);
  GPIO.output(9, False)
  GPIO.output(10, False)
  GPIO.output(11, False )
  time.sleep(1);

def set_leds():
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(9, GPIO.OUT)
  GPIO.setup(10, GPIO.OUT)
  GPIO.setup(11, GPIO.OUT)



def led_display(line_1, line_2, style):
  #afisare de text pe LCD
  lcd_byte(LCD_LINE_1, LCD_CMD)
  lcd_string(line_1,style)
  lcd_byte(LCD_LINE_2, LCD_CMD)
  lcd_string(line_2,style)


def lcd_init():
  lcd_byte(0x33,LCD_CMD)
  lcd_byte(0x32,LCD_CMD)
  lcd_byte(0x28,LCD_CMD)
  lcd_byte(0x0C,LCD_CMD)
  lcd_byte(0x06,LCD_CMD)
  lcd_byte(0x01,LCD_CMD)

def lcd_string(message,style):
  # Send string to display
  # style=1 Left justified
  # style=2 Centred
  # style=3 Right justified

  if style==1:
    message = message.ljust(LCD_WIDTH," ")
  elif style==2:
    message = message.center(LCD_WIDTH," ")
  elif style==3:
    message = message.rjust(LCD_WIDTH," ")

  for i in range(LCD_WIDTH):
    lcd_byte(ord(message[i]),LCD_CHR)

def lcd_byte(bits, mode):
  GPIO.output(LCD_RS, mode)

  GPIO.output(LCD_D4, False)
  GPIO.output(LCD_D5, False)
  GPIO.output(LCD_D6, False)
  GPIO.output(LCD_D7, False)
  if bits&0x10==0x10:
    GPIO.output(LCD_D4, True)
  if bits&0x20==0x20:
    GPIO.output(LCD_D5, True)
  if bits&0x40==0x40:
    GPIO.output(LCD_D6, True)
  if bits&0x80==0x80:
    GPIO.output(LCD_D7, True)

  time.sleep(E_DELAY)
  GPIO.output(LCD_E, True)
  time.sleep(E_PULSE)
  GPIO.output(LCD_E, False)
  time.sleep(E_DELAY)

  GPIO.output(LCD_D4, False)
  GPIO.output(LCD_D5, False)
  GPIO.output(LCD_D6, False)
  GPIO.output(LCD_D7, False)
  if bits&0x01==0x01:
    GPIO.output(LCD_D4, True)
  if bits&0x02==0x02:
    GPIO.output(LCD_D5, True)
  if bits&0x04==0x04:
    GPIO.output(LCD_D6, True)
  if bits&0x08==0x08:
    GPIO.output(LCD_D7, True)

  time.sleep(E_DELAY)
  GPIO.output(LCD_E, True)
  time.sleep(E_PULSE)
  GPIO.output(LCD_E, False)
  time.sleep(E_DELAY)

if __name__ == '__main__':
  main()
