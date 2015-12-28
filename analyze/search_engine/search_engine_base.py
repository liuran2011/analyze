import urllib

class SearchEngineBase(object):
    def __init__(self,conf):
        self.conf=conf

    def fetch_page(self,url):
        page=None
        try:
            fd=urllib.urlopen(url)
            page=fd.read()
            fd.close()
            return page
        except IOError as e:
            print "open url:%s failed."%(url)
            return page

    def next(self):
        pass

