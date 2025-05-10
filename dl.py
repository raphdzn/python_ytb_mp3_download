import os
import yt_dlp

def create_output_directory(output_dir="output"):
    """Crée le dossier de sortie s'il n'existe pas."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

def download_youtube_to_mp3(links_file, output_dir="output"):
    """Télécharge les vidéos YouTube en MP3 à partir d'un fichier texte."""
    # Obtenir le chemin absolu du dossier ffmpeg dans le projet
    script_dir = os.path.dirname(os.path.abspath(__file__))
    ffmpeg_path = os.path.join(script_dir, "ffmpeg")

    # Vérifier si les binaires FFmpeg existent
    if not os.path.exists(os.path.join(ffmpeg_path, "ffmpeg.exe")):
        raise FileNotFoundError("ffmpeg.exe introuvable dans le dossier ffmpeg. Assurez-vous qu'il est inclus dans le projet.")
    if not os.path.exists(os.path.join(ffmpeg_path, "ffprobe.exe")):
        raise FileNotFoundError("ffprobe.exe introuvable dans le dossier ffmpeg. Assurez-vous qu'il est inclus dans le projet.")

    # Options pour yt-dlp
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',
        }],
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
        'noplaylist': True,
        'ffmpeg_location': ffmpeg_path,  # Utilise le dossier ffmpeg local
    }

    # Lire les liens du fichier texte
    try:
        with open(links_file, 'r', encoding='utf-8') as file:
            links = [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print(f"Erreur : Le fichier {links_file} n'a pas été trouvé.")
        return
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier : {e}")
        return

    # Télécharger chaque lien
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        for link in links:
            try:
                print(f"Téléchargement de : {link}")
                ydl.download([link])
                print(f"Téléchargement terminé pour : {link}")
            except Exception as e:
                print(f"Erreur lors du téléchargement de {link} : {e}")

def main():
    # Créer le dossier output
    create_output_directory()
    
    # Nom du fichier contenant les liens
    links_file = "links.txt"
    
    # Lancer le téléchargement
    download_youtube_to_mp3(links_file)

if __name__ == "__main__":
    main()