from kombu import Exchange,Connection,Producer
from constants import *
import uuid

class SearchEngineMQ(object):
    def __init__(self,conf,env):
        self.conf=conf
        self.env=env

        self._gen_id()

        self._stat_init()

    def _gen_id(self):
        try:
            f=open(self.env.uuid_file())
            self.id=f.read()
            f.close()
        except IOError:
            self.id=str(uuid.uuid1())
            f=open(self.env.uuid_file(),"w")
            f.write(self.id)
            f.close()
            
    def _stat_init(self):
        self.stat_exchange=Exchange(SE_STATS_EXCHANGE,
                                "topic",delivery_mode=1)
        self.stat_routing_key=".".join([self.id,SE_STATS_TOPIC_SUFFIX])
        self.connect=Connection(self.conf.rabbit_connection())
        self.stat_producer=self.connect.Producer(exchange=self.stat_exchange,
                                                routing_key=self.stat_routing_key)

    def publish_stats(self,stat):
        msg={MESSAGE_ID:self.id,MESSAGE_STATS:stat}
        self.stat_producer.publish(msg)
