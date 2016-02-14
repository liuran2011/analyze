from kombu import Exchange,Connection,Producer
from constants import *
import uuid

class SearchEngineMQ(object):
    def __init__(self,conf):
        self.conf=conf
        self.id=str(uuid.uuid1())

        self._stat_init()

    def _stat_init(self):
        self.stat_exchange=Exchange(SE_STATS_EXCHANGE,
                                "topic",delivery_mode=1)
        self.stat_routing_key=".".join([self.id,SE_STATS_TOPIC_SUFFIX])
        self.connect=Connection(self.conf.rabbit_connection())
        self.stat_producer=self.connect.Producer(exchange=self.stat_exchange,
                                                routing_key=self.stat_routing_key)

    def publish_stats(self,stat):
        msg={"id":self.id,"stats":stat}
        print "routing_key...",self.stat_routing_key
        self.stat_producer.publish(msg)
