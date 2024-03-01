from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .api import get_top_rated_movies, get_latest_movies, get_popular_shows, get_trending_movies,get_top_viewed_movies,get_related_movies,get_upcoming_movies
import requests
import datetime
# Create your views here.



def index(request):
    top_rated_movies = get_top_rated_movies()
    latest_movies=get_latest_movies()
    popular_shows=get_popular_shows()
    trending_movies=get_trending_movies()
    top_views=get_top_viewed_movies()
    url = 'https://api.themoviedb.org/3/genre/movie/list'
    params = {
        'api_key': '917968e6a5cfe116419446e1aec0d397',  # Replace with your TMDB API key
        'language': 'en-US',
    }

    response = requests.get(url, params=params)
    data = response.json()
    categories = data.get('genres', [])
    return render(request, 'index.html',{'top_rated_movies': top_rated_movies[:3], 'latest_movies': latest_movies[:3],'popular_shows':popular_shows[:3],'trending_movies':trending_movies[:3],'top_views':top_views[:3],'categories': categories})

def category(request, category_name):
    genre_search_url = 'https://api.themoviedb.org/3/genre/movie/list'
    genre_search_params = {
        'api_key': '917968e6a5cfe116419446e1aec0d397',  # Replace with your TMDB API key
        'language': 'en-US',
    }

    genre_search_response = requests.get(genre_search_url, params=genre_search_params)
    genre_search_data = genre_search_response.json()
    genres = genre_search_data.get('genres', [])

    selected_genre = None
    for genre in genres:
        if genre['name'].lower() == category_name.lower():
            selected_genre = genre
            break

    if not selected_genre:
        # Handle the case where the selected genre is not found
        return render(request, 'category_not_found.html')

    movies_url = f'https://api.themoviedb.org/3/discover/movie'
    movies_params = {
        'api_key': '917968e6a5cfe116419446e1aec0d397',  # Replace with your TMDB API key
        'language': 'en-US',
        'with_genres': selected_genre['id'],
        'include_image_language': 'en,null',  # Include image URLs in English
    }

    movies_response = requests.get(movies_url, params=movies_params)
    movies_data = movies_response.json()
    movies = movies_data.get('results', [])
    base_image_url = "https://image.tmdb.org/t/p/w500"
    for movie in movies:
        movie["poster_url"] = base_image_url + movie["poster_path"]
    url = 'https://api.themoviedb.org/3/genre/movie/list'
    params = {
        'api_key': '917968e6a5cfe116419446e1aec0d397',  # Replace with your TMDB API key
        'language': 'en-US',
    }
    top_views=get_top_viewed_movies()
    response = requests.get(url, params=params)
    data = response.json()
    categories = data.get('genres', [])
    return render(request, 'categories.html', {'category_name': category_name, 'movies': movies[:10],'categories':categories,'top_views':top_views[:3]})

def movie_details(request, movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}"
    params = {
        "api_key": "917968e6a5cfe116419446e1aec0d397",
        "language": "en-US"
    }
    response = requests.get(url, params=params)
    genres_url = 'https://api.themoviedb.org/3/genre/movie/list'
    genres_params = {
        'api_key': '917968e6a5cfe116419446e1aec0d397',  # Replace with your TMDB API key
        'language': 'en-US',
    }
    related_movies = get_related_movies(movie_id)
    genres_response = requests.get(genres_url, params=genres_params)
    genres_data = genres_response.json()
    categories = genres_data.get('genres', [])
    if response.status_code == 200:
        movie = response.json()
        
        base_image_url = "https://image.tmdb.org/t/p/w500"
        movie["poster_url"] = base_image_url + movie["poster_path"]
        return render(request, 'movie-details.html', {'movie': movie,'categories':categories,'related_movies':related_movies[:5]})
    else:
        return render(request, 'error.html', {'message': 'Failed to retrieve movie details.'})
def signup(request):
    url = 'https://api.themoviedb.org/3/genre/movie/list'
    params = {
        'api_key': '917968e6a5cfe116419446e1aec0d397',  # Replace with your TMDB API key
        'language': 'en-US',
    }

    response = requests.get(url, params=params)
    data = response.json()
    categories = data.get('genres', [])
    if request.method=="POST":
        email= request.POST['email']
        username= request.POST['username']
        password= request.POST['password']
        if User.objects.filter(email=email).exists():
            messages.info(request,"Email Already Used!")
            return redirect('signup')
        elif User.objects.filter(username=username).exists():
            messages.info(request,"Username Already Used!")
            return redirect('signup')
        else:
            user=User.objects.create_user(username=username, email=email, password=password)
            user.save
            return redirect('index')
    else:
        return render(request, 'signup.html', {'categories': categories})
    
def login(request):
    url = 'https://api.themoviedb.org/3/genre/movie/list'
    params = {
        'api_key': '917968e6a5cfe116419446e1aec0d397',  # Replace with your TMDB API key
        'language': 'en-US',
    }

    response = requests.get(url, params=params)
    data = response.json()
    categories = data.get('genres', [])
    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['password']
        user= auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request,user)
            return redirect('/')
        else:
            messages.info(request, "Invalid Credentials!")
            return redirect('login')
    else:
        return render(request, 'login.html',{'categories': categories})
    

def blog(request):

    url = 'https://api.themoviedb.org/3/genre/movie/list'
    params = {
        'api_key': '917968e6a5cfe116419446e1aec0d397',  # Replace with your TMDB API key
        'language': 'en-US',
    }

    response = requests.get(url, params=params)
    data = response.json()
    categories = data.get('genres', [])
     # Retrieve the upcoming movies
    
    api_key = "917968e6a5cfe116419446e1aec0d397"

# Get the current date
    current_date = datetime.date.today()

    upcoming_movies = get_upcoming_movies(api_key,current_date)

    # Render the template with the upcoming movies
    context = {
        'upcoming_movies': upcoming_movies,
        'categories': categories
    }
    return render(request, 'blog.html', context)
def movie(request):
    return render( request, 'movie-details.html')

def logout(request):
    auth.logout(request)
    return redirect('/')