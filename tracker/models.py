from django.db import models
from django.contrib.auth.models import User

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
    description = models.TextField(max_length=500, blank=True, help_text='Optional: Description of the series',
                                   default='No description provided.')
    release_day = models.CharField(max_length=10, help_text='Release day, e.g., Monday', choices=DAYS_CHOICES)
    submitted_user = models.ForeignKey(User)
    stream_site = models.URLField(blank=True, help_text='URL to view this series.')
    cover_image_url = models.URLField(blank=True, help_text='Cover image URL.')

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'series'


