from time import *
import RPi.GPIO as GPIO
import I2C_LCD_driver as LCDDriver #Usage: mylcd = LCDDriver.lcd(), mylcd.lcd_display_string(myString)
from ethjsonrpc import EthJsonRpc #Ethereun JSON RPC Lib

#Initialize externals
c = EthJsonRpc('127.0.0.1', 8454) #Connect to local geth node
disp = LCDDriver.lcd()
#TODO configure Georgian characters for LCD

#Name pins as variables
btnUP =
btnDown =
btnLeft =
btnRight =

#"Compactify"
BTNs = [btnUp, btnDown, btnLeft, btnRight]
BTN_States = [0]*4

#Mode of pin numbering
GPIO.setmode(GPIO.BCM)

#Setup all pins
for btn in BTNs:
    GPIO.setup(btn, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


#Global variables indicating current state
passAsk = False #On password ask
doClear = True #Clear LCD after each loop

#Initial vector
Cursor = [1, 1] #Cursor vector


while True: #Main Loop
    if doClear:
        disp.lcd_clear()
    
    for btn in BTNs: #Get value of each button
        BTN_States = GPIO.input(btn)
    #TODO Char-control,and really, handle all other events that can or will happen
    if passAsk: #Password input handler
        disp.lcd_clear()
        Cursor = [1,1] #Reset cursor vector
        disp.lcd_display_string("Enter Password:", Cursor[1], Cursor[0])
        Cursor[1] += 1
        disp.lcd_display_string("______", Cursor[1], Cursor[0]) #Password entry
