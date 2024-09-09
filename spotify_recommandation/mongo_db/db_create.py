import json
import os
from pymongo import MongoClient
import numpy as np

# Connexion à MongoDB
client = MongoClient(
    host = "127.0.0.1",
    port = 27017,
    username = "root",
    password = "antoine"
)

db = client['spotify']

# Créer les collections
playlists_collection = db['playlists']
tracks_collection = db['tracks']
link_data_collection = db['link_data']

# Chemin vers le dossier contenant les fichiers JSON
json_directory = '/home/antoine/spotify/spotify_recommandation/mongo_db/sample_training'

# Parcourir tous les fichiers JSON dans le répertoire
for filename in os.listdir(json_directory):
    if filename.endswith('.json'):
        with open(os.path.join(json_directory, filename), 'r') as file:
            playlists = json.load(file)
            for playlist in playlists['playlists']:
                # Insérer les données de la playlist
                playlist_data = {
                    "pid": playlist.get('pid', None),
                    "name": playlist.get('name', None),
                    "description" : playlist.get("description", None),
                    "num_artists": playlist.get('num_artists', np.NaN),
                    "num_albums": playlist.get('num_albums', np.NaN),
                    "num_tracks": playlist.get('num_tracks', np.NaN),
                    "num_followers": playlist.get('num_followers', np.NaN),
                    "duration_ms": playlist.get('duration_ms', np.NaN),
                    "collaborative": playlist.get('collaborative', None)
                }
                playlists_collection.insert_one(playlist_data)

                # Insérer les données des pistes
                for track in playlist.get('tracks', []):
                    track_data = {
                        "track_id": f"{playlist['pid']}_{track['pos']}",  # ID unique pour la piste
                        "pid": playlist.get('pid', None),
                        "pos": track.get('pos', None),
                        "track_name": track.get('track_name', None),
                        "artist_name": track.get('artist_name', None),
                        "album_name": track.get('album_name', None),
                        "duration_ms": track.get('duration_ms', np.NaN)
                    }
                    tracks_collection.insert_one(track_data)

                    # Insérer les données de lien
                    link_data = {
                        "track_id": track.get('track_id', None),
                        "track_uri": track.get('track_uri', None),
                        "artist_uri": track.get('artist_uri', None),
                        "album_uri": track.get('album_uri', None)
                    }
                    link_data_collection.insert_one(link_data)

print("Données importées avec succès !")