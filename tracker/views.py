from datetime import datetime
import json

from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.http import HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import UpdateView

from tracker.models import Series
from tracker.forms import SeriesForm
import image_search

day_converter = {0: 'MONDAY', 1: 'TUESDAY', 2: 'WEDNESDAY', 3: 'THURSDAY',
                 4: 'FRIDAY', 5: 'SATURDAY', 6: 'SUNDAY'}


@login_required()
def index(request):
    
    context_dict = {'username': request.user.username}
                    
    if request.GET.get('new') == 'True':
        context_dict['newUser'] = True
    
    all_series = Series.objects.filter(submitted_user=request.user)
    
    if request.GET.get('sort') == 'Today':
        weekday = day_converter[datetime.now().weekday() - 1]
        filtered_series = []
        for a_series in all_series:
            if a_series.release_day == weekday:
                filtered_series.append(a_series)
        context_dict['series_list'] = filtered_series
    elif request.GET.get('sort') == 'All':
        context_dict['series_list'] = all_series
    else:
        context_dict['series_list'] = all_series
        
    if request.GET.get('newCard'):
        context_dict['newCard'] = request.GET.get('newCard')


    form = SeriesForm()
    
    context_dict['form'] = form
        
    return render(request, 'tracker/index.html', context_dict)

@login_required()
def add_series(request):
    if request.method == 'POST':
        message = None
        form = SeriesForm(request.POST)
        if form.is_valid():
            series = form.save(commit=False)
            message = request.POST['title']
            series.submitted_user = request.user
            try:
                if not form.cleaned_data['cover_image_url']:
                    img_url = image_search.search(request, form.cleaned_data['title'] + form.cleaned_data['tag'])
                    series.cover_image_url = img_url
            except:
                series.cover_image_url = '/static/images/avatar.png'

            series.save()
            return HttpResponse(series.title)
    else:
        form = SeriesForm()

@login_required()
def delete_series(request, pk):
    series = Series.objects.filter(submitted_user=request.user).get(pk=pk)
    series_title = series.title
    series.delete()
    return HttpResponse(series_title)
    

@login_required()
def update_episode(request, pk):
    series = Series.objects.filter(submitted_user=request.user).get(pk=pk)
    series.current_episode = series.current_episode + 1
    series.save()
    return HttpResponse(series.current_episode)
    
    
@login_required()
def watch_episode(request, pk):
    series = Series.objects.filter(submitted_user=request.user).get(pk=pk)
    context_dict = {'series': series}
    
    if request.GET.get('newCard'):
        context_dict['newCard'] = request.GET.get('newCard')
    
    if len(series.stream_site) < 7:
        context_dict['noiframe'] = True

    form = SeriesForm()
    
    context_dict['form'] = form
    
    return render(request, 'tracker/watch_episode.html', context_dict)
    
class SeriesUpdate(UpdateView):
    model = Series
    success_url = '/tracker/'
    form_class = SeriesForm

    def get_object(self, queryset=None):
        series = Series.objects.filter(submitted_user=self.request.user).get(pk=self.kwargs['pk'])
        return series
