#coding=utf-8

from constants import *
from kombu.mixins import ConsumerMixin
from kombu import Exchange,Queue,Consumer,Connection
from analyze.http_codes import *

class ReportRequestConsumer(ConsumerMixin):
    def __init__(self,connection,mq):
        self.connection=connection
        self.mq=mq
        self.report_req_exchange=Exchange(REPORT_REQUEST_EXCHANGE,"direct",delivery_mode=1)
        self.report_req_queue=Queue(REPORT_REQUEST_QUEUE,
                                    exchange=self.report_req_exchange,
                                    routing_key=REPORT_REQUEST_ROUTING_KEY)

    def get_consumers(self,Consumer,channel):
        return [Consumer(queues=[self.report_req_queue],callbacks=[self._report_req_proc])]

    def _report_req_proc(self,body,message):
        self.mq.report_request(body)
        message.ack()

class ReportMQ(object):
    def __init__(self,report_gen,conf):
        self.report_gen=report_gen
        self.conf=conf
        self.connect=Connection(self.conf.rabbit_connection())
        self.report_res_exchange=Exchange(REPORT_RESPONSE_EXCHANGE,"direct",delivery_mode=1)
        self.report_res=self.connect.Producer(exchange=self.report_res_exchange,
                                    routing_key=REPORT_RESPONSE_ROUTING_KEY)
        self.report_req_consumer=ReportRequestConsumer(self.connect,self)

    def report_request(self,body):
        status=HTTP_INTERNAL_ERROR
        if self.report_gen.report_request(body[REPORT_USERNAME],
                                    body[REPORT_REQUEST_START_TIME],
                                    body[REPORT_REQUEST_END_TIME]):
            status=HTTP_OK

        msg={REPORT_USERNAME:body[REPORT_USERNAME],
             REPORT_STATUS:status}
        self.report_res.publish(msg)

    def run(self):
        self.report_req_consumer.run()
