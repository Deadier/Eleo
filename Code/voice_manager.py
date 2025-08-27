"""
Gestionnaire de reconnaissance vocale pour Emo
Implémente la reconnaissance et synthèse vocale
"""

import speech_recognition as sr
import pyttsx3
import threading
import queue
import logging
from typing import Optional, Callable
import time

class VoiceManager:
    """Gestionnaire de reconnaissance et synthèse vocale"""
    
    def __init__(self, language='fr-FR'):
        self.language = language
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.tts_engine = pyttsx3.init()
        self.is_listening = False
        self.command_queue = queue.Queue()
        self.callback_functions = {}
        
        # Configuration TTS
        self.tts_engine.setProperty('rate', 150)  # Vitesse de parole
        self.tts_engine.setProperty('volume', 0.8)  # Volume
        
        # Calibrage du microphone
        self._calibrate_microphone()
        
    def _calibrate_microphone(self):
        """Calibre le microphone pour le bruit ambiant"""
        try:
            with self.microphone as source:
                logging.info("Calibrage du microphone...")
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                logging.info("Calibrage terminé")
        except Exception as e:
            logging.error(f"Erreur calibrage microphone: {e}")
    
    def start_listening(self):
        """Démarre l'écoute en continu"""
        if self.is_listening:
            return
            
        self.is_listening = True
        listening_thread = threading.Thread(target=self._listen_continuously)
        listening_thread.daemon = True
        listening_thread.start()
        logging.info("Écoute vocale démarrée")
    
    def stop_listening(self):
        """Arrête l'écoute"""
        self.is_listening = False
        logging.info("Écoute vocale arrêtée")
    
    def _listen_continuously(self):
        """Boucle d'écoute continue"""
        while self.is_listening:
            try:
                with self.microphone as source:
                    # Écoute avec timeout
                    audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=5)
                
                # Reconnaissance en arrière-plan
                threading.Thread(target=self._process_audio, args=(audio,)).start()
                    
            except sr.WaitTimeoutError:
                continue
            except Exception as e:
                logging.error(f"Erreur écoute: {e}")
                time.sleep(0.1)
    
    def _process_audio(self, audio):
        """Traite l'audio capturé"""
        try:
            # Reconnaissance vocale
            text = self.recognizer.recognize_google(audio, language=self.language)
            logging.info(f"Commande reconnue: {text}")
            
            # Ajout à la queue des commandes
            self.command_queue.put(text.lower())
            
            # Exécution des callbacks
            self._execute_callbacks(text.lower())
            
        except sr.UnknownValueError:
            pass  # Pas de parole détectée
        except sr.RequestError as e:
            logging.error(f"Erreur service reconnaissance: {e}")
    
    def speak(self, text: str, wait: bool = True):
        """Fait parler le robot"""
        try:
            if wait:
                self.tts_engine.say(text)
                self.tts_engine.runAndWait()
            else:
                # Parole en arrière-plan
                threading.Thread(target=self._speak_background, args=(text,)).start()
        except Exception as e:
            logging.error(f"Erreur synthèse vocale: {e}")
    
    def _speak_background(self, text: str):
        """Parole en arrière-plan"""
        self.tts_engine.say(text)
        self.tts_engine.runAndWait()
    
    def register_command_callback(self, keyword: str, callback: Callable):
        """Enregistre un callback pour un mot-clé"""
        self.callback_functions[keyword.lower()] = callback
    
    def _execute_callbacks(self, text: str):
        """Exécute les callbacks correspondants"""
        for keyword, callback in self.callback_functions.items():
            if keyword in text:
                try:
                    callback(text)
                except Exception as e:
                    logging.error(f"Erreur callback {keyword}: {e}")
    
    def get_command(self, timeout: Optional[float] = None) -> Optional[str]:
        """Récupère la prochaine commande vocale"""
        try:
            return self.command_queue.get(timeout=timeout)
        except queue.Empty:
            return None
    
    def set_voice_properties(self, rate: int = 150, volume: float = 0.8, voice_id: Optional[int] = None):
        """Configure les propriétés de la voix"""
        self.tts_engine.setProperty('rate', rate)
        self.tts_engine.setProperty('volume', volume)
        
        if voice_id is not None:
            voices = self.tts_engine.getProperty('voices')
            if voice_id < len(voices):
                self.tts_engine.setProperty('voice', voices[voice_id].id)

# Commandes vocales prédéfinies
VOICE_COMMANDS = {
    'salut': 'happy',
    'bonjour': 'happy',
    'hello': 'happy',
    'triste': 'sad',
    'colère': 'angry',
    'en colère': 'angry',
    'excité': 'excited',
    'content': 'happy',
    'danse': 'dance_mode',
    'jeu': 'game_mode',
    'perroquet': 'parrot_mode',
    'marionnette': 'puppet_mode',
    'arrêt': 'stop',
    'stop': 'stop',
    'volume plus': 'volume_up',
    'volume moins': 'volume_down',
    'luminosité plus': 'brightness_up',
    'luminosité moins': 'brightness_down'
}

def create_voice_manager(robot_instance) -> VoiceManager:
    """Créé et configure le gestionnaire vocal pour le robot"""
    voice_manager = VoiceManager()
    
    # Enregistrement des callbacks
    for command, emotion in VOICE_COMMANDS.items():
        if hasattr(robot_instance, f'handle_{emotion}'):
            voice_manager.register_command_callback(
                command, 
                getattr(robot_instance, f'handle_{emotion}')
            )
    
    return voice_manager
