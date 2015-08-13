from django.db import models
from django.contrib.auth.models import User

import urllib, json
from datetime import time

temp_user = User
temp_time = time(0)

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User)
    
    def __unicode__(self):
        return str(self.user)
    
class FavoriteSites(models.Model):
    site_url = models.URLField(default='')
    submitted_user = models.ForeignKey(User, default=temp_user)
    
    def __unicode__(self):
        return str(self.site_url)
        
    class Meta:
        verbose_name_plural = 'Favorite Sites'

def get_wiki_description(title):
    url = "https://en.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&exintro=&explaintext=&titles=" + urllib.quote(title)
    response = urllib.urlopen(url)
    data = json.loads(response.read())
    description = 'No description provided. I was unable to autogenerate one.'
    try:
        description = data['query']['pages'].values()[0]['extract']
    except KeyError:
        pass
    return description


class Series(models.Model):
    DAYS_CHOICES = (
        ('MONDAY', 'Monday'),
        ('TUESDAY', 'Tuesday'),
        ('WEDNESDAY', 'Wednesday'),
        ('THURSDAY', 'Thursday'),
        ('FRIDAY', 'Friday'),
        ('SATURDAY', 'Saturday'),
        ('SUNDAY', 'Sunday'),
        ('UNKNOWN', 'Unknown'),
    )
    title = models.CharField(max_length=200, help_text='The title of the series.')
    description = models.TextField(max_length=200, blank=True, help_text='Optional: Description of the series',
                                   default='No description provided.')
    release_day = models.CharField(max_length=10, help_text='Release day, e.g., Monday', choices=DAYS_CHOICES)
    submitted_user = models.ForeignKey(User, default=temp_user)
    stream_site = models.URLField(blank=True, help_text='URL to view this series.')
    cover_image_url = models.URLField(blank=True, help_text='Cover image URL.')
    current_episode = models.IntegerField(help_text='Current episode you are on.', default=1)
    tag = models.CharField(max_length=30, help_text='Relevent tag for the series, e.g., anime. Helps with generating a cover image.', default='anime')
    time = models.TimeField(blank=True, help_text='Time when the show airs', default=temp_time)
    season = models.IntegerField(default=1, blank=True, help_text='Season currently on.')
    public = models.BooleanField(default=False, blank=True)
    
    def __unicode__(self):
        return self.title

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.title = self.title[0].upper() + self.title[1:]
        if self.description == 'No description provided.':
            self.description = get_wiki_description(self.title)
        super(Series, self).save()

    class Meta:
        verbose_name_plural = 'series'

