"""
Utilitaires pour le robot Emo
Fonctions helper et utilitaires communs
"""

import os
import logging
import multiprocessing
import time
from pathlib import Path

def setup_logging(log_level=logging.INFO):
    """Configure le système de logging"""
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('emo_robot.log'),
            logging.StreamHandler()
        ]
    )

def validate_file_exists(file_path):
    """Vérifie qu'un fichier existe"""
    return Path(file_path).exists()

def safe_terminate_process(process, timeout=1.0):
    """Termine un processus de manière sécurisée"""
    if process is None or not process.is_alive():
        return
    
    try:
        process.terminate()
        process.join(timeout=timeout)
        
        if process.is_alive():
            logging.warning(f"Force killing process {process.name}")
            process.kill()
            process.join()
            
    except Exception as e:
        logging.error(f"Erreur lors de la terminaison du processus: {e}")

def clear_queue(queue):
    """Vide complètement une queue multiprocessing"""
    while not queue.empty():
        try:
            queue.get_nowait()
        except:
            break

def validate_servo_angle(angle):
    """Valide qu'un angle de servomoteur est dans la plage correcte"""
    return max(0, min(180, angle))

def create_directories(base_path, subdirs):
    """Crée les répertoires nécessaires s'ils n'existent pas"""
    for subdir in subdirs:
        dir_path = os.path.join(base_path, subdir)
        os.makedirs(dir_path, exist_ok=True)

class ProcessManager:
    """Gestionnaire de processus pour éviter les fuites de ressources"""
    
    def __init__(self):
        self.processes = {}
        self.protected_names = ['p1', 'p5', 'p6']  # Processus à ne pas terminer
    
    def add_process(self, name, process):
        """Ajoute un processus à la gestion"""
        self.processes[name] = process
    
    def terminate_all_except_protected(self):
        """Termine tous les processus sauf ceux protégés"""
        for name, process in list(self.processes.items()):
            if name not in self.protected_names:
                safe_terminate_process(process)
                del self.processes[name]
    
    def cleanup(self):
        """Nettoie tous les processus"""
        for name, process in list(self.processes.items()):
            safe_terminate_process(process)
        self.processes.clear()

def retry_operation(func, max_retries=3, delay=0.1):
    """Retry une opération en cas d'échec"""
    for attempt in range(max_retries):
        try:
            return func()
        except Exception as e:
            if attempt == max_retries - 1:
                raise e
            logging.warning(f"Tentative {attempt + 1} échouée: {e}")
            time.sleep(delay)
