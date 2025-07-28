from rest_framework import serializers

class MovieSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=255)
    overview = serializers.CharField()
    poster_path = serializers.CharField(allow_null=True, required=False)
    release_date = serializers.DateField(allow_null=True, required=False)
    vote_average = serializers.FloatField(allow_null=True, required=False)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if representation.get('poster_path'):
            # TMDb base image URL
            representation['poster_url'] = f"https://image.tmdb.org/t/p/w500{representation['poster_path']}"
        else:
            representation['poster_url'] = None
        return representation
