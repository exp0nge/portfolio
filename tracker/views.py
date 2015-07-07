from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from tracker.models import Series
from tracker.forms import UserForm

# Create your views here.
def index(request):
    context_dict = {}
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/tracker/login')
    else:
        all_series = Series.objects.all()
        context_dict['all'] = all_series
        return render(request, 'tracker/index.html', context_dict)
        
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return HttpResponseRedirect('/tracker/')
        else:
            return HttpResponse('Invalid credentials')
    else:
        return render(request, 'tracker/login.html', {})
        

def register(request):
    registered = False
    
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            registered = True
        else:
            print user_form.errors()

    else:
        user_form = UserForm()

    return render(request, 'rango/register.html', {'user_form': user_form, 'registered': registered})
        
        
        
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/tracker/')