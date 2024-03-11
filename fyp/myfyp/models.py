from django.db import models
from django.contrib.auth.models import User

class Review(models.Model):
    movie_id = models.IntegerField()  # ID of the movie
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)], null=True)
    review_text = models.TextField(max_length=500)  # Textual review by the user
    created_at = models.DateTimeField(auto_now_add=True)
