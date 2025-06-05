import importlib.util
import os
import sys
import types
from pathlib import Path

def load_frame_count():
    """Import frame_count from Code/final.py with stubbed dependencies."""
    # Create stub modules for hardware-specific dependencies
    stubs = {}
    if 'board' not in sys.modules:
        board = types.ModuleType('board')
        board.SCL = None
        board.SDA = None
        stubs['board'] = board
        sys.modules['board'] = board
    if 'busio' not in sys.modules:
        busio = types.ModuleType('busio')
        stubs['busio'] = busio
        sys.modules['busio'] = busio
    if 'adafruit_servokit' not in sys.modules:
        servokit = types.ModuleType('adafruit_servokit')
        class DummyServo:
            def __init__(self):
                self.angle = 0
        class DummyKit:
            def __init__(self, channels=16):
                self.servo = [DummyServo() for _ in range(channels)]
        servokit.ServoKit = DummyKit
        stubs['adafruit_servokit'] = servokit
        sys.modules['adafruit_servokit'] = servokit
    if 'RPi' not in sys.modules:
        rpi = types.ModuleType('RPi')
        gpio = types.ModuleType('GPIO')
        gpio.BCM = gpio.IN = gpio.HIGH = 0
        gpio.setmode = lambda *a, **k: None
        gpio.setup = lambda *a, **k: None
        gpio.input = lambda *a, **k: 0
        rpi.GPIO = gpio
        stubs['RPi'] = rpi
        stubs['RPi.GPIO'] = gpio
        sys.modules['RPi'] = rpi
        sys.modules['RPi.GPIO'] = gpio
    if 'spidev' not in sys.modules:
        spidev = types.ModuleType('spidev')
        stubs['spidev'] = spidev
        sys.modules['spidev'] = spidev
    if 'lib' not in sys.modules:
        sys.modules['lib'] = types.ModuleType('lib')
    if 'lib.LCD_2inch' not in sys.modules:
        lcd_mod = types.ModuleType('LCD_2inch')
        class DummyLCD:
            def Init(self):
                pass
            def ShowImage(self, *a, **k):
                pass
            def module_exit(self):
                pass
        lcd_mod.LCD_2inch = DummyLCD
        stubs['lib.LCD_2inch'] = lcd_mod
        sys.modules['lib.LCD_2inch'] = lcd_mod
    for name in ['PIL', 'PIL.Image', 'PIL.ImageDraw', 'PIL.ImageFont']:
        if name not in sys.modules:
            mod = types.ModuleType(name.split('.')[-1])
            stubs[name] = mod
            sys.modules[name] = mod
    # Load the module from file
    final_path = Path(__file__).resolve().parents[1] / 'Code' / 'final.py'
    spec = importlib.util.spec_from_file_location('final', final_path)
    final = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(final)
    return final.frame_count

def test_emotion_frame_counts():
    frame_count = load_frame_count()
    base = Path(__file__).resolve().parents[1] / 'Code' / 'emotions'
    for emotion, expected in frame_count.items():
        emotion_dir = base / emotion
        files = [f for f in emotion_dir.iterdir() if f.is_file()]
        assert len(files) == expected, f"{emotion} should have {expected} frames"
