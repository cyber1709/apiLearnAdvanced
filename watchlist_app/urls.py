from django.urls import path
from watchlist_app.views import WatchListAV, WatchListDetailAV, StreamPlatformAV, StreamPlatformDetailsAV

urlpatterns = [
    path('list/', WatchListAV.as_view(), name="movie-list"),
    path('list/<int:pk>', WatchListDetailAV.as_view(), name="movie-detail"),
    path('platform/', StreamPlatformAV.as_view(), name="streaming-platforms"),
    path('platform/<int:pk>', StreamPlatformDetailsAV.as_view(), name='streamplatform-detail'),
]
