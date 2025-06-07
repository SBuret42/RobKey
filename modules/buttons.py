from machine import Pin
from time import sleep

# Importer les modules est inutile car ils sont déjà importés dans boot.py

class Buttons():
    def __init__(self):
        #self.name = "t-display-s3"
        
        # NomDuBouton : [                    PinUtilisé                     ,    mode    , value ]
        #      1      : [ Pin 3 en mode INPUT avec une résistance Pull-Down ,   levier   ,   0   ]
        # 1 : [ Pin(3, mode=Pin.IN, pull=Pin.PULL_DOWN), 1, 0 ]
        
        # Note : le chiffre de value dans la liste n'est pas pris en compte si le bouton est en mode "poussoir" -> On ne peut pas mettre None car si on décide de changer le mode du bouton, la valeur devient importante.
        
        
        # Pour une raison inconnue, "left" et "right" ne fonctionne plus.
        self.list_button = {"left" : [Pin(14, Pin.IN, Pin.PULL_UP),0,1],
                            "right" : [Pin(0, Pin.IN, Pin.PULL_UP),0,1],
                            1 : [Pin(17, mode=Pin.IN, pull=Pin.PULL_UP),0,1],
                            2 : [Pin(18, Pin.IN, Pin.PULL_UP),0,1]
                            }


    def getButton(self, button):
        return self.list_button[button]
    
    def setButton(self, button, pin, mode, value=None): # Le set fait également add.
        self.list_button[button] = [pin,mode,value]

    def setMode(self, button, val:bool): # Ce mode change le mode du bouton -> soit "levier" soit "poussoir"
        if isinstance(val, bool) or val in (0,1):
            self.list_button[button][1] = val
            if not(val):
                self.list_button[button][2] = 1
            return print("Mode définie sur : " + str(self.list_button[button][1]))
        else:
            raise ValueError("val must be a boolean or a integer included between 0 and 1.")
    
    def setValue(self, button, value):
        if self.list_button[button][1]:
            self.list_button[button][2] = value
            return print("Valeur définie sur : " + str(self.list_button[button][2])) 
        else:
            print("Button must be a toogle button, not a push button.")
            return False
    
    def getValue(self, button): # Renvoie la valeur du bouton
        if not(self.list_button[button][1]): # Si le statut de mode_toogle est égal à 0 <=> Si le bouton est en mode "poussoir" et non "levier"
            return self.list_button[button][0].value()
        else:
            if not(self.list_button[button][0].value()):
                self.list_button[button][2] = 0 if self.list_button[button][2] else 1
                sleep(0.25)
            return self.list_button[button][2]
    
    def isButtonPressed(self,button): # Renvoie True si le bouton est pressé (donc si value = 0) et False sinon
        return not(self.getValue(button))
                
