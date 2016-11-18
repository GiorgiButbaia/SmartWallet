import RPi.GPIO as GPIO
print GPIO.VERSION

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

