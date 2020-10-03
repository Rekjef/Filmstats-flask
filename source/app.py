from flask import Flask, render_template, url_for, request, redirect
import requests, random

app = Flask(__name__)
'''genres ={
    
    10759: {
      "name": "Action & Adventure",
      "color"
    },
    16:{
      "name": "Animation"
    },
    35:{
      "name": "Comedy"
    },
    80:{
      "name": "Crime"
    },
    99:{
      "name": "Documentary"
    },
    18:{
      "name": "Drama"
    },
    10751:{
      "name": "Family"
    },
    10762:{
      "name": "Kids"
    },
9648,
      "name": "Mystery"
    },
 10763,
      "name": "News"
    },
10764,
      "name": "Reality"
    },
10765,
      "name": "Sci-Fi & Fantasy"
    },
10766,
      "name": "Soap"
    },
10767,
      "name": "Talk"
    },
10768,
      "name": "War & Politics"
    },
    37,
      "name": "Western"
    }'''
apiKey = "d8bf019d0cca372bd804735f172f67e8"
# ! https://api.themoviedb.org/3/tv/popular?api_key=d8bf019d0cca372bd804735f172f67e8&language=pl&page=1
class MovieCard:
    def __init__(self, data):
        self.title = data['original_name']
        self.released = data['first_air_date']
        #self.genres = data['Genre'].split(', ')
        #self.runtime = data["Runtime"]
        #self.director = data['Director']
        #self.writer = data['Writer']
        #self.actors = data['Actors']
        self.plot = data['overview']
        self.poster = data['poster_path']
        self.ratings = {"rating": data["vote_average"], "votes": data["vote_count"]}
        #if data["totalSeasons"] is not None:
        #    self.totalSeasons = data['totalSeasons']

class Movie:
    def __init__(self, searchedDetails, searchedImagesList, searchedActors):
        self.title = searchedDetails['name']
        self.titleOriginal = searchedDetails['original_name']
        self.released = searchedDetails['first_air_date']
        self.genres = [x['name'] for x in searchedDetails['genres']]
        #self.runtime = data["Runtime"]
        self.director = ', '.join([x['name'] for x in searchedDetails['created_by']])
        #self.writer = data['Writer']
        self.actors = [{'name': x['name'], 'character_name': x['character'], 'image_id': x['profile_path']} for x in searchedActors['cast']]
        self.plot = searchedDetails['overview']
        self.poster = self.pickRandomPosterFromList(searchedImagesList, 'posters')
        self.backdrop_path = self.pickRandomPosterFromList(searchedImagesList, 'backdrops')
        self.ratings = {"rating": searchedDetails["vote_average"], "votes": searchedDetails["vote_count"]}
        self.totalSeasons = searchedDetails['number_of_seasons']
        self.totalEpisodes = searchedDetails['number_of_episodes']
        self.streamingPlatforms = [{'name': x['name'], 'logo': x['logo_path']}for x in searchedDetails['networks']]
        
    def pickRandomPosterFromList(self, searchedImagesList, typeOfImg: str):
        index = random.randrange(len(searchedImagesList[typeOfImg]))
        return searchedImagesList[typeOfImg][index]['file_path']
        
def getListOfPopularTvShows(sites: int):
    # ? 1 site is 20 elements
    cards = list()
    for i in range(1, sites + 1):
        data = getData(f"https://api.themoviedb.org/3/tv/popular?api_key=d8bf019d0cca372bd804735f172f67e8&language=pl&page={i}")
        for x in range(len(data['results'])):
            cards.append(MovieCard(data['results'][x]))
    return cards

def getInformationsAboutSpecificTvShow(title):
    id = getData(f'https://api.themoviedb.org/3/search/multi?api_key=d8bf019d0cca372bd804735f172f67e8&language=pl&query={title}&page=1&include_adult=false')['results'][0]['id']
    searchedDetails = getData(f'https://api.themoviedb.org/3/tv/{id}?api_key=d8bf019d0cca372bd804735f172f67e8&language=pl')
    searchedImagesList = getData(f'https://api.themoviedb.org/3/tv/{id}/images?api_key=d8bf019d0cca372bd804735f172f67e8')
    searchedActors = getData(f'https://api.themoviedb.org/3/tv/{id}/credits?api_key=d8bf019d0cca372bd804735f172f67e8')
    return Movie(searchedDetails, searchedImagesList, searchedActors)



def getData(url):
    print(url)
    return requests.get(url).json()


@app.route('/')
def index():
    #return redirect('/')
    return render_template("card-template.html", movies=getListOfPopularTvShows(2))

@app.route('/serials/<title>')
def serial(title):
    return render_template("serial-template.html", details=getInformationsAboutSpecificTvShow(title))
    #return title

@app.route('/search/<title>')
def search(title):
    return title

if __name__ == "__main__":
    app.run(debug=True)