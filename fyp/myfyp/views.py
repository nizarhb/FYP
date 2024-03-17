from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .api import search_movies,search_movies_with_cast, get_top_rated_movies, get_latest_movies, get_popular_shows, get_trending_movies,get_top_viewed_movies,get_related_movies,get_upcoming_movies
import requests
import datetime
from .models import Review
import numpy as np
from collections import defaultdict


def search_view(request):
    query = request.GET.get('query')
    movie_results = search_movies(query)
    cast_results =search_movies_with_cast(query)
    url = 'https://api.themoviedb.org/3/genre/movie/list'
    params = {
        'api_key': '917968e6a5cfe116419446e1aec0d397',  # Replace with your TMDB API key
        'language': 'en-US',
    }

    response = requests.get(url, params=params)
    data = response.json()
    categories = data.get('genres', [])

    return render(request, 'search_results.html', {'movie_results': movie_results, 'categories': categories, 'cast_results':cast_results})
def generate_movie_recommendations(user):
    # Step 1: Retrieve all reviews
    reviews = Review.objects.all()

    # Step 2: Group reviews by movie ID
    reviews_by_movie = defaultdict(list)
    for review in reviews:
        reviews_by_movie[review.movie_id].append(review)

    # Step 3: Find users with similar ratings
    similar_ratings = []
    for movie_reviews in reviews_by_movie.values():
        for i, review1 in enumerate(movie_reviews):
            for j in range(i + 1, len(movie_reviews)):
                review2 = movie_reviews[j]

                # If ratings are similar, add them to the list
                if review1.rating == review2.rating:
                    similar_ratings.append((review1, review2))

    # Step 4: Extract unique movie IDs for recommendation
    recommended_movies = set()
    for review1, review2 in similar_ratings:
        recommended_movies.update([review.movie_id for review in review1.user.review_set.all()])

    # Step 5: Remove rated movies by the user
    rated_movies = [review.movie_id for review in user.review_set.all()]
    recommended_movies -= set(rated_movies)

    # Step 6: Fetch movie details from the TMDB API
    recommended_movie_details = fetch_movie_details(recommended_movies)

    return recommended_movie_details
# Create your views here.

def fetch_movie_details(movie_ids):
    movie_details = []

    for movie_id in movie_ids:
        # Make an API request to fetch movie details
        response = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=917968e6a5cfe116419446e1aec0d397")

        if response.status_code == 200:
            # Parse the response JSON
            movie_data = response.json()

            # Extract the relevant movie details
            movie_title = movie_data['title']
            movie_genres = [genre['name'] for genre in movie_data['genres']]
            movie_overview = movie_data['overview']
            movie_poster_url = f"https://image.tmdb.org/t/p/w500/{movie_data['poster_path']}"

            # Create a dictionary with the movie details
            movie_detail = {
                'id': movie_id,
                'title': movie_title,
                'genres': movie_genres,
                'overview': movie_overview,
                'poster_url': movie_poster_url
            }

            movie_details.append(movie_detail)

    return movie_details
def submit_review(request):
    if request.method == 'POST':
        # Retrieve form data
        movie_id = request.POST.get('movie_id')
        review_text = request.POST.get('review_text')
        rating = int(request.POST.get('rating'))
        # Create a new Review object
        review = Review.objects.create(
            movie_id=movie_id,
            rating=rating,
            user=request.user,
            review_text=review_text
        )

        # Redirect to the movie detail page or any other appropriate page
        return redirect('movie-details', movie_id=movie_id)

    # Handle GET requests if needed
    # ...

def get_logged_in_user(request):
    # Assuming you are using Django's built-in authentication system
    if request.user.is_authenticated:
        return request.user
    else:
        return None

def index(request):
    user_reviews = Review.objects.all().values("movie_id", "user", "rating", "review_text", "created_at")
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
    recommendation=generate_movie_recommendations(request.user)
    return render(request, 'index.html',{'recommendation':recommendation, 'top_rated_movies': top_rated_movies[:3], 'latest_movies': latest_movies[:3],'popular_shows':popular_shows[:3],'trending_movies':trending_movies[:3],'top_views':top_views[:3],'categories': categories})

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
        reviews = Review.objects.filter(movie_id=movie_id)
        return render(request, 'movie-details.html', {'movie': movie,'categories':categories,'related_movies':related_movies[:5],'reviews': reviews})
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

def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    review.delete()
    return redirect('movie-details', movie_id=review.movie_id)