
def getDomain(url, timeout=10):
    import urllib2
    import re
    try:        
        response=urllib2.urlopen(url, timeout=10)
        realUrl=response.geturl()
        domain=re.search('//[^/]+/?', realUrl).group().replace('/', '')
    except Exception:
        domain=u'_invalid'
    return domain