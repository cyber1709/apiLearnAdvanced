from django.shortcuts import render
from watchlist_app.models import Movie
from django.http  import JsonResponse
from django.core import serializers
from watchlist_app.serializers import MovieSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
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
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def movie_description(request, id):
    
    if request.method == 'GET':
        movie_desc = Movie.objects.filter(id=id)
        serializer = MovieSerializer(movie_desc, many=True)
        return Response(serializer.data)
    
    if request.method == 'PUT':
        movie_desc = Movie.objects.filter(id=id).first()
        serializer = MovieSerializer(movie_desc, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        
            
    if request.method == 'DELETE':
        movie = Movie.objects.filter(id=id)
        movie.delete()
        return Response()
        
    