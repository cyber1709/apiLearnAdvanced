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
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from watchlist_app.pagination import WatchListLOPagination
 


class UserReview(generics.ListAPIView):
    serializer_class = ReviewSerializer
    # permission_classes = [IsAuthenticated]
    # authentication_classes = [TokenAuthentication]

    filter_backends = [DjangoFilterBackend] 
    filterset_fields = ['review_user__username', 'active']
    
    # def get_queryset(self):
    #     username = self.kwargs['username']
    #     return Review.objects.filter(review_user__username=username)

    # def get_queryset(self):
    #     username = self.request.query_params.get('username', None)
    #     if username is not None:
    #         if Review.objects.filter(review_user__username=username).exists():
    #             return Review.objects.filter(review_user__username=username)
    #         else:
    #             raise ValidationError({"error": "No review found for this user."})

               

class UserReviewAboveRating(generics.ListAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    
    def get_queryset(self):
        rating = self.request.query_params.get('rating', None)
        if rating is not None:
            if Review.objects.filter(rating__gte=rating).exists():
                return Review.objects.filter(rating__gte=rating)
            else:
                raise ValidationError({"error": "No review found for this rating."})
        else:
                raise ValidationError({'error': 'Wrong parameter passed.'})
        


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
    # throttle_classes = [ReviewListThrottle]
    
    filter_backends = [DjangoFilterBackend] 
    filterset_fields = ['review_user__username', 'active']
    
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
    pagination_class = WatchListLOPagination
    
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
    # throttle_classes = [UserRateThrottle, AnonRateThrottle]
    
    """
    code for filtering
    """
    
    # filter_backends = [DjangoFilterBackend] 
    # filterset_fields = ['name','about']
    
    """ Code for searching
    ^ - Starts-with-search
    = - Exact matching
    @ - full text search
    $ - Regex seach
    
    search_fields = ['=username', '=email']
    
    """
    
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'about', 'website']
    
    queryset = StreamPlatform.objects.all()
    serializer_class = StreamPlatformSerializer