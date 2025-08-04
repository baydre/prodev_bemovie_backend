from django.contrib.auth.models import User
from django.db import models


class FavoriteMovie(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="favorite_movies"
    )
    movie_id = models.IntegerField(db_index=True)
    title = models.CharField(max_length=255)
    poster_path = models.CharField(max_length=255, null=True, blank=True)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "movie_id")
        ordering = ["-added_at"]

    def __str__(self):
        return f"{self.user.username}'s favorite: {self.title} (ID: {self.movie_id})"
