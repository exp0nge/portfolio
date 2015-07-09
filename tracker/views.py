from datetime import datetime

from django.shortcuts import render, HttpResponseRedirect
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
        weekday = day_converter[datetime.now().weekday()]
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
        
    # Check if user is trying to submit a series
    if request.method == 'POST':
        form = SeriesForm(request.POST)
        if form.is_valid():
            series = form.save(commit=False)
            series.submitted_user = request.user
            if not form.cleaned_data['cover_image_url']:
                img_url = image_search.search(request, form.cleaned_data['title'])
                series.cover_image_url = img_url
            series.save()
            return HttpResponseRedirect('/tracker/?newCard=' + series.title)
        else:
            context_dict['form_errors'] = True
    else:
        form = SeriesForm()
    
    context_dict['form'] = form
        
    return render(request, 'tracker/index.html', context_dict)

@login_required()
def add_series(request):
    if request.method == 'POST':
        form = SeriesForm(request.POST)
        if form.is_valid():
            series = form.save(commit=False)
            series.submitted_user = request.user
            if not form.cleaned_data['cover_image_url']:
                img_url = image_search.search(request, form.cleaned_data['title'])
                series.cover_image_url = img_url
            series.save()
            return HttpResponseRedirect('/tracker/')
    else:
        form = SeriesForm()

    return render(request, 'tracker/add_series.html', {'form': form})

@login_required()
def delete_series(request, pk):
    series = Series.objects.filter(pk=pk)
    series_title = series[0].title
    if series[0].submitted_user == request.user:
        series.delete()
        return HttpResponseRedirect('/tracker/?deleted=' + series_title)
    return HttpResponseRedirect('/tracker/?deleted=Failed')
    
    
class SeriesUpdate(UpdateView):
    model = Series
    success_url = '/tracker/'
    form_class = SeriesForm
    template_url = 'add_series_modal'

    def get_object(self, queryset=None):
        series = Series.objects.filter(pk=self.kwargs['pk']).get(submitted_user=self.request.user)
        return series
            