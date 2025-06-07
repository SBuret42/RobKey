from modules.servo import Servo
import time

motor=Servo(pin=12) # A changer selon la broche utilisée
motorbd=Servo(pin=10)
motorbg=Servo(pin=11)
 
def droit(t=1):
    motor.move(285)
    time.sleep(t)

def bassin_left(t=1):
    motor.move(265)
    time.sleep(t)

def bassin_right(t=1):
    motor.move(305)
    time.sleep(t)

def baissebg(t=0.5):
#     motorbg.move(270)
#     time.sleep(0.5)
    motorbg.move(335)
    time.sleep(t)
    
def levebg(t=0.5):
#     motorbg.move(335)
#     time.sleep(0.5)
    motorbg.move(270)
    time.sleep(t)

def baissebd(t=0.5):
#     motorbd.move(270)
#     time.sleep(0.5)
    motorbd.move(335)
    time.sleep(t)
    
def levebd(t=0.5):
#     motorbd.move(335)
#     time.sleep(0.5)
    motorbd.move(270)
    time.sleep(t)
    
droit()
baissebd()
baissebg()