from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from .models import FavoriteMovie


class FavoriteMovieSerializer(serializers.ModelSerializer):
    movie_url = serializers.SerializerMethodField()

    class Meta:
        model = FavoriteMovie
        fields = ["id", "movie_id", "title", "poster_path", "added_at", "movie_url"]
        read_only_fields = [
            "user",
            "title",
            "poster_path",
            "added_at",
        ]  # These will be set by the view

    @extend_schema_field(serializers.CharField(allow_null=True))
    def get_movie_url(self, obj) -> str | None:
        # Construct the full TMDb image URL if poster_path exists
        if obj.poster_path:
            return f"https://image.tmdb.org/t/p/w500{obj.poster_path}"
        return None
