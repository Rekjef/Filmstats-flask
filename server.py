from flask import Flask, render_template, url_for, request, redirect
import requests, random
app = Flask(__name__)
genres ={
    10759: {
      "name": "Action & Adventure",
      "color": "#2663b3"
    },
    16:{
      "name": "Animation",
      "color": "#db07ce"
    },
    35:{
      "name": "Comedy",
      "color": "#a2b900"
    },
    80:{
      "name": "Crime",
      "color": "#d90d0d"
    },
    99:{
      "name": "Documentary",
      "color": "#4d4d4d"
    },
    18:{
      "name": "Drama",
      "color": "#d90d0d"
    },
    10751:{
      "name": "Family",
      "color": "#c80cce"
    },
    10762:{
      "name": "Kids",
      "color": "#c80cce"
    },
    9648:{
      "name": "Mystery",
      "color": "#176810"
    },
    10763:{
      "name": "News",
      "color": "#0c73ce"
    },
    10764:{
      "name": "Reality",
      "color": "#0c73ce"
    },
    10765:{
      "name": "Sci-Fi & Fantasy",
      "color": "#848484"
    },
    10766:{
      "name": "Soap",
      "color": "#ce670c"
    },
    10767:{
      "name": "Talk",
      "color": "#ce670c"
    },
    10768:{
      "name": "War & Politics",
      "color": "#4d4d4d"
    },
    37:{
      "name": "Western",
      "color": "#642323"
    }
}
apiKey = ""
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
        self.poster = f"https://image.tmdb.org/t/p/w500/{data['poster_path']}"
        self.ratings = {"rating": data["vote_average"], "votes": data["vote_count"]}
        #if data["totalSeasons"] is not None:
        #    self.totalSeasons = data['totalSeasons']

class Serial:
    def __init__(self, searchedDetails, searchedImagesList, searchedActors):
        self.title = searchedDetails['name']
        self.titleOriginal = searchedDetails['original_name']
        self.released = searchedDetails['first_air_date']
        self.genres = [{"name": x['name'], "color": genres[x["id"]]["color"]} for x in searchedDetails['genres']]
        #self.runtime = data["Runtime"]
        self.director = ', '.join([x['name'] for x in searchedDetails['created_by']])
        #self.writer = data['Writer']
        self.actors = [{'name': x['name'], 'character_name': x['character'], 'image_id': x['profile_path']} for x in searchedActors['cast']]
        self.plot = searchedDetails['overview']
        self.poster =  f"https://image.tmdb.org/t/p/w500/{self.pickRandomPosterFromList(searchedImagesList, 'posters')}"
        self.backdrop_path = self.pickRandomPosterFromList(searchedImagesList, 'backdrops')
        self.ratings = {"rating": searchedDetails["vote_average"], "votes": searchedDetails["vote_count"]}
        self.totalSeasons = searchedDetails['number_of_seasons']
        self.seasons = [{"overview": x['overview'], "episodes": x['episode_count'], "name": x['name'], "poster": x['poster_path'], "date": searchedDetails['first_air_date']} for x in searchedDetails['seasons']]
        self.totalEpisodes = searchedDetails['number_of_episodes']
        self.streamingPlatforms = [{'name': x['name'], 'logo': x['logo_path']}for x in searchedDetails['networks']]
        
    def pickRandomPosterFromList(self, searchedImagesList, typeOfImg: str):
        index = random.randrange(len(searchedImagesList[typeOfImg]))
        return searchedImagesList[typeOfImg][index]['file_path']
# class Movie:
class SearchResult:
    def __init__(self, data):
        self.genres = list()
        for x in data['genre_ids']:
            if x in genres:
              self.genres.append({"name": genres[x]['name'], "color": genres[x]["color"]})
        self.mediaType = data["media_type"]
        self.plot = data['overview']
        self.poster = f"https://image.tmdb.org/t/p/w500/{data['poster_path']}"
        self.backdrop_path = data['backdrop_path']
        self.ratings = {"rating": data["vote_average"], "votes": data["vote_count"]}
        if self.mediaType == 'tv':
          self.released = data.get('first_air_date', 'xx-xx-xxxx')
          self.title = data['name']
          self.titleOriginal = data['original_name']
        elif self.mediaType == 'movie':
          self.released = data.get('release_date', 'xx-xx-xxxx')
          self.title = data['title']
          self.titleOriginal = data['original_title']         

def getListOfPopularTvShows(sites: int):
    # ? 1 site is 20 elements
    cards = list()
    for i in range(1, sites + 1):
        data = getData(f"https://api.themoviedb.org/3/tv/popular?api_key={apiKey}&page={i}")
        for x in range(len(data['results'])):
            cards.append(MovieCard(data['results'][x]))
    return cards

def getInformationsAboutSpecificTvShow(title: str):
    id = getData(f'https://api.themoviedb.org/3/search/multi?api_key={apiKey}&query={title}&page=1&include_adult=false')['results'][0]['id']
    searchedDetails = getData(f'https://api.themoviedb.org/3/tv/{id}?api_key={apiKey}&language=pl')
    searchedImagesList = getData(f'https://api.themoviedb.org/3/tv/{id}/images?api_key={apiKey}')
    searchedActors = getData(f'https://api.themoviedb.org/3/tv/{id}/credits?api_key={apiKey}')
    return Serial(searchedDetails, searchedImagesList, searchedActors)

def getMultiSearchResults(title: str, page = 1):
    cards = list()
    for i in range(1, page + 1):
        data = getData(f'https://api.themoviedb.org/3/search/multi?api_key={apiKey}&query={title}&page={i}&include_adult=false')
        for x in range(len(data['results'])):
            cards.append(SearchResult(data['results'][x]))
    return cards

def getData(url):
    print(url)
    return requests.get(url).json()


@app.route('/')
def index():
    #return redirect('/')
    return render_template("card-template.html", movies=getListOfPopularTvShows(2))

@app.route('/serial/<title>')
def serial(title):
    return render_template("serial-template.html", details=getInformationsAboutSpecificTvShow(title))
    #return title
@app.route('/search/<title>')
def search(title):
    return render_template("searchResults-template.html", results=getMultiSearchResults(title))

if __name__ == "__main__":
    app.run(debug=True)