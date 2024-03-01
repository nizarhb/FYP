from django.urls import path 
from . import views
urlpatterns=[
    path('', views.index, name='index'),
    path('signup',views.signup, name='signup'), 
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('category/<str:category_name>/', views.category, name='category'),
    path('movie-details/<int:movie_id>/', views.movie_details, name='movie-details'),
    path('blog', views.blog, name='blog'), 
]
