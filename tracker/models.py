from django.db import models
from django.contrib.auth.models import User
from django.core.files import File
import urllib, os

# Create your models here.
class Series(models.Model):
    DAYS_CHOICES = (
        ('MONDAY', 'Monday'),
        ('TUEDAY', 'Tuesday'),
        ('WEDNESDAY', 'Wednesday'),
        ('THURSDAY', 'Thursday'),
        ('FRIDAY', 'Friday'),
        ('SATURDAY', 'Saturday'),
        ('SUNDAY', 'Sunday'),
        ('UNKNOWN', 'Unknown'),
        )
    title = models.CharField(max_length=200, help_text='The title of the series.')
    description = models.TextField(max_length=500, blank=True, help_text='Optional: Description of the series', default='No description provided.')
    release_day = models.CharField(max_length=10, help_text='Release day, e.g., Monday', choices=DAYS_CHOICES)
    sumbmitted_user = models.ForeignKey('UserProfile')
    stream_site = models.URLField(blank=True, help_text='URL to view this series.')
    cover_image = models.ImageField(upload_to='series_imgs', blank=True)
    
    def cache(self):
        if not self.cover_image:
            self.url = 'https://docs.djangoproject.com/s/img/small-fundraising-heart.png'
            img = urllib.urlretrieve(self.url)
            self.cover_image.save(
                    os.path.basename(self.url),
                    File(open(img[0], 'rb'))
                    )
            super(Series, self).save()
    
    def __unicode__(self):
        return self.title
    
    class Meta:
        verbose_name_plural = 'series'


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    
    def __unicode__(self):
        return self.user.username
    