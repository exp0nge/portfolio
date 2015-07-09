from django import forms

from tracker.models import Series


class SeriesForm(forms.ModelForm):
    class Meta:
        model = Series
        fields = ('title', 'description', 'release_day', 'current_episode', 'stream_site', 'cover_image_url')
