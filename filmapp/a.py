import requests

def typeof(key_id):
    res = requests.get("https://api.themoviedb.org/3/movie/" + str(key_id) + "?api_key=7afd10215ac669bb5736cf2a670d681e")
    res.close()
    if res.status_code == 200:
        return "mv"
    else:
        return "tv"


