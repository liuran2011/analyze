from kombu import Exchange,Queue,Consumer,Connection
from constants import *
from kombu.mixins import ConsumerMixin
from constants import *

class AnalyzeConsumer(ConsumerMixin):
    def __init__(self,connection,mq):
        self.connection=connection
        self.mq=mq
        self.msg_proc_callbacks=[]
        self.stats_exchange=Exchange(SE_STATS_EXCHANGE,"topic",delivery_mode=1)
        self.stats_queue=Queue(SE_STATS_QUEUE,
                            exchange=self.stats_exchange,
                            routing_key='*.'+SE_STATS_TOPIC_SUFFIX)
        
    def get_consumers(self,Consumer,channel):
        return [Consumer(queues=[self.stats_queue],callbacks=[self._stats_msg_proc])]

    def register_msg_proc(self,func):
        for n in self.msg_proc_callbacks:
            if n==func:
                break
        else:
            self.msg_proc_callbacks.append(func)

    def _stats_msg_proc(self,body,message):
        for func in self.msg_proc_callbacks:
            func(body)

        message.ack()

class AnalyzeMQ(object):
    def __init__(self,conf,se_mgr):
        self.conf=conf
        self.se_mgr=se_mgr

        self._stats_init()

    def _stats_init(self):
        self.connect=Connection(self.conf.rabbit_connection())

        self.consumer=AnalyzeConsumer(self.connect,self.se_mgr)
        self.consumer.register_msg_proc(self.update_queue)
        self.consumer.register_msg_proc(self.se_mgr.stats_update)
    
    def update_queue(self,msg):
        print "update queue..."

    def run(self):
        self.consumer.run()
