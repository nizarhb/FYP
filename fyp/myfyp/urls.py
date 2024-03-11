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
    path('submit-review/', views.submit_review, name='submit_review'),
    path('delete-review/<int:review_id>/', views.delete_review, name='delete_review'),
]
