import RPi.GPIO as GPIO
import time
from SMCPINAJU.py import S5
from SMCPINAJU.py import S4
from SMCPINAJU.py import S3

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()
GPIO.setup(16, GPIO.OUT)
while True:

	if (S1<0.09 and S2<0.09 and S5>0.09):
		GPIO.output(16, True)
		Print("Carga conectada")

	else if (S1>0.09 and S2>0.09 and S5<0.09): 
		GPIO.output(16, False)
		Print("Carga desconectada")

