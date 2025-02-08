from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from watchlist_app.models import WatchList, StreamPlatform, Review
from watchlist_app.serializers import WatchListSerializer, StreamPlatformSerializer, ReviewSerializer
from rest_framework import generics, mixins
from rest_framework import viewsets



class ReviewCreate(generics.CreateAPIView):
    serializer_class = ReviewSerializer

    def perform_create(self, serializer):
        pk= self.kwargs.get('pk')
        watchlist = WatchList.objects.get(pk=pk)
        serializer.save(watchlist=watchlist)


class ReviewList(generics.ListAPIView):

    # queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_queryset(self):
        pk = self.kwargs['pk']
        return Review.objects.filter(watchlist=pk)

class ReviewListDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
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

