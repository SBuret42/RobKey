# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
#import webrepl
#webrepl.start()

import st7789
import modules.tft_config as conf
import modules.connection as connect
import romanp as font
import dht
from machine import Pin
import modules.geoloc as geoloc
import modules.meteo as meteo
import modules.api_txt as api_txt
from time import sleep, time, localtime
import modules.affichage as affichage
from modules.buttons import Buttons
from modules.temperature import getTemperatureAndHumidity
import modules.motor as motor
from random import random,choice
import modules.ntptime as ntptime

capteur = dht.DHT11(Pin(44))
display = conf.config(2)
wlan_info = ("","") # Changez vos informations de connexionx ici : SSID,MDP


google_api_key = "" # Veuillez ajouter votre clé Google Maps API ici

list_anim = {"content":(2,1),"endormi":(4,1),"somnole":(3,1),"observe":(0,0),"monocle":(2,1)}

connect.connect_to_wifi(display, font, wlan_info[0], wlan_info[1])

def googleApi(graph=0): # Maximum une fois toutes les 2 mins pour 1 mois maximum - ATTENTION, PAS SUR QUE CA SE RESET PAR MOIS DONC EVITER DE LE FAIRE AU MAXIMUM
    global location, google_api_key
    old_location_r = open("data/old-location.txt",'r')
    
    if graph:
        display.init()
        display.draw(font,"Recherche d'une",20,111)
        display.draw(font,"localisation",40,126)
    
    try:
        location = geoloc.getLocation(google_api_key)
    except:
        if graph:
            display.fill_rect(0,107,170,25,st7789.BLACK)
            display.draw(font,'Erreur !',45,111)
            sleep(0.4)
            display.fill_rect(0,107,170,10,st7789.BLACK)
            display.deinit()
        location = False
    
    if not(location):
        liste = old_location_r.read().split(",")
        ##print("liste =", liste)
        location = {"lat":float(liste[0]),"lng":float(liste[1])}
    else:
        old_location_w = open("data/old-location.txt",'w')
        old_location_w.write(str(location["lat"]) + "," + str(location["lng"]))
        old_location_w.close()

    old_location_r.close()
    
    if graph:
        display.fill_rect(0,107,170,25,st7789.BLACK)
        display.draw(font,'Ok !',65,111)
        sleep(0.4)
        display.fill_rect(0,107,170,10,st7789.BLACK)
        display.deinit()

def meteoApi(graph = 0): # Maximum une fois toutes les 5 mins pour 1 mois maximum - Se recharge tous les mois
    global infos_meteo, location
    api_reset_r = open("data/reset-api.txt", 'r')
    meteo_api_reset_str = api_reset_r.read()
    meteo_api_reset = meteo_api_reset_str.split(",")[1].split("-")
    if localtime()[1] > int(meteo_api_reset[0]) or localtime()[0] > int(meteo_api_reset[1]):
        api_txt.set_api_counter(1,0)
    #print(location)
    
    if graph:
        display.init()
        display.draw(font,"Analyse de la meteo",0,111)
    
    try:
        infos_meteo = meteo.get_meteo(location["lat"],location["lng"])
        if graph:
            display.fill_rect(0,107,170,25,st7789.BLACK)
            display.draw(font,'Ok !',65,111)
            sleep(0.4)
            display.fill_rect(0,107,170,10,st7789.BLACK)
            display.deinit()
    except:
        if graph:
            display.fill_rect(0,107,170,25,st7789.BLACK)
            display.draw(font,'Erreur !',45,111)
            sleep(0.8)
            display.fill_rect(0,107,170,10,st7789.BLACK)
            display.deinit()
        infos_meteo = {"current":
            {"temperature":
             [
                 "E",
                 "E"
                 ],
             "precipitation":
             [
                 "E",
                 "E"
                 ]
             },
            "demain":
            {"temperature": ["E","E"],
             "precipitation":
             [
                 "E",
                 "E"
                 ]
             },
            "apres-demain":
            {"temperature": ["E","E"],
             "precipitation":[
                 "E",
                 "E"
                 ]
             }
            }

list_host = ["ntp.accelance.net","pool.ntp.org","ntp.unice.fr"]
for i in range(3):
    display.init()
    display.draw(font,"Mise a jour de",15,111)
    display.draw(font,"l'heure",50,126)
    try:
        ntptime.host = list_host[i]
        ntptime.settime()
        display.fill_rect(0,107,170,25,st7789.BLACK)
        display.draw(font,'Ok !',65,111)
        sleep(0.4)
        display.fill_rect(0,107,170,10,st7789.BLACK)
        display.deinit()
        break
    except:
        display.fill_rect(0,107,170,25,st7789.BLACK)
        display.draw(font,"Erreur ! L'heure",10,111)
        display.draw(font,"peut etre inexacte",5,126)
        display.draw(font,"Tentative : " + str(i+1),30,141)
        sleep(1.2)
        display.fill_rect(0,107,170,40,st7789.BLACK)
        display.deinit()
      
googleApi(1)
meteoApi(1)

time_since_google_check, time_since_meteo_check = time(),time()
counter = 0
limit = choice([2300,1700,1900])

try:
    display.init()
    
    b = Buttons()
    temp_humidity = getTemperatureAndHumidity(capteur)
    
    affichage.main_menu(display,font,temp_humidity[0],infos_meteo)
    display.hline(0,106,170,st7789.WHITE)
    affichage.animation(display, "content",list_anim["content"][0],list_anim["content"][1])
    
    while 1:
        anim_name = "content" #if random() < 0.9 else "somnole"
        if b.isButtonPressed("left"):
            sleep(0.05)
            if b.isButtonPressed("right"):
                #print("eteint")
                anim_name = "endormi"
                display.fill_rect(0,106,170,214,st7789.BLACK)
                affichage.animation(display, anim_name,list_anim[anim_name][0],list_anim[anim_name][1])
                break
            anim_name = "monocle"
            affichage.animation(display, anim_name,list_anim[anim_name][0],list_anim[anim_name][1])
            if new_time - time_since_meteo_check > 10:
                #print("Changement météo")
                meteoApi()
                time_since_meteo_check = new_time
                
                if infos_meteo["current"]["precipitation"][0] > 0:
                    icone = "pluie"
                    motor.baissebg()
                    motor.levebd()
                else:
                    icone = "soleil"
                    motor.baissebd()
                    motor.levebg()
                affichage.meteo_widget(display,font,infos_meteo,10,191)
                #print('infos_meteo["current"]["precipitation"]', infos_meteo["current"]["precipitation"])
                affichage.meteo_icon(display,icone,110,111)
            #print("left esp pressed")
        elif b.isButtonPressed("right"):
            sleep(0.05)
            if b.isButtonPressed("left"):
                #print("eteint")
                anim_name = "endormi"
                display.fill_rect(0,106,170,214,st7789.BLACK)
                affichage.animation(display, anim_name,list_anim[anim_name][0],list_anim[anim_name][1])
                break
            anim_name = "monocle"
            affichage.animation(display, anim_name,list_anim[anim_name][0],list_anim[anim_name][1])
            temp_humidity = getTemperatureAndHumidity(capteur)
            #print(temp_humidity)
            affichage.display_temperature(display,font,temp_humidity[0],10,151)
        elif b.isButtonPressed(1):
            sleep(0.05)
            if b.isButtonPressed(2):
                #print("eteint")
                anim_name = "endormi"
                display.fill_rect(0,106,170,214,st7789.BLACK)
                affichage.animation(display, anim_name,list_anim[anim_name][0],list_anim[anim_name][1])
                break
            anim_name = "somnole"
            affichage.animation(display, anim_name,list_anim[anim_name][0],list_anim[anim_name][1])
            #print("b1 pressed")
            motor.bassin_right()
        elif b.isButtonPressed(2):
            sleep(0.05)
            if b.isButtonPressed(1):
                #print("eteint")
                anim_name = "endormi"
                display.fill_rect(0,106,170,214,st7789.BLACK)
                affichage.animation(display, anim_name,list_anim[anim_name][0],list_anim[anim_name][1])
                break
            anim_name = "somnole"
            affichage.animation(display, anim_name,list_anim[anim_name][0],list_anim[anim_name][1])
            #print("b2 pressed")
            motor.bassin_left()
        
        new_time = time()
            
        affichage.display_time(display,font, 10, 111)
        if counter == limit or anim_name != "content":
            anim_name = "content"
            affichage.animation(display, anim_name,list_anim[anim_name][0],list_anim[anim_name][1])
            counter = 0
            limit = choice([2300,1700,1900])
        
        counter += 1

finally:
    motor.droit()
    motor.baissebg()
    motor.baissebg()
    display.deinit()