import network
import st7789 #En théorie inutile car déjà importé dans boot.py
from time import sleep

def connect_to_wifi(display, font, ssid, mdp):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        display.init()
        display.draw(font,"Connexion a un point",0,111)
        display.draw(font,"d'acces en cours",15,126)
        wlan.connect(ssid,mdp)
        while not wlan.isconnected():
            pass
    display.fill_rect(0,107,170,25,st7789.BLACK)
    display.draw(font,'Connecte !',40,111)
    sleep(0.8)
    display.fill_rect(0,107,170,10,st7789.BLACK)
    display.deinit()

def search_wlan():
    station = network.WLAN(network.STA_IF)
    station.active(True)
    return station.scan()