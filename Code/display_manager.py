"""
Gestionnaire d'affichage avancé pour Emo
Gère l'écran LCD avec contrôles de luminosité, animations et interfaces de jeu
"""

import os
import sys
import logging
from PIL import Image, ImageDraw, ImageFont
import threading
import time
from typing import Dict, List, Optional, Tuple
import json

sys.path.append("..")
from lib import LCD_2inch

class DisplayManager:
    """Gestionnaire avancé de l'affichage LCD"""
    
    def __init__(self, base_dir: str):
        self.base_dir = base_dir
        self.disp = None
        self.brightness = 80  # Luminosité par défaut (0-100)
        self.current_animation = None
        self.animation_thread = None
        self.is_animating = False
        
        # Dimensions de l'écran
        self.width = 240
        self.height = 240
        
        # Cache des images pour performance
        self.image_cache = {}
        
        # Police pour le texte
        self.font_path = self._get_font_path()
        
        self._initialize_display()
    
    def _initialize_display(self):
        """Initialise l'écran LCD"""
        try:
            self.disp = LCD_2inch.LCD_2inch()
            self.disp.Init()
            logging.info("Écran LCD initialisé")
        except Exception as e:
            logging.error(f"Erreur initialisation écran: {e}")
    
    def _get_font_path(self) -> str:
        """Trouve une police système disponible"""
        font_paths = [
            "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "/System/Library/Fonts/Arial.ttf",  # macOS
            "C:\\Windows\\Fonts\\arial.ttf"      # Windows
        ]
        
        for path in font_paths:
            if os.path.exists(path):
                return path
        
        return None  # Police par défaut PIL
    
    def set_brightness(self, brightness: int):
        """Ajuste la luminosité (0-100)"""
        self.brightness = max(0, min(100, brightness))
        # Note: L'implémentation réelle dépend du hardware LCD
        logging.info(f"Luminosité réglée à {self.brightness}%")
    
    def show_emotion(self, emotion: str, count: int = 1, speed: float = 1.0):
        """Affiche une émotion avec contrôle de vitesse"""
        if not self.disp:
            logging.error("Écran non initialisé")
            return
        
        self.stop_current_animation()
        
        self.is_animating = True
        self.animation_thread = threading.Thread(
            target=self._animate_emotion, 
            args=(emotion, count, speed)
        )
        self.animation_thread.start()
    
    def _animate_emotion(self, emotion: str, count: int, speed: float):
        """Anime une émotion"""
        try:
            frame_count = self._get_frame_count(emotion)
            
            for cycle in range(count):
                if not self.is_animating:
                    break
                
                for frame in range(frame_count):
                    if not self.is_animating:
                        break
                    
                    image = self._load_frame(emotion, frame)
                    if image:
                        self.disp.ShowImage(image)
                    
                    # Délai basé sur la vitesse
                    time.sleep(0.05 / speed)
                    
        except Exception as e:
            logging.error(f"Erreur animation {emotion}: {e}")
        finally:
            self.is_animating = False
    
    def _load_frame(self, emotion: str, frame_num: int) -> Optional[Image.Image]:
        """Charge une frame d'émotion avec cache"""
        cache_key = f"{emotion}_{frame_num}"
        
        if cache_key in self.image_cache:
            return self.image_cache[cache_key]
        
        image_path = os.path.join(
            self.base_dir, "emotions", emotion, f"frame{frame_num}.png"
        )
        
        if os.path.exists(image_path):
            try:
                image = Image.open(image_path)
                # Redimensionner si nécessaire
                if image.size != (self.width, self.height):
                    image = image.resize((self.width, self.height))
                
                self.image_cache[cache_key] = image
                return image
            except Exception as e:
                logging.error(f"Erreur chargement image {image_path}: {e}")
        
        return None
    
    def _get_frame_count(self, emotion: str) -> int:
        """Récupère le nombre de frames pour une émotion"""
        from config import FRAME_COUNT
        return FRAME_COUNT.get(emotion, 20)
    
    def stop_current_animation(self):
        """Arrête l'animation en cours"""
        self.is_animating = False
        if self.animation_thread and self.animation_thread.is_alive():
            self.animation_thread.join(timeout=1)
    
    def show_text(self, text: str, font_size: int = 20, color: Tuple[int, int, int] = (255, 255, 255)):
        """Affiche du texte sur l'écran"""
        if not self.disp:
            return
        
        try:
            # Créer une image avec le texte
            image = Image.new('RGB', (self.width, self.height), (0, 0, 0))
            draw = ImageDraw.Draw(image)
            
            # Charger la police
            font = None
            if self.font_path:
                try:
                    font = ImageFont.truetype(self.font_path, font_size)
                except:
                    font = ImageFont.load_default()
            else:
                font = ImageFont.load_default()
            
            # Calculer la position pour centrer le texte
            text_bbox = draw.textbbox((0, 0), text, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]
            
            x = (self.width - text_width) // 2
            y = (self.height - text_height) // 2
            
            draw.text((x, y), text, fill=color, font=font)
            
            self.disp.ShowImage(image)
            
        except Exception as e:
            logging.error(f"Erreur affichage texte: {e}")
    
    def show_menu(self, title: str, options: List[str], selected: int = 0):
        """Affiche un menu interactif"""
        if not self.disp:
            return
        
        try:
            image = Image.new('RGB', (self.width, self.height), (0, 0, 50))
            draw = ImageDraw.Draw(image)
            
            font_title = None
            font_option = None
            
            if self.font_path:
                try:
                    font_title = ImageFont.truetype(self.font_path, 16)
                    font_option = ImageFont.truetype(self.font_path, 14)
                except:
                    font_title = ImageFont.load_default()
                    font_option = ImageFont.load_default()
            else:
                font_title = ImageFont.load_default()
                font_option = ImageFont.load_default()
            
            # Titre
            title_bbox = draw.textbbox((0, 0), title, font=font_title)
            title_width = title_bbox[2] - title_bbox[0]
            title_x = (self.width - title_width) // 2
            draw.text((title_x, 10), title, fill=(255, 255, 255), font=font_title)
            
            # Options
            start_y = 50
            for i, option in enumerate(options):
                y = start_y + i * 25
                color = (255, 255, 0) if i == selected else (200, 200, 200)
                prefix = "► " if i == selected else "  "
                draw.text((10, y), f"{prefix}{option}", fill=color, font=font_option)
            
            self.disp.ShowImage(image)
            
        except Exception as e:
            logging.error(f"Erreur affichage menu: {e}")
    
    def show_target(self, target_info: Dict[str, int]):
        """Affiche une cible pour le jeu de tir"""
        if not self.disp:
            return
        
        try:
            image = Image.new('RGB', (self.width, self.height), (0, 0, 0))
            draw = ImageDraw.Draw(image)
            
            x = target_info['x']
            y = target_info['y']
            size = target_info['size']
            
            # Dessiner la cible (cercles concentriques)
            colors = [(255, 0, 0), (255, 255, 255), (255, 0, 0)]
            for i, color in enumerate(colors):
                radius = size - (i * size // 4)
                if radius > 0:
                    draw.ellipse([x-radius, y-radius, x+radius, y+radius], fill=color)
            
            self.disp.ShowImage(image)
            
        except Exception as e:
            logging.error(f"Erreur affichage cible: {e}")
    
    def show_game_score(self, score: int, max_score: int, game_name: str):
        """Affiche le score d'un jeu"""
        if not self.disp:
            return
        
        try:
            image = Image.new('RGB', (self.width, self.height), (0, 50, 0))
            draw = ImageDraw.Draw(image)
            
            font = None
            if self.font_path:
                try:
                    font = ImageFont.truetype(self.font_path, 18)
                except:
                    font = ImageFont.load_default()
            else:
                font = ImageFont.load_default()
            
            # Titre du jeu
            game_bbox = draw.textbbox((0, 0), game_name, font=font)
            game_width = game_bbox[2] - game_bbox[0]
            game_x = (self.width - game_width) // 2
            draw.text((game_x, 30), game_name, fill=(255, 255, 255), font=font)
            
            # Score
            score_text = f"Score: {score}/{max_score}"
            score_bbox = draw.textbbox((0, 0), score_text, font=font)
            score_width = score_bbox[2] - score_bbox[0]
            score_x = (self.width - score_width) // 2
            draw.text((score_x, 80), score_text, fill=(255, 255, 0), font=font)
            
            # Barre de progression
            bar_width = 200
            bar_height = 20
            bar_x = (self.width - bar_width) // 2
            bar_y = 120
            
            # Fond de la barre
            draw.rectangle([bar_x, bar_y, bar_x + bar_width, bar_y + bar_height], 
                         fill=(50, 50, 50), outline=(100, 100, 100))
            
            # Progression
            if max_score > 0:
                progress_width = int((score / max_score) * bar_width)
                draw.rectangle([bar_x, bar_y, bar_x + progress_width, bar_y + bar_height], 
                             fill=(0, 255, 0))
            
            # Pourcentage
            if max_score > 0:
                percentage = int((score / max_score) * 100)
                perc_text = f"{percentage}%"
                perc_bbox = draw.textbbox((0, 0), perc_text, font=font)
                perc_width = perc_bbox[2] - perc_bbox[0]
                perc_x = (self.width - perc_width) // 2
                draw.text((perc_x, 160), perc_text, fill=(255, 255, 255), font=font)
            
            self.disp.ShowImage(image)
            
        except Exception as e:
            logging.error(f"Erreur affichage score: {e}")
    
    def show_battery_status(self, battery_level: int):
        """Affiche le niveau de batterie"""
        if not self.disp:
            return
        
        try:
            image = Image.new('RGB', (self.width, self.height), (0, 0, 0))
            draw = ImageDraw.Draw(image)
            
            # Icône de batterie
            battery_width = 80
            battery_height = 40
            battery_x = (self.width - battery_width) // 2
            battery_y = (self.height - battery_height) // 2
            
            # Contour de la batterie
            draw.rectangle([battery_x, battery_y, battery_x + battery_width, battery_y + battery_height],
                         outline=(255, 255, 255), width=2)
            
            # Borne positive
            draw.rectangle([battery_x + battery_width, battery_y + 10, 
                          battery_x + battery_width + 5, battery_y + 30], fill=(255, 255, 255))
            
            # Niveau de batterie
            fill_width = int((battery_level / 100) * (battery_width - 4))
            color = (0, 255, 0) if battery_level > 30 else (255, 255, 0) if battery_level > 15 else (255, 0, 0)
            
            if fill_width > 0:
                draw.rectangle([battery_x + 2, battery_y + 2, 
                              battery_x + 2 + fill_width, battery_y + battery_height - 2], 
                             fill=color)
            
            # Pourcentage
            font = None
            if self.font_path:
                try:
                    font = ImageFont.truetype(self.font_path, 16)
                except:
                    font = ImageFont.load_default()
            else:
                font = ImageFont.load_default()
            
            perc_text = f"{battery_level}%"
            perc_bbox = draw.textbbox((0, 0), perc_text, font=font)
            perc_width = perc_bbox[2] - perc_bbox[0]
            perc_x = (self.width - perc_width) // 2
            draw.text((perc_x, battery_y + battery_height + 20), perc_text, 
                     fill=(255, 255, 255), font=font)
            
            self.disp.ShowImage(image)
            
        except Exception as e:
            logging.error(f"Erreur affichage batterie: {e}")
    
    def clear_screen(self, color: Tuple[int, int, int] = (0, 0, 0)):
        """Efface l'écran avec une couleur"""
        if not self.disp:
            return
        
        try:
            image = Image.new('RGB', (self.width, self.height), color)
            self.disp.ShowImage(image)
        except Exception as e:
            logging.error(f"Erreur effacement écran: {e}")
    
    def cleanup(self):
        """Nettoie les ressources"""
        self.stop_current_animation()
        if self.disp:
            try:
                self.disp.module_exit()
            except:
                pass
        self.image_cache.clear()
        logging.info("DisplayManager nettoyé")
