from django.urls import path, include
from rest_framework.routers import DefaultRouter
from watchlist_app.views import (
    WatchListAV, WatchListDetailAV, StreamPlatformAV, 
    ReviewList, ReviewDetail, ReviewCreate
)

router = DefaultRouter()
router.register('platform', StreamPlatformAV, basename='streamplatform')

urlpatterns = [
    path('list/', WatchListAV.as_view(), name="movie-list"),
    path('<int:pk>/', WatchListDetailAV.as_view(), name="movie-detail"),
    path('', include(router.urls)),
    path('<int:pk>/review-create/', ReviewCreate.as_view(), name='review-create'),
    path('<int:pk>/review/', ReviewList.as_view(), name='review-list'),
    path('review/<int:pk>/', ReviewDetail.as_view(), name='review-detail'),
] 