# YouTube MP3 Downloader

Script Python pour télécharger des vidéos YouTube en MP3 à partir d'un fichier texte contenant des liens.

## Prérequis
- **Python 3.8+** : Assurez-vous que Python est installé sur votre système. Téléchargez-le depuis [python.org](https://www.python.org/downloads/) si nécessaire.
- **FFmpeg** : Les binaires FFmpeg doivent être placés manuellement dans le dossier `ffmpeg/` (voir instructions ci-dessous).
- Un environnement virtuel (venv) est recommandé pour gérer les dépendances.

## Installation

- `git clone <URL_DU_DEPOT>`
- `cd python_ytb_mp3_download`
- `python -m venv venv`
- `.\venv\Scripts\activate  # Sur Windows`
- `source venv/bin/activate # Sur macOS/Linux`
- `pip install -r requirements.txt`
- `python dl.py`
