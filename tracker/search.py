import urllib2
import urllib

from ipware.ip import get_ip
import simplejson
from fuzzywuzzy import process


class NoResultError(Exception):
    pass


def check_blacklist(index, deserialized_output):
        result_url = deserialized_output['responseData']['results'][index]['unescapedUrl']
        
        
        if index < 5:
            if 'imdb' in result_url:
                check_blacklist(index + 1, deserialized_output)
            else:
                return deserialized_output['responseData']['results'][index]['unescapedUrl']
        else:
            raise NoResultError('No results found')


def img_search(request, query):
    fetcher = urllib2.build_opener()
    query = urllib.quote(query)
    user_ip = str(get_ip(request))
    search_url = 'http://ajax.googleapis.com/ajax/services/search/images?v=1.0&q=' + query + \
                 '&start=0&safe=active&userip=' + user_ip
    f = fetcher.open(search_url)
    deserialized_output = simplejson.load(f)
    
    # check_blacklist(0, deserialized_output)
    return deserialized_output['responseData']['results'][0]['unescapedUrl']


def fuzzy_series_search(list_of_series, query):
    series_list = []
    for series in list_of_series:
        series_list.append(series.__unicode__())
    series_list = process.extract(query, series_list, limit=3)
    if len(series_list) == 0:
        raise NoResultError('No result found for series name')
    filtered_list = []
    for result in series_list:
        filtered_list.append(result[0])
    return filtered_list
