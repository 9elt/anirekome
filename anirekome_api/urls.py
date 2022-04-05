from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('privacy', views.privacy, name='privacy'),
    path('terms', views.terms, name='terms'),
    path('rekome', views.getRekome, name='rekome'),
    path('more', views.moreRekome, name='more'),
    path('refresh', views.refreshRekome, name='refresh'),
    path('trash', views.trashRekome, name='trash'),
    path('disconnect', views.disconnectUser, name='disconnect'),
]
