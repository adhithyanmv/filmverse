from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate, login, logout
from . models import Users
import requests
from requests.exceptions import ConnectionError
import json
import time
import datetime

# 🦄🦄🦄🦄🦄🦄🦄🦄🦄🦄🦄🦄🦄🦄🦄🦄🦄🦄🦄
# check why the user is changing to admin automatically and also pass the username to home
# 🦄🦄🦄🦄🦄🦄🦄🦄🦄🦄🦄🦄🦄🦄🦄🦄🦄🦄🦄

def getSeasonDetails(data):
    arr = []
    for i in data:
        obj = {}
        if i["name"]:
            obj["name"] = i["name"]
        else:
            obj["name"] = "unknown"

        if i["id"]:
            obj["id"] = i["id"]

        if i["poster_path"]:
            obj["poster_path"] = i["poster_path"]
        else:
            obj["poster_path"] = "../../static/assets/img/profile.png"

        if i["overview"]:
            obj["overview"] = i["overview"]
        else:
            obj["overview"] = ""

        if i["air_date"]:
            obj["air_date"] = i["air_date"]
        else:
            obj["air_date"] = "unknown"

        if i["episode_count"]:
            obj["episode_count"] = i["episode_count"]
        else:
            obj["episode_count"] = "unknown"

        if i["season_number"]:
            obj["season_number"] = i["season_number"]
        else:
            obj["season_number"] = "unknown"
        
        arr.append(obj)
    return arr

def getSimilar(mvid, t):

    if t == "tv":
        try:
            res = requests.get("https://api.themoviedb.org/3/tv/" + str(mvid) + "/similar?api_key=7afd10215ac669bb5736cf2a670d681e")
            res.close()
            data = res.text
            parsed = json.loads(data)
        except ConnectionError as e:
            pass
        
        arr = []

        for x in parsed["results"]:
            if len(arr) >= 10:
                break
            obj = {}
            if x["backdrop_path"]:
                obj["simImg"] = x["backdrop_path"]
            elif x["poster_path"]:
                obj["simImg"] = x["poster_path"]
            else:
                obj["simImg"] = ""
            
            if x["name"]:
                obj["name"] = x["name"]
            elif x["original_name"]:
                obj["name"] = x["original_name"]
            elif x["original_title"]:
                obj["name"] = x["original_title"]
            else:
                obj["name"] = "unknown"

            if x["first_air_date"]:
                obj["first_air_date"] = x["first_air_date"]
            else:
                obj["first_air_date"] = "unknown"

            if x["id"]:
                obj["mvId"] = x["id"]
            
            obj["type"] = "tv"
            arr.append(obj)
        return arr

    if t == "movie":
        try:
            res = requests.get("https://api.themoviedb.org/3/movie/" + str(mvid) + "/similar?api_key=7afd10215ac669bb5736cf2a670d681e")
            res.close()
            data = res.text
            parsed = json.loads(data)
        except ConnectionError as e:
            pass
        time.sleep(1)
        arr = []

        try:
            for x in parsed["results"]:
                if len(arr) >= 10:
                    break
                obj = {}
                if x["backdrop_path"]:
                    obj["simImg"] = x["backdrop_path"]
                elif x["poster_path"]:
                    obj["simImg"] = x["poster_path"]
                else:
                    obj["simImg"] = ""
                
                if x["original_title"]:
                    obj["name"] = x["original_title"]
                elif x["original_name"]:
                    obj["name"] = x["original_name"]
                elif x["original_title"]:
                    obj["name"] = x["original_title"]
                else:
                    obj["name"] = "unknown"

                if x["release_date"]:
                    obj["first_air_date"] = x["release_date"]
                else:
                    obj["first_air_date"] = "unknown"

                if x["id"]:
                    obj["mvId"] = x["id"]
                
                obj["type"] = "movie"
                arr.append(obj)
            return arr
        except UnboundLocalError as e:
            pass


def getCasts(mvid, t):
    if t == "movie":
        try:
            res = requests.get("https://api.themoviedb.org/3/movie/" + str(mvid) + "?api_key=7afd10215ac669bb5736cf2a670d681e&append_to_response=casts")
            res.close()
            data = res.text
            parsed = json.loads(data)
        except ConnectionError as e:
            pass

        casts = sorted(parsed["casts"]["cast"], key = lambda d: d["popularity"], reverse = True)
        mainCasts = []

        if len(casts) > 10:
            for i in casts:
                if len(mainCasts) >= 10:
                    break
                obj = {}
                realName = i["original_name"] if i["original_name"] else "unknown"
                charName = i["character"].split("/")[0] if i["character"] else "unknown"
                artistId = i["id"] if i["id"] else "unknown"
                charImg = i["profile_path"] if i["profile_path"] else ""
                obj["realname"] = realName
                obj["charname"] = charName
                obj["artistid"] = artistId
                obj["charimg"] = charImg

                mainCasts.append(obj)
        else:
            mainCasts = casts
        
        return mainCasts
    
    if t == "tv":
        try:
            res = requests.get("https://api.themoviedb.org/3/tv/" + str(mvid) + "/credits?api_key=7afd10215ac669bb5736cf2a670d681e")
            res.close()
            data = res.text
            parsed = json.loads(data)
        except ConnectionError as e:
            pass

        casts = sorted(parsed["cast"], key = lambda d: d["popularity"], reverse = True)
        mainCasts = []

        if len(casts) > 10:
            for i in casts:
                if len(mainCasts) >= 10:
                    break
                obj = {}
                realName = i["original_name"] if i["original_name"] else "unknown"
                charName = i["character"].split("/")[0] if i["character"] else "unknown"
                artistId = i["id"] if i["id"] else "unknown"
                charImg = i["profile_path"] if i["profile_path"] else ""
                obj["realname"] = realName
                obj["charname"] = charName
                obj["artistid"] = artistId
                obj["charimg"] = charImg
                mainCasts.append(obj)
        else:
            for i in casts:
                obj = {}
                realName = i["original_name"] if i["original_name"] else "unknown"
                charName = i["character"].split("/")[0] if i["character"] else "unknown"
                artistId = i["id"] if i["id"] else "unknown"
                charImg = i["profile_path"] if i["profile_path"] else ""
                obj["realname"] = realName
                obj["charname"] = charName
                obj["artistid"] = artistId
                obj["charimg"] = charImg
                mainCasts.append(obj)

        return mainCasts

currentData = {}


def customise(data, t):
    if t == "movie":
        dic = {}

        releaseDate = ""
        mvName = ""
        mvPic = ""
        mvYtLink = ""
        mvDesc = ""
        runTime = ""
        mvLanguage = ""
        mvGenre = []
        mvid = ""
        impCasts = getCasts(data["id"], "movie")
        

        if data["id"]:
            mvid = data["id"]

        if data["release_date"]:
            releaseDate = data["release_date"]
        else:
            releaseDate = "01-01-01"
        
        if data["original_title"]:
            mvName = data["original_title"]
        elif data["title"]:
            mvName = data["title"]
        elif data["original_name"]:
            mvName = data["original_name"]
        else:
            mvName = "unknown"
        
        if data["backdrop_path"]:
            mvPic = data["backdrop_path"]
        elif data["poster_path"]:
            mvPic = data["poster_path"]
        else:
            mvPic = "../../static/assets/img/profile.png"

        if data["videos"]["results"]:
            mvYtLink = "/" + data["videos"]["results"][0]["key"]

        if data["overview"]:
            mvDesc = data["overview"]
        else:
            mvDesc = ""

        if data["runtime"]:
            runTime = data["runtime"]
        else:
            runTime = "00"
        
        if data["spoken_languages"][0]:
            mvLanguage = data["spoken_languages"][0]["english_name"]
        else:
            mvLanguage = "unknown"

        if data["genres"]:
            for i in data["genres"]:
                mvGenre.append(i["name"])
        
        dic["genres"] = mvGenre
        dic["releasedate"] = releaseDate
        dic["mvname"] = mvName
        dic["mvpic"] = mvPic
        dic["mvytlink"] = "https://www.youtube.com/embed"+str(mvYtLink)
        dic["mvdesc"] = mvDesc
        dic["runtime"] = runTime
        dic["mvlanguage"] = mvLanguage
        dic["mvgenre"] = mvGenre
        dic["casts"] = impCasts
        dic["mvid"] = mvid

        currentData["name"] = mvName
        currentData["pic"] = mvPic
        currentData["id"] = mvid

        return dic
    
    if t == "tv":
        dic = {}

        releaseDate = ""
        lastReleaseDate = ""
        mvName = ""
        mvPic = ""
        mvYtLink = ""
        mvDesc = ""
        seasons = ""
        episodes = ""
        mvLanguage = ""
        mvGenre = []
        mvid = ""
        impCasts = getCasts(data["id"], "tv")
        tvDetails = getSeasonDetails(data["seasons"])

        if data["id"]:
            mvid = data["id"]

        if data["first_air_date"]:
            releaseDate = data["first_air_date"]
        else:
            releaseDate = "01-01-01"
        
        if data["last_air_date"]:
            lastReleaseDate = data["last_air_date"]
        else:
            lastReleaseDate = "02-02-02"
        
        if data["original_name"]:
            mvName = data["original_name"]
        elif data["title"]:
            mvName = data["title"]
        elif data["original_title"]:
            mvName = data["original_title"]
        else:
            mvName = "unknown"
        
        if data["backdrop_path"]:
            mvPic = data["backdrop_path"]
        elif data["poster_path"]:
            mvPic = data["poster_path"]
        else:
            mvPic = "../../static/assets/img/profile.png"

        if data["videos"]["results"]:
            mvYtLink = "/" + data["videos"]["results"][0]["key"]

        if data["overview"]:
            mvDesc = data["overview"]
        else:
            mvDesc = ""

        if data["number_of_episodes"]:
            episodes = data["number_of_episodes"]
        else:
            episodes = "0"
        
        if data["number_of_seasons"]:
            seasons = data["number_of_seasons"]
        else:
            seasons = "0"
        
        if data["spoken_languages"][0]:
            mvLanguage = data["spoken_languages"][0]["english_name"]
        else:
            mvLanguage = "unknown"

        if data["genres"]:
            for i in data["genres"]:
                mvGenre.append(i["name"])
        
        dic["genres"] = mvGenre
        dic["number_of_episodes"] = episodes
        dic["number_of_seasons"] = seasons
        dic["releaseDate"] = releaseDate
        dic["lastReleaseDate"] = lastReleaseDate
        dic["mvname"] = mvName
        dic["mvpic"] = mvPic
        dic["mvytlink"] = "https://www.youtube.com/embed"+str(mvYtLink)
        dic["mvdesc"] = mvDesc
        dic["mvlanguage"] = mvLanguage
        dic["mvgenre"] = mvGenre
        dic["casts"] = impCasts
        dic["mvid"] = mvid
        dic["tvDetails"] = tvDetails

        return dic
    

def getDetails(keyid, t):
    if t == "movie":
        try:
            res = requests.get("https://api.themoviedb.org/3/movie/" + str(keyid) + "?api_key=7afd10215ac669bb5736cf2a670d681e&append_to_response=videos")
            res.close()
            data = res.text
            parsed = json.loads(data)
            customisedData = customise(parsed, "movie")
            return customisedData
        except ConnectionError as e:
            pass
    if t == "tv":
        try:
            res = requests.get("https://api.themoviedb.org/3/tv/" + str(keyid) + "?api_key=7afd10215ac669bb5736cf2a670d681e&append_to_response=videos")
            res.close()
            data = res.text
            parsed = json.loads(data)
            customisedData = customise(parsed, "tv")
            return customisedData
        except ConnectionError as e:
            return customisedData

def getArtistMvTv(keyid, t):
    if t == "mv":
        try:
            res = requests.get("https://api.themoviedb.org/3/person/" + str(keyid) + "/movie_credits?api_key=7afd10215ac669bb5736cf2a670d681e")
            res.close()
            data = res.text
            parsed = json.loads(data)
        except ConnectionError as e:
            pass

        sort = sorted(parsed["cast"], key = lambda d: d["popularity"], reverse = True)
        arr = []

        for x in sort:
            obj = {}
            if len(arr) >= 10:
                break
            
            if "backdrop_path" in x and x["backdrop_path"] is not None:
                obj["artistmvimg"] = "https://image.tmdb.org/t/p/original" + x["backdrop_path"]
            elif "poster_path" in x and x["poster_path"] is not None:
                obj["artistmvimg"] = "https://image.tmdb.org/t/p/original" + x["poster_path"]
            else:
                obj["artistmvimg"] = "../../static/assets/img/profile.png"
            
            if "title" in x and x["title"] is not None:
                obj["artistmvname"] =  x["title"]
            elif "original_title" in x and x["title"] is not None:
                obj["artistmvname"] = x["original_title"]
            
            if "id" in x:
                obj["artistmvid"] = x["id"]

            arr.append(obj)
        
        return arr
    
    if t == "tv":
        try:
            res = requests.get("https://api.themoviedb.org/3/person/" + str(keyid) + "/tv_credits?api_key=7afd10215ac669bb5736cf2a670d681e")
            res.close()
            data = res.text
            parsed = json.loads(data)
        except ConnectionError as e:
            pass

        sort = sorted(parsed["cast"], key = lambda d: d["popularity"], reverse = True)
        arr = []

        for x in sort:
            obj = {}
            if len(arr) >= 10:
                break
            
            if "backdrop_path" in x  and x["backdrop_path"] is not None:
                obj["artisttvimg"] = "https://image.tmdb.org/t/p/original/" + x["backdrop_path"]
            elif "poster_path" in x  and x["poster_path"] is not None:
                obj["artisttvimg"] = "https://image.tmdb.org/t/p/original" + x["poster_path"]
            else:
                obj["artisttvimg"] = "../../static/assets/img/profile.png"
            
            if "original_name" in x:
                obj["artisttvname"] = x["original_name"]
            elif "name" in x:
                obj["artisttvname"] = x["name"]
            
            if "id" in x:
                obj["artisttvid"] = x["id"]

            arr.append(obj)
        
        return arr



def getArtistDetails(keyid):
    details = {}
    try:
        res = requests.get("https://api.themoviedb.org/3/person/" + str(keyid) + "?api_key=7afd10215ac669bb5736cf2a670d681e")
        res.close()
        data = res.text
        parsed = json.loads(data)
    except ConnectionError as e:
        pass
        
    now = datetime.datetime.now().year

    try:
        details["age"] = now - int(parsed["birthday"].split("-")[0])
        details["bio"] = parsed["biography"]
        details["name"] = parsed["name"]
        details["artistimg"] = parsed["profile_path"] if parsed["profile_path"] else "../../static/assets/img/profile.png"
        details["dead"] = parsed["deathday"]
        details["born"] = parsed["birthday"]
        details["place"] = parsed["place_of_birth"]
        details["tvs"] = getArtistMvTv(keyid, "tv")
        details["movies"] = getArtistMvTv(keyid, "mv")

        return details
    except UnboundLocalError as e:
        pass


def getSearch(query, t):
    if t == "mv":
        movies = []
        try:
            q = "+".join((query.split(" ")))
            res = requests.get("https://api.themoviedb.org/3/search/movie?api_key=7afd10215ac669bb5736cf2a670d681e&query=" + str(q))
            res.close()
            data = res.text
            parsed = json.loads(data)
        except ConnectionError as e:
            pass
        
        try:
            for x in parsed["results"]:
                if len(movies) >= 12:
                    break
                obj = {}

                if "backdrop_path" in x and x["backdrop_path"] is not None:
                    obj["mvimg"] = x["backdrop_path"]
                elif "poster_path" in x and x["poster_path"]:
                    obj["mvimg"] = x["poster_path"]
                else:
                    obj["mvimg"] = ""

                if "overview" in x and x["overview"] is not None:
                    obj["mvoverview"] = x["overview"]
                else:
                    obj["mvoverview"] = ""
                
                if "id" in x and x["id"] is not None:
                    obj["mvid"] = x["id"]

                if "title" in x and x["title"] is not None:
                    obj["mvtitle"] = x["title"]
                elif "original_title" in x and x["original_title"] is not None:
                    obj["mvtitle"] = x["original_title"]
                elif "name" in x and x["name"] is not None:
                    obj["mvtitle"] = x["name"]
                else:
                    obj["mvtitle"] = ""
                
                movies.append(obj)
        except UnboundLocalError as e:
            pass
        
        return movies


    if t == "tv":
        tvs = []
        try:
            q = "+".join((query.split(" ")))
            res = requests.get("https://api.themoviedb.org/3/search/tv?api_key=7afd10215ac669bb5736cf2a670d681e&query=" + str(q))
            res.close()
            data = res.text
            parsed = json.loads(data)
        except ConnectionError as e:
            pass
        
        try:
            for x in parsed["results"]:
                if len(tvs) >= 12:
                    break
                obj = {}

                if "backdrop_path" in x and x["backdrop_path"] is not None:
                    obj["tvimg"] = x["backdrop_path"]
                elif "poster_path" in x and x["poster_path"]:
                    obj["tvimg"] = x["poster_path"]
                else:
                    obj["tvimg"] = ""

                if "overview" in x and x["overview"] is not None:
                    obj["tvoverview"] = x["overview"]
                else:
                    obj["tvoverview"] = ""
                
                if "id" in x and x["id"] is not None:
                    obj["tvid"] = x["id"]

                if "title" in x and x["title"] is not None:
                    obj["tvtitle"] = x["title"]
                elif "original_name" in x and x["original_name"] is not None:
                    obj["tvtitle"] = x["original_name"]
                elif "name" in x and x["name"] is not None:
                    obj["tvtitle"] = x["name"]
                else:
                    obj["tvtitle"] = ""
                
                tvs.append(obj)

            return tvs
        except UnboundLocalError as e:
            pass



def index(request):
    return render(request, 'index.html', {"firstname" : request.user.username})

def movie(request, key_id):

    details = getDetails(key_id, "movie")
    similar = getSimilar(key_id, "movie")
    # return render(request, 'movie-details.html', {"moviename" : details["mvname"], "moviedate" : details["releasedate"], "mvdesc" : details["mvdesc"], "runtime" : details["runtime"], "language" : details["mvlanguage"], "genres" : details["genres"], "casts" : details["casts"], "mvpic" : "https://image.tmdb.org/t/p/original" +  details["mvpic"], "mvytlink" : details["mvytlink"], "similar" : similar})

    if request.method == "POST":
        if not request.user.username:
            return redirect("../../accounts/login")
        
        # if the row for users fav list not exist
        if not Users.objects.filter(username=request.user.username):
            Users.objects.create(username=request.user.username, usermoviename=[details["mvname"]], usermovieimage=["https://image.tmdb.org/t/p/original" +  details["mvpic"]], usermovieid=[key_id])
            return render(request, 'movie-details.html', {"moviename" : details["mvname"], "moviedate" : details["releasedate"], "mvdesc" : details["mvdesc"], "runtime" : details["runtime"], "language" : details["mvlanguage"], "genres" : details["genres"], "casts" : details["casts"], "mvpic" : "https://image.tmdb.org/t/p/original" +  details["mvpic"], "mvytlink" : details["mvytlink"], "similar" : similar, "exists" : True})
        else:
            # if the user fav row exists and so now check if the user wants to remove or append the movie details to db
            userdata = Users.objects.get(username=request.user.username)

            if key_id in Users.objects.get(username=request.user.username).usermovieid:
                index = userdata.usermovieid.index(key_id)
                userdata.usermovieid.remove(userdata.usermovieid[index])
                userdata.save()
                userdata.usermovietype.remove(userdata.usermovietype[index])
                userdata.save()
                userdata.usermoviename.remove(userdata.usermoviename[index])
                userdata.save()
                userdata.usermovieimage.remove(userdata.usermovieimage[index])
                userdata.save()
                return render(request, 'movie-details.html', {"moviename" : details["mvname"], "moviedate" : details["releasedate"], "mvdesc" : details["mvdesc"], "runtime" : details["runtime"], "language" : details["mvlanguage"], "genres" : details["genres"], "casts" : details["casts"], "mvpic" : "https://image.tmdb.org/t/p/original" +  details["mvpic"], "mvytlink" : details["mvytlink"], "similar" : similar})
            else:
                userdata.usermovieid.append(key_id)
                userdata.save()
                userdata.usermovieimage.append("https://image.tmdb.org/t/p/original" +  details["mvpic"])
                userdata.save()
                userdata.usermoviename.append(details["mvname"])
                userdata.save()
                userdata.usermovietype.append("mv")
                userdata.save()
                return render(request, 'movie-details.html', {"moviename" : details["mvname"], "moviedate" : details["releasedate"], "mvdesc" : details["mvdesc"], "runtime" : details["runtime"], "language" : details["mvlanguage"], "genres" : details["genres"], "casts" : details["casts"], "mvpic" : "https://image.tmdb.org/t/p/original" +  details["mvpic"], "mvytlink" : details["mvytlink"], "similar" : similar, "exists" : True})

    
    if not Users.objects.filter(username=request.user.username):
        return render(request, 'movie-details.html', {"moviename" : details["mvname"], "moviedate" : details["releasedate"], "mvdesc" : details["mvdesc"], "runtime" : details["runtime"], "language" : details["mvlanguage"], "genres" : details["genres"], "casts" : details["casts"], "mvpic" : "https://image.tmdb.org/t/p/original" +  details["mvpic"], "mvytlink" : details["mvytlink"], "similar" : similar, "exists" : False})
    else:
        userdata = Users.objects.get(username=request.user.username)
        if key_id in userdata.usermovieid:
            return render(request, 'movie-details.html', {"moviename" : details["mvname"], "moviedate" : details["releasedate"], "mvdesc" : details["mvdesc"], "runtime" : details["runtime"], "language" : details["mvlanguage"], "genres" : details["genres"], "casts" : details["casts"], "mvpic" : "https://image.tmdb.org/t/p/original" +  details["mvpic"], "mvytlink" : details["mvytlink"], "similar" : similar, "exists" : True})
        else:
            return render(request, 'movie-details.html', {"moviename" : details["mvname"], "moviedate" : details["releasedate"], "mvdesc" : details["mvdesc"], "runtime" : details["runtime"], "language" : details["mvlanguage"], "genres" : details["genres"], "casts" : details["casts"], "mvpic" : "https://image.tmdb.org/t/p/original" +  details["mvpic"], "mvytlink" : details["mvytlink"], "similar" : similar, "exists" : False})


def tv(request, key_id):
    details = getDetails(key_id, "tv")
    similar = getSimilar(key_id, "tv")
    
    if request.method == "POST":
        if not request.user.username:
            return redirect("../../accounts/login")
        
        # if the row for users fav list not exist
        if not Users.objects.filter(username=request.user.username):
            Users.objects.create(username=request.user.username, usermoviename=[details["mvname"]], usermovieimage=["https://image.tmdb.org/t/p/original" +  details["mvpic"]], usermovieid=[key_id])
            return render(request, 'tv-details.html', {"moviename" : details["mvname"], "releasedate" : details["releaseDate"], "lastReleaseDate" : details["lastReleaseDate"], "mvdesc" : details["mvdesc"], "language" : details["mvlanguage"], "genres" : details["genres"], "casts" : details["casts"], "mvpic" : "https://image.tmdb.org/t/p/original" +  details["mvpic"], "mvytlink" : details["mvytlink"], "seasons" : details["number_of_seasons"], "episodes" : details["number_of_episodes"], "tvDetails" : details["tvDetails"], "similar" : similar, "exists" : True})
        else:
            # if the user fav row exists and so now check if the user wants to remove or append the movie details to db
            userdata = Users.objects.get(username=request.user.username)

            if key_id in Users.objects.get(username=request.user.username).usermovieid:
                index = userdata.usermovieid.index(key_id)
                userdata.usermovieid.remove(userdata.usermovieid[index])
                userdata.save()
                userdata.usermoviename.remove(userdata.usermoviename[index])
                userdata.save()
                userdata.usermovieimage.remove(userdata.usermovieimage[index])
                userdata.save()
                userdata.usermovietype.remove(userdata.usermovietype[index])
                userdata.save()
                return render(request, 'tv-details.html', {"moviename" : details["mvname"], "releasedate" : details["releaseDate"], "lastReleaseDate" : details["lastReleaseDate"], "mvdesc" : details["mvdesc"], "language" : details["mvlanguage"], "genres" : details["genres"], "casts" : details["casts"], "mvpic" : "https://image.tmdb.org/t/p/original" +  details["mvpic"], "mvytlink" : details["mvytlink"], "seasons" : details["number_of_seasons"], "episodes" : details["number_of_episodes"], "tvDetails" : details["tvDetails"], "similar" : similar})
            else:
                userdata.usermovieid.append(key_id)
                userdata.save()
                userdata.usermovieimage.append("https://image.tmdb.org/t/p/original" +  details["mvpic"])
                userdata.save()
                userdata.usermoviename.append(details["mvname"])
                userdata.save()
                userdata.usermovietype.append("tv")
                userdata.save()
                return render(request, 'tv-details.html', {"moviename" : details["mvname"], "releasedate" : details["releaseDate"], "lastReleaseDate" : details["lastReleaseDate"], "mvdesc" : details["mvdesc"], "language" : details["mvlanguage"], "genres" : details["genres"], "casts" : details["casts"], "mvpic" : "https://image.tmdb.org/t/p/original" +  details["mvpic"], "mvytlink" : details["mvytlink"], "seasons" : details["number_of_seasons"], "episodes" : details["number_of_episodes"], "tvDetails" : details["tvDetails"], "similar" : similar, "exists" : True})

    
    if not Users.objects.filter(username=request.user.username):
        return render(request, 'tv-details.html', {"moviename" : details["mvname"], "releasedate" : details["releaseDate"], "lastReleaseDate" : details["lastReleaseDate"], "mvdesc" : details["mvdesc"], "language" : details["mvlanguage"], "genres" : details["genres"], "casts" : details["casts"], "mvpic" : "https://image.tmdb.org/t/p/original" +  details["mvpic"], "mvytlink" : details["mvytlink"], "seasons" : details["number_of_seasons"], "episodes" : details["number_of_episodes"], "tvDetails" : details["tvDetails"], "similar" : similar})
    else:
        userdata = Users.objects.get(username=request.user.username)
        if key_id in userdata.usermovieid:
            return render(request, 'tv-details.html', {"moviename" : details["mvname"], "releasedate" : details["releaseDate"], "lastReleaseDate" : details["lastReleaseDate"], "mvdesc" : details["mvdesc"], "language" : details["mvlanguage"], "genres" : details["genres"], "casts" : details["casts"], "mvpic" : "https://image.tmdb.org/t/p/original" +  details["mvpic"], "mvytlink" : details["mvytlink"], "seasons" : details["number_of_seasons"], "episodes" : details["number_of_episodes"], "tvDetails" : details["tvDetails"], "similar" : similar, "exists" : True})
        else:
            return render(request, 'tv-details.html', {"moviename" : details["mvname"], "releasedate" : details["releaseDate"], "lastReleaseDate" : details["lastReleaseDate"], "mvdesc" : details["mvdesc"], "language" : details["mvlanguage"], "genres" : details["genres"], "casts" : details["casts"], "mvpic" : "https://image.tmdb.org/t/p/original" +  details["mvpic"], "mvytlink" : details["mvytlink"], "seasons" : details["number_of_seasons"], "episodes" : details["number_of_episodes"], "tvDetails" : details["tvDetails"], "similar" : similar})


def artist(request, key_id):
    artistDetails = getArtistDetails(key_id)
    return render(request, 'artist-detail.html', artistDetails)

def search(request):
    mvresult = getSearch(request.GET["query"], "mv")
    tvresult = getSearch(request.GET["query"], "tv")
    return render(request, 'search.html', {"movies" : mvresult, "tvs" : tvresult})

def wishlist(request):
    if not request.user.username:
        return redirect("../login")
    
    if not Users.objects.filter(username=request.user.username):
        print(request.user.username)
        return render(request, 'favourites.html')
    
    wishlist = {}
    userdata = Users.objects.get(username=request.user.username)

    arr = []
    for i in range(len(userdata.usermovieid)):
        temp = {}
        temp["id"] = userdata.usermovieid[i]
        temp["img"] = userdata.usermovieimage[i]
        temp["mvname"] = userdata.usermoviename[i]
        temp["type"] = userdata.usermovietype[i]
        arr.append(temp)

    wishlist["favs"] = arr

    return render(request, 'favourites.html', {"favs" : wishlist["favs"]})
