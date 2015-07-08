import urllib2
import urllib

import simplejson


def search(query):
    fetcher = urllib2.build_opener()
    query = urllib.quote(query + ' anime background')
    search_url = "http://ajax.googleapis.com/ajax/services/search/images?v=1.0&q=" + query + "&start=0"
    f = fetcher.open(search_url)
    deserialized_output = simplejson.load(f)
    return deserialized_output['responseData']['results'][0]['unescapedUrl']