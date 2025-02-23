from rest_framework import generics, viewsets, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from watchlist_app.models import WatchList, StreamPlatform, Review
from watchlist_app.serializers import WatchListSerializer, StreamPlatformSerializer, ReviewSerializer
from watchlist_app.permissions import IsAdminOrReadOnly, ReviewUserOrReadOnly
from rest_framework.authentication import TokenAuthentication
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from watchlist_app.throttling import ReviewCreateThrottle, ReviewListThrottle


class ReviewCreate(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    throttle_classes = [ReviewCreateThrottle]

    def get_queryset(self):
        return Review.objects.all()

    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        watchlist = WatchList.objects.get(pk=pk)
        review_user = self.request.user
        
        if Review.objects.filter(watchlist=watchlist, review_user=review_user).exists():
            raise ValidationError({"error": "You have already reviewed this movie."})
        
        if watchlist.number_rating == 0:
            watchlist.avg_rating = serializer.validated_data['rating'] 
            watchlist.number_rating = 1
            watchlist.save()
        else:
            watchlist.number_rating = watchlist.number_rating + 1
            watchlist.avg_rating = (watchlist.avg_rating + serializer.validated_data['rating']) / watchlist.number_rating
            
            watchlist.save()
        
        serializer.save(watchlist=watchlist, review_user=review_user)


class ReviewList(generics.ListAPIView):
    serializer_class = ReviewSerializer
    
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    throttle_classes = [ReviewListThrottle]
    
    def get_queryset(self):
        return Review.objects.filter(watchlist=self.kwargs['pk'])


class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAdminOrReadOnly, ReviewUserOrReadOnly]
    lookup_field = "pk"


class WatchListAV(generics.ListCreateAPIView):
    
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    
    queryset = WatchList.objects.all()
    serializer_class = WatchListSerializer


class WatchListDetailAV(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminOrReadOnly]
    queryset = WatchList.objects.all()
    
    serializer_class = WatchListSerializer
    lookup_field = "pk"


class StreamPlatformAV(viewsets.ModelViewSet):
    
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminOrReadOnly, IsAuthenticated]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    
    queryset = StreamPlatform.objects.all()
    serializer_class = StreamPlatformSerializer