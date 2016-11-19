from time import *
import RPi.GPIO as GPIO
import I2C_LCD_driver as LCDDriver #Usage: mylcd = LCDDriver.lcd(), mylcd.lcd_display_string(myString)
from ethjsonrpc import EthJsonRpc #Ethereum JSON RPC Lib

GPIO.cleanup() #Clean GPIO pins

#Initialize externals
c = EthJsonRpc('127.0.0.1', 8454) #Connect to local geth node
disp = LCDDriver.lcd()
#TODO configure Georgian characters for LCD

#Name pins as variables
btnUP = 14
btnDown = 15
btnLeft = 18
btnRight = 23

#"Compactify"
BTNs = [btnUp, btnDown, btnLeft, btnRight]
BTN_States = [0]*4
prev_BTN_States = [0]*4

#Mode of pin numbering
GPIO.setmode(GPIO.BCM)

#Setup all pins
for btn in BTNs:
    GPIO.setup(btn, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


#Global variables indicating current state
passAsk = False #On password ask
doClear = True #Clear LCD after each loop

#Initial vector
Cursor = [0, 0] #Cursor vector


#More compact notation. TODO move definitions to library
def lcdPrint(text, cursorPos=Cursor): #lcdPrint starts counting from zero
    #lcd_display_string starts counting from one
    disp.lcd_display_string(text, cursorPos[1]+1, cursorPos[0]+1)
def setCursor(xPos, yPos):
    Cursor[0] = xPos
    Cursor[1] = yPos
def lcdClear():
    disp.lcd_clear()
def getCursor():
    return Cursor

#Chars
abc123 = " 0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
pwInput = [""]*6

b = 0 #Selected Char index

while True: #Main Loop
    if doClear:
        lcdClear()
    
    for btn in BTNs: #Get value of each button
        BTN_States = GPIO.input(btn)

    if passAsk: #Password input handler
        lcdClear()
        setCursor(0,0)
        lcdPrint("Enter Password:")
        setCursor(0,1)
        lcdPrint("------")
	#Up
	if BTN_States[0] == 1 and prev_BTN_states[0] == 0: #Trigger only if the derivative of the state w.r.t. time is positive
            b += 1
            #Cycle handler
            if b > 62:
                b = 0 #Reset
            elif b < 0:
                b = 62
            lcdPrint(abc123[b])
	#Down
        if BTN_States[1] == 1 and prev_BTN_states[1] == 0:
            b -= 1
            if b > 62:
                b = 0
            elif b < 0:
                b = 62
            lcdPrint(abc123[b])
        #Left
        if BTN_States[2] == 1 and prev_BTN_states[2] == 0:
           xPos = getCursor()[0]
           pwInput[xPos] = abc123[b]
           xPos -= 1
           xPos = xPos % 6
           b = 0
           setCursor(xPos, getCursor()[1])
        #Right
        if BTN_States[3] == 1 and prev_BTN_states[3] == 0:
           xPos = getCursor()[0]
           pwInput[xPos] = abc123[b]
           xPos += 1
           b = 0
           setCursor(xPos, getCursor()[1])
           if xPos == 6:
               passAsk = False
        
    #Log previous states
    prev_BTN_states = BTN_States
		
