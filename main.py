from time import sleep
from meteofrance_api import MeteoFranceClient
from LCDScreen import LCDScreen
import json
import signal
import RPi.GPIO as GPIO
import serial

BUTTON_CHANGE_VIEW_PIN = 12
BUTTON_NEXT_STEP_PIN = 13
STATE = 0


meteo = MeteoFranceClient()

screen = LCDScreen()

jsonConfig = None

capaciteCuve = 1000# en litres
water_level = 0
water_temp = 0

communicator = serial.Serial('/dev/ttyACM0', baudrate=9600)

def recvCuveData():
    if communicator.in_waiting > 0:
        return communicator.readline().decode()
    return None

def sendCuveQuery(query):
    data = (query + '\n').encode()
    communicator.write(data)
    return recvCuveData()

def parseCuveLine(line):
    global water_level
    global water_temp

    try:
        json_object = json.loads(line)
    except:
        print("failed decode", line)
    else:
        print(json_object)
        if json_object["type"] == "info_sensor":
            water_level = json_object["params"]["water_level"]
            water_temp = json_object["params"]["water_temperature"]
            
def readCuveData():
    line = recvCuveData()
    while line is not None:
        parseCuveLine(line)
        line = recvCuveData()

def loop():
    # Attendre que data.json existe
    algoSplash()
    readCuveData()

def algoSplash():
    global jsonConfig

    file = open('data.json')
    jsonConfig = json.load(file)

    # Afficher tout va bien
    sleep(5)
    
    # Afficher qu'il faut arroser

#############
# Affichage #
#############

def afficheNiveauEau():
    global screen
    global capaciteCuve

    screen.setText("Niveau d'eau :  "+str(round(water_level*(capaciteCuve/1024),3))+"L/"+str(capaciteCuve)+"L")    
    sleep(2)
    screen.setText("")

    print("Niveau d'eau :  "+str((water_level*(capaciteCuve/1024)))+"L/"+str(capaciteCuve)+"L")


def afficheTemperature():
    global jsonData
    global screen

    screen.setText("Temperature eau:"+str(round(water_temp,1))+"-C")    
    sleep(2)
    screen.setText("")

    print("Temperature eau:"+str(round(water_temp,1))+"-C")


def afficheMeteo():
    global meteo
    
    previsions = meteo.get_forecast(45.64135619912203, 5.870128080576113,"fr").daily_forecast[1]
    temp = (previsions["T"]["min"]+previsions["T"]["max"])/2
    humidite = (previsions["humidity"]["min"]+previsions["humidity"]["max"])/2
    precipitation = previsions["precipitation"]["24h"]
    
    #32 car max par setText(txt)
    screen.setText("Meteo :         Temp : "+str(round(temp,1))+"-C")
    sleep(2)
    screen.setText("Meteo :         Humidite : "+str(round(humidite,1))+"%")
    sleep(2)
    screen.setText("Meteo :         Pluie : "+str(round(precipitation,1))+"%")
    sleep(2)
    screen.setText("")
    
    print("Météo  Température : "+str(temp)+"°C   -  Humidité : "+str(humidite)+"%   -  Précipitations (24H) : "+str(precipitation)+"%")


###########
# Boutons #
###########

def change_view(channel):
    global STATE
    print("change view")
    if STATE == 0:
        afficheNiveauEau()
    elif STATE == 1:
        afficheTemperature()
    elif STATE == 2:
        afficheMeteo()
    else:
        pass

    STATE = (STATE+1)%3
    
    

def next_step(channel):
	print("next step")


########
# Main #
########

button_event_map = [
	(BUTTON_CHANGE_VIEW_PIN, change_view),
	(BUTTON_NEXT_STEP_PIN, next_step)
]

algoSplash()
print("Config terminee")

GPIO.setmode(GPIO.BCM)

for pin, callback in button_event_map:
	GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	GPIO.add_event_detect(pin, GPIO.FALLING)
	GPIO.add_event_callback(pin, callback=callback)

while True:
    loop()