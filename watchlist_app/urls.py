from django.urls import path, include
from rest_framework.routers import DefaultRouter
from watchlist_app.views import (
    WatchListAV, WatchListDetailAV, StreamPlatformAV, 
    ReviewList, ReviewDetail, ReviewCreate, UserReview,
    UserReviewAboveRating
)
from django.urls import path, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


router = DefaultRouter()
router.register('platform', StreamPlatformAV, basename='streamplatform')

schema_view = get_schema_view(
    openapi.Info(
        title="IMDB API",
        default_version="v1",
        description="API documentation",
        terms_of_service="https://your-terms-url.com",
        contact=openapi.Contact(email="support@example.com"),
        license=openapi.License(name="BSD Lisence"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)




urlpatterns = [
    path('list/', WatchListAV.as_view(), name="movie-list"),
    path('<int:pk>/', WatchListDetailAV.as_view(), name="movie-detail"),
    path('', include(router.urls)),
    path('<int:pk>/review-create/', ReviewCreate.as_view(), name='review-create'),
    path('<int:pk>/review/', ReviewList.as_view(), name='review-list'),
    path('review/<int:pk>/', ReviewDetail.as_view(), name='review-detail'),

    # path('review/<str:username>/', UserReview.as_view(), name='user-review-detail'),
    path('review/', UserReview.as_view(), name='user-review-detail'),
    path('review-above-rating/', UserReviewAboveRating.as_view(), name='user-review-above-rating'),
    
    
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),


] 