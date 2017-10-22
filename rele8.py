#Este script lee la ultima configuracion de unos pines GPIO desde un archivo que se
#crea desde este mismo programa. Cuano se inicia el programa se lee el archivo
#y cuada ve que se modifia el estado de un pin, se guarda dicha configuracion
#el bucle principal solicita la introduccion de un pin (del uno al 8)
#si no se introduce ningun dato se termina el programa. Esto se realiza con
#un subproceso

import RPi.GPIO as GPIO
import time
import sys
import threading

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#Abrimos el archivo que contiene la informacin de los estados de los reles
#La infromacion de la ultima configuracion de los reles tiene formato:
#{'Rel1': 0, 'Rel2': 1, 'Rel3': 0, 'Rel4': 1, 'Rel5': 1, 'Rel6': 1, 'Rel7': 0, 'Rel8': 1} 

#Abrimos el archivo
archivo = open("Desktop/releEstados.txt")

#Dividimos la lina por las comas y cerramos el archivo
#El archivo debe de contener una cadena antes de iniciar la aplicacion
for line in archivo:
    line = line[1:len(line)-1]
    releXinfo=line.split(",")
archivo.close()

#Extraemos el estado de cada rele. Para ello dividimos por : y cojemos la parte derecha (1)   
valueX = []
for i in range(len(releXinfo)):
    valueX.append(int(releXinfo[i].split(':')[1]))

#Genero un diccionario con los valores de cada rele y una linea de texto a guardar
reles={"Rel1":valueX[0],"Rel2":valueX[1],"Rel3":valueX[2],"Rel4":valueX[3],"Rel5":valueX[4],"Rel6":valueX[5],"Rel7":valueX[6],"Rel8":valueX[7]}
lineaGuardar = "{'Rel1': "+str(reles["Rel1"])+", 'Rel2': "+str(reles["Rel2"])+", 'Rel3': "+str(reles["Rel3"])+", 'Rel4': "+str(reles["Rel4"])+", 'Rel5': "+str(reles["Rel5"])+", 'Rel6': "+str(reles["Rel6"])+", 'Rel7': "+str(reles["Rel7"])+", 'Rel8': "+str(reles["Rel8"])+"}"
print lineaGuardar

    
#Esta funcion comprueba el numero de rele introducido y asigna el pin de salida apropiado
def comprobar(n):
    if n==1:
        pinSalida = 2
    elif n==2:
        pinSalida = 3
    elif n==3:
        pinSalida = 4
    elif n==4:
        pinSalida = 17
    elif n==5:
        pinSalida = 27
    elif n==6:
        pinSalida = 22
    elif n==7:
        pinSalida = 10
    elif n==8:
        pinSalida = 9

    return pinSalida


#activos los pines segun la ultima configuracion
for i in range(8):
    pin=comprobar(i+1)
    GPIO.setup(pin,GPIO.OUT)
    GPIO.output(pin,valueX[i])
    
#EStas dos funciones son para activar un subproceso con su caracteristica
#demon. El subproceso estara activo durante una cantidad de tiempo
#especificada en join
def activarDemonio():
    t = threading.Thread(target=entrada)
    t.daemon=True
    t.start()
    t.join(20)

#El subproceso que se activa es el de solicitar una entrada
nRele = None
def entrada():
    global nRele
    nRele =raw_input("Introduzca rele: ")

#bucle principal
while (1):

    #Si hay una entrada o si termina el tiempo se acaba el subproceso
    activarDemonio()

    #si no hay entrada entonces habra ocurrido que ha acabado el tiempo
    #entonces cerramos el programa. En caso de de que haya habido entrada
    #procesamo esa entrada
    if nRele is None:
        print "Exiting"
        sys.exit()
        
    else:

        try:
            nRele = int(nRele)
        except:
            print "Selecciones uno de los 8 reles disponibles [1,8] o 0 para salir del programa"
            
        if nRele>0 and nRele<9:

            pin = comprobar(nRele)

            if reles["Rel"+str(nRele)]==0:
                reles["Rel"+str(nRele)]=1
                GPIO.output(pin,1)
            elif reles["Rel"+str(nRele)]==1:
                reles["Rel"+str(nRele)]=0
                GPIO.output(pin,0)

            lineaGuardar = "{'Rel1': "+str(reles["Rel1"])+", 'Rel2': "+str(reles["Rel2"])+", 'Rel3': "+str(reles["Rel3"])+", 'Rel4': "+str(reles["Rel4"])+", 'Rel5': "+str(reles["Rel5"])+", 'Rel6': "+str(reles["Rel6"])+", 'Rel7': "+str(reles["Rel7"])+", 'Rel8': "+str(reles["Rel8"])+"}"
            print lineaGuardar
            archivo = open("Desktop/releEstados.txt","w")
            archivo.write(lineaGuardar)
            archivo.close()
                
        elif nRele == 0 :
            print "Se termino la ejecucion del programa"
            sys.exit()

        nRele=None


            
    
    
