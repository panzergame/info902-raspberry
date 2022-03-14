import json
from time import sleep
from meteofrance_api import MeteoFranceClient


splashTaskState = "Nothing" # Définit l'état de Splash, Nothing : rien à faire / Todo : une tâche d'arrosage à faire / During : en cours de réalisation

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

def main():
    # Attendre que data.json existe
    while (not checkFileExist("data.json")) :
        sleep(1)

    algoSplash()

    print("End")


def algoSplash():
    # Afficher tout va bien
    sleep(5)
    
    # Afficher qu'il faut arroser
    splashTaskState = "Todo"

def watering():
    if splashTaskState == "Todo" :
        meteo = MeteoFranceClient()

        prevision = meteo.get_forecast(45.527532, 5.960843,"fr")
        print(prevision.daily_forecast)

    # Opening data.json file
    f = open('data.json')
    data = json.load(f)
 
    # Itération sur data
    for i in data['emp_details']:
        print(i)
 
    # Closing file
    f.close()


main()