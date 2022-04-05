from django.contrib import admin

from .models import Anime, UserList, UserModel

admin.site.register(Anime)
admin.site.register(UserList)
admin.site.register(UserModel)