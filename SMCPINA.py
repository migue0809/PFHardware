import spidev
import time
import os
import Adafruit_MCP3008
import Adafruit_GPIO.SPI as SPI
import serial
import requests
from datetime import datetime as date
from time import sleep
from ina219 import INA219

ina = INA219(shunt_ohms=0.1,
             max_expected_amps = 2.0,
             address=0x40)

ina1 = INA219(shunt_ohms=0.1,
             max_expected_amps = 2.0,
             address=0x44)

ina2 = INA219(shunt_ohms=0.1,
             max_expected_amps = 2.0,
             address=0x41)

ina3 = INA219(shunt_ohms=0.1,
             max_expected_amps = 2.0,
             address=0x45)

ina.configure(voltage_range=ina.RANGE_32V,
              gain=ina.GAIN_AUTO,
              bus_adc=ina.ADC_128SAMP,
              shunt_adc=ina.ADC_128SAMP)

ina1.configure(voltage_range=ina.RANGE_32V,
              gain=ina.GAIN_AUTO,
              bus_adc=ina.ADC_128SAMP,
              shunt_adc=ina.ADC_128SAMP)

ina2.configure(voltage_range=ina.RANGE_32V,
              gain=ina.GAIN_AUTO,
              bus_adc=ina.ADC_128SAMP,
              shunt_adc=ina.ADC_128SAMP)

ina3.configure(voltage_range=ina.RANGE_32V,
              gain=ina.GAIN_AUTO,
              bus_adc=ina.ADC_128SAMP,
              shunt_adc=ina.ADC_128SAMP)
SPI_PORT   = 0
SPI_DEVICE = 0
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

while True:
    S1 = 0
    S2 = 0
    S3 = 0
    S4 = 0
    S5 = 0
    S6 = 0
    S7 = 0
    S8 = 0

    t = 0
    while t<120:
	A1 = mcp.read_adc(2)
	A2 = mcp.read_adc(7)
	A3 = mcp.read_adc(3)
	A4 = mcp.read_adc(1)
	A5 = mcp.read_adc(0)
	V1 = mcp.read_adc(4)
	V2 = mcp.read_adc(5)
	V3 = mcp.read_adc(6)
	S1 = S1 + A1
	S2 = S2 + A2
	S3 = S3 + A3
	S4 = S4 + A4
	S5 = S5 + A5
	S6 = S6 + V1
	S7 = S7 + V2
	S8 = S8 + V3

	t = t + 1
    m = 120

    S_1 = ((((S1/m)+20)*(5.0/1023))-2.5)/(0.095)
    S_2 = ((((S2/m)+20)*(5.0/1023))-2.5)/(0.063)
    S_3 = ((((S3/m)+20)*(5.0/1023))-2.5)/(0.090)
    S_4 = ((((S4/m)+20)*(5.0/1023))-2.5)/(0.095)
    S_5 = ((((S5/m)+20)*(5.0/1023))-2.5)/(0.088)
    S_6 = (((S6/m)*(5.0/1023))*(37000.0/7500.0))*14.4594417077 
    S_7 = (((S7/m)*(5.0/1023))*(37000.0/7500.0))*13.4594417077
    S_8 = ((S8/m)*(5.0/1023))*(37000.0/7500.0)
    
    p = 1.0
    while (p<10.0)
        if (S_1>p and S_1<(p+1.0))
            S_6 = S_6+((3.2*p)-(p-1))
            S_7 = S_7-1.5*(p-1)
            S_8 = S_8-(p-1)/2
            break
        p=p+1
    if(S_1<0.05):
        S_6=0.0
    S_1=str(S_1)
    S_2=str(S_2)
    S_3=str(S_3)
    S_4=str(S_4)
    S_5=str(S_5)
    S_6=str(S_6)
    S_7=str(S_7)
    S_8=str(S_8)
    v = ina.voltage()
    i = str(ina.current()/1000)
    p = ina.power()

    v1 = ina1.voltage()
    i1 = str(ina1.current()/1000)
    p1 = ina1.power()

    v2 = ina2.voltage()
    i2 = str(ina2.current()/1000)
    p2 = ina2.power()

    v3 = ina3.voltage()
    i3 = str(ina3.current()/1000)
    p3 = ina3.power()

    #Vistos de izquierda a derecha
    print("Corriente sensor 1 = "+i)   ## Sensor de corriente 1 de I2C
    print("Corriente sensor 2 = "+i1)	## Sensor de corriente 2 de I2C
    print("Corriente sensor 3 = "+i2)	## Sensor de corriente 3 de I2C
    print("Corriente sensor 4 = "+i3)	## Sensor de corriente 4 de I2C

    print("Voltaje sensor 1 = "+S_6)	## Sensor 1 de ADC  Canal 4
    print("Corriente sensor 5 = "+S_1)	## Sensor 2 de ADC  Canal 2
    print("Corriente sensor 6 = "+S_2)	## Sensor 3 de ADC  Canal 7
    print("Voltaje sensor 2 = "+S_7)	## Sensor 4 de ADC  Canal 5
    print("Corriente sensor 7 = "+S_3)	## Sensor 5 de ADC  Canal 3
    print("Corriente sensor 8 = "+S_4)	## Sensor 6 de ADC  Canal 1
    print("Corriente sensor 9 = "+S_5)	## Sensor 7 de ADC  Canal 0
    print("Voltaje sensor 3 = "+S_8)	## Sensor 8 de ADC  Canal 6
	


    response6 = requests.get('http://104.236.0.105/voltage_sensors?voltage1=%s&voltage2=%s&voltage3=%s&create=%s'%(S_6,S_7,S_8, str(date.now())),
                        auth=requests.auth.HTTPBasicAuth(
                          'admin',
                          'uninorte'))
    response7 = requests.get('http://104.236.0.105/low_current_sensors?current1=%s&current2=%s&current3=%s&current4=%s&create=%s'%(i, i1, i2, i3,str(date.now())),
                        auth=requests.auth.HTTPBasicAuth(
                          'admin',
                          'uninorte'))
    response8 = requests.get('http://104.236.0.105/high_current_sensors?current5=%s&current6=%s&current7=%s&current8%s&current9=%s&create=%s'%(S_1,S_2,S_3,S_4,S_5,str(date.now())),
                            auth=requests.auth.HTTPBasicAuth(
                              'admin',
                              'uninorte'))
    print(response6)
    print(response7)
    print(response8)
    time.sleep(50)