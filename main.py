from time import sleep
from meteofrance_api import MeteoFranceClient
from LCDScreen import LCDScreen
import json

meteo = MeteoFranceClient()

screen = LCDScreen()

jsonData = None
jsonConfig = None

capaciteCuve = 1000# en litres

def main():
    # Attendre que data.json existe

    algoSplash()


def algoSplash():
    global jsonData
    global jsonConfig
    file = open('capteurdata.json')
    jsonData = json.load(file)
    file = open('data.json')
    jsonConfig = json.load(file)

    # Afficher tout va bien
    sleep(5)
    
    # Afficher qu'il faut arroser

def switchInfo():
    STATE = 0


def afficheNiveauEau():
    global jsonData
    global screen
    global capaciteCuve

    water_level = jsonData["water_level"]
    screen.setText("Niveau d'eau :  "+str(round(water_level*(capaciteCuve/1024),3))+"L/"+str(capaciteCuve)+"L")    
    sleep(2)
    screen.setText("")
    
    print("Niveau d'eau :  "+str((water_level*(capaciteCuve/1024)))+"L/"+str(capaciteCuve)+"L")

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

algoSplash()
afficheNiveauEau()
afficheMeteo()