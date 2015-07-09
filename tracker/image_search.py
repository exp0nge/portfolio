import urllib2
import urllib

from ipware.ip import get_ip
import simplejson


def search(request, query):
    fetcher = urllib2.build_opener()
    query = urllib.quote(query)
    user_ip = str(get_ip(request))
    search_url = 'http://ajax.googleapis.com/ajax/services/search/images?v=1.0&q=' + query + \
                 '&start=0&imgsz=large&safe=active&userip=' + user_ip
    f = fetcher.open(search_url)
    deserialized_output = simplejson.load(f)
    return deserialized_output['responseData']['results'][0]['unescapedUrl']
