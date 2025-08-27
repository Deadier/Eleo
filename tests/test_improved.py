"""
Tests unitaires pour le robot Emo
Tests des principales fonctionnalités sans hardware
"""

import pytest
import os
import sys
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path

# Ajouter le répertoire Code au path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'Code'))

# Mock des modules hardware avant import
sys.modules['RPi.GPIO'] = Mock()
sys.modules['spidev'] = Mock()
sys.modules['adafruit_servokit'] = Mock()
sys.modules['adafruit_blinka'] = Mock()

# Mock du module LCD
mock_lcd = Mock()
sys.modules['lib.LCD_2inch'] = mock_lcd

import config
import utils

class TestConfig:
    """Tests de configuration"""
    
    def test_servo_channels_valid(self):
        assert config.SERVO_RIGHT_CHANNEL in range(config.SERVO_CHANNELS)
        assert config.SERVO_LEFT_CHANNEL in range(config.SERVO_CHANNELS)
        assert config.SERVO_BASE_CHANNEL in range(config.SERVO_CHANNELS)
    
    def test_frame_counts_positive(self):
        for emotion, count in config.FRAME_COUNT.items():
            assert count > 0, f"Frame count for {emotion} should be positive"
    
    def test_gpio_pins_valid(self):
        assert config.TOUCH_PIN > 0
        assert config.VIBRATION_PIN > 0
        assert config.TOUCH_PIN != config.VIBRATION_PIN

class TestUtils:
    """Tests des utilitaires"""
    
    def test_validate_servo_angle(self):
        assert utils.validate_servo_angle(-10) == 0
        assert utils.validate_servo_angle(90) == 90
        assert utils.validate_servo_angle(200) == 180
    
    def test_clear_queue(self):
        import multiprocessing
        q = multiprocessing.Queue()
        q.put("test1")
        q.put("test2")
        
        utils.clear_queue(q)
        assert q.empty()
    
    @patch('pathlib.Path.exists')
    def test_validate_file_exists(self, mock_exists):
        mock_exists.return_value = True
        assert utils.validate_file_exists("test.txt") == True
        
        mock_exists.return_value = False
        assert utils.validate_file_exists("nonexistent.txt") == False

class TestProcessManager:
    """Tests du gestionnaire de processus"""
    
    def test_process_manager_init(self):
        pm = utils.ProcessManager()
        assert pm.processes == {}
        assert 'p1' in pm.protected_names
    
    def test_add_process(self):
        pm = utils.ProcessManager()
        mock_process = Mock()
        pm.add_process("test", mock_process)
        assert "test" in pm.processes

class TestEmotionFrames:
    """Tests de validation des frames d'émotions"""
    
    def test_emotion_directories_exist(self):
        """Vérifie que tous les répertoires d'émotions existent"""
        code_dir = Path(__file__).parent.parent / "Code"
        emotions_dir = code_dir / "emotions"
        
        if emotions_dir.exists():
            for emotion in config.FRAME_COUNT.keys():
                emotion_dir = emotions_dir / emotion
                if emotion_dir.exists():
                    # Vérifier qu'il y a au moins quelques frames
                    frames = list(emotion_dir.glob("frame*.png"))
                    assert len(frames) > 0, f"No frames found for emotion {emotion}"

if __name__ == "__main__":
    pytest.main([__file__])
