from django.contrib import admin

from tracker.models import Series, FavoriteSites
# Register your models here.
admin.site.register(Series)
admin.site.register(FavoriteSites)