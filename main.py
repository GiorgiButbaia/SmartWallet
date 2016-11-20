from time import *
import RPi.GPIO as GPIO
import I2C_LCD_driver as LCDDriver #Usage: mylcd = LCDDriver.lcd(), mylcd.lcd_display_string(myString)
from ethjsonrpc import EthJsonRpc #Ethereum JSON RPC Lib

GPIO.cleanup() #Clean GPIO pins

#Mode of pin numbering
GPIO.setmode(GPIO.BCM)

#Initialize externals
c = EthJsonRpc('127.0.0.1', 8545) #Connect to local geth node
disp = LCDDriver.lcd()
#TODO configure Georgian characters for LCD

#Name pins as variables
btnUp = 14
btnDown = 15
btnLeft = 18
btnRight = 23

btnUp_STATE = 0
btnDown_STATE = 0
btnLeft_STATE = 0
btnRight_STATE = 0

prev_btnUp_STATE = 0
prev_btnDown_STATE = 0
prev_btnLeft_STATE = 0
prev_btnRight_STATE = 0


#Setup all pins
GPIO.setup(btnUp, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(btnDown, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(btnLeft, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(btnRight, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

#Global variables indicating current state
passAsk = True #On password ask

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
pwdLen = 8
pwInput = [""]*pwdLen

b = 0 #Selected Char index

lcdClear()
setCursor(0,0)
lcdPrint("Enter Password:")
setCursor(0,1)

auth= False #Authenticated
while True: #Main Loop
    btnUp_STATE = GPIO.input(btnUp)
    btnDown_STATE = GPIO.input(btnDown)
    btnLeft_STATE = GPIO.input(btnLeft)
    btnRight_STATE = GPIO.input(btnRight)

    if passAsk: #Password input handler
	#Up
        if btnUp_STATE == 1 and prev_btnUp_STATE == 0: #Trigger only if the derivative of the state w.r.t. time is positive
            b += 1
            #Cycle handler
            if b > 62:
                b = 0 #Reset
            elif b < 0:
                b = 62
            lcdPrint(abc123[b])
	#Down
        if btnDown_STATE== 1 and prev_btnDown_STATE == 0:
            b -= 1
            if b > 62:
                b = 0
            elif b < 0:
                b = 62
            lcdPrint(abc123[b])
        #Left
        if btnLeft_STATE == 1 and prev_btnLeft_STATE == 0:
           xPos = getCursor()[0]
           pwInput[xPos] = abc123[b]
           xPos -= 1
           xPos = xPos % pwdLen
           b = 0
           setCursor(xPos, getCursor()[1])
        #Right
        if btnRight_STATE == 1 and prev_btnRight_STATE == 0:
           xPos = getCursor()[0]
           pwInput[xPos] = abc123[b]
           xPos += 1
           b = 0
           setCursor(xPos, getCursor()[1])
           if xPos > pwdLen - 1:
               passAsk = False
               lcdClear()
               pwd = "" #Password buffer

               #Notify user about the ongoing process
               setCursor(0,0)
               lcdPrint("Please wait..")
               setCursor(0,1)
               lcdPrint("Authenticating")
               
               for i in range(0, pwdLen): #Build String
                   pwd += pwInput[i]
               try: #Try to unlock account
                   print c.personal_unlockAccount(c.eth_accounts()[1], pwd, 10)

                   #Reset password variables, for security reasons
                   lcdClear()
                   pwd = 0
                   pwInput = [""]*pwdLen
                   setCursor(0,0)
                   lcdPrint("Authenticated!")
                   auth= True #Authentication succesful
               except:
                   #Possibly incorrect password
                   lcdClear()
                   setCursor(0,0)
                   lcdPrint("Nope...")
               if auth:
                   try:
                      c.eth_sendTransaction(to_address=c.eth_accounts()[0], from_address=c.eth_accounts()[1], value= 1000)
                      lcdClear()
                      lcd.setCursor(0,0)
                      lcdPrint("Transaction")
                      lcd.setCursro(0,1)
                      lcdPrint("Sucessful")
                   except:
                      lcdClear()
                      setCursor(0,0)
                      lcdPrint("Failed")
                      setCursor(0,1)
                      lcdPrint("Insufficient balance")
                   auth=False
           xPos = xPos % pwdLen
        sleep(0.07)
        
    #Log previous states
    prev_btnUp_STATE = btnUp_STATE
    prev_btnDown_STATE = btnDown_STATE
    prev_btnLeft_STATE = btnLeft_STATE
    prev_btnRight_STATE = btnRight_STATE
