import urllib2
import urllib

from ipware.ip import get_ip
import simplejson


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


def search(request, query):
    fetcher = urllib2.build_opener()
    query = urllib.quote(query)
    user_ip = str(get_ip(request))
    search_url = 'http://ajax.googleapis.com/ajax/services/search/images?v=1.0&q=' + query + \
                 '&start=0&imgsz=large&safe=active&userip=' + user_ip
    f = fetcher.open(search_url)
    deserialized_output = simplejson.load(f)
    
    # check_blacklist(0, deserialized_output)
    return deserialized_output['responseData']['results'][0]['unescapedUrl']
