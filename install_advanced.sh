#!/bin/bash
# Script d'installation et de configuration pour Emo Robot avancé

echo "🤖 Installation d'Emo Robot - Version avancée"
echo "============================================="

# Vérification des privilèges
if [ "$EUID" -ne 0 ]; then
    echo "❌ Ce script doit être exécuté avec sudo"
    exit 1
fi

# Mise à jour du système
echo "📦 Mise à jour du système..."
apt update && apt upgrade -y

# Installation des dépendances système
echo "🔧 Installation des dépendances système..."
apt install -y \
    python3-pip \
    python3-venv \
    git \
    alsa-utils \
    espeak \
    espeak-data \
    libespeak1 \
    portaudio19-dev \
    python3-pyaudio \
    flac \
    sox \
    libsox-fmt-all \
    python3-dev \
    libasound2-dev \
    build-essential

# Configuration audio
echo "🔊 Configuration audio..."
# Activer l'audio par défaut
amixer set PCM 100%
amixer set Master 100%

# Configuration des permissions GPIO
echo "⚡ Configuration des permissions GPIO..."
usermod -a -G gpio pi
usermod -a -G audio pi

# Création de l'environnement virtuel Python
echo "🐍 Création de l'environnement Python..."
VENV_PATH="/home/pi/emo_env"
python3 -m venv $VENV_PATH
source $VENV_PATH/bin/activate

# Installation des dépendances Python
echo "📚 Installation des dépendances Python..."
pip install --upgrade pip setuptools wheel

# Installation des dépendances depuis requirements.txt
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
else
    echo "❌ Fichier requirements.txt non trouvé"
    exit 1
fi

# Configuration du démarrage automatique
echo "🚀 Configuration du démarrage automatique..."
cat > /etc/systemd/system/emo-robot.service << EOF
[Unit]
Description=Emo Robot Advanced
After=network.target sound.target
Wants=network.target

[Service]
Type=simple
User=pi
Group=pi
WorkingDirectory=/home/pi/Eleo/Code
Environment=PATH=$VENV_PATH/bin:/usr/local/bin:/usr/bin:/bin
ExecStart=$VENV_PATH/bin/python advanced_emo.py
Restart=always
RestartSec=5
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF

# Activation du service
systemctl daemon-reload
systemctl enable emo-robot.service

# Configuration de l'I2C et SPI
echo "🔌 Configuration I2C et SPI..."
raspi-config nonint do_i2c 0
raspi-config nonint do_spi 0

# Configuration du microphone
echo "🎤 Configuration du microphone..."
# Ajouter la configuration audio pour USB
if ! grep -q "snd_bcm2835" /etc/modules; then
    echo "snd_bcm2835" >> /etc/modules
fi

# Créer le fichier de configuration audio
cat > /home/pi/.asoundrc << EOF
pcm.!default {
    type asym
    playback.pcm "plughw:0,0"
    capture.pcm "plughw:1,0"
}
ctl.!default {
    type hw
    card 0
}
EOF

# Configuration des logs
echo "📝 Configuration des logs..."
mkdir -p /var/log/emo-robot
chown pi:pi /var/log/emo-robot

# Configuration logrotate
cat > /etc/logrotate.d/emo-robot << EOF
/var/log/emo-robot/*.log {
    daily
    missingok
    rotate 7
    compress
    delaycompress
    notifempty
    create 644 pi pi
}
EOF

# Test de la configuration
echo "🧪 Test de la configuration..."
sudo -u pi $VENV_PATH/bin/python -c "
import sys
try:
    import speech_recognition
    import pyttsx3
    import RPi.GPIO
    import adafruit_servokit
    print('✅ Toutes les dépendances principales sont installées')
except ImportError as e:
    print(f'❌ Dépendance manquante: {e}')
    sys.exit(1)
"

# Création des répertoires nécessaires
echo "📁 Création des répertoires..."
mkdir -p /home/pi/Eleo/logs
mkdir -p /home/pi/Eleo/backups
mkdir -p /home/pi/Eleo/updates
chown -R pi:pi /home/pi/Eleo

# Configuration du firewall (optionnel pour l'interface web future)
echo "🔒 Configuration réseau..."
ufw allow 8080/tcp  # Pour l'interface web future
ufw --force enable

echo ""
echo "✅ Installation terminée!"
echo ""
echo "🎯 Prochaines étapes:"
echo "1. Redémarrez le Raspberry Pi: sudo reboot"
echo "2. Le robot démarrera automatiquement au boot"
echo "3. Vérifiez les logs: journalctl -u emo-robot.service -f"
echo "4. Pour arrêter: sudo systemctl stop emo-robot.service"
echo "5. Pour démarrer manuellement: sudo systemctl start emo-robot.service"
echo ""
echo "📋 Commandes utiles:"
echo "- État du service: sudo systemctl status emo-robot.service"
echo "- Logs en temps réel: journalctl -u emo-robot.service -f"
echo "- Redémarrer le service: sudo systemctl restart emo-robot.service"
echo ""
echo "🔧 Dépannage:"
echo "- Vérifiez le microphone: arecord -l"
echo "- Testez l'audio: speaker-test -t sine -f 1000 -l 1"
echo "- Vérifiez I2C: i2cdetect -y 1"
echo "- Vérifiez SPI: ls /dev/spi*"
echo ""
echo "🎉 Emo Robot est prêt!"
