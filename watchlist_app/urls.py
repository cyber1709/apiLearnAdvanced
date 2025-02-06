from django.urls import path
from watchlist_app.views import MovieListAV, MovieDetailAV

urlpatterns = [
    path('list/', MovieListAV.as_view() , name="movie-list"),
    path('list/<id>', MovieDetailAV.as_view() , name="movie-desc")
]
