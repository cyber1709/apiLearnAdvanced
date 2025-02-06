from django.urls import path
from watchlist_app.views import movie_list, movie_description

urlpatterns = [
    path('list/', movie_list, name="movie-list"),
    path('list/<id>', movie_description, name="movie-desc")
]
