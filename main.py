from time import sleep

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

main()