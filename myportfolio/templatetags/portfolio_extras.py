from django import template
from myportfolio.models import Project

register = template.Library()

@register.inclusion_tag('myportfolio/projects.html')
def get_projects_list(act_project=None):
    return {'projects_list': Project.objects.all(), 'act_project': act_project}
