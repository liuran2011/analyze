from basic_conf import BasicConf
from constants import *

class AnalyzeConf(BasicConf):
    def __init__(self,conf_file):
        super(AnalyzeConf,self).__init__(conf_file)

    def filter_list(self):
        return self.parser.get(DEFAULT,SCHEDULER_FILTER)

    def rest_server_address(self):
        return self.parser.get(REST,REST_SERVER_ADDRESS)

    def rest_server_port(self):
        return int(self.parser.get(REST,REST_SERVER_PORT))

    def db_connection(self):
        return self.parser.get(DATABASE,CONNECTION)

    def search_engine_down_time(self):
        return self.parser.get(DEFAULT,SEARCH_ENGINE_DOWN_TIME)

    def rabbit_connection(self):
        host=self.parser.get(RABBITMQ,HOST)
        if not host:
            host=RABBITMQ_DEFAULT_HOST

        port=self.parser.get(RABBITMQ,PORT)
        if not port:
            port=RABBITMQ_DEFAULT_PORT

        username=self.parser.get(RABBITMQ,USERNAME)
        if not username:
            username=RABBITMQ_DEFAULT_USERNAME

        password=self.parser.get(RABBITMQ,PASSWORD)
        if not password:
            password=RABBITMQ_DEFAULT_PASSWORD

        return "amqp://"+username+":"+password+"@"+host+":"+port
