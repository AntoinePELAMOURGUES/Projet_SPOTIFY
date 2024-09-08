from typing import Union
import requests
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/tokens/")
def recover_token():
    '''
    Fonction qui requête spotify afin d'obtenir notre token valable 1 heure
    '''
    url = "https://accounts.spotify.com/api/token"
    headers = {
    "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "client_credentials",
        "client_id": "7c0c251516b747ddb0ede65d713316a4",
        "client_secret": "baa3b9dad0904935940dcaafe7b5bfa6"
    }
    response = requests.post(url, headers=headers, data=data)
    # Check the response
    if response.status_code == 200:
        token_info = response.json()
        access_token = token_info['access_token']
        token_type = token_info['token_type']
        return access_token, token_type
    else:
        print("Error:", response.status_code, response.text)
        return None, None

@app.get("/artiste_info/{artist_uri}")
def spotify_info_artist(artist_uri : str):
    """
    Fonction qui requête spotify afin d'obtenir les informations sur l'artiste
    """
    # Récupération token et type_token
    access_token, type_token = recover_token()
    # URL spotify
    url = f"https://api.spotify.com/v1/artists/{artist_uri}"
    header = {"Authorization" : f"{type_token} {access_token}"}
    # Construct request
    artist_request = requests.get(url, headers= header)
    # Condition en fonction de notre token valable sinon on relance une demande de token
    if artist_request.status_code == 401:
        access_token, type_token = recover_token()
        if access_token and type_token:
            header["Authorization"] = f"{type_token} {access_token}"
            artist_request = requests.get(url, headers= header)
    if artist_request.status_code == 200:
        artist_info = artist_request.json()
        return artist_info
    else :
        return {
            "error": "Failed to retrieve artist information",
            "status": artist_request.status_code,
            "message": artist_request.text
        }

@app.get("/album_info/{album_uri}")
def spotify_info_album(album_uri : str):
    """
    Fonction qui requête spotify afin d'obtenir les informations sur l'album'
    """
    # Récupération token et type_token
    access_token, type_token = recover_token()
    # URL spotify
    url = f"https://api.spotify.com/v1/albums/{album_uri}"
    header = {"Authorization" : f"{type_token} {access_token}"}
    # Construct request
    album_request = requests.get(url, headers= header)
    # Condition en fonction de notre token valable sinon on relance une demande de token
    if album_request.status_code == 401:
        access_token, type_token = recover_token()
        if access_token and type_token:
            header["Authorization"] = f"{type_token} {access_token}"
            album_request = requests.get(url, headers= header)
    if album_request.status_code == 200:
        album_info = album_request.json()
        return album_info
    else :
        return {
            "error": "Failed to retrieve album information",
            "status": album_request.status_code,
            "message": album_request.text
        }

@app.get("/track_info/{track_uri}")
def spotify_info_album(track_uri : str):
    """
    Fonction qui requête spotify afin d'obtenir les informations sur la piste'
    """
    # Récupération token et type_token
    access_token, type_token = recover_token()
    # URL spotify
    url = f"https://api.spotify.com/v1/tracks/{track_uri}"
    header = {"Authorization" : f"{type_token} {access_token}"}
    # Construct request
    track_request = requests.get(url, headers= header)
    # Condition en fonction de notre token valable sinon on relance une demande de token
    if track_request.status_code == 401:
        access_token, type_token = recover_token()
        if access_token and type_token:
            header["Authorization"] = f"{type_token} {access_token}"
            track_request = requests.get(url, headers= header)
    if track_request.status_code == 200:
        track_info = track_request.json()
        return track_info
    else :
        return {
            "error": "Failed to retrieve track information",
            "status": track_request.status_code,
            "message": track_request.text
        }