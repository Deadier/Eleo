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

## Matériel nécessaire
- 1 raspberry Pi (Modèle 3B+ ou supérieur recommandé)
- 1 écran LCD 2,4 pouces
- 1 capteur tactile TTP223
- 1 capteur de vibration SW-420
- 1 amplificateur PAM8403
- 1 haut-parleur
- 2 servomoteurs SG90 pour les bras
- 1 servomoteur MG90S pour la rotation du corps
- 1 contrôleur de servomoteur PCA9685PW
- Câbles de connexion et breadboard

## Installation
### Préparation du Raspberry Pi
1. **Installation de l'OS** : Utilisez [Raspberry Pi Imager](https://www.raspberrypi.com/software/) pour installer le système d'exploitation Raspberry Pi OS sur une carte SD.
2. **Activation du SSH** : Pour activer le SSH, insérez la carte SD dans votre ordinateur, ouvrez le volume "boot" et créez un fichier vide nommé `ssh` sans extension.
3. **Connexion SSH** : Pour vous connecter à votre Raspberry Pi via SSH depuis un PC Windows, téléchargez et installez [PuTTY](https://www.putty.org/). Trouvez l'adresse IP de votre Raspberry Pi en consultant votre routeur ou en utilisant un outil de scan réseau comme Advanced IP Scanner.
4. **Mise à jour du système** : Connectez-vous à votre Raspberry Pi via SSH et exécutez les commandes suivantes pour mettre à jour votre système :

>     sudo apt update && sudo apt full-upgrade

5. **Redémarrage** : Redémarrez votre Raspberry Pi pour appliquer les mises à jour avec
>     sudo reboot

### Configuration matérielle
Suivez les schémas de câblage fournis dans le dossier `diagrams` pour connecter tous les composants électroniques au Raspberry Pi.

### Configuration logicielle
 1. Clonez ce dépôt sur votre Raspberry Pi :

>     git clone https://github.com/Deadier/Elo.git

 2. Installez les dépendances nécessaires :

>     pip install adafruit-circuitpython-servokit RPi.GPIO spidev pillow

 3. Exécutez le script principal pour démarrer le robot :

>     python3 main.py

## Instructions de montage pour le robot Emo

### Préparation et impression 3D

-   **Modélisation**: Employez des techniques de modélisation solide et de modélisation libre pour concevoir les différentes parties du robot. Cette méthode facilite l'impression 3D et assure la compatibilité des pièces.
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

## Fichiers STL
Les modèles 3D pour l'impression des composants du robot sont disponibles dans le dossier `3D Design/STL`. Ces fichiers permettent de personnaliser et de construire votre propre version d'Emo.

## Contribution
Les contributions à Emo sont toujours bienvenues. Que ce soit pour des corrections de bugs, des améliorations de fonctionnalités ou des suggestions de nouvelles idées, n'hésitez pas à créer une issue ou soumettre une pull request.

## Vidéo de présentation
Pour voir Emo en action, regardez la [vidéo de présentation](https://www.youtube.com/watch?v=3RIea8zPLhQ) sur YouTube.

## Licence
Ce projet est sous licence MIT - voir le fichier [LICENSE.md](LICENSE.md) pour les détails.

## Auteurs
- **Coder's Cafe** - *Travail initial* - [[CodersCafeTech](https://github.com/CodersCafeTech)/
-   [Emo](https://github.com/CodersCafeTech/Emo)]
- Contributions et améliorations par [Deadier](https://github.com/Deadier)

## Remerciements
- Merci à [CodersCafeTech](https://github.com/CodersCafeTech/Emo) pour le projet original qui a inspiré cette version.
- Un grand merci à [ChatGPT](https://chat.openai.com/) pour son aide précieuse dans l'amélioration de ce projet.
