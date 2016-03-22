from flask import *
from log.log import LOG
from http_codes import *

class RestServer(object):
    USER_LIST="user_list"
    USER_NAME="name"
    USER_PASSWORD="password"
    USER_EMAIL="email"
    USER_MOBILE_PHONE="mobile_phone"
    USER_PERMISSION="permission"
    USER_COMPANY="company"
    USER_MONITOR_KEYWORD="monitor_keyword"
    USER_LAST_REPORT_TIME="last_report_time"

    GLB_SETTING='global_setting'
    GLB_SETTING_EMAIL='email'

    def __init__(self,conf,db):
        self.conf=conf
        self.db=db

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
        self.app.add_url_rule('/user/<string:username>',
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

    def _add_user_check(self,req):
        if not req:
            return HTTP_BAD_REQUEST_STR,HTTP_BAD_REQUEST
        
        if (not req.get(self.USER_NAME,None) 
            or not req.get(self.USER_PASSWORD,None)
            or not req.get(self.USER_EMAIL,None) 
            or not req.get(self.USER_MOBILE_PHONE,None)
            or not req.get(self.USER_COMPANY,None)
            or not req.get(self.USER_PERMISSION,None)
            or not req.get(self.USER_MONITOR_KEYWORD,None)):
            return HTTP_BAD_REQUEST_STR,HTTP_BAD_REQUEST
        
        if (len(req[self.USER_NAME])==0
            or len(req[self.USER_PASSWORD])==0
            or len(req[self.USER_EMAIL])==0
            or len(req[self.USER_MONITOR_KEYWORD])==0
            or len(req[self.USER_PERMISSION])==0):
            return HTTP_BAD_REQUEST_STR,HTTP_BAD_REQUEST
        
        return HTTP_OK_STR,HTTP_OK

    def _add_user(self):
        req=request.json
        ret_str,ret=self._add_user_check(req)
        if ret!=HTTP_OK:
            return ret_str,ret

        self.db.user_add(req[self.USER_NAME],req[self.USER_PASSWORD],req[self.USER_EMAIL],
                        req[self.USER_MOBILE_PHONE],req[self.USER_PERMISSION],
                        req[self.USER_COMPANY],req[self.USER_MONITOR_KEYWORD])
        
        return HTTP_OK_STR,HTTP_OK

    def _get_user(self):
        result=[]
        for user in self.db.user_list() or []:
            result.append({self.USER_NAME:user[0],
                            self.USER_EMAIL:user[1],
                            self.USER_MOBILE_PHONE:user[2],
                            self.USER_PERMISSION:user[3],
                            self.USER_COMPANY:user[4],
                            self.USER_MONITOR_KEYWORD:user[5],
                            self.USER_LAST_REPORT_TIME:user[6]})
        return jsonify({self.USER_LIST:result}),HTTP_OK

    def _del_user(self,username):
        self.db.user_del(username)
        
        return HTTP_OK_STR,HTTP_OK

    def _global_setting_set(self,request):
        pass

    def _global_setting_get(self):
        result={}
        glb_setting=self.db.global_setting()
        if glb_setting:
            result[self.GLB_SETTING_EMAIL]=glb_setting[0]

        return jsonify(result),HTTP_OK

    def run(self):
        LOG.info('rest server run at %s:%d'%(self.conf.rest_server_address(),
                self.conf.rest_server_port()))

        self.app.run(self.conf.rest_server_address(),
                     self.conf.rest_server_port(),
                     True)
