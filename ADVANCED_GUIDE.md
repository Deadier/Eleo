# 🤖 Guide d'utilisation - Emo Robot Avancé

## 🚀 Vue d'ensemble des nouvelles fonctionnalités

Votre robot Emo dispose maintenant de toutes les fonctionnalités avancées mentionnées dans le README :

### ✨ Fonctionnalités principales
- 🎤 **Reconnaissance vocale** - Commandes vocales en français
- 🔊 **Synthèse vocale** - Le robot vous parle
- 🎮 **5 jeux interactifs** - Divertissement intelligent
- 📱 **Affichage avancé** - Menus, scores, animations
- 🔋 **Gestion de batterie** - Surveillance et alertes
- ⚙️ **Contrôles avancés** - Volume, luminosité

## 🎤 Commandes vocales disponibles

### Salutations
- "Bonjour" / "Salut" / "Hello" → Réponse amicale

### Contrôle des émotions
- "Content" / "Heureux" → Expression joyeuse
- "Triste" → Expression triste  
- "En colère" / "Colère" → Expression de colère
- "Excité" → Expression d'excitation

### Jeux interactifs
- "Jeu" → Active le mode jeu et liste les options
- "Danse" → Jeu "Dance to the Beat"
- "Perroquet" → Mode perroquet (répète vos paroles)
- "Marionnette" → Mode marionnette (contrôle manuel)

### Contrôles système
- "Volume plus" / "Volume moins" → Ajuste le volume
- "Luminosité plus" / "Luminosité moins" → Ajuste l'écran
- "Arrêt" / "Stop" → Retour au mode normal

## 🎮 Jeux interactifs détaillés

### 1. 🎯 Left or Right Game
**Activation :** Dites "jeu" puis "gauche droite"
- Jeu de mémoire où Emo cache un objet
- Devinez sous quel "verre" il est caché
- 5 manches avec score final
- Répondez par "gauche" ou "droite"

### 2. 💃 Dance to the Beat  
**Activation :** Dites "danse"
- Applaudissez et Emo dansera sur votre rythme
- Plus vous applaudissez fort, plus il danse énergiquement
- Session de 30 secondes de danse interactive

### 3. 🎯 Shooting Game
**Activation :** Dites "jeu" puis "tir"
- Des cibles apparaissent sur l'écran
- Touchez l'écran tactile pour les viser
- 10 cibles à toucher avec calcul de précision

### 4. 🦜 Mode Perroquet
**Activation :** Dites "perroquet"
- Emo répète tout ce que vous dites
- Parfait pour s'amuser ou tester la reconnaissance vocale
- Dites "arrêt" pour quitter

### 5. 🎭 Mode Marionnette  
**Activation :** Dites "marionnette"
- Contrôlez les expressions d'Emo par la voix
- Commandes disponibles : "content", "triste", "colère", "excité", "neutre"
- Mode idéal pour les démonstrations

## 📱 Interface d'affichage avancée

### Types d'affichage
- **Émotions animées** - Animations fluides haute qualité
- **Menus interactifs** - Navigation par commandes vocales
- **Scores de jeux** - Affichage des résultats avec barres de progression
- **État système** - Batterie, volume, luminosité
- **Messages texte** - Notifications et instructions

### Contrôles de luminosité
- Réglage de 10% à 100% par paliers de 10%
- Commande vocale : "Luminosité plus/moins"
- Adaptation automatique selon l'environnement

## 🔋 Gestion de la batterie

### Surveillance automatique
- Décharge simulée progressive
- Alertes vocales à 20% et 10%
- Affichage visuel du niveau sur l'écran

### États de batterie
- **100-50%** : Fonctionnement normal (vert)
- **49-20%** : Fonctionnement réduit (orange)  
- **19-10%** : Mode économie (rouge)
- **<10%** : Arrêt automatique recommandé

## 🎛️ Modes de fonctionnement

### Mode Normal (par défaut)
- Réactions aux capteurs tactiles et de vibration
- Animations neutres périodiques
- Réponse aux commandes vocales de base

### Mode Jeu
- Accès à tous les jeux interactifs
- Interface dédiée avec scores
- Commandes vocales étendues

### Mode Vocal
- Reconnaissance vocale continue
- Réponses conversationnelles
- Contrôle total par la voix

### Mode Démonstration
- Cycle automatique des émotions
- Parfait pour les présentations
- Pas d'interaction utilisateur

## 🚨 Dépannage et maintenance

### Problèmes courants

#### Le robot ne répond pas aux commandes vocales
- Vérifiez le microphone : `arecord -l`
- Testez l'enregistrement : `arecord -d 3 test.wav`
- Redémarrez le service : `sudo systemctl restart emo-robot.service`

#### Pas de son
- Vérifiez l'audio : `speaker-test -t sine -f 1000 -l 1`
- Ajustez le volume : `alsamixer`
- Vérifiez les connexions du haut-parleur

#### Écran noir
- Vérifiez les connexions SPI : `ls /dev/spi*`
- Redémarrez le système : `sudo reboot`
- Vérifiez les logs : `journalctl -u emo-robot.service -f`

#### Servomoteurs ne bougent pas
- Vérifiez I2C : `i2cdetect -y 1`
- Vérifiez l'alimentation des servos
- Testez les connexions du PCA9685

### Logs et diagnostic

#### Consulter les logs
```bash
# Logs en temps réel
journalctl -u emo-robot.service -f

# Logs récents
journalctl -u emo-robot.service -n 50

# Logs avec erreurs seulement
journalctl -u emo-robot.service -p err
```

#### Fichiers de configuration
- Service : `/etc/systemd/system/emo-robot.service`
- Audio : `/home/pi/.asoundrc`
- Logs : `/var/log/emo-robot/`

### Maintenance préventive

#### Quotidienne
- Vérifiez l'état de la batterie
- Nettoyez l'écran LCD délicatement
- Vérifiez les connexions libres

#### Hebdomadaire  
- Redémarrage complet du système
- Vérification des logs d'erreur
- Test de toutes les fonctionnalités

#### Mensuelle
- Sauvegarde de la configuration
- Mise à jour du système
- Nettoyage des fichiers temporaires

## 🔧 Personnalisation avancée

### Ajouter de nouvelles commandes vocales
1. Éditez `voice_manager.py`
2. Ajoutez vos mots-clés dans `VOICE_COMMANDS`
3. Implémentez les fonctions correspondantes dans `advanced_emo.py`

### Créer de nouvelles émotions
1. Ajoutez les frames PNG dans `emotions/[nom_emotion]/`
2. Mettez à jour `FRAME_COUNT` dans `config.py`
3. Ajoutez le fichier son dans `sound/[nom_emotion].wav`

### Modifier les mouvements
1. Éditez les fonctions de mouvement dans `advanced_emo.py`
2. Ajustez les angles et timings selon vos besoins
3. Testez avec précaution pour éviter les blocages mécaniques

## 📊 Statistiques et monitoring

### Métriques collectées
- Temps de fonctionnement
- Commandes vocales reconnues
- Jeux joués et scores
- Erreurs système

### Monitoring en temps réel
```bash
# CPU et mémoire
htop

# Température
vcgencmd measure_temp

# Utilisation disque
df -h

# État des services
systemctl status emo-robot.service
```

## 🌐 Fonctionnalités futures

### Interface web (en développement)
- Contrôle à distance via navigateur
- Configuration avancée
- Historique des interactions
- Mise à jour OTA (Over-The-Air)

### Extensions possibles
- Reconnaissance faciale
- Contrôle par gestures
- Intégration IoT (smart home)
- Mode multi-utilisateurs
- API REST complète

## 📞 Support et communauté

### Ressources
- Documentation technique dans `/docs/`
- Exemples de code dans `/examples/`  
- Tests dans `/tests/`

### Contribution
1. Fork du repository GitHub
2. Créez votre branche feature
3. Testez vos modifications
4. Soumettez une Pull Request

---

🎉 **Amusez-vous bien avec votre Emo Robot avancé !**

Pour toute question ou suggestion d'amélioration, n'hésitez pas à ouvrir une issue sur GitHub.
