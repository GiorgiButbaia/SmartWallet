from time import *
import RPi.GPIO as GPIO
import I2C_LCD_driver as LCDDriver #Usage: mylcd = LCDDriver.lcd(), mylcd.lcd_display_string(myString)


btnUP =
btnDown =
btnLeft =
btnRight =

#Mode of pin numbering
GPIO.setmode(GPIO.BCM)

#Setup all pins
GPIO.setup(btnUP, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(btnDown, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(btnLeft, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(btnRight, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

 
