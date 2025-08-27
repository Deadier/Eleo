"""
Système de jeux interactifs pour Emo
Implémente les différents jeux mentionnés dans les spécifications
"""

import random
import time
import threading
import logging
from enum import Enum
from typing import List, Dict, Optional, Callable
import pygame
import numpy as np

class GameState(Enum):
    IDLE = "idle"
    PLAYING = "playing"
    PAUSED = "paused"
    GAME_OVER = "game_over"

class InteractiveGames:
    """Gestionnaire des jeux interactifs"""
    
    def __init__(self, robot_instance, display_manager, audio_manager):
        self.robot = robot_instance
        self.display = display_manager
        self.audio = audio_manager
        self.current_game = None
        self.game_state = GameState.IDLE
        self.score = 0
        
        # Initialisation de pygame pour les jeux
        pygame.mixer.init()
        
    def start_game(self, game_name: str):
        """Démarre un jeu spécifique"""
        games = {
            'left_right': self.left_or_right_game,
            'dance_beat': self.dance_to_beat_game,
            'shooting': self.shooting_game,
            'parrot': self.parrot_mode,
            'puppet': self.puppet_mode
        }
        
        if game_name in games:
            self.current_game = game_name
            self.game_state = GameState.PLAYING
            self.score = 0
            games[game_name]()
        else:
            logging.error(f"Jeu inconnu: {game_name}")
    
    def stop_current_game(self):
        """Arrête le jeu en cours"""
        self.game_state = GameState.IDLE
        self.current_game = None
        self.robot.show_emotion('neutral')
        self.robot.speak("Jeu terminé!")

    def left_or_right_game(self):
        """Jeu Left or Right - Jeu de mémoire"""
        logging.info("Début du jeu Left or Right")
        self.robot.speak("Bienvenue dans le jeu Left or Right!")
        self.robot.speak("Je vais cacher un objet sous un verre. Devine où il est!")
        
        rounds = 5
        correct_answers = 0
        
        for round_num in range(1, rounds + 1):
            if self.game_state != GameState.PLAYING:
                break
                
            # Choix aléatoire gauche ou droite
            correct_side = random.choice(['left', 'right'])
            
            self.robot.speak(f"Manche {round_num}. L'objet est caché!")
            
            # Animation de mélange
            self._animate_mixing()
            
            self.robot.speak("Dis 'gauche' ou 'droite'")
            
            # Attendre la réponse vocale
            user_answer = self._wait_for_voice_input(['gauche', 'droite', 'left', 'right'], timeout=10)
            
            if user_answer:
                # Normalisation de la réponse
                if user_answer in ['gauche', 'left']:
                    user_side = 'left'
                else:
                    user_side = 'right'
                
                if user_side == correct_side:
                    correct_answers += 1
                    self.robot.speak("Bravo! C'est correct!")
                    self.robot.show_emotion('happy')
                    self._celebrate_animation()
                else:
                    self.robot.speak(f"Raté! C'était à {correct_side}!")
                    self.robot.show_emotion('sad')
            else:
                self.robot.speak("Temps écoulé!")
                self.robot.show_emotion('neutral')
            
            time.sleep(2)
        
        # Résultats finaux
        self.score = correct_answers
        self.robot.speak(f"Jeu terminé! Tu as {correct_answers} bonnes réponses sur {rounds}!")
        
        if correct_answers >= rounds * 0.7:
            self.robot.speak("Excellent score!")
            self.robot.show_emotion('excited')
        else:
            self.robot.speak("Tu peux faire mieux la prochaine fois!")
            self.robot.show_emotion('happy')
    
    def dance_to_beat_game(self):
        """Jeu Dance to the Beat - Danse sur le rythme"""
        logging.info("Début du jeu Dance to the Beat")
        self.robot.speak("C'est l'heure de danser! Applaudis et je danserai sur ton rythme!")
        
        # Démarrer la détection audio pour les applaudissements
        beat_detector = BeatDetector(self.audio)
        beat_detector.start_detection()
        
        dance_duration = 30  # 30 secondes de danse
        start_time = time.time()
        
        while time.time() - start_time < dance_duration and self.game_state == GameState.PLAYING:
            beats = beat_detector.get_beats()
            
            if beats:
                # Danser selon le rythme détecté
                self._dance_to_rhythm(beats)
            else:
                # Attendre en position neutre
                self.robot.show_emotion('neutral')
                time.sleep(0.1)
        
        beat_detector.stop_detection()
        self.robot.speak("C'était génial de danser avec toi!")
        self.robot.show_emotion('happy')
    
    def shooting_game(self):
        """Jeu de tir - Toucher des cibles à l'écran"""
        logging.info("Début du jeu de tir")
        self.robot.speak("Jeu de tir! Touche les cibles qui apparaissent!")
        
        targets_hit = 0
        total_targets = 10
        
        for target_num in range(total_targets):
            if self.game_state != GameState.PLAYING:
                break
            
            # Générer une cible aléatoire
            target_position = self._generate_target()
            
            self.robot.speak("Cible!")
            
            # Afficher la cible sur l'écran
            self.display.show_target(target_position)
            
            # Attendre le toucher sur l'écran tactile
            hit = self._wait_for_touch_input(target_position, timeout=3)
            
            if hit:
                targets_hit += 1
                self.robot.speak("Touché!")
                self.robot.show_emotion('excited')
                self._hit_animation()
            else:
                self.robot.speak("Raté!")
                self.robot.show_emotion('neutral')
            
            time.sleep(1)
        
        self.score = targets_hit
        accuracy = (targets_hit / total_targets) * 100
        self.robot.speak(f"Jeu terminé! {targets_hit} cibles touchées sur {total_targets}!")
        self.robot.speak(f"Précision: {accuracy:.0f}%!")
        
        if accuracy >= 70:
            self.robot.speak("Excellent tireur!")
            self.robot.show_emotion('happy')
        else:
            self.robot.speak("Continue à t'entraîner!")
    
    def parrot_mode(self):
        """Mode Perroquet - Répète ce que l'utilisateur dit"""
        logging.info("Début du mode Perroquet")
        self.robot.speak("Mode perroquet activé! Je vais répéter tout ce que tu dis!")
        self.robot.speak("Dis 'arrêt' pour quitter le mode.")
        
        while self.game_state == GameState.PLAYING:
            # Attendre une phrase de l'utilisateur
            user_input = self._wait_for_voice_input([], timeout=5)
            
            if user_input:
                if 'arrêt' in user_input.lower() or 'stop' in user_input.lower():
                    break
                
                # Répéter avec une voix légèrement différente
                self.robot.speak(f"{user_input}!", wait=False)
                self.robot.show_emotion('happy')
            else:
                # Montrer que le robot attend
                self.robot.show_emotion('neutral')
        
        self.robot.speak("Mode perroquet désactivé!")
    
    def puppet_mode(self):
        """Mode Marionnette - Contrôle manuel des expressions"""
        logging.info("Début du mode Marionnette")
        self.robot.speak("Mode marionnette! Contrôle mes expressions avec ta voix!")
        self.robot.speak("Dis une émotion: content, triste, en colère, excité, ou arrêt")
        
        emotion_commands = {
            'content': 'happy',
            'heureux': 'happy',
            'joie': 'happy',
            'triste': 'sad',
            'tristesse': 'sad',
            'colère': 'angry',
            'en colère': 'angry',
            'énervé': 'angry',
            'excité': 'excited',
            'excitation': 'excited',
            'neutre': 'neutral',
            'normal': 'neutral',
            'cligne': 'blink'
        }
        
        while self.game_state == GameState.PLAYING:
            command = self._wait_for_voice_input(list(emotion_commands.keys()) + ['arrêt', 'stop'], timeout=10)
            
            if command:
                if command in ['arrêt', 'stop']:
                    break
                
                emotion = emotion_commands.get(command, 'neutral')
                self.robot.show_emotion(emotion)
                self.robot.speak(f"Expression {command}!")
            else:
                self.robot.speak("Dis une émotion!")
        
        self.robot.speak("Mode marionnette désactivé!")
    
    def _animate_mixing(self):
        """Animation de mélange pour le jeu Left or Right"""
        for _ in range(5):
            if self.game_state != GameState.PLAYING:
                break
            self.robot.move_arms_random()
            time.sleep(0.3)
    
    def _celebrate_animation(self):
        """Animation de célébration"""
        self.robot.happy_dance()
    
    def _dance_to_rhythm(self, beats: List[float]):
        """Fait danser le robot selon un rythme"""
        for beat_intensity in beats:
            if self.game_state != GameState.PLAYING:
                break
            
            if beat_intensity > 0.7:
                self.robot.show_emotion('excited')
                self.robot.big_dance_move()
            elif beat_intensity > 0.4:
                self.robot.show_emotion('happy')
                self.robot.medium_dance_move()
            else:
                self.robot.small_dance_move()
            
            time.sleep(0.1)
    
    def _generate_target(self) -> Dict[str, int]:
        """Génère une position de cible aléatoire"""
        return {
            'x': random.randint(20, 220),
            'y': random.randint(20, 220),
            'size': random.randint(15, 30)
        }
    
    def _wait_for_voice_input(self, expected_words: List[str], timeout: float = 5) -> Optional[str]:
        """Attend une commande vocale spécifique"""
        # Cette fonction devrait utiliser le VoiceManager
        # Implémentation simplifiée pour l'exemple
        start_time = time.time()
        while time.time() - start_time < timeout:
            if hasattr(self.robot, 'voice_manager'):
                command = self.robot.voice_manager.get_command(timeout=0.1)
                if command:
                    for word in expected_words:
                        if word.lower() in command.lower():
                            return word.lower()
                    return command.lower()
            time.sleep(0.1)
        return None
    
    def _wait_for_touch_input(self, target_position: Dict, timeout: float = 3) -> bool:
        """Attend un toucher sur l'écran tactile"""
        # Implémentation simplifiée - devrait utiliser les capteurs tactiles
        start_time = time.time()
        while time.time() - start_time < timeout:
            if hasattr(self.robot, 'touch_detected') and self.robot.touch_detected:
                self.robot.touch_detected = False
                return True
            time.sleep(0.1)
        return False
    
    def _hit_animation(self):
        """Animation quand une cible est touchée"""
        self.robot.show_emotion('excited')
        self.robot.celebrate_move()

class BeatDetector:
    """Détecteur de rythme pour le jeu de danse"""
    
    def __init__(self, audio_manager):
        self.audio_manager = audio_manager
        self.is_detecting = False
        self.beats = []
        self.detection_thread = None
    
    def start_detection(self):
        """Démarre la détection de rythme"""
        self.is_detecting = True
        self.detection_thread = threading.Thread(target=self._detect_beats)
        self.detection_thread.start()
    
    def stop_detection(self):
        """Arrête la détection"""
        self.is_detecting = False
        if self.detection_thread:
            self.detection_thread.join()
    
    def _detect_beats(self):
        """Détection de rythme en arrière-plan"""
        while self.is_detecting:
            # Implémentation simplifiée
            # Dans la vraie version, analyser l'audio en temps réel
            beat_intensity = random.random()  # Simulation
            if beat_intensity > 0.3:
                self.beats.append(beat_intensity)
            time.sleep(0.1)
    
    def get_beats(self) -> List[float]:
        """Récupère les beats détectés"""
        current_beats = self.beats.copy()
        self.beats.clear()
        return current_beats
