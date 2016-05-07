#coding=utf-8

from basic import BasicGenerator
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics,ttfonts
from reportlab.platypus import Paragraph,SimpleDocTemplate
from reportlab.lib.styles import getSampleStyleSheet
from constants import *
import datetime
import copy

class Generator(BasicGenerator):
    def __init__(self,conf,env,db,notify):
        super(Generator,self).__init__(conf,env,db,notify)
        
        pdfmetrics.registerFont(ttfonts.TTFont('song','analyze/fonts/simsun.ttc'))
        self.style=copy.deepcopy(getSampleStyleSheet()['Normal'])
        self.style.fontName='song'
        self.style.fontSize=12
        self.content=[]

    def ready(self,username):
        self.content=[]
        self.content.append(Paragraph(USERNAME+':'+username,self.style))

    def add(self,result):
        self.content.append(Paragraph(DATETIME+":"+result[DATETIME_INDEX].ctime()+" "
                            +KEYWORD+":"+result[KEYWORD_INDEX]+" "
                            +SEARCH_ENGINE+":"+result[SOURCE_URL_INDEX]+" "
                            +URL+":"+"<a href="+result[URL_INDEX]+">"+result[URL_INDEX]
                            +"</a>",self.style))

    def finish(self,username):
        date_time=datetime.datetime.now()
        file_name=self.env.run_dir()+"/"+str(date_time.date())+str(date_time.time())+".pdf"
        doc=SimpleDocTemplate(file_name)
        doc.build(self.content)
        
        return file_name

    def format(self):
        return "pdf"
