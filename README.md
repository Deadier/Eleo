# Emo - Votre robot compagnon personnel

## Description
Emo est un robot compagnon avancé, conçu pour interagir avec les humains à travers des mouvements physiques, des réponses vocales, et des expressions faciales dynamiques affichées sur un écran LCD. Inspiré par le projet original disponible sur [CodersCafeTech/Emo](https://github.com/CodersCafeTech/Emo), ce fork vise à explorer et étendre les interactions homme-machine de manière intuitive et engageante.

## Fonctionnalités
- **Interactions tactiles** : Réagit au toucher grâce à des capteurs intégrés pour une interaction intuitive.
- **Détection de vibration** : Intègre un capteur de vibration pour détecter les interactions physiques et les mouvements environnants.
- **Sortie audio** : Utilise un amplificateur PAM8403 pour émettre des réponses sonores et parler avec l'utilisateur.
- **Mouvements servomoteurs** : Effectue des gestes et expressions via plusieurs servomoteurs, permettant une gamme de mouvements fluides et expressifs.
- **Affichage LCD expressif** : Montre des émotions ou des informations via un écran LCD, rendant Emo visuellement expressif et communicatif.
- **Reconnaissance vocale** : Capable de comprendre et de répondre aux commandes vocales, facilitant une interaction naturelle et mains libres.
- **Feedback vibratoire** : Le robot vibre lorsqu'il est touché à certains endroits, ajoutant une dimension sensorielle à l'interaction.
- **Réactions émotionnelles** : Capable de pleurer, de se mettre en colère, de montrer de la tristesse, du bonheur, etc.
- **Jeux interactifs** :
  - **Left or Right Game** : Jeu de mémoire où il faut deviner l'objet caché sous un verre.
  - **Dance to the Beat** : Jeu où Emo danse en fonction du rythme des applaudissements.
  - **Shooting Game** : Jeu de tir où il faut toucher des cibles à l'écran.
  - **Parrot Mode** : Emo répète ce que l'utilisateur dit.
  - **Puppet Mode** : Permet de manipuler les expressions de Emo.
- **Affichage et animations de haute qualité** : Affiche des animations de haute qualité et permet de régler le volume et la luminosité de l'écran.
- **Batterie rechargeable** : Autonomie d'environ une heure et demie avec une interaction continue et temps de recharge rapide d'environ 30 minutes.
- **Mises à jour logicielles** : Mise à jour du firmware via Windows avec l'ajout de nouvelles animations et fonctionnalités via des mises à jour.

## Matériel nécessaire

### Composants électroniques

1.  **1 Raspberry Pi** (Modèle 3B+ ou supérieur recommandé)
2.  **1 écran LCD 2,4 pouces** - Modèle WaveShare IPS recommandé
3.  **3 capteurs tactile TTP223**
   -   **Capteur de tête** : Détecte les touchers sur la tête.
   - **Capteur de dos** : Réagit aux touchers sur le dos.
   - **Capteur de ventre** : Sensible aux touchers sur le ventre.
4.  **1 capteur de vibration SW-420**
5. **Capteur de fond** : Détecte quand le robot est soulevé.
6.  **1 amplificateur PAM8403**
7.  **1 haut-parleur** - 18,5 watts recommandé
8.  **Servomoteurs** :
    -   2 servomoteurs SG90 pour les bras
    -   1 servomoteur MG90S pour la rotation du corps
9.  **1 contrôleur de servomoteur PCA9685PW**
10.  **Câbles de connexion** et **breadboard**
11.  **Module micro USB** pour l'alimentation

### Matériel d'impression 3D

1.  **Imprimante 3D** - Pour imprimer les pièces du robot
2.  **Filament PLA** - Couleurs bleu et blanc recommandées
3.  **Vis M3 (10 mm et 15 mm)**

### Outils supplémentaires

1.  **Colle forte** - Pour fixer certains composants
2.  **Tournevis** - Pour les vis M3
3.  **Multimètre** - Pour vérifier les connexions électriques
4.  **Fer à souder** - Si nécessaire pour certaines connexions



## Installation
### Préparation du Raspberry Pi

#### Installation de l'OS avec Raspberry Pi Imager
1. **Téléchargez et installez Raspberry Pi Imager** depuis [Raspberry Pi Software](https://www.raspberrypi.com/software/).
2. **Ouvrez Raspberry Pi Imager** et choisissez l'OS recommandé (Raspberry Pi OS Full).
3. **Sélectionnez la carte SD** sur laquelle l'OS sera installé.
4. **Cliquez sur 'WRITE'** pour flasher la carte SD avec l'OS.

#### Activation du SSH
Pour activer le SSH sans accéder à l'interface graphique du Raspberry Pi:
1. **Placez la carte SD** dans votre ordinateur.
2. **Naviguez vers la partition 'boot'** de la carte SD.
3. **Créez un fichier vide nommé 'ssh'** sans extension dans le répertoire racine.

#### Connexion au Raspberry Pi via SSH avec PuTTY
1. **Téléchargez et installez PuTTY** depuis [PuTTY Download Page](https://www.putty.org/).
2. **Trouvez l'adresse IP du Raspberry Pi** :
   - Connectez votre Raspberry Pi à votre réseau local via Ethernet ou Wi-Fi.
   - Utilisez votre routeur ou un scanner de réseau pour trouver l'adresse IP attribuée à votre Raspberry Pi.
3. **Ouvrez PuTTY** et entrez l'adresse IP du Raspberry Pi dans le champ 'Host Name (or IP address)'.
4. **Cliquez sur 'Open'** pour établir une connexion SSH.
   - Si demandé, acceptez la clé de l'hôte en cliquant sur 'Yes'.
   - Connectez-vous en utilisant le nom d'utilisateur par défaut (`pi`) et le mot de passe par défaut (`raspberry`).

#### Mise à jour du système
Pour vous assurer que votre système d'exploitation est à jour:
1. **Mettez à jour la liste des paquets** :

>     sudo apt update

2. **Effectuez une mise à niveau complète** :
>     sudo apt full-upgrade

5. **Redémarrage** : Redémarrez votre Raspberry Pi pour appliquer les mises à jour avec
>     sudo reboot

### Configuration matérielle
Suivez les schémas de câblage fournis dans le dossier `Circuit` pour connecter tous les composants électroniques au Raspberry Pi.

### Configuration logicielle
 1. Clonez ce dépôt sur votre Raspberry Pi :

>     git clone https://github.com/Deadier/Eleo.git

 3. Installez les dépendances nécessaires :

Installation des paquets disponibles via apt
>     sudo apt install python3-numpy python3-pil python3-rpi.gpio python3-spidev

Installation des paquets non disponibles via apt avec pip
>     pip install adafruit-circuitpython-servokit --break-system-packages

 4. Exécutez le script principal pour démarrer le robot :

>     python3 <path/to/your/project>/Code/final.py

## Instructions de montage pour le robot Emo

### Préparation et impression 3D

-   **Impression des pièces**: Divisez le robot en plusieurs segments pour simplifier l'assemblage. Imprimez la base avec un taux de remplissage de 40 % pour garantir sa robustesse. Les autres composants doivent être imprimés avec un taux de remplissage de 20 % pour optimiser la résistance et l'économie de matériel.

### Assemblage de la base

-   **Installation électrique**: Commencez par installer le module micro USB dans la partie basse pour alimenter le robot. Placez à proximité le capteur de vibrations SW-420 pour qu'il puisse détecter efficacement les vibrations.
-   **Fixation du couvercle**: Utilisez des vis M3 de 10 mm pour attacher solidement le couvercle à la base.

### Configuration des capteurs et de l'affichage

-   **Capteur tactile**: Intégrez un capteur tactile capacitatif dans la tête du robot. Sa petite taille permet une installation discrète et efficace.
-   **Installation de l'écran**: Installez un écran IPS de 2 pouces de chez WaveShare pour afficher les expressions du robot. Fixez l'écran avec des supports noirs et sécurisez-le avec un peu de colle forte pour éviter tout mouvement lors de l'utilisation.

### Montage des servomoteurs et installation audio

-   **Installation des haut-parleurs**: Montez un haut-parleur de 18,5 watts sur le côté de la tête pour la diffusion du son. Amplifiez le signal audio provenant du Raspberry Pi avec un amplificateur PAM8403.
-   **Servomoteurs**: Placez trois servomoteurs – deux SD9D pour les bras et un Engin ID pour la rotation du corps. Utilisez un contrôleur PC9685 pour une gestion aisée des servomoteurs.

### Assemblage final et tests

-   **Assemblage de la tête et du corps**: Fixez la tête au corps à l'aide de vis M3 de 15 mm. Assurez-vous que toutes les parties sont correctement alignées et sécurisées.
-   **Tests de fonctionnalité**: Avant de finaliser l'assemblage, testez toutes les composantes électriques et mécaniques pour vous assurer qu'elles fonctionnent correctement. Vérifiez les connexions et les réponses du robot aux commandes.

### Conseils d'utilisation et de maintenance

-   **Interaction douce**: Emo est sensible aux interactions. Évitez les tapotements excessifs qui pourraient l'affecter émotionnellement. Privilégiez des caresses légères pour maintenir son bien-être.

## Programmation des interactions
Pour programmer Emo afin qu'il réponde aux commandes vocales et suive les mouvements, consultez le dossier `Code` qui contient des exemples de code pour intégrer la reconnaissance vocale et le suivi de mouvement.

## Attributions des sons

Les effets sonores utilisés pour les émotions d'Emo sont sous licence Creative Commons 0 (CC0) et proviennent de Freesound. Voici les attributions spécifiques pour chaque émotion :

- **Angry**: Son par kanyonwyvern, disponible sur [Freesound](https://freesound.org/people/kanyonwyvern/sounds/713755/).
- **Blink**: Son par newagesoup, disponible sur [Freesound](https://freesound.org/people/newagesoup/sounds/350359/).
- **Dizzy**: Son par martian, disponible sur [Freesound](https://freesound.org/people/martian/sounds/403002/).
- **Excited**: Son par dersuperanton, disponible sur [Freesound](https://freesound.org/people/dersuperanton/sounds/436168/).
- **Happy**: Son par SergeQuadrado, disponible sur [Freesound](https://freesound.org/people/SergeQuadrado/sounds/636955/).
- **Sad**: Son par SergeQuadrado, disponible sur [Freesound](https://freesound.org/people/SergeQuadrado/sounds/636956/).
- **Sleep**: Son par bsmacbride, disponible sur [Freesound](https://freesound.org/people/bsmacbride/sounds/108517/).

Ces sons ont été choisis pour enrichir l'expérience interactive avec Emo, en lui permettant de communiquer ses émotions de manière plus expressive.

## Fichiers STL
Les modèles 3D pour l'impression des composants du robot sont disponibles dans le dossier `3D Design/STL`. Ces fichiers permettent de personnaliser et de construire votre propre version d'Emo.

## Contribution
Les contributions à Emo sont toujours bienvenues. Que ce soit pour des corrections de bugs, des améliorations de fonctionnalités ou des suggestions de nouvelles idées, n'hésitez pas à créer une issue ou soumettre une pull request.

## Vidéo de présentation
Pour voir Emo en action, regardez la [vidéo de présentation](https://www.youtube.com/watch?v=3RIea8zPLhQ) sur YouTube.

## Licence
Ce projet est sous licence MIT - voir le fichier [LICENSE.md](LICENSE.md) pour les détails.

## Auteurs
- **Coder's Cafe** - *Travail initial* - [CodersCafeTech](https://github.com/CodersCafeTech/Emo)
- Contributions et améliorations par [Deadier](https://github.com/Deadier)

## Remerciements
- Merci à [CodersCafeTech](https://github.com/CodersCafeTech/Emo) pour le projet original qui a inspiré cette version.
- Un grand merci à [ChatGPT](https://chat.openai.com/) pour son aide précieuse dans l'amélioration de ce projet.
