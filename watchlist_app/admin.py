from django.contrib import admin
from watchlist_app.models import WatchList, StreamPlatform


class WatchListAdmin(admin.ModelAdmin):
    list_display = ('title', 'storyline', 'active', 'platform', 'created',)
    search_fields = ['title']
    list_filter = ['active', 'created']

admin.site.register(WatchList, WatchListAdmin)


class StreamPlatformAdmin(admin.ModelAdmin):
    list_display = ('name', 'about', 'website')

admin.site.register(StreamPlatform, StreamPlatformAdmin)

# Register your models here.
