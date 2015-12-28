from search_engine.html_parser_base import HTMLParserBase

class SogouHTMLParser(HTMLParserBase):
    def __init__(self):
        HTMLParserBase.__init__(self)

        self.reset_parser()

    def reset_parser(self):
        self.search_result_div_start=False
        self.search_result_div_level=0
        self.search_result_href=[]
        self.div_level=0
    
    def _results_div(self,attrs):
        if len(attrs)==0:
            return False

        for attr in attrs:
            if attr[0]=='class' and attr[1]=='results':
                return True

        return False

    def _handle_start_div(self,attrs):
        if self._results_div(attrs):
            self.search_result_div_start=True
            self.search_result_div_level=self.div_level

        self.div_level+=1

    def _handle_start_a(self,attrs):
        href=self._result_href(attrs)
        if not href:
            return

        self.search_result_href.append(href)

    def _handle_end_div(self):
        self.div_level-=1

        if (self.search_result_div_start 
            and self.div_level==self.search_result_div_level):
            self.search_result_div_start=False

    def handle_starttag(self,tag,attrs):
        if tag=='div':
            self._handle_start_div(attrs)
        elif tag=='a':
            self._handle_start_a(attrs)

    def handle_endtag(self,tag):
        if tag=='div':
            self._handle_end_div()
            
    def _result_href(self,attrs):
        if len(attrs)==0:
            return None
       
        for attr in attrs:
            if attr[0]=='href':
                return attr[1]

        return None
