import st7789
from time import sleep, localtime
import modules.motor as motor
from machine import RTC

last_temps = -1

def display_time(display,font,x,y):
    global last_temps
#     temps = list(RTC().datetime())
    temps = list(localtime())
    temps[3] += 1
    if last_temps < temps[5]:
        display.png("/images/icones/horloge.png",x,y,True)
        display.fill_rect(x+30,y+5,60+6,10,st7789.BLACK)
        display.draw(font, str(temps[3]) + ":" + str(temps[4]) + ":" + str(temps[5]),x+30,y+10)
    last_temps = temps[5]

def display_meteo(display,font,infos_meteo, x, y):
    """
    counter = 0
    for i in infos_meteo:
        display.draw(font,str(infos_meteo[i][0]),x,y+20*counter)
        if infos_meteo[i][1] == "°C":
            display.draw(font, font.LAST,x + display.draw_len(font,str(infos_meteo[i][0])), y+20*counter)
            display.draw(font, " C",x + display.draw_len(font,str(infos_meteo[i][0])), y+20*counter)
        else:
            display.draw(font,str(infos_meteo[i][1]),x + display.draw_len(font,str(infos_meteo[i][0])),y+20*counter)
        counter += 1
    """
    """
    counter = 0
    for i in infos_meteo:
        print(i, counter)
        display.draw(font,str(infos_meteo[i][0]),x + counter,y)
        if infos_meteo[i][1] == "°C":
            display.draw(font, font.LAST,x + counter + display.draw_len(font,str(infos_meteo[i][0])), y)
            display.draw(font, " C",x + counter + display.draw_len(font,str(infos_meteo[i][0])), y)
        else:
            display.draw(font,str(infos_meteo[i][1]),x + display.draw_len(font,str(infos_meteo[i][0])),y)
        counter = display.draw_len(font,str(infos_meteo[i][0])) + 20
    """
    display.draw(font,str(infos_meteo["temperature"][0]),x,y)
    display.draw(font, font.LAST,x + display.draw_len(font,str(infos_meteo["temperature"][0])), y)
    display.draw(font, " C",x + display.draw_len(font,str(infos_meteo["temperature"][0])), y)
    
    display.draw(font,str(infos_meteo["precipitation"][0]),x+80,y)
    display.draw(font,str(infos_meteo["precipitation"][1]),x + 80 + display.draw_len(font,str(infos_meteo["precipitation"][0])),y)

def display_temperature(display,font,infos_temperature,x,y):
    display.fill_rect(x,y,70,20,st7789.BLACK)
    display.png("/images/icones/temperature.png",x,y,True)
    display.draw(font,str(infos_temperature) + " C",x+30,y+9)
    display.draw(font,font.LAST,x+30+display.draw_len(font,str(infos_temperature)), + y+9)    
    
def meteo_icon(display,icone,x,y):
    display.fill_rect(x,y,50,50,st7789.BLACK)
    if icone == "pluie":
        display.png("/images/icones/mauvais_temps.png",x,y,True) #Nuage pluie gris pas content
    else:
        display.png("/images/icones/beau_temps.png",x,y,True) # Soleil content
        

def meteo_widget(display,font,infos_meteo,x,y):
    display.fill_rect(x,y,170,200,st7789.BLACK)
    
    
    display.draw(font, "Auj.",x,y)
    display_meteo(display,font,infos_meteo["current"],x, y+20) #x,y+20)
    
    display.draw(font, "Dem.", x, y+40) #x+50, y)
    display_meteo(display,font,infos_meteo["demain"], x, y+60) #x+50,y+20)
    
    display.draw(font, "Apr-Dem.", x, y+80) #x+90, y)
    display_meteo(display,font,infos_meteo["apres-demain"], x, y+100) #x+90,y+20)

def main_menu(display,font,infos_temp,infos_meteo):
    display_time(display,font, 10, 111) # x = 52 pour un semblant de centrage
    display_temperature(display,font,infos_temp,10,151)
    
    if infos_meteo["current"]["precipitation"][0] > 0:
        icone = "pluie"
        motor.baissebg()
        motor.levebd()
    else:
        icone = "soleil"
        motor.baissebd()
        motor.levebg()
    
    meteo_widget(display,font,infos_meteo,10,191)
    meteo_icon(display,icone,110,111)

def animation(display,name:str,iteration:int,i_fixe:int): # list_anim : {"content":(2,1),"endormi":(4,1),"somnole":(3,1),"observe":(0,0),"monocle":(2,1)}
    display.fill_rect(0,0,170,105,st7789.BLACK)
    for i in range(2,iteration+1):
        display.png("/images/" + name + "/" + name + str(i) + ".png",0,0)
        if name == "endormi":
            sleep(0.3)
    for i in range(iteration,0,-1):
        display.png("/images/" + name + "/" + name + str(i) + ".png",0,0)
        if name == "endormi":
            sleep(0.3)
    display.png("/images/" + name + "/" + name + str(i_fixe) + ".png",0,0)
    