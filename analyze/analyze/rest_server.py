from flask import *
from log.log import LOG

class RestServer(object):
    def __init__(self,conf):
        self.conf=conf

        self.app=Flask(__name__)
        self.app.add_url_rule('/gloal_setting',
                                'set_global_setting',
                                self._global_setting_set,
                                methods=['POST'])
        self.app.add_url_rule('/global_setting',
                                'get_global_setting',
                                self._global_setting_get,
                                methods=['GET'])

        self.app.add_url_rule('/user','add_user',self._add_user,
                            methods=['POST'])
        self.app.add_url_rule('/user','get_user',self._get_user,
                            methods=['GET'])
        self.app.add_url_rule('/user/<string:location>',
                                'del_user',self._del_user,
                                methods=['DELETE'])
        self.app.add_url_rule('/user/<string:location>',
                                'modify_user',self._modify_user,
                                methods=['PUT'])

        self.app.add_url_rule('/token','get_token',self._token_get,
                                methods=['GET'])

    def _token_get(self):
        pass

    def _modify_user(self,user,request):
        pass

    def _add_user(self,user):
        pass

    def _get_user(self):
        pass

    def _del_user(self,username):
        pass

    def _global_setting_set(self,request):
        pass

    def _global_setting_get(self):
        pass

    def run(self):
        LOG.info('rest server run at %s:%d'%(self.conf.rest_server_address(),
                self.conf.rest_server_port()))

        self.app.run(self.conf.rest_server_address(),
                     self.conf.rest_server_port(),
                     True)
