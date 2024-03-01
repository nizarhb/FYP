import requests


url = "https://api.themoviedb.org/3/configuration"

headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI5MTc5NjhlNmE1Y2ZlMTE2NDE5NDQ2ZTFhZWMwZDM5NyIsInN1YiI6IjY1Y2ZiNDIzZDdjZDA2MDE3YmZkYzEyNiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.OT35zZi5-IbSbuWmrK10WG0cEKeaSCCuWvFBiMCcjEE"
}

response = requests.get(url, headers=headers)

def get_related_movies(movie_id):
    # Make an API request to get the selected movie's details
    movie_url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=917968e6a5cfe116419446e1aec0d397"
    response = requests.get(movie_url)
    movie_data = response.json()

    # Extract the genre IDs from the selected movie
    genre_ids = [genre['id'] for genre in movie_data['genres']]

    # Make an API request to get related movies with similar genres
    related_movies_url = f"https://api.themoviedb.org/3/discover/movie?api_key=917968e6a5cfe116419446e1aec0d397&with_genres={','.join(map(str, genre_ids))}"
    response = requests.get(related_movies_url)
    related_movies_data = response.json()

    # Extract the related movies from the API response
    related_movies = related_movies_data['results']

    # Filter out the original movie from the related movies list
    related_movies = [movie for movie in related_movies if movie['id'] != movie_id]

    base_image_url = "https://image.tmdb.org/t/p/w500"
    for movie in related_movies:
        movie["poster_url"] = base_image_url + movie["poster_path"]

    return related_movies[:10]
def fetch_genre_data():
    url = "https://api.themoviedb.org/3/genre/movie/list"
    params = {
        "api_key": "917968e6a5cfe116419446e1aec0d397",
        "language": "en-US"
    }
    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        genres = {genre['id']: genre['name'] for genre in data['genres']}
        return genres
    else:
        return {}
def get_top_rated_movies():
    url = "https://api.themoviedb.org/3/movie/top_rated"
    params = {
        "api_key": "917968e6a5cfe116419446e1aec0d397",
        "language": "en-US",
        "page": 1
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        movies = response.json()['results']
        genres = fetch_genre_data()

        for movie in movies:
            genre_ids = movie['genre_ids']
            movie['genres'] = [genres[genre_id] for genre_id in genre_ids if genre_id in genres]


        base_image_url = "https://image.tmdb.org/t/p/w500"
        for movie in movies:
            movie["poster_url"] = base_image_url + movie["poster_path"]
        return movies[:100]  
    else:
        return None

def get_latest_movies():
    url = "https://api.themoviedb.org/3/movie/now_playing"
    params = {
        "api_key": "917968e6a5cfe116419446e1aec0d397",
        "language": "en-US",
        "page": 1
    }
    response = requests.get(url, params=params)

    if response.status_code == 200:
        movies = response.json()['results']
        genres = fetch_genre_data()

        for movie in movies:
            genre_ids = movie['genre_ids']
            movie['genres'] = [genres[genre_id] for genre_id in genre_ids if genre_id in genres]

        base_image_url = "https://image.tmdb.org/t/p/w500"
        for movie in movies:
            movie["poster_url"] = base_image_url + movie["poster_path"]
        return movies[:100]
    else:
        return None

def get_popular_shows():
    url = "https://api.themoviedb.org/3/tv/popular"
    params = {
        "api_key": "917968e6a5cfe116419446e1aec0d397",
        "language": "en-US",
        "page": 1
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        movies = response.json()['results']
        genres = fetch_genre_data()

        for movie in movies:
            genre_ids = movie['genre_ids']
            movie['genres'] = [genres[genre_id] for genre_id in genre_ids if genre_id in genres]

        base_image_url = "https://image.tmdb.org/t/p/w500"
        for movie in movies:
            movie["poster_url"] = base_image_url + movie["poster_path"]
        return movies[:100]
    else:
        return None
    
def get_trending_movies():
    url = "https://api.themoviedb.org/3/trending/movie/day"
    params = {
        "api_key": "917968e6a5cfe116419446e1aec0d397",
        "language": "en-US",
        "page": 1
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        movies = response.json()['results']
        genres = fetch_genre_data()

        for movie in movies:
            genre_ids = movie['genre_ids']
            movie['genres'] = [genres[genre_id] for genre_id in genre_ids if genre_id in genres]

        base_image_url = "https://image.tmdb.org/t/p/w500"
        for movie in movies:
            movie["poster_url"] = base_image_url + movie["poster_path"]
        return movies[:100]
    else:
        return None
    
def get_top_viewed_movies():
    url = "https://api.themoviedb.org/3/discover/movie"
    params = {
        "api_key": "917968e6a5cfe116419446e1aec0d397",
        "language": "en-US",
        "sort_by": "vote_count.desc",
        "page": 1
    }
    response = requests.get(url, params=params)

    if response.status_code == 200:
        movies = response.json()['results']
        genres = fetch_genre_data()

        for movie in movies:
            genre_ids = movie['genre_ids']
            movie['genres'] = [genres[genre_id] for genre_id in genre_ids if genre_id in genres]

        base_image_url = "https://image.tmdb.org/t/p/w500"
        for movie in movies:
            movie["poster_url"] = base_image_url + movie["poster_path"]
        return movies[:100]
    else:
        return None

def get_upcoming_movies(api_key, date):
    # Construct the API request URL
    base_url = "https://api.themoviedb.org/3/movie/upcoming"
    params = {
        "api_key": api_key,
        "language": "en-US",
        "region": "US",
        "sort_by": "release_date.asc",
        "include_adult": False,
        "include_video": False,
        "page": 1,
        "primary_release_date.gte": date
    }
    response = requests.get(base_url, params=params)
    
    # Check if the request was successful
    if response.status_code == 200:
        upcoming_movies_data = response.json()
        upcoming_movies = upcoming_movies_data['results']
        
        # Add poster URLs to the movie data
        base_image_url = "https://image.tmdb.org/t/p/w500"
        for movie in upcoming_movies:
            if movie["poster_path"] is not None:
                movie["poster_url"] = base_image_url + movie["poster_path"]
        
        return upcoming_movies
    else:
        # Handle the error if the request was not successful
        print("Error:", response.status_code)
        return []

# Provide your TMDb API key
