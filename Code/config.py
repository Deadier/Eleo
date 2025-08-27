"""
Configuration du robot Emo
Centralise tous les paramètres de configuration
"""

# Configuration des broches GPIO
TOUCH_PIN = 17
VIBRATION_PIN = 22

# Configuration de l'écran LCD
RST = 27
DC = 25
BL = 18
SPI_BUS = 0
SPI_DEVICE = 0

# Configuration des servomoteurs
SERVO_CHANNELS = 16
SERVO_RIGHT_CHANNEL = 5   # Bras droit (référence 0°)
SERVO_LEFT_CHANNEL = 11   # Bras gauche (référence 180°)
SERVO_BASE_CHANNEL = 13   # Base rotation (référence 90°)

# Positions des servomoteurs
SERVO_POSITIONS = {
    'RIGHT_MIN': 0,
    'RIGHT_MID': 90,
    'RIGHT_MAX': 180,
    'LEFT_MIN': 0, 
    'LEFT_MID': 90,
    'LEFT_MAX': 180,
    'BASE_MIN': 0,
    'BASE_MID': 90,
    'BASE_MAX': 180
}

# Configuration des émotions
FRAME_COUNT = {
    'blink': 39, 
    'happy': 45, 
    'sad': 47,
    'dizzy': 67,
    'excited': 24,
    'neutral': 61,
    'happy2': 20,
    'angry': 20,
    'happy3': 26,
    'bootup3': 124,
    'blink2': 20
}

# Émotions disponibles
EMOTION_TYPES = {
    'TRIGGERED': ['angry', 'sad', 'excited'],
    'NORMAL': ['neutral', 'blink2']
}

# Timing et délais
SENSOR_POLL_DELAY = 0.05  # Délai de lecture des capteurs (50ms)
PROCESS_TIMEOUT = 1.0     # Timeout pour terminer les processus
ANIMATION_SPEED = {
    'FAST': 0.004,
    'MEDIUM': 0.01,
    'SLOW': 0.02
}

# Chemins des fichiers
EMOTIONS_DIR = "emotions"
SOUNDS_DIR = "sound"
LIB_DIR = "lib"
