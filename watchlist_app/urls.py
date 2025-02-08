from django.urls import path, include
from watchlist_app.views import (WatchListAV, WatchListDetailAV, StreamPlatformAV, 
                                  ReviewList, ReviewListDetail,
                                 ReviewCreate )

from rest_framework.routers import DefaultRouter
router = DefaultRouter()

router.register('platform', StreamPlatformAV, basename='streamplatform')

urlpatterns = [
    path('list/', WatchListAV.as_view(), name="movie-list"),
    path('list/<int:pk>', WatchListDetailAV.as_view(), name="movie-detail"),
    # path('platform/', StreamPlatformAV.as_view(), name="streaming-platforms"),
    # path('platform/<int:pk>', StreamPlatformDetailsAV.as_view(), name='streamplatform-detail'),
    path('', include(router.urls)),

    path('platform/<int:pk>/review-create/', ReviewCreate.as_view(), name='review-list'),
    path('platform/<int:pk>/review/', ReviewList.as_view(), name='review-list'),
    path('platform/review/<int:pk>', ReviewListDetail.as_view(), name='review-detail'),
    
    
    # path('review/', ReviewAV.as_view(), name='review-list'),
    # path('review/<int:pk>', ReviewDetailAV.as_view(), name='review-detail'),


]
