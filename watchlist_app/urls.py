from django.urls import path
from watchlist_app.views import WatchListAV, WatchListDetailAV, StreamPlatformAV, StreamPlatformDetailsAV

urlpatterns = [
    path('list/', WatchListAV.as_view() , name="movie-list"),
    path('list/<id>', WatchListDetailAV.as_view() , name="movie-desc"),
    path('platform/', StreamPlatformAV.as_view(), name="streaming-platforms"),
    path('platform/<id>', StreamPlatformDetailsAV.as_view(), name='stream-platform-details')
    
]
