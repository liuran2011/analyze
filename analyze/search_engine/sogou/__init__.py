#coding=utf-8

import sys
import time
import urllib
import copy
from analyze.search_engine.search_engine_base import SearchEngineBase
from html_parser import SogouHTMLParser
from analyze.log.log import LOG

class SearchEngine(SearchEngineBase):
    def __init__(self,conf,env,db):
        super(SearchEngine,self).__init__(conf,env,db)
        self.html_parser=SogouHTMLParser()
        self.page_count=0

    def _first_abs_page(self,search_keyword):
        search_url=self.conf.url()+"/web?query="+search_keyword+"&_asf=www.sogou.com&_ast=&w=01019900&p=40040100&ie=utf8&sut=7403&sst0=1451221676273&lkt=0%2C0%2C0"
        return self.fetch_page(search_url)

    def _search_one_negative_word(self,user,page,word,url):
        if self.algorithm.match(word,page):
            LOG.info("find match: user: %s url:%s word:%s"%(user,url,word))
            self.db.add_result(user['username'],url,self.conf.url(),word)

    def _search_negative_word(self,user,link):
        page=self.fetch_page(link) 
        if not page:
            return

        try:
            self.html_parser.reset_parser()
            self.html_parser.feed(page)
        except:
            LOG.warn("parse link:%s failed."%(link))
            return

        url=link
        if self.html_parser.redirect_url:
            page=self.fetch_page(self.html_parser.redirect_url)
            url=self.html_parser.redirect_url
    
        for negative_word in user['negative_word']:
            self._search_one_negative_word(user,page,negative_word,url)

    def _search_keyword(self,user,keyword):
        abs_page=self._first_abs_page(keyword)
        if not abs_page:
            return

        self.html_parser.reset_parser()
        self.html_parser.feed(abs_page)
        if len(self.html_parser.search_result_href)==0:
            return

        self.page_cout=0

        while True:
            if self.page_count>=self.max_page:
                break
           
            nextpage_url=None

            if self.html_parser.nextpage_url:
                nextpage_url=self.conf.url()+self.html_parser.nextpage_url
            
            search_result_href=copy.deepcopy(self.html_parser.search_result_href)
            for link in search_result_href:
                self._search_negative_word(user,link)

            if not nextpage_url:
                break

            time.sleep(self.conf.search_interval())

            page=self.fetch_page(nextpage_url)
            if not page:
                break

            LOG.debug("search next page:%s"%(nextpage_url))

            self.html_parser.reset_parser()
            self.html_parser.feed(page)

            if len(self.html_parser.search_result_href)==0:
                break

    def search_user(self,user):
        print user
        LOG.info("username:%s"%(user['username']))
        LOG.info('keyword:%s'%(user['keyword']))
        LOG.info('negative_word:%s'%(user['negative_word']))

        for keyword in user['keyword']:
            self._search_keyword(user,keyword)
            time.sleep(self.conf.search_interval())
