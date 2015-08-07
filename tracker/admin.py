from django.contrib import admin

from tracker.models import Series, FavoriteSites, UserProfile
# Register your models here.
admin.site.register(Series)
admin.site.register(FavoriteSites)
admin.site.register(UserProfile)