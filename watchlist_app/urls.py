from django.urls import path
from watchlist_app.views import WatchListAV, WatchListDetailAV

urlpatterns = [
    path('list/', WatchListAV.as_view() , name="movie-list"),
    path('list/<id>', WatchListDetailAV.as_view() , name="movie-desc")
]
