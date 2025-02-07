from django.shortcuts import render
from watchlist_app.models import WatchList, StreamPlatform
from django.http  import JsonResponse
from django.core import serializers
from watchlist_app.serializers import WatchListSerializer, StreamPlatformSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.views import APIView

class WatchListAV(APIView):

    def get(self, request):
        shows = WatchList.objects.all()
        serializers =  WatchListSerializer(shows, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)
     
    def post(self, request):
        serializer = WatchListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class WatchListDetailAV(APIView):

    def get(self, request, id):
        try:
            movie = WatchList.objects.get(id=id)
        except WatchList.DoesNotExist:
            return Response({'Error': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = WatchListSerializer(movie)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, id):
        movie = WatchList.objects.get(id=id)
        serializer = WatchListSerializer(movie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    
    def delete(self, request, id):
        movie = WatchList.objects.get(id=id)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


 

class StreamPlatformAV(APIView):
    
    def get(self, request):
        platforms = StreamPlatform.objects.all()
        serializer = StreamPlatformSerializer(platforms, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = StreamPlatformSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
class StreamPlatformDetailsAV(APIView):
    
    def get(self,request,id):
        platform = StreamPlatform.objects.get(id=id)
        serializer = StreamPlatformSerializer(platform)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, id):
        platform = StreamPlatform.objects.get(id=id)
        serializer = StreamPlatformSerializer(platform, request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id):
        platform = StreamPlatform.objects.get(id=id)
        platform.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)