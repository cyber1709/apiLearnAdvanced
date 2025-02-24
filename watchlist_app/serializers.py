from rest_framework import serializers
from watchlist_app.models import WatchList, StreamPlatform, Review

# class MovieSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     name = serializers.CharField()
#     description = serializers.CharField()
#     active = serializers.BooleanField()
    
#     def create(self, validated_data):
#         return Movie.objects.create(**validated_data)
    
#     def update(self, instance, validated_data):
#         instance.name = validated_data.get('name', instance.name)
#         instance.description = validated_data.get('description', instance.description)
#         instance.active = validated_data.get('active', instance.active)
#         instance.save()
#         return instance
    
    
#     def validate(self, data):
#         if data['name'] == data['description']:
#             raise serializers.ValidationError("Description and title should not be same")
#         else:
#             return data
    
#     def validate_name(self, value):
#         if len(value) < 2:
#             raise serializers.ValidationError("Name is too short")
#         else:
#             return value

class ReviewSerializer(serializers.ModelSerializer):

    review_user = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = Review
        # fields = '__all__'
        exclude = ('watchlist',)
        read_only_fields = ['id']        

class WatchListSerializer(serializers.ModelSerializer):

    reviews = ReviewSerializer(many=True, read_only=True)
    
    class Meta:
        model = WatchList
        fields = '__all__'
        read_only_fields = ['id']
        
    

class StreamPlatformSerializer(serializers.ModelSerializer):

    watchlist = WatchListSerializer(many=True, read_only=True)

    class Meta:
        model = StreamPlatform
        fields = '__all__'
        read_only_fields = ['id']

    def validate(self, data):
        """
        Validate uniqueness of platform name and website.
        """
        if StreamPlatform.objects.filter(name=data['name']).exists():
            raise serializers.ValidationError({'name': 'Platform name must be unique!'})

        if StreamPlatform.objects.filter(website=data['website']).exists():
            raise serializers.ValidationError({'website': 'Website must be unique!'})

        return data