from glob import glob
import json
from locale import atoi
from LCDScreen import LCDScreen
from time import sleep
from meteofrance_api import MeteoFranceClient
import signal
import RPi.GPIO as GPIO
import serial

parcelDataPath = "data.json" # path pour le fichier configurant la parcelle et la quantité d'eau de la cuve
jsonConfig = None

numEtape = 0 # numéro de l'étape de l'arrosage

# Coordonnée GPS 
latitude = 45.527532
longitude = 5.960843
meteo = MeteoFranceClient()

splashTaskState = "Nothing" # Définit l'état de Splash, Nothing : rien à faire / Todo : une tâche d'arrosage à faire / During : en cours de réalisation

capaciteCuve = 1000 # en litres
water_level = 0
water_temp = 0

BUTTON_CHANGE_VIEW_PIN = 12
BUTTON_NEXT_STEP_PIN = 13
STATE = 0

screen = LCDScreen()
communicator = serial.Serial('/dev/ttyACM0', baudrate=9600)

def checkFileExist(filePath):
    """Vérifier si un fichier existe.

    Parameters
    ----------
    filepath : string 
        le path du fichier dont on veut vérifier l'existance.

    Returns
    -------
    boolean
        True si le fichier exist, False si le fichier n'existe pas.

    """

    try:
        with open(filePath, 'r') as f:
            return True
    except FileNotFoundError as e:
        return False
    except IOError as e:
        return False

def recvCuveData():
    """ Récupérer les messages de l'arduino
    """
    if communicator.in_waiting > 0:
        return communicator.readline().decode()
    return None

def sendCuveQuery(query):
    """ Envoyer des messages à l'arduino
    """
    data = (query + '\n').encode()
    communicator.write(data)
    return recvCuveData()

def parseCuveLine(line):
    """ Parser les données récupérer depuis l'arduino
    """
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
    """Lire les données envoyées depuis l'arduino"""
    line = recvCuveData()
    while line is not None:
        parseCuveLine(line)
        line = recvCuveData()

def calculateWater(plant, dim):
    """ Algorithme pour calculer la quantité d'eau pour arroser une parcelle par rapport au type de plante, ca dimension et la météo

    Parameters
    ----------
    plant : string
        le type de plante
    dim : int
        la dimension de la parcelle

    Return
    ------
        La quantité d'eau pour arroser la parcelle
    """
    plant_mult = 0

    if (plant == 'Tomates'):
        plant_mult = 0.5
    elif (plant == 'Carottes'):
        plant_mult = 0.1
    else:
        print("Plant not define !")

    meteo = MeteoFranceClient()
    prevision = meteo.get_forecast(latitude, longitude,"fr")    
    # print(prevision.daily_forecast)

    # TODO 

    return plant_mult * dim


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
    


def guidedWatering(etape):
    """ Gestion d'une session d'arrosage guidé 
    """
    l = calculateWater(parcels[etape]['name'], atoi(parcels[etape]['dim']))
    print("Send to arduino : Arroser la parcelle ", parcels[etape]['name'], " avec ", l, " litres d'eau")

          

def next_step(channel):
    """ Quand utilise le bouton de droite, démarre un arrosage guidé et change les étapes
    
    """
    global numEtape, splashTaskState

    if splashTaskState == "Todo" :
        splashTaskState = "During"
    else:
        print("Pas de tâches à réaliser pour le moment !")
    
    if splashTaskState == "During":

        numEtape += 1

        if (numEtape > len(parcels)) :
            splashTaskState = "Nothing"
            numEtape = 0
        else:
            guidedWatering(numEtape)


########
# Main #
########

button_event_map = [
	(BUTTON_CHANGE_VIEW_PIN, change_view),
	(BUTTON_NEXT_STEP_PIN, next_step)
]

GPIO.setmode(GPIO.BCM)

for pin, callback in button_event_map:
	GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	GPIO.add_event_detect(pin, GPIO.FALLING)
	GPIO.add_event_callback(pin, callback=callback)



# Attendre que data.json existe
while (not checkFileExist(parcelDataPath)) :
    sleep(1)

f = open(parcelDataPath)
jsonConfig = json.load(f)

capaciteCuve = atoi(jsonConfig['capacity'])
parcels = jsonConfig['parcels']

# Splash a une tâche à faire au bout de 2 sec
sleep(2)
splashTaskState = "Todo"

def loop():
    readCuveData()

while True:
    loop()



