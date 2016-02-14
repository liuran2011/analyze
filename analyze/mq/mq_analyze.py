from kombu import Exchange,Queue,Consumer,Connection
from constants import *
from kombu.mixins import ConsumerMixin

class AnalyzeConsumer(ConsumerMixin):
    def __init__(self,connection):
        self.connection=connection
        self.stats_exchange=Exchange(SE_STATS_EXCHANGE,"topic",delivery_mode=1)
        self.stats_queue=Queue(SE_STATS_QUEUE,
                            exchange=self.stats_exchange,
                            routing_key='*.'+SE_STATS_TOPIC_SUFFIX)
        
    def get_consumers(self,Consumer,channel):
        return [Consumer(queues=[self.stats_queue],callbacks=[self._stats_msg_proc])]

    def _stats_msg_proc(self,body,message):
        print body
        message.ack()

class AnalyzeMQ(Consumer):
    def __init__(self,conf):
        self.conf=conf

        self._stats_init()

    def _stats_init(self):
        self.connect=Connection(self.conf.rabbit_connection())
        self.consumer=AnalyzeConsumer(self.connect)

    def run(self):
        self.consumer.run()
