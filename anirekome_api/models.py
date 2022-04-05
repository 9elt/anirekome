from django.db import models


class Anime(models.Model):
    anime_id = models.IntegerField(primary_key=True)
    anime_title = models.CharField(max_length=256)
    anime_picture = models.CharField(max_length=100)
    anime_date = models.CharField(max_length=4, null=True)
    anime_mean = models.DecimalField(max_digits=5, decimal_places=2)
    anime_status = models.CharField(max_length=64)
    anime_rating = models.CharField(max_length=32, null=True)
    anime_episodes = models.CharField(max_length=4, null=True)
    anime_genres = models.JSONField(null=True)    
    anime_related = models.JSONField(null=True)

class UserList(models.Model):
    user_name = models.CharField(max_length=64, primary_key=True)
    user_list = models.JSONField()

class UserModel(models.Model):
    user_name = models.CharField(max_length=64, primary_key=True)
    fav_dates = models.JSONField()
    fav_episodes = models.JSONField()
    fav_ratings = models.JSONField()
    fav_genres = models.JSONField()
    fav_themes = models.JSONField()
    fav_demographics = models.JSONField()