from time import sleep  #Inutile car importé dans boot.py

def getTemperatureAndHumidity(capteur): # Capteur doit etre sous cette forme : capteur = dht.DHT11(Pin(17)) -> Ne pas oublier d'importer le module dht
    try:
        capteur.measure() # Met à jour les données de températures et d'humidités
        sleep(1)
        return (capteur.temperature(),capteur.humidity())
    except:
        print("Valeurs non récupérées")
        return ("E")