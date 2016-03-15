#coding=utf-8

from basic import BasicGenerator
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from constants import *
import datetime

class Generator(BasicGenerator):
    def __init__(self,conf,env,db):
        super(Generator,self).__init__(conf,env,db)
    
    def _new_text(self):
        self.text=self.canvas.beginText()
        self.text.setTextOrigin(cm,PDF_GEN_Y_ORIGIN_UNITS*cm)

    def _save_page(self):
        self.canvas.drawText(self.text)
        self.canvas.showPage()
        self.canvas.save()

    def ready(self,username):
        date_time=datetime.datetime.now()
        file_name=self.env.run_dir()+"/"+str(date_time.date())+str(date_time.time())+".pdf"

        self.canvas=canvas.Canvas(file_name)
        self._new_text()
        self.text.textLine(USERNAME+":"+username)
        self.text.textLine(RESULTS+":")
        self.textlines=2

    def add(self,result):
        self.text.textLine(DATETIME+":"+result[DATETIME_INDEX].ctime()+" "
                            +KEYWORD+":"+result[KEYWORD_INDEX]+" "
                            +SEARCH_ENGINE+":"+result[SOURCE_URL_INDEX]+" "
                            +URL+":"+result[URL_INDEX])
        self.textlines=self.textlines+1
        if self.textlines>PDF_GEN_MAX_LINE_PER_PAGE:
            self._save_page()
            self._new_text()

    def finish(self,username):
        self._save_page()
