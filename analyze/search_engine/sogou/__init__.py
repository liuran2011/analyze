#coding=utf-8

import sys
import time
import urllib
from search_engine.search_engine_base import SearchEngineBase
from html_parser import SogouHTMLParser

class SearchEngine(SearchEngineBase):
    def __init__(self,conf):
        super(SearchEngine,self).__init__(conf)
        self.user_list=[{'username':'liuran',
                        'keyword':['中兴通讯'],
                        'negative_word':['不好','垃圾','渣渣','不合法','不给力']}]
        self.html_parser=SogouHTMLParser()
        self.page_count=0

    def _first_abs_page(self,search_keyword):
        search_url=self.conf.url()+"/web?query="+search_keyword+"&_asf=www.sogou.com&_ast=&w=01019900&p=40040100&ie=utf8&sut=7403&sst0=1451221676273&lkt=0%2C0%2C0"
        return self.fetch_page(search_url)

    def _search_one_negative_word(self,user,page,word):
        
        print "user:",user['username'],"neg word:",word

    def _search_negative_word(self,user,link):
        page=self.fetch_page(link) 
        if not page:
            return

        try:
            self.html_parser.reset_parser()
            self.html_parser.feed(page)
        except:
            print "parse link:",link,"failed."
            return


        if self.html_parser.redirect_url:
            page=self.fetch_page(self.html_parser.redirect_url)

        for negative_word in user['negative_word']:
            self._search_one_negative_word(user,page,negative_word)

    def _search_keyword(self,user,keyword):
        abs_page=self._first_abs_page(keyword)
        if not abs_page:
            return

        self.html_parser.reset_parser()

        self.html_parser.feed(abs_page)
        if len(self.html_parser.search_result_href)==0:
            return

        print len(self.html_parser.search_result_href)
        for link in self.html_parser.search_result_href:
            self._search_negative_word(user,link)

    def _search_user(self,user):
        print "username:",user['username']
        print 'keyword:',user['keyword']
        print 'negative_word:',user['negative_word']

        for keyword in user['keyword']:
            self._search_keyword(user,keyword)
            time.sleep(self.conf.search_interval())

    def start(self):
        print "sogou search engine running...."
        
        for user in self.user_list:
            self._search_user(user)

            time.sleep(self.conf.search_interval())
