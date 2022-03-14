import json
from locale import atoi
from time import sleep
from meteofrance_api import MeteoFranceClient

parcelDataPath = "data.json" # path pour le fichier configurant la parcelle et la quantité d'eau de la cuve
latitude = 45.527532
longitude = 5.960843
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
    while (not checkFileExist(parcelDataPath)) :
        sleep(1)

    algoSplash()

    print("End")


def algoSplash():
    global splashTaskState
    # Afficher tout va bien
    sleep(5)
    
    # Afficher qu'il faut arroser
    splashTaskState = "Todo"

    guidedWatering()

def guidedWatering():
    """ Gestion d'une session d'arrosage guidé 
    """
    global splashTaskState
    if splashTaskState == "Todo" :
        splashTaskState = "During"
        
        # Opening data.json file
        f = open(parcelDataPath)
        data = json.load(f)
    
        # Itération sur parcels
        for parcel in data['parcels']:
            l = calculateWater(parcel['name'], atoi(parcel['dim']))
            print("Send to arduino : Arroser la parcelle ", parcel['name'], " avec ", l, " litres d'eau")
            # TODO attendre passage suivant 

        # Closing file
        f.close()

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

main()