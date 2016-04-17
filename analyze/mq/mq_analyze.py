#coding=utf-8

from kombu import Exchange,Queue,Consumer,Connection
from kombu.mixins import ConsumerMixin
from constants import *
from log.log import LOG
import gevent

class ReportResponseConsumer(ConsumerMixin):
    def __init__(self,connection):
        self.connection=connection
        self.callback=None
        self.report_res_exchange=Exchange(REPORT_RESPONSE_EXCHANGE,"direct",delivery_mode=1)
        self.report_res_queue=Queue(REPORT_RESPONSE_QUEUE,
                                exchange=self.report_res_exchange,
                                routing_key=REPORT_RESPONSE_ROUTING_KEY)
    
    def get_consumers(self,Consumer,channel):
        return [Consumer(queues=[self.report_res_queue],callbacks=[self._report_res_proc])]

    def _report_res_proc(self,body,message):
        self.callback(body[REPORT_STATUS])
        message.ack()

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
        self._user_info_init()
        self._report_init()

    def set_rest_server(self,rest_server):
        self.rest_server=rest_server
        self.report_res_consumer.callback=self.rest_server.report_res

    def _report_init(self):
        self.report_req_exchange=Exchange(REPORT_REQUEST_EXCHANGE,"direct",delivery_mode=1)
        self.report_req=self.connect.Producer(exchange=self.report_req_exchange,
                                    routing_key=REPORT_REQUEST_ROUTING_KEY)
        self.report_res_consumer=ReportResponseConsumer(self.connect)

    def report_request(self,username,req_start_time,req_end_time):
        msg={REPORT_USERNAME:username,REPORT_REQUEST_START_TIME:req_start_time,
            REPORT_REQUEST_END_TIME:req_end_time}
        self.report_req.publish(msg)

    def _user_info_init(self):
        self.se_queues={}
        self.user_info_exchange=Exchange(SE_USER_EXCHANGE,"direct",delivery_mode=1)

    def _stats_init(self):
        self.connect=Connection(self.conf.rabbit_connection())

        self.consumer=AnalyzeConsumer(self.connect,self.se_mgr)
        self.consumer.register_msg_proc(self.add_queue)
        self.consumer.register_msg_proc(self.se_mgr.stats_update)
    
    def add_queue(self,msg):
        key=msg[MESSAGE_ID]

        if self.se_queues.get(key,None):
            return

        self.se_queues[key]=self.connect.Producer(exchange=self.user_info_exchange,
                                        routing_key=key+"."+SE_USER_ROUTING_KEY_SUFFIX)
        LOG.info("add queue %s"%(key))

    def del_queue(self,id):
        if not self.se_queues.get(id,None):
            return

        producer=self.se_queues.pop(id)
        producer.close()
        LOG.info("del queue %s"%(id))

    def run(self):
        gevent.spawn(self.report_res_consumer.run)
        self.consumer.run()
