"""
Robot Emo avancé avec toutes les fonctionnalités
Version améliorée intégrant reconnaissance vocale, jeux, et fonctionnalités avancées
"""

import time
import multiprocessing
import threading
import logging
import os
import sys
import signal
from typing import Dict, Optional

# Imports hardware (avec gestion d'erreur pour les tests)
try:
    import RPi.GPIO as GPIO
    from adafruit_servokit import ServoKit
    HARDWARE_AVAILABLE = True
except ImportError:
    logging.warning("Hardware non disponible - mode simulation")
    HARDWARE_AVAILABLE = False

# Imports des modules du projet
sys.path.append(os.path.dirname(__file__))
from config import *
from utils import ProcessManager, setup_logging, safe_terminate_process, clear_queue
from voice_manager import VoiceManager, create_voice_manager
from games_manager import InteractiveGames
from display_manager import DisplayManager

class AdvancedEmoRobot:
    """Robot Emo avancé avec toutes les fonctionnalités"""
    
    def __init__(self):
        # Configuration logging
        setup_logging()
        logging.info("Initialisation du robot Emo avancé...")
        
        # Répertoire de base
        self.base_dir = os.path.dirname(os.path.realpath(__file__))
        
        # État du robot
        self.is_running = False
        self.current_mode = "normal"  # normal, game, voice_control, parrot, puppet
        self.battery_level = 100
        self.touch_detected = False
        self.volume = 80
        
        # Gestionnaires
        self.process_manager = ProcessManager()
        self.display_manager = DisplayManager(self.base_dir)
        self.voice_manager = None
        self.games_manager = None
        
        # Communication inter-processus
        self.command_queue = multiprocessing.Queue()
        self.event = multiprocessing.Event()
        
        # Hardware
        self.kit = None
        self.servoR = None
        self.servoL = None
        self.servoB = None
        
        self._initialize_hardware()
        self._initialize_managers()
        self._setup_signal_handlers()
    
    def _initialize_hardware(self):
        """Initialise le hardware si disponible"""
        if not HARDWARE_AVAILABLE:
            logging.warning("Hardware non disponible - fonctions simulées")
            return
        
        try:
            # Configuration GPIO
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(TOUCH_PIN, GPIO.IN)
            GPIO.setup(VIBRATION_PIN, GPIO.IN)
            
            # Servomoteurs
            self.kit = ServoKit(channels=SERVO_CHANNELS)
            self.servoR = self.kit.servo[SERVO_RIGHT_CHANNEL]
            self.servoL = self.kit.servo[SERVO_LEFT_CHANNEL]
            self.servoB = self.kit.servo[SERVO_BASE_CHANNEL]
            
            logging.info("Hardware initialisé avec succès")
            
        except Exception as e:
            logging.error(f"Erreur initialisation hardware: {e}")
            HARDWARE_AVAILABLE = False
    
    def _initialize_managers(self):
        """Initialise les gestionnaires"""
        try:
            # Gestionnaire vocal
            self.voice_manager = create_voice_manager(self)
            
            # Gestionnaire de jeux
            self.games_manager = InteractiveGames(
                self, self.display_manager, None  # audio_manager à implémenter
            )
            
            logging.info("Gestionnaires initialisés")
            
        except Exception as e:
            logging.error(f"Erreur initialisation gestionnaires: {e}")
    
    def _setup_signal_handlers(self):
        """Configure les gestionnaires de signaux pour arrêt propre"""
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
    
    def _signal_handler(self, signum, frame):
        """Gestionnaire d'arrêt propre"""
        logging.info(f"Signal {signum} reçu - arrêt en cours...")
        self.shutdown()
    
    def start(self):
        """Démarre le robot"""
        if self.is_running:
            return
        
        self.is_running = True
        logging.info("Démarrage du robot Emo...")
        
        # Affichage de démarrage
        self.display_manager.show_text("Emo Starting...", font_size=24)
        time.sleep(2)
        
        # Animation de démarrage
        self.show_emotion('bootup3', count=1)
        
        # Démarrage des services
        self._start_sensor_monitoring()
        self._start_voice_recognition()
        
        # Boucle principale
        self._main_loop()
    
    def _start_sensor_monitoring(self):
        """Démarre la surveillance des capteurs"""
        sensor_process = multiprocessing.Process(
            target=self._sensor_monitoring_loop, 
            name='sensor_monitor'
        )
        sensor_process.start()
        self.process_manager.add_process('sensor_monitor', sensor_process)
    
    def _start_voice_recognition(self):
        """Démarre la reconnaissance vocale"""
        if self.voice_manager:
            self.voice_manager.start_listening()
            logging.info("Reconnaissance vocale démarrée")
    
    def _sensor_monitoring_loop(self):
        """Boucle de surveillance des capteurs"""
        if not HARDWARE_AVAILABLE:
            return
        
        previous_touch_state = GPIO.input(TOUCH_PIN)
        
        while self.is_running:
            try:
                # Capteur tactile
                current_touch_state = GPIO.input(TOUCH_PIN)
                if current_touch_state == GPIO.HIGH and previous_touch_state != current_touch_state:
                    self.touch_detected = True
                    if self.command_queue.qsize() == 0:
                        self.event.set()
                        self.command_queue.put('touch_happy')
                
                previous_touch_state = current_touch_state
                
                # Capteur de vibration
                if GPIO.input(VIBRATION_PIN) == 1:
                    if self.command_queue.qsize() == 0:
                        self.event.set()
                        emotions = EMOTION_TYPES['TRIGGERED']
                        emotion = emotions[time.time_ns() % len(emotions)]
                        self.command_queue.put(f'vibration_{emotion}')
                
                time.sleep(SENSOR_POLL_DELAY)
                
            except Exception as e:
                logging.error(f"Erreur surveillance capteurs: {e}")
                time.sleep(1)
    
    def _main_loop(self):
        """Boucle principale du robot"""
        logging.info("Boucle principale démarrée")
        
        # Message de bienvenue
        self.speak("Bonjour! Je suis Emo, votre robot compagnon!")
        self.show_emotion('happy', count=2)
        
        while self.is_running:
            try:
                if self.event.is_set():
                    self._handle_command()
                else:
                    self._idle_behavior()
                
                # Vérification de la batterie
                self._check_battery()
                
                time.sleep(0.1)
                
            except Exception as e:
                logging.error(f"Erreur boucle principale: {e}")
                time.sleep(1)
    
    def _handle_command(self):
        """Traite les commandes reçues"""
        self.event.clear()
        
        try:
            command = self.command_queue.get_nowait()
            logging.info(f"Commande reçue: {command}")
            
            # Commandes tactiles/vibration
            if command.startswith('touch_'):
                emotion = command.split('_', 1)[1]
                self._execute_emotion(emotion)
            elif command.startswith('vibration_'):
                emotion = command.split('_', 1)[1]
                self._execute_emotion(emotion)
            
            # Commandes vocales
            elif command in ['salut', 'bonjour', 'hello']:
                self.handle_greeting()
            elif command in ['jeu', 'game']:
                self.handle_game_mode()
            elif command == 'danse':
                self.handle_dance_mode()
            elif command == 'perroquet':
                self.handle_parrot_mode()
            elif command == 'marionnette':
                self.handle_puppet_mode()
            elif command in ['arrêt', 'stop']:
                self.handle_stop()
            elif 'volume' in command:
                self.handle_volume_control(command)
            elif 'luminosité' in command:
                self.handle_brightness_control(command)
            else:
                # Émotion directe
                if command in FRAME_COUNT:
                    self._execute_emotion(command)
        
        except Exception as e:
            logging.error(f"Erreur traitement commande: {e}")
        
        # Vider le reste de la queue
        clear_queue(self.command_queue)
    
    def _execute_emotion(self, emotion: str):
        """Exécute une émotion (affichage + mouvement + son)"""
        try:
            # Processus parallèles pour affichage, mouvement et son
            processes = []
            
            # Affichage
            display_process = multiprocessing.Process(
                target=self.show_emotion,
                args=(emotion, 3)
            )
            processes.append(display_process)
            
            # Son
            sound_process = multiprocessing.Process(
                target=self.play_sound,
                args=(emotion,)
            )
            processes.append(sound_process)
            
            # Mouvement
            if emotion == 'happy':
                movement_process = multiprocessing.Process(target=self.happy_dance)
            elif emotion == 'angry':
                movement_process = multiprocessing.Process(target=self.angry_movement)
            elif emotion == 'sad':
                movement_process = multiprocessing.Process(target=self.sad_movement)
            elif emotion == 'excited':
                movement_process = multiprocessing.Process(target=self.excited_movement)
            else:
                movement_process = multiprocessing.Process(target=self.neutral_position)
            
            processes.append(movement_process)
            
            # Démarrer tous les processus
            for p in processes:
                p.start()
            
            # Attendre la fin
            for p in processes:
                p.join(timeout=5)
                if p.is_alive():
                    p.terminate()
                    p.join()
            
        except Exception as e:
            logging.error(f"Erreur exécution émotion {emotion}: {e}")
    
    def _idle_behavior(self):
        """Comportement en mode inactif"""
        # Animation neutre périodique
        if time.time() % 10 < 0.1:  # Toutes les 10 secondes environ
            neutral_emotions = EMOTION_TYPES['NORMAL']
            emotion = neutral_emotions[int(time.time()) % len(neutral_emotions)]
            self._execute_emotion(emotion)
    
    def _check_battery(self):
        """Vérifie le niveau de batterie"""
        # Simulation de décharge de batterie
        if time.time() % 60 < 0.1:  # Toutes les minutes
            self.battery_level = max(0, self.battery_level - 1)
            
            if self.battery_level < 20:
                logging.warning(f"Batterie faible: {self.battery_level}%")
                if self.battery_level < 10:
                    self.speak("Batterie très faible!")
                    self.display_manager.show_battery_status(self.battery_level)
    
    # Gestionnaires de commandes vocales
    def handle_greeting(self):
        """Gestionnaire de salutation"""
        responses = [
            "Bonjour! Comment allez-vous?",
            "Salut! Je suis ravi de vous voir!",
            "Hello! Que puis-je faire pour vous?"
        ]
        response = responses[int(time.time()) % len(responses)]
        self.speak(response)
        self._execute_emotion('happy')
    
    def handle_game_mode(self):
        """Gestionnaire du mode jeu"""
        self.current_mode = "game"
        self.speak("Mode jeu activé! Choisissez un jeu:")
        self.speak("Dites: gauche droite, danse, tir, perroquet, ou marionnette")
        self._execute_emotion('excited')
    
    def handle_dance_mode(self):
        """Gestionnaire du mode danse"""
        if self.games_manager:
            self.games_manager.start_game('dance_beat')
    
    def handle_parrot_mode(self):
        """Gestionnaire du mode perroquet"""
        self.current_mode = "parrot"
        if self.games_manager:
            self.games_manager.start_game('parrot')
    
    def handle_puppet_mode(self):
        """Gestionnaire du mode marionnette"""
        self.current_mode = "puppet"
        if self.games_manager:
            self.games_manager.start_game('puppet')
    
    def handle_stop(self):
        """Gestionnaire d'arrêt"""
        self.current_mode = "normal"
        if self.games_manager:
            self.games_manager.stop_current_game()
        self.speak("Mode normal activé")
        self._execute_emotion('neutral')
    
    def handle_volume_control(self, command: str):
        """Gestionnaire de contrôle du volume"""
        if 'plus' in command:
            self.volume = min(100, self.volume + 10)
        else:
            self.volume = max(0, self.volume - 10)
        
        self.speak(f"Volume réglé à {self.volume}%")
        
        if self.voice_manager:
            self.voice_manager.set_voice_properties(volume=self.volume/100)
    
    def handle_brightness_control(self, command: str):
        """Gestionnaire de contrôle de la luminosité"""
        current_brightness = self.display_manager.brightness
        
        if 'plus' in command:
            new_brightness = min(100, current_brightness + 10)
        else:
            new_brightness = max(10, current_brightness - 10)
        
        self.display_manager.set_brightness(new_brightness)
        self.speak(f"Luminosité réglée à {new_brightness}%")
    
    # Méthodes de mouvement
    def neutral_position(self):
        """Position neutre"""
        if not HARDWARE_AVAILABLE:
            return
        try:
            self.servoR.angle = SERVO_POSITIONS['RIGHT_MID']
            self.servoL.angle = SERVO_POSITIONS['LEFT_MID']
            self.servoB.angle = SERVO_POSITIONS['BASE_MID']
        except Exception as e:
            logging.error(f"Erreur position neutre: {e}")
    
    def happy_dance(self):
        """Danse joyeuse"""
        if not HARDWARE_AVAILABLE:
            return
        try:
            for _ in range(5):
                for i in range(0, 120):
                    if i <= 30:
                        self.servoR.angle = 90 + i
                        self.servoL.angle = 90 - i
                        self.servoB.angle = 90 - i
                    elif i <= 90:
                        self.servoR.angle = 150 - i
                        self.servoL.angle = i + 30
                        self.servoB.angle = i + 30
                    else:
                        self.servoR.angle = i - 30
                        self.servoL.angle = 210 - i
                        self.servoB.angle = 210 - i
                    time.sleep(ANIMATION_SPEED['FAST'])
        except Exception as e:
            logging.error(f"Erreur danse joyeuse: {e}")
    
    def angry_movement(self):
        """Mouvement de colère"""
        if not HARDWARE_AVAILABLE:
            return
        try:
            for _ in range(5):
                self.servoB.angle = 90 + (time.time_ns() % 30)
                time.sleep(ANIMATION_SPEED['MEDIUM'])
        except Exception as e:
            logging.error(f"Erreur mouvement colère: {e}")
    
    def sad_movement(self):
        """Mouvement de tristesse"""
        if not HARDWARE_AVAILABLE:
            return
        try:
            self.servoR.angle = 0
            self.servoL.angle = 180
            for i in range(60):
                if i <= 15:
                    self.servoB.angle = 90 - i
                elif i <= 45:
                    self.servoB.angle = 60 + i
                else:
                    self.servoB.angle = 150 - i
                time.sleep(ANIMATION_SPEED['SLOW'])
        except Exception as e:
            logging.error(f"Erreur mouvement tristesse: {e}")
    
    def excited_movement(self):
        """Mouvement d'excitation"""
        if not HARDWARE_AVAILABLE:
            return
        try:
            self.servoR.angle = 0
            self.servoL.angle = 180
            for i in range(120):
                if i <= 30:
                    self.servoB.angle = 90 - i
                elif i <= 90:
                    self.servoB.angle = i + 30
                else:
                    self.servoB.angle = 210 - i
                time.sleep(ANIMATION_SPEED['MEDIUM'])
        except Exception as e:
            logging.error(f"Erreur mouvement excitation: {e}")
    
    # Méthodes utilitaires
    def show_emotion(self, emotion: str, count: int = 1):
        """Affiche une émotion"""
        self.display_manager.show_emotion(emotion, count)
    
    def speak(self, text: str, wait: bool = True):
        """Fait parler le robot"""
        if self.voice_manager:
            self.voice_manager.speak(text, wait)
        else:
            logging.info(f"Robot dit: {text}")
    
    def play_sound(self, emotion: str):
        """Joue un son d'émotion"""
        try:
            sound_path = os.path.join(self.base_dir, "sound", f"{emotion}.wav")
            if os.path.exists(sound_path):
                os.system(f"aplay {sound_path}")
        except Exception as e:
            logging.error(f"Erreur son {emotion}: {e}")
    
    def shutdown(self):
        """Arrêt propre du robot"""
        logging.info("Arrêt du robot...")
        self.is_running = False
        
        # Arrêter les services
        if self.voice_manager:
            self.voice_manager.stop_listening()
        
        if self.games_manager:
            self.games_manager.stop_current_game()
        
        # Message d'au revoir
        self.speak("Au revoir!")
        self.show_emotion('neutral', count=1)
        
        # Nettoyer les ressources
        self.process_manager.cleanup()
        self.display_manager.cleanup()
        
        if HARDWARE_AVAILABLE:
            try:
                GPIO.cleanup()
            except:
                pass
        
        logging.info("Robot arrêté proprement")

def main():
    """Point d'entrée principal"""
    robot = AdvancedEmoRobot()
    
    try:
        robot.start()
    except KeyboardInterrupt:
        logging.info("Interruption clavier détectée")
    except Exception as e:
        logging.error(f"Erreur critique: {e}")
    finally:
        robot.shutdown()

if __name__ == '__main__':
    main()
