from basic import BasicGenerator

class Generator(BasicGenerator):
    def __init__(self,conf,db):
        super(Generator,self).__init__(conf,db)

    def ready(self,username):
        print "ready to user:",username

    def add(self,result):
        print "add ersult:",result
    def finish(self,username):
        print "finish user",username
