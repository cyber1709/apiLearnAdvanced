from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from watchlist_app.models import WatchList, StreamPlatform, Review
from watchlist_app.serializers import WatchListSerializer, StreamPlatformSerializer, ReviewSerializer
from rest_framework import generics, mixins
from rest_framework import viewsets
from django.core.exceptions import ValidationError




from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from watchlist_app.models import WatchList, Review
from watchlist_app.serializers import ReviewSerializer
from rest_framework.permissions import IsAuthenticated
from watchlist_app .permissions import AdminOrReadOnly


class ReviewCreate(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    # permission_classes = [IsAuthenticated]
    

    def get_queryset(self):
        return Review.objects.all()

    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        watchlist = WatchList.objects.get(pk=pk)

        review_user = self.request.user
        review_queryset = Review.objects.filter(watchlist=watchlist, review_user=review_user)

        if review_queryset.exists():
            raise ValidationError({"error": "You have already reviewed this movie"})  # Dictionary format ensures proper JSON response
        
        serializer.save(watchlist=watchlist, review_user=review_user)


class ReviewList(generics.ListAPIView):

    # queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_queryset(self):
        pk = self.kwargs['pk']
        return Review.objects.filter(watchlist=pk)

class ReviewListDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    permission_classes = [AdminOrReadOnly]
    serializer_class = ReviewSerializer
    lookup_field = "pk" 


class WatchListAV(generics.ListCreateAPIView):
    queryset = WatchList.objects.all()
    serializer_class = WatchListSerializer

class WatchListDetailAV(generics.RetrieveUpdateDestroyAPIView):
    queryset = WatchList.objects.all()
    serializer_class = WatchListSerializer
    lookup_field = "pk"



class StreamPlatformAV(viewsets.ModelViewSet):
    queryset = StreamPlatform.objects.all()
    serializer_class = StreamPlatformSerializer


# class StreamPlatformAV(generics.ListCreateAPIView):
#     queryset = StreamPlatform.objects.all()
#     serializer_class = StreamPlatformSerializer

# class StreamPlatformDetailsAV(generics.RetrieveUpdateDestroyAPIView):    
#     queryset = StreamPlatform.objects.all()
#     serializer_class = StreamPlatformSerializer
#     lookup_field = "pk"

