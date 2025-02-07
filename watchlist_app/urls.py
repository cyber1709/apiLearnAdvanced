from django.urls import path
from watchlist_app.views import WatchListAV, WatchListDetailAV, StreamPlatformAV, StreamPlatformDetailsAV

urlpatterns = [
    path('list/', WatchListAV.as_view(), name="movie-list"),
    path('list/<int:id>', WatchListDetailAV.as_view(), name="movie-detail"),
    path('platform/', StreamPlatformAV.as_view(), name="streaming-platforms"),
    path('platform/<int:id>', StreamPlatformDetailsAV.as_view(), name='stream-platform-details'),
]
