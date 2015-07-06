from django.shortcuts import render

from myportfolio.models import Project

def index(request):
    context_dict = {}
    p_list = Project.objects.all()
    context_dict['projects'] = p_list
    projects = {}
    for p in p_list:
        projects['project_title'] = p.title
        projects['description'] = p.description
        projects['github_url'] = p.github_url
        projects['a_project'] = p

    return render(request, 'myportfolio/index.html', context_dict)

def project(request, project_title_slug):
    context_dict = {}
    try:
        a_project = Project.objects.get(slug=project_title_slug)
        context_dict['project_title'] = a_project.title
        context_dict['a_project'] = a_project
        context_dict['description'] = a_project.description
        context_dict['github_url'] = a_project.github_url
    except Project.DoesNotExist:
        pass

    context_dict['project_title_slug'] = project_title_slug

    return render(request, 'myportfolio/project.html', context_dict)

def project_list(request):
    context_dict = {'projects': Project.objects.all()}

    return render(request, 'myportfolio/project-list.html', context_dict)
