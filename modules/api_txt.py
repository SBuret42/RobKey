"""
api[0] => Google Maps API
api[1] => Météo API
"""

def get_api_counter():
    fichier_r = open("data/counter-api.txt",'r')
    liste = fichier_r.read().split(",")
    fichier_r.close()
    return liste

def add_api_counter(indice_api): # ne fonctionne qu'avec deux apis
    fichier_w = open("data/counter-api.txt",'w')
    val = get_api_counter()
    val[indice_api] = int(val[indice_api]) + 1
    
    fichier_w.write(str(val[0]) + "," + str(val[1]))
    fichier_w.close()

def set_api_counter(indice_api,value): # ne fonctionne qu'avec deux apis
    fichier_w = open("data/counter-api.txt",'w')
    api_value = get_api_counter()
    api_value[indice_api] = str(value)
    fichier_w.write(api_value[0] + "," + api_value[1])
    fichier_w.close()