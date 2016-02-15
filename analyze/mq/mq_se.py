from kombu import Queue,Exchange,Connection,Producer
from constants import *
import uuid
from kombu.mixins import ConsumerMixin

class SEConsumer(ConsumerMixin):
    def __init__(self,connection,id):
        self.connection=connection
        self.id=id
        self.callbacks=[]
        self.exchange=Exchange(SE_USER_EXCHANGE,"direct",delivery_mode=1)
        self.queue=Queue(self.id+"."+SE_USER_QUEUE_SUFFIX,
                        exchange=self.exchange,
                        routing_key=self.id+"."+SE_USER_ROUTING_KEY_SUFFIX)
    
    def get_consumers(self,Consumer,channel):
        return [Consumer(queues=[self.queue],callbacks=[self._user_info_proc])]

    def register_callbacks(self,func):
        for f in self.callbacks:
            if f==func:
                break
        else:
            self.callbacks.append(func)

    def _user_info_proc(self,body,message):
        for func in self.callbacks:
            func(body[MESSAGE_USER_INFO])

        message.ack()

class SearchEngineMQ(object):
    def __init__(self,conf,env,user_info_export):
        self.conf=conf
        self.env=env
        self.user_info_export=user_info_export

        self._gen_id()

        self._stat_init()

        self.consumer=SEConsumer(self.connect,self.id)
        self.consumer.register_callbacks(self.user_info_export.export)

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

    def run(self):
        self.consumer.run()
