import urllib2
import cookielib

cj = cookielib.CookieJar()

def get(url):
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    r = opener.open(url)
    return r.read()
