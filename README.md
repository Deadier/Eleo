# Emo - Votre robot compagnon personnel

## Description
Emo est un robot compagnon avancé, conçu pour interagir avec les humains à travers des mouvements physiques, des réponses vocales, et des expressions faciales dynamiques affichées sur un écran LCD. Inspiré par le projet original disponible sur [CodersCafeTech/Emo](https://github.com/CodersCafeTech/Emo), ce fork vise à explorer et étendre les interactions homme-machine de manière intuitive et engageante.

## Fonctionnalités
- **Interactions tactiles** : Réagit au toucher grâce à des capteurs intégrés pour une interaction intuitive.
- **Sortie audio** : Utilise un amplificateur PAM8403 pour émettre des réponses sonores et parler avec l'utilisateur.
- **Mouvements servomoteurs** : Effectue des gestes et expressions via plusieurs servomoteurs, permettant une gamme de mouvements fluides et expressifs.
- **Affichage LCD expressif** : Montre des émotions ou des informations via un écran LCD, rendant Emo visuellement expressif et communicatif.
- **Reconnaissance vocale** : Capable de comprendre et de répondre aux commandes vocales, facilitant une interaction naturelle et mains libres.

## Matériel nécessaire
- Raspberry Pi (Modèle 3B+ ou supérieur recommandé)
- Écran LCD 2,4 pouces
- Capteur tactile TTP223
- Amplificateur PAM8403 et haut-parleur
- Servomoteurs et contrôleur de servomoteur
- Câbles de connexion et breadboard

## Installation
### Configuration matérielle
Suivez les schémas de câblage fournis dans le dossier `diagrams` pour connecter tous les composants électroniques au Raspberry Pi.

### Configuration logicielle
 1. Clonez ce dépôt sur votre Raspberry Pi :

>     git clone https://github.com/Deadier/Elo.git

 2. Installez les dépendances nécessaires :

>     pip install adafruit-circuitpython-servokit RPi.GPIO spidev pillow

 3. Exécutez le script principal pour démarrer le robot :

>     python3 main.py

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
