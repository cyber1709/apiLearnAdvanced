from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from rest_framework.authtoken.models import Token
from watchlist_app.models import WatchList, StreamPlatform, Review
from watchlist_app.serializers import ReviewSerializer, StreamPlatformSerializer, WatchListSerializer

class StreamPlatformTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='example', password='example')
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.stream = StreamPlatform.objects.create(name='Netflix', about='Best Platform', website='http://www.netflix.com')


    def test_streamplatform_create(self):
        data = {
            "name": "Netflix",
            "about": "Best Platform",
            "webiste" : "http://www.netflix.com"
        }
        response = self.client.post(reverse('streamplatform-list'), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_streamplatform_list(self):
        response = self.client.get(reverse('streamplatform-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_streamplatform_ind(self):
        response = self.client.get(reverse('streamplatform-detail', args=(self.stream.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK) 


class WatchListTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='example', password='example')
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.stream = StreamPlatform.objects.create(name='Netflix', about='Best Platform', website='http://www.netflix.com')
        self.watchlist = WatchList.objects.create(title='example', storyline='example', platform=self.stream)

    
    def test_watchlist_create(self):
        data = {
            "title": "example",
            "storyline": "example",
            "platform": self.stream.id
        }
        response = self.client.post(reverse('movie-list'), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_watchlist_list(self):
        response = self.client.get(reverse('movie-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_watchlist_ind(self):
        response = self.client.get(reverse('movie-detail', args=(self.watchlist.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(WatchList.objects.count(), 1)
        self.assertEqual(WatchList.objects.get().title, 'example')
        
class ReviewTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='example', password='example')
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.stream = StreamPlatform.objects.create(name='Netflix', about='Best Platform', website='http://www.netflix.com')
        self.watchlist = WatchList.objects.create(title='example', storyline='example', platform=self.stream)
        

    
    def test_review_create(self):
        data = {
            "review_user": self.user.id,
            "rating": 5,
            "description": "Great Movie",
            "watchlist": self.watchlist.id,
            "active" : True 
        }
        response = self.client.post(reverse('review-create', args=(self.watchlist.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.post(reverse('review-create', args=(self.watchlist.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Review.objects.count(), 1)
        self.assertEqual(Review.objects.get().rating, 5)
        self.assertEqual(Review.objects.get().description, 'Great Movie')
        
    def test_review_create_unauth(self):
        
        
        data = {
            "review_user": self.user.id,
            "rating": 5,
            "description": "Great Movie",
            "watchlist": self.watchlist.id,
            "active" : True 
        }
        self.client.force_authenticate(user=None)
        response = self.client.post(reverse('review-create', args=(self.watchlist.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED) 

    def test_review_list(self):
        response = self.client.get(reverse('review-list', args=(self.watchlist.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_review_ind(self):
        review = Review.objects.create(review_user=self.user, rating=5, description='Great Movie', watchlist=self.watchlist)
        response = self.client.get(reverse('review-detail', args=(review.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Review.objects.count(), 1)
        self.assertEqual(Review.objects.get().rating, 5)
        self.assertEqual(Review.objects.get().description, 'Great Movie')
    
    def test_review_update(self):
        review = Review.objects.create(review_user=self.user, rating=5, description='Great Movie', watchlist=self.watchlist)
        data = {
            "rating": 4,
            "description": "Great Movie"
        }
        response = self.client.put(reverse('review-detail', args=(review.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)