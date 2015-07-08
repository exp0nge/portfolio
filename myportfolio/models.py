from django.db import models
from django.template.defaultfilters import slugify


class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=500)
    slug = models.SlugField(unique=True)
    github_url = models.URLField(default='https://github.com')
    lang_type = models.CharField(max_length=50)
    site_url = models.URLField(blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Project, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.title
