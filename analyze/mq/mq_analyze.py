from kombu import Exchange,Queue,Consumer,Connection
from constants import *

class AnalyzeMQ(object):
    def __init__(self,conf):
        self.conf=conf

        self._stats_init()

    def _stats_msg_proc(self,body,message):
        print body
        message.ack()

    def _stats_init(self):
        self.connect=Connection(self.conf.rabbit_connection())
        self.stats_exchange=Exchange(SE_STATS_EXCHANGE,"topic",delivery_mode=1)
        self.stats_queue=Queue(SE_STATS_QUEUE,
                            exchange=self.stats_exchange,
                            routing_key='*.'+SE_STATS_TOPIC_SUFFIX)
        self.stats_consumer=self.connect.Consumer(self.stats_queue,callbacks=[self._stats_msg_proc])

    def run(self):
        while True:
            print "drain event..."
            #self.stats_consumer.consume()
            self.connect.drain_events()
