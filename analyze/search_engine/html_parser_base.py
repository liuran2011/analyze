from sgmllib import SGMLParser

class HTMLParserBase(SGMLParser):
    def __init__(self):
        SGMLParser.__init__(self)
