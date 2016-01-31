#coding=utf-8

import re
from search_engine.html_parser_base import HTMLParserBase

class SogouHTMLParser(HTMLParserBase):
    def __init__(self):
        HTMLParserBase.__init__(self)

        self.reset_parser()

    def reset_parser(self):
        self.search_result_div_start=False
        self.vrwrap_div_start=False
        self.h3_start=False
        self.vrwrap_div_level=0
        self.search_result_div_level=0
        self.search_result_href=[]
        self.div_level=0
        self.redirect_url=None
        self.pagebar_div_start=False
        self.pagebar_div_level=0
        self.nextpage_url=None
        self.reset()

    def _results_div(self,attrs):
        if len(attrs)==0:
            return False

        for attr in attrs:
            if attr[0]=='class' and attr[1]=='results':
                return True

        return False

    def _vrwrap_div(self,attrs):
        if len(attrs)==0:
            return False

        for attr in attrs:
            if attr[0]=='class' and (attr[1]=='vrwrap' or attr[1]=='rb'):
                return True

        return False

    def _pagebar_div(self,attrs):
        if len(attrs)==0:
            return False

        class_p=False
        id_container=False

        for attr in attrs:
            if attr[0]=='class' and attr[1]=='p':
                class_p=True
            elif attr[0]=='id' and attr[1]=='pagebar_container':
                id_container=True

        if class_p and id_container:
            return True

        return False

    def _is_redirect(self,attrs):
        for attr in attrs:
            if attr[0]=='http-equiv' and attr[1].upper()=='REFRESH':
                return True

        return False

    def _handle_meta(self,attrs):
        if not self._is_redirect(attrs):
            return

        for attr in attrs:
            if attr[0].upper()=='CONTENT':
                r=re.search("URL='(.*)'",attr[1])
                if r:
                    self.redirect_url=r.groups()[0]

    def _handle_start_div(self,attrs):
        if self._results_div(attrs):
            self.search_result_div_start=True
            self.search_result_div_level=self.div_level
        elif self._vrwrap_div(attrs):
            self.vrwrap_div_start=True
            self.vrwrap_div_level=self.div_level
        elif self._pagebar_div(attrs):
            self.pagebar_div_start=True
            self.pagebar_div_level=self.div_level

        self.div_level+=1

    def _handle_start_a(self,attrs):
        href=self._pagebar_href(attrs)
        if href:
            self.nextpage_url="/web"+href;
            return

        href=self._result_href(attrs)
        if not href:
            return

        self.search_result_href.append(href)

    def _handle_start_h3(self,attrs):
        if (not self.search_result_div_start 
            or not self.vrwrap_div_start):
            return

        self.h3_start=True

    def _handle_end_h3(self):
        self.h3_start=False

    def _handle_end_div(self):
        self.div_level-=1

        if (self.search_result_div_start 
            and self.div_level==self.search_result_div_level):
            self.search_result_div_start=False

        if (self.vrwrap_div_start
            and self.div_level==self.vrwrap_div_level):
            self.vrwrap_div_start=False

        if (self.pagebar_div_start
            and self.div_level==self.pagebar_div_level):
            self.pagebar_div_start=False

    def handle_starttag(self,tag,attrs):
        if tag=='div':
            self._handle_start_div(attrs)
        elif tag=='a':
            self._handle_start_a(attrs)
        elif tag=='h3':
            self._handle_start_h3(attrs)
        elif tag.upper()=='META':
            self._handle_meta(attrs)
      
    def handle_endtag(self,tag):
        if tag=='div':
            self._handle_end_div()
        elif tag=='h3':
            self._handle_end_h3()

    def _pagebar_href(self,attrs):
        if not self.pagebar_div_start:
            return None
       
        a_id=False
        href=None

        for attr in attrs:
            if attr[0]=='id' and attr[1]=='sogou_next':
                a_id=True
            elif attr[0]=='href':
                href=attr[1]

        if (not a_id) or (not href):
            return None
        
        return href

    def _result_href(self,attrs):
        if len(attrs)==0:
            return None
       
        if not self.search_result_div_start:
            return None

        if not self.vrwrap_div_start:
            return None

        if not self.h3_start:
            return None

        href=None

        for attr in attrs:
            if attr[0]=='href':
                href=attr[1]
                break

        if not href:
            return None

        if (not href.startswith('http://') 
            and not href.startswith('https://')):
            return None

        return href
