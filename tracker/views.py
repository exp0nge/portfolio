import json
from collections import OrderedDict

from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import UpdateView

from tracker.models import Series, FavoriteSites
from tracker.forms import SeriesForm
import search

day_converter = {1: 'MONDAY', 2: 'TUESDAY', 3: 'WEDNESDAY', 4: 'THURSDAY',
                 5: 'FRIDAY', 6: 'SATURDAY', 0: 'SUNDAY'}


@login_required()
def index(request):
    context_dict = {'username': request.user.username}

    if request.GET.get('new') == 'True':
        context_dict['newUser'] = True

    if request.GET.get('newCard'):
        context_dict['newCard'] = request.GET.get('newCard')

    form = SeriesForm()

    context_dict['form'] = form

    return render(request, 'tracker/index.html', context_dict)


@login_required()
def get_series_as_json(request):
    if request.method == 'GET':
        all_series = Series.objects.filter(submitted_user=request.user)
        _series = None

        if request.GET.get('q'):
            query = request.GET.get('q')
            results = search.fuzzy_series_search(all_series, query)
            jsonify_results = OrderedDict()
            _series = []
            for title in results:
                for series in all_series.filter(title=title):
                    _series.append(series)
            for each_series in _series:
                jsonify_results[each_series.title] = {
                    "id": each_series.id,
                    "title": each_series.title,
                    "description": each_series.description,
                    "release_day": each_series.release_day,
                    "stream_site": each_series.stream_site,
                    "cover_image_url": each_series.cover_image_url,
                    "current_episode": each_series.current_episode,
                    "tag": each_series.tag,
                    "time": each_series.time.isoformat(),
                    "season": each_series.season
                }
            return HttpResponse(json.dumps(jsonify_results), content_type='application/json')

        if request.GET.get('sort') == 'All':
            _series = all_series
        elif request.GET.get('sort'):
            sort_type = request.GET.get('sort')
            if sort_type == 'tag':
                _series = all_series.order_by('tag')
                print _series
            else:
                _series = all_series.filter(release_day=sort_type)
        else:
            _series = all_series

        jsonify_series = OrderedDict()
        for each_series in _series:
            jsonify_series[each_series.title] = {
                "id": each_series.id,
                "title": each_series.title,
                "description": each_series.description,
                "release_day": each_series.release_day,
                "stream_site": each_series.stream_site,
                "cover_image_url": each_series.cover_image_url,
                "current_episode": each_series.current_episode,
                "tag": each_series.tag,
                "time": each_series.time.isoformat(),
                "season": each_series.season
            }
            
        return HttpResponse(json.dumps(jsonify_series), content_type='application/json')


@login_required()
def series_by_id_as_json(request):
    if request.method == 'GET':
        series_id = request.GET.get('pk')
        series = Series.objects.filter(submitted_user=request.user).get(pk=series_id)
        return HttpResponse(json.dumps({"id": series.id,
                                        "title": series.title,
                                        "description": series.description,
                                        "release_day": series.release_day,
                                        "stream_site": series.stream_site,
                                        "cover_image_url": series.cover_image_url,
                                        "current_episode": series.current_episode,
                                        "tag": series.tag,
                                        "time": series.time.isoformat(),
                                        "season": series.season}),
                            content_type='application/json')


@login_required()
def add_series(request):
    if request.method == 'POST':
        message = None
        form = SeriesForm(request.POST)
        if form.is_valid():
            series = form.save(commit=False)
            message = request.POST['title']
            series.submitted_user = request.user

            if not form.cleaned_data['cover_image_url']:
                try:
                    img_url = search.img_search(request, form.cleaned_data['title'] + form.cleaned_data['tag'])
                    series.cover_image_url = img_url
                except:
                    series.cover_image_url = '/static/images/avatar.png'

            series.save()
            jsonify_series = {0: {
                "id": series.id,
                "title": series.title,
                "description": series.description,
                "release_day": series.release_day,
                "stream_site": series.stream_site,
                "cover_image_url": series.cover_image_url,
                "current_episode": series.current_episode,
                "tag": series.tag,
                "time": series.time.isoformat(),
                "season": series.season
            }}
            return HttpResponse(json.dumps(jsonify_series), content_type='application/json')
        else:
            jsonify_errors = {0: 'error', 'errors': [value for value in form.errors.keys()]}
            return HttpResponse(json.dumps(jsonify_errors), content_type='application/json')
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

    if len(series.stream_site) < 7:
        return HttpResponseRedirect('/tracker/stream_missing/' + pk + '?title=' + series.title)

    context_dict = {'series': series}

    if request.GET.get('newCard'):
        context_dict['newCard'] = request.GET.get('newCard')

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


@login_required()
def stream_missing(request, pk):
    context_dict = {'pk': pk, 'title': request.GET.get('title')}
    return render(request, 'tracker/stream_missing.html', context_dict)


@login_required()
def add_favorite_site(request):
    if request.method == 'POST':
        site_url = request.GET.get('site')
        favorite_site = FavoriteSites(submitted_user=request.user, site_url=site_url)
        favorite_site.save()
        return HttpResponse('Site added!')


@login_required()
def get_favorite_sites(request):
    if request.method == 'GET':
        fav_sites = FavoriteSites.objects.filter(submitted_user=request.user)
        json_dict = {}
        for site in fav_sites:
            json_dict[site.site_url] = site.site_url
        return HttpResponse(json.dumps(json_dict), content_type='application/json')


@login_required()
def fuzzy_series_search(request):
    if request.method == 'GET':
        query = request.GET.get('q')
        try:
            results = search.fuzzy_series_search(Series.objects.filter(submitted_user=request.user), query)
            series_id = []
            for title in results:
                for series in Series.objects.filter(title=title):
                    series_id.append(series.id)
            return HttpResponse(
                json.dumps({0: 'success', 'results': series_id}), content_type='application/json')
        except search.NoResultError:
            return HttpResponse(json.dumps({0: 'failure'}), content_type='application/json')
