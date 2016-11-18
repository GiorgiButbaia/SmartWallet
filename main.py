from time import *
import RPi.GPIO as GPIO
import I2C_LCD_driver as LCDDriver #Usage: mylcd = LCDDriver.lcd(), mylcd.lcd_display_string(myString)
from ethjsonrpc import EthJsonRpc #Ethereun JSON RPC Lib

c = EthJsonRpc('127.0.0.1', 8454) #Connect to local node


btnUP =
btnDown =
btnLeft =
btnRight =

BTNs = [btnUp, btnDown, btnLeft, btnRight]
BTN_States = [0]*4

#Mode of pin numbering
GPIO.setmode(GPIO.BCM)

#Setup all pins
for btn in BTNs:
    GPIO.setup(btn, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


while True: #Main Loop
    for btn in BTNs: #Get value of each button
        BTN_States = GPIO.input(btn)
    #TODO Char-control
    
