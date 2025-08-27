import time
from adafruit_servokit import ServoKit
import multiprocessing

import RPi.GPIO as GPIO
import os
import sys
import logging
import spidev as SPI
sys.path.append("..")
from lib import LCD_2inch
from PIL import Image

from random import randint

# Détermination du répertoire de base pour les chemins relatifs
base_dir = os.path.dirname(os.path.realpath(__file__))

# Configuration des broches pour les capteurs tactiles et de vibration
TOUCH_PIN = 17
VIBRATION_PIN = 22

# Configuration des broches du Raspberry Pi pour l'écran LCD
RST = 27
DC = 25
BL = 18
BUS = 0 
DEVICE = 0 

# Configuration des servomoteurs
SERVO_RIGHT_CHANNEL = 5   # Bras droit
SERVO_LEFT_CHANNEL = 11   # Bras gauche  
SERVO_BASE_CHANNEL = 13   # Base rotation

# Initialisation des broches GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(TOUCH_PIN, GPIO.IN)
GPIO.setup(VIBRATION_PIN, GPIO.IN) 

# Initialisation du kit de servomoteurs avec 16 canaux
kit = ServoKit(channels=16)

# Déclaration des servomoteurs
servoR = kit.servo[SERVO_RIGHT_CHANNEL]  # Référence à 0
servoL = kit.servo[SERVO_LEFT_CHANNEL]   # Référence à 180
servoB = kit.servo[SERVO_BASE_CHANNEL]   # Référence à 90

# Nombre de frames pour chaque animation d'émotion
frame_count = {'blink':39, 'happy':45, 'sad':47,'dizzy':67,'excited':24,'neutral':61,'happy2':20,'angry':20,'happy3':26,'bootup3':124,'blink2':20}

# Liste des émotions possibles
emotion = ['angry','sad','excited']

# États neutres par défaut
normal = ['neutral','blink2']

# File d'attente pour les processus et événement pour la synchronisation
q = multiprocessing.Queue()
event = multiprocessing.Event()

def check_sensor():
    """Surveille les capteurs tactiles et de vibration.

    Le code d'origine ne mettait jamais ``previous_state`` à jour, ce qui
    provoquait un déclenchement permanent tant que le capteur tactile restait
    actionné. ``previous_state`` est maintenant mis à jour à chaque boucle afin
    de ne réagir qu'à un changement d'état.
    """
    try:
        previous_state = GPIO.input(TOUCH_PIN)
        while True:
            current_state = GPIO.input(TOUCH_PIN)

            if current_state == GPIO.HIGH and previous_state != current_state:
                if q.qsize() == 0:
                    event.set()
                    q.put('happy')

            previous_state = current_state

            if GPIO.input(VIBRATION_PIN) == 1:
                print('vib')
                if q.qsize() == 0:
                    event.set()
                    q.put(emotion[randint(0, 2)])

            time.sleep(0.05)
    except Exception as e:
        print(f"Erreur capteurs: {e}")
        GPIO.cleanup()

def servoMed():
    # Place les servomoteurs en position médiane
    try:
        servoR.angle = 90
        servoL.angle = 90
        servoB.angle = 90
    except Exception as e:
        print(f"Erreur servomoteurs: {e}")

def servoDown():
    # Abaisse les servomoteurs
    try:
        servoR.angle = 0
        servoL.angle = 180
        servoB.angle = 90
    except Exception as e:
        print(f"Erreur servomoteurs: {e}")

def baserotate(reference,change,timedelay):
    # Effectue une rotation de la base du servomoteur
    for i in range(reference,reference+change,1):
        servoB.angle = i
        time.sleep(timedelay)
    for j in range(reference+change, reference-change,-1):
        servoB.angle = j
        time.sleep(timedelay)
    for k in range(reference-change, reference,1):
        servoB.angle = k
        time.sleep(timedelay)

def HandDownToUp(start,end,timedelay):
    # Anime les mains du bas vers le haut
    for i,j in zip(range(0+start,end,1),range((180-start),(180-end),-1)):
        servoR.angle = i
        servoL.angle = j
        time.sleep(timedelay)

def HandUpToDown(start,end,timedelay):
    # Anime les mains du haut vers le bas
    for i,j in zip(range(0+start,end,-1),range((180-start),(180-end),1)):
        servoR.angle = i
        servoL.angle = j
        time.sleep(timedelay)

def rotate(start,end,timedelay):
    # Détermine la direction de rotation des mains et effectue l'animation
    if start<end:
        HandDownToUp(start,end,timedelay)
        HandUpToDown(end,start,timedelay)
    else:
        HandUpToDown(end,start,timedelay)
        HandDownToUp(start,end,timedelay)

def happy():
    # Anime le robot pour exprimer la joie
    servoMed()
    for n in range(5):
        for i in range(0, 120):
            if i <= 30:
                servoR.angle = 90 + i #at 120
                servoL.angle = 90 - i #at 60
                servoB.angle = 90 - i
            if (i > 30 and i <=90):
                servoR.angle = 150 - i #at 60
                servoL.angle = i + 30 #at 120
                servoB.angle = i + 30
            if i>90:
                servoR.angle = i - 30 #at 90
                servoL.angle = 210 - i #at 90
                servoB.angle = 210 - i
            time.sleep(0.004)

def angry():
    # Anime le robot pour exprimer la colère
    for i in range(5):
        baserotate(90,randint(0,30),0.01)

def angry2():
    # Une autre animation pour exprimer la colère
    servoMed()
    for i in range(90):
        servoR.angle = 90-i
        servoL.angle = i+90
        servoB.angle = 90 - randint(-12,12)
        time.sleep(0.02)

def sad():
    # Anime le robot pour exprimer la tristesse
    servoDown()
    for i in range(0,60):
        if i<=15:
            servoB.angle = 90 - i
        if (i>15 and i<=45):
            servoB.angle = 60+i
        if(i>45):
            servoB.angle = 150 - i
        time.sleep(0.09)

def excited():
    # Anime le robot pour exprimer l'excitation
    servoDown()
    for i in range(0,120):
        if i<=30:
            servoB.angle = 90 - i #at 60
        if (i>30 and i<=90):
            servoB.angle = i + 30 #at 120
        if(i>90):
            servoB.angle = 210 - i
        time.sleep(0.01)

def blink():
    # Fait cligner les yeux du robot
    servoR.angle = 0
    servoL.angle = 180
    servoB.angle = 90

def bootup():
    # Initialise le robot et affiche une animation de démarrage
    show('bootup3',1)
    for i in range(1):
        p2 = multiprocessing.Process(target=show,args=('blink2',3))
        p3 = multiprocessing.Process(target=rotate,args=(0,150,0.005))
        p4 = multiprocessing.Process(target=baserotate,args=(90,45,0.01))
        p2.start()
        p3.start()
        p4.start()
        p4.join()
        p2.join()
        p3.join()
    
def sound(emotion):
    # Joue un son associé à une émotion
    sound_path = os.path.join(base_dir, "sound", f"{emotion}.wav")
    for i in range(1):
        sound_path = os.path.join(base_dir, "sound", f"{emotion}.wav")
        os.system(f"aplay {sound_path}")
    
def show(emotion,count):
    # Affiche les images correspondant à une émotion sur l'écran LCD
    disp = None
    try:
        for i in range(count):
            disp = LCD_2inch.LCD_2inch()
            disp.Init()
            for i in range(frame_count[emotion]):
                image_path = os.path.join(base_dir, "emotions", emotion, f"frame{str(i)}.png")
                if os.path.exists(image_path):
                    image = Image.open(image_path)  
                    disp.ShowImage(image)
                else:
                    print(f"Image manquante: {image_path}")
    except IOError as e:
        print(f"Erreur I/O: {e}")
        logging.info(e)    
    except KeyboardInterrupt:
        print("Interruption utilisateur")
        if disp:
            disp.module_exit()
        servoDown()
        logging.info("quit:")
        exit()
    except Exception as e:
        print(f"Erreur affichage: {e}")
    finally:
        if disp:
            try:
                disp.module_exit()
            except:
                pass

if __name__ == '__main__':
    # Processus principal, lance la surveillance des capteurs et réagit aux émotions détectées
    p1 = multiprocessing.Process(target=check_sensor, name='p1')
    p1.start()
    bootup()
    p5 = None
    p6 = None
    while True:
        if event.is_set():
                if p5 is not None:
                    p5.terminate()
                event.clear()
                emotion = q.get()
                # Vider correctement la queue
                while not q.empty():
                    try:
                        q.get_nowait()
                    except:
                        break
                print(emotion)
                p2 = multiprocessing.Process(target=show,args=(emotion,4))
                p3 = multiprocessing.Process(target=sound,args=(emotion,))
                if emotion == 'happy':
                    p4 = multiprocessing.Process(target=happy)
                elif emotion == 'angry':
                    p4 = multiprocessing.Process(target=angry)
                elif emotion == 'sad':
                    p4 = multiprocessing.Process(target=sad)
                elif emotion == 'excited':
                    p4 = multiprocessing.Process(target=excited)
                elif emotion == 'blink':
                    p4 = multiprocessing.Process(target=blink)
                else:
                    continue
                p2.start()
                p3.start()
                p4.start()
                p2.join()
                p3.join()
                p4.join()
        else:
            # Gère les processus enfants et affiche un état neutre
            p = multiprocessing.active_children()
            for i in p:
                if i.name not in ['p1','p5','p6']:
                    try:
                        i.terminate()
                        i.join(timeout=1)  # Attendre max 1 seconde
                        if i.is_alive():
                            i.kill()  # Forcer si nécessaire
                    except:
                        pass
            neutral = normal[0]
            p5 = multiprocessing.Process(target=show,args=(neutral,4),name='p5')
            p6 = multiprocessing.Process(target=baserotate,args=(90,60,0.02),name='p6')
            p5.start()
            p6.start()
            p6.join()
            p5.join()
