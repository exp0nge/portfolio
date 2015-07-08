from django.shortcuts import render, HttpResponseRedirect

from django.contrib.auth.decorators import login_required

from tracker.models import Series
from tracker.forms import SeriesForm
import image_search


@login_required()
def index(request):
    context_dict = {'username': request.user.username}
    
    new = request.GET.get('new')
    print new
    if new is not None:
        context_dict['new'] = new
    
    all_series = Series.objects.filter(submitted_user=request.user)
    context_dict['series_list'] = all_series
    return render(request, 'tracker/index.html', context_dict)

@login_required()
def add_series(request):
    if request.method == 'POST':
        form = SeriesForm(request.POST)
        if form.is_valid():
            series = form.save(commit=False)
            series.submitted_user = request.user
            if not form.cleaned_data['cover_image_url']:
                img_url = image_search.search(form.cleaned_data['title'])
                series.cover_image_url = img_url
            series.save()
            return HttpResponseRedirect('/tracker/')
    else:
        form = SeriesForm()

    return render(request, 'tracker/add_series.html', {'form': form})
