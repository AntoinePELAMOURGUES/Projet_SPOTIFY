import json
import os
from pymongo import MongoClient
import pandas as pd

client = MongoClient(
    host = "127.0.0.1",
    port = 27017,
    username = "root",
    password = "antoine"
)

db = client['global_spotify_data']

track = db['track']

#  Récupérer les données
documents = list(track.find())  # Récupère tous les documents de la collection

# Convertir en DataFrame
df = pd.DataFrame(documents)

# Supprimer la colonne '_id' si elle n'est pas nécessaire
if '_id' in df.columns:
    df.drop('_id', axis=1, inplace=True)

path = '/home/antoine/spotify/data/processed/global_df.csv'

df.to_csv(path)

