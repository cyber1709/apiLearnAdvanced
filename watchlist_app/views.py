from django.shortcuts import render
from watchlist_app.models import Movie
from django.http  import JsonResponse
from django.core import serializers
from watchlist_app.serializers import MovieSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
# Create your views here.



@api_view(['GET', 'POST'])
def movie_list(request):
    if request.method == 'GET':
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)
    
    if request.method == 'POST':
        serializer = MovieSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,  status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def movie_description(request, id):
    
    if request.method == 'GET':
        
        try:
            movie_desc = Movie.objects.get(id=id)
        except Movie.DoesNotExist:
            return Response({'Error': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = MovieSerializer(movie_desc, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    if request.method == 'PUT':
        movie_desc = Movie.objects.filter(id=id).first()
        serializer = MovieSerializer(movie_desc, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
            
    if request.method == 'DELETE':
        movie = Movie.objects.filter(id=id)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        
    