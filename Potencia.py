import spidev
import time
import os
from math import *
import Adafruit_MCP3008
import Adafruit_GPIO.SPI as SPI
import RPi.GPIO as GPIO
import serial
import requests
from datetime import datetime as date
from time import sleep
from ina219 import INA219
from Tkinter import *
root=Tk()
Frame=Frame(root,width=500,height=400)
ListS_1=[]
ListS_6=[]
ListS_7=[]
ListS_8=[]
D0=StringVar()
D1=StringVar()
D2=StringVar()
D3=StringVar()
D4=StringVar()
D5=StringVar()
D6=StringVar()
D7=StringVar()
D8=StringVar()
PBB=StringVar()
PAB=StringVar()
PBB1=StringVar()
PAB1=StringVar()
PBI=StringVar()
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
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()
GPIO.setup(16, GPIO.OUT)
a=0

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

    S_1 = (((((S1/m)+7)*(5.0/1023))-2.5)/(0.090))+0.2
    S_2 = (((((S2/m)+6)*(5.0/1023))-2.5)/(0.063))+0.2
    S_3 = (((((S3/m)+7)*(5.0/1023))-2.5)/(0.073))+0.2
    S_4 = (((((S4/m)+7)*(5.0/1023))-2.5)/(0.095))
    S_5 = (((((S5/m)+7)*(5.0/1023))-2.5)/(0.106))
    S_6 = (((S6/m)*(5.0/1023))*(37000.0/7500.0))*14.5
    S_7 = (((S7/m)*(5.0/1023))*(37000.0/7500.0))*12.5
    S_8 = ((S8/m)*(5.0/1023))*(37000.0/7500.0)
    
    p = 1.0
    while (p<10.0):
        if (S_1>(p+0.5) and S_1<(p+1.5)):
            S_6 = S_6+(2*p)
            S_7 = S_7-(1.5*p)
            S_8 = S_8-(p+1)/2
            break
        p=p+1
    if(S_1<0.05):
        S_6=0.0
    if (S_1<0.1 and S_2<0.1 and S_5>0.09):
	    GPIO.output(16, False)
	    print("Carga desconectada")

    elif (S_1>0.1 or S_2>0.1 and S_5>0.09): 
	    GPIO.output(16, True)
	    print("Carga conectada")
    v = ina.voltage()
    i = round(ina.current()/1000,2)
    p = ina.power()

    v1 = ina1.voltage()
    i1 = round(ina1.current()/1000,2)
    p1 = ina1.power()

    v2 = ina2.voltage()
    i2 = round(ina2.current()/1000,2)
    p2 = ina2.power()

    v3 = ina3.voltage()
    i3 = round(ina3.current()/1000,2)
    p3 = ina3.power()
    if(i<=0.0):
        i=0.01
    if(i1<=0.0):
        i1=0.01
    if(i2<=0.0):
        i2=0.01
    if(i3<=0.0):
        i3=0.01
    if(S_1<=0.0):
        S_1=0.01
    if(S_2<=0.0):
        S_2=0.01
    if(S_3<=0.0):
        S_3=0.01
    if(S_4<=0.0):
        S_4=0.01
    if(S_5<=0.0):
        S_5=0.01
    i4=S_1
    i5=S_2
    if S_3==S_4:
        i6=0.01
    else:
        i6=abs(S_3-S_4)
    i7=S_4
    i8=abs(S_5-S_3+S_4)
    If = i+i1+i2+i3
    Pf = str(round(If*S_6,2))
    Vp = ((2.5+S_2*0.1)*6)
    Pp = str(round(Vp*S_2,2))
    Ib = S_5-S_3
    Pb = str(abs(round(S_8*Ib,2)))
    VD0_AB=round(0.0326*log(i)+0.7812,3)
    VD1_AB=round(0.0326*log(i1)+0.7812,3)
    VD2_AB=round(0.0326*log(i2)+0.7812,3)
    VD3_AB=round(0.0326*log(i3)+0.7812,3)
    VD4_AB=round(0.0326*log(i4)+0.7812,3)
    VD5_AB=round(0.0326*log(i5)+0.7812,3)
    VD6_AB=round(0.0326*log(i6)+0.7812,3)
    VD7_AB=round(0.0326*log(i7)+0.7812,3)
    VD8_AB=round(0.0326*log(i8)+0.7812,3)
    
    VAD0=VD0_AB+S_6
    VAD1=VD1_AB+S_6
    VAD2=VD2_AB+S_6
    VAD3=VD3_AB+S_6
    VAD4=VD4_AB+S_7
    VAD5=VD5_AB+S_7
    VAD6=VD6_AB+S_8
    VAD8=VD8_AB+S_8
    print("Voltaje Diodo 0 "+str(VD0_AB))
    print("Voltaje Diodo 1 "+str(VD1_AB))
    print("Voltaje Diodo 2 "+str(VD2_AB))
    print("Voltaje Diodo 3 "+str(VD3_AB))
    print("Voltaje Diodo 4 "+str(VD4_AB))
    print("Voltaje Diodo 5 "+str(VD5_AB))
    print("Voltaje Diodo 6 "+str(VD6_AB))
    print("Voltaje Diodo 7 "+str(VD7_AB))
    print("Voltaje Diodo 8 "+str(VD8_AB))

    #Potencias antes de diodos
    PAD0=VAD0*i
    PAD1=VAD1*i1
    PAD2=VAD2*i2
    PAD3=VAD3*i3
    PAD4=VAD4*i4
    PAD5=VAD5*i5
    PAD6=VAD6*i6
    PAD7=VAD6*i7
    PAD8=VAD8*i8
    print("Potencia antes del Diodo 0 "+str(PAD0))
    print("Potencia antes del Diodo 1 "+str(PAD1))
    print("Potencia antes del Diodo 2 "+str(PAD2))
    print("Potencia antes del Diodo 3 "+str(PAD3))
    print("Potencia antes del Diodo 4 "+str(PAD4))
    print("Potencia antes del Diodo 5 "+str(PAD5))
    print("Potencia antes del Diodo 6 "+str(PAD6))
    print("Potencia antes del Diodo 7 "+str(PAD7))
    print("Potencia antes del Diodo 8 "+str(PAD8))
    #Potencias despues diodos
    PDD0=S_6*i
    PDD1=S_6*i1
    PDD2=S_6*i2
    PDD3=S_6*i3
    PDD4=S_7*i4
    PDD5=S_7*i5
    PDD6=S_8*i6
    PDD7=VAD8*i7
    PDD8=S_8*i8
    print("Potencia despues del Diodo 0 "+str(PDD0))
    print("Potencia despues del Diodo 1 "+str(PDD1))
    print("Potencia despues del Diodo 2 "+str(PDD2))
    print("Potencia despues del Diodo 3 "+str(PDD3))
    print("Potencia despues del Diodo 4 "+str(PDD4))
    print("Potencia despues del Diodo 5 "+str(PDD5))
    print("Potencia despues del Diodo 6 "+str(PDD6))
    print("Potencia despues del Diodo 7 "+str(PDD7))
    print("Potencia despues del Diodo 8 "+str(PDD8))
    fichero = open('Diodo0.txt', 'a')
    fichero.write(str(PAD0)+os.linesep)
    fichero.write(str(PDD0)+os.linesep)
    fichero.close()
    fichero1= open('Diodo1.txt', 'a')
    fichero1.write(str(PAD1)+os.linesep)
    fichero1.write(str(PDD1)+os.linesep)
    fichero1.close()
    fichero2= open('Diodo2.txt', 'a')
    fichero2.write(str(PAD2)+os.linesep)
    fichero2.write(str(PDD2)+os.linesep)
    fichero2.close()
    fichero3= open('Diodo3.txt', 'a')
    fichero3.write(str(PAD3)+os.linesep)
    fichero3.write(str(PDD3)+os.linesep)
    fichero3.close()
    fichero4= open('Diodo4.txt', 'a')
    fichero4.write(str(PAD4)+os.linesep)
    fichero4.write(str(PDD4)+os.linesep)
    fichero4.close()
    fichero5= open('Diodo5.txt', 'a')
    fichero5.write(str(PAD5)+os.linesep)
    fichero5.write(str(PDD5)+os.linesep)
    fichero5.close()
    fichero6= open('Diodo6.txt', 'a')
    fichero6.write(str(PAD6)+os.linesep)
    fichero6.write(str(PDD6)+os.linesep)
    fichero6.close()
    fichero7= open('Diodo7.txt', 'a')
    fichero7.write(str(PAD7)+os.linesep)
    fichero7.write(str(PDD7)+os.linesep)
    fichero7.close()
    fichero8= open('Diodo8.txt', 'a')
    fichero8.write(str(PAD8)+os.linesep)
    fichero8.write(str(PDD8)+os.linesep)
    fichero8.close()

    PD1=str(round(VD1_AB*i1,3))
    PD2=str(round(VD2_AB*i2,3))
    PD3=str(round(VD3_AB*i3,3))
    PD4=str(round(VD4_AB*i4,3))
    PD5=str(round(VD5_AB*i5,3))
    PD6=str(round(VD6_AB*i6,3))
    PD7=str(round(VD7_AB*i7,3))
    PD8=str(round(VD8_AB*i8,3))
    VAfterBuck=round(S_7+VD4_AB,3)
    
    PBeforeBuck=Pf
    if If<0.1:
        S_1=0.0
    PAfterBuck=str(round((VAfterBuck*S_1),1))
    
        
    
    PBeforeBuck1=str(round((S_7*(i4+i5)),1))
    VAfterBuck1=round(S_8+VD6_AB,1)
    PAfterBuck1=str(round(VAfterBuck1*S_3,1))
    PBeforeInverter=str(round(S_8*S_5,1))
    ListS_1.append(S_1)
    i=str(i)
    i1=str(i1)
    i2=str(i2)
    i3=str(i3)
    S_1=str(round(S_1,2))
    S_2=str(round(S_2,2))
    S_3=str(round(S_3,2))
    S_4=str(round(S_4,2))
    S_5=str(round(S_5,2))
    S_6=str(round(S_6,2))
    S_7=str(round(S_7,2))
    S_8=str(round(S_8,2))
    fichero9= open('Buck1.txt', 'a')
    fichero9.write(PBeforeBuck+os.linesep)
    fichero9.write(PAfterBuck+os.linesep)
    fichero9.close()
    fichero10= open('Buck2.txt', 'a')
    fichero10.write(PBeforeBuck1+os.linesep)
    fichero10.write(PAfterBuck1+os.linesep)
    fichero10.close()
    fichero11= open('Inverter.txt', 'a')
    fichero11.write(PBeforeInverter+os.linesep)
    fichero11.close()
        

    #D0.set(PD0)
    D1.set(PD1)
    D2.set(PD2)
    D3.set(PD3)
    D4.set(PD4)
    D5.set(PD5)
    D6.set(PD6)
    D7.set(PD7)
    D8.set(PD8)
    
    PBB.set(PBeforeBuck)
    PAB.set(PAfterBuck)
    PBB1.set(PBeforeBuck1)
    PAB1.set(PAfterBuck1)
    PBI.set(PBeforeInverter)
    Sensor1Label=Label(Frame,text="PDiodo 1").grid(row=0, column=0)
    cuadro1=Entry(Frame, textvariable=0).grid(row=0, column=1)
    Sensor2Label=Label(Frame,text="PDiodo 2").grid(row=1, column=0)
    cuadro2=Entry(Frame, textvariable=D1).grid(row=1, column=1)
    Sensor3Label=Label(Frame,text="PDiodo 3").grid(row=2, column=0)
    cuadro3=Entry(Frame, textvariable=D2).grid(row=2, column=1)
    Sensor4Label=Label(Frame,text="PDiodo 4").grid(row=3, column=0)
    cuadro4=Entry(Frame, textvariable=D3).grid(row=3, column=1)
    BBuckLabel=Label(Frame,text="PAntesBuck ").grid(row=4, column=0)
    cuadroBBuck=Entry(Frame, textvariable=PBB).grid(row=4, column=1)
    ABuckLabel=Label(Frame,text="PDespuesBuck ").grid(row=5, column=0)
    cuadroABuck=Entry(Frame, textvariable=PAB).grid(row=5, column=1)
    Sensor5Label=Label(Frame,text="PDiodo 5").grid(row=6, column=0)
    cuadro5=Entry(Frame, textvariable=D4).grid(row=6, column=1)
    Sensor6Label=Label(Frame,text="PDiodo 6").grid(row=7, column=0)
    cuadro6=Entry(Frame, textvariable=D5).grid(row=7, column=1)
    BBuck1Label=Label(Frame,text="PAntesBuck 2 ").grid(row=8, column=0)
    cuadroBBuck1=Entry(Frame, textvariable=PBB1).grid(row=8, column=1)
    ABuck1Label=Label(Frame,text="PDespuesBuck ").grid(row=9, column=0)
    cuadroABuck1=Entry(Frame, textvariable=PAB1).grid(row=9, column=1)
    Sensor7Label=Label(Frame,text="PDiodo 7").grid(row=10, column=0)
    cuadro7=Entry(Frame, textvariable=D6).grid(row=10, column=1)
    Sensor8Label=Label(Frame,text="PDiodo 8").grid(row=11, column=0)
    cuadro8=Entry(Frame, textvariable=D7).grid(row=11, column=1)
    Sensor9Label=Label(Frame,text="PDiodo 9").grid(row=12, column=0)
    cuadro9=Entry(Frame, textvariable=D8).grid(row=12, column=1)
    BInverterLabel=Label(Frame,text="PAntesInverter ").grid(row=13, column=0)
    cuadroBInverter=Entry(Frame, textvariable=PBI).grid(row=13, column=1)

    root.title("Interfaz Nodo 611")
    Frame.pack()
    root.update()
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
    print("Potencia de la fuente = "+Pf)
    print("Potencia del panel = "+Pp)
    print("Potencia de la bateria = "+Pb)
    a=a+1	
    print("Iteracion ="+str(a))
    try:
        response6 = requests.get('http://104.236.0.105:8080/voltage_sensors?voltage1=%s&voltage2=%s&voltage3=%s&create=%s'%(S_6,S_7,S_8, str(date.now())),
                            auth=requests.auth.HTTPBasicAuth(
                              'admin',
                              'uninorte'))
        response7 = requests.get('http://104.236.0.105:8080/low_current_sensors?current1=%s&current2=%s&current3=%s&current4=%s&create=%s'%(i, i1, i2, i3,str(date.now())),
                            auth=requests.auth.HTTPBasicAuth(
                              'admin',
                              'uninorte'))
        response8 = requests.get('http://104.236.0.105:8080/high_current_sensors?current5=%s&current6=%s&current7=%s&current8%s&current9=%s&create=%s'%(S_1,S_2,S_3,S_4,S_5,str(date.now())),
                            auth=requests.auth.HTTPBasicAuth(
                              'admin',
                              'uninorte'))
        response9 = requests.get('http://104.236.0.105:8080/node_powers?batteries=%s&red=%s&panel=%s&create=%s'%(Pb,Pf,Pp, str(date.now())),
                            auth=requests.auth.HTTPBasicAuth(
                              'admin',
                              'uninorte'))
        print(response6)
        print(response7)
        print(response8)
        print(response9)
        time.sleep(60)
    except:
        time.sleep(10)
    