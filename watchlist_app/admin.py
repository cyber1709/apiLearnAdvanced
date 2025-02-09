from django.contrib import admin
from watchlist_app.models import WatchList, StreamPlatform, Review


class WatchListAdmin(admin.ModelAdmin):
    list_display = ('title', 'storyline', 'active', 'platform', 'created',)
    search_fields = ['title']
    list_filter = ['active', 'created']

admin.site.register(WatchList, WatchListAdmin)


class StreamPlatformAdmin(admin.ModelAdmin):
    list_display = ('name', 'about', 'website')

admin.site.register(StreamPlatform, StreamPlatformAdmin)

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('review_user', 'rating', 'description', 'watchlist', 'active', 'created', 'updated')
    list_filter = ['active', 'rating']
    search_fields = ['watchlist__title']

admin.site.register(Review, ReviewAdmin)

# Register your models here.
