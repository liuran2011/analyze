#coding=utf-8

from flask import *
from log.log import LOG
from http_codes import *
import gevent
import mq.constants as mqc

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
    USER_REPORT_START_TIME="report_start_time"
    USER_REPORT_END_TIME="report_end_time"

    GLB_SETTING='global_setting'
    GLB_SETTING_EMAIL='email'
    GLB_SETTING_SMTP_SERVER='smtp_server'
    GLB_SETTING_SMTP_PORT='smtp_port'
    GLB_SETTING_SMTP_USERNAME='smtp_username'
    GLB_SETTING_SMTP_PASSWORD='smtp_password'

    def __init__(self,conf,db,mq):
        self.conf=conf
        self.db=db
        self.mq=mq

        self.app=Flask(__name__)
        self.app.add_url_rule('/global_setting',
                                'set_global_setting',
                                self._global_setting,
                                methods=['POST','GET'])

        self.app.add_url_rule('/user','add_user',self._add_user,
                            methods=['POST'])
        self.app.add_url_rule('/user','get_user',self._get_user,
                            methods=['GET'])
        self.app.add_url_rule('/user/<string:username>',
                                'del_user',self._del_user,
                                methods=['DELETE'])
        self.app.add_url_rule('/user/<string:username>',
                                'modify_user',self._modify_user,
                                methods=['PUT'])

        self.app.add_url_rule('/token','get_token',self._token_get,
                                methods=['GET'])

        self.app.add_url_rule('/report','gen_report',self._gen_report,
                                methods=['POST'])

    def report_res(self,status_code):
        self.report_event.set()
        self._report_res=status_code

    def _report_check(self,req):
        if not req:
            return HTTP_BAD_REQUEST_STR,HTTP_BAD_REQUEST

        if (not req.get(self.USER_NAME,None)
            or not req.get(self.USER_REPORT_START_TIME,None)
            or not req.get(self.USER_REPORT_END_TIME,None)):
            return HTTP_BAD_REQUEST_STR,HTTP_BAD_REQUEST
        
        if (len(req[self.USER_NAME])==0
            or len(req[self.USER_REPORT_START_TIME])==0):
            return HTTP_BAD_REQUEST_STR,HTTP_BAD_REQUEST

        return HTTP_OK_STR,HTTP_OK

    def _gen_report(self):
        req=request.json
        ret_str,ret=self._report_check(req)
        if ret!=HTTP_OK:
            return ret_str,ret

        self.mq.report_request(req[self.USER_NAME],
                                req[self.USER_REPORT_START_TIME],
                                req[self.USER_REPORT_END_TIME])

        #wait reponse
        self._report_res=HTTP_INTERNAL_ERROR
        self.report_event=gevent.event.Event()
        self.report_event.wait(timeout=mqc.MQ_TIMEOUT)
        if not self._report_res or self._report_res!=HTTP_OK:
            return HTTP_INTERNAL_ERROR_STR,self._report_res
        else:
            return HTTP_OK_STR,HTTP_OK

    def _token_get(self):
        pass

    def _modify_user(self,username):
        req=request.json
        ret_str,ret=self._user_check(req)
        if ret!=HTTP_OK:
            return ret_str,ret

        self.db.user_update(username,
                            req[self.USER_PASSWORD],
                            req[self.USER_EMAIL],
                            req[self.USER_MOBILE_PHONE],
                            req[self.USER_PERMISSION],
                            req[self.USER_COMPANY],
                            req[self.USER_MONITOR_KEYWORD])

        return HTTP_OK_STR,HTTP_OK
        
    def _user_check(self,req):
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
        ret_str,ret=self._user_check(req)
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

    def _global_setting_check(self,req):
        print req
        if not req:
            return HTTP_BAD_REQUEST_STR,HTTP_BAD_REQUEST

        if ( not req.get(self.GLB_SETTING_EMAIL,None)
            or not req.get(self.GLB_SETTING_SMTP_SERVER,None)
            or not req.get(self.GLB_SETTING_SMTP_PORT,None)
            or not req.get(self.GLB_SETTING_SMTP_USERNAME,None)
            or not req.get(self.GLB_SETTING_SMTP_PASSWORD,None)):
            return HTTP_BAD_REQUEST_STR,HTTP_BAD_REQUEST
        print "abc"
        if (len(req[self.GLB_SETTING_EMAIL])==0
            or len(req[self.GLB_SETTING_SMTP_SERVER])==0
            or len(req[self.GLB_SETTING_SMTP_USERNAME])==0
            or len(req[self.GLB_SETTING_SMTP_PORT])==0
            or len(req[self.GLB_SETTING_SMTP_PASSWORD])==0):
            return HTTP_BAD_REQUEST_STR,HTTP_BAD_REQUEST
        print "def"
        return HTTP_OK_STR,HTTP_OK

    def _global_setting_set(self):
        req=request.json
        ret_str,ret=self._global_setting_check(req)
        if ret!=HTTP_OK:
            return ret_str,ret

        self.db.global_setting_update(req[self.GLB_SETTING_EMAIL],
                            req[self.GLB_SETTING_SMTP_SERVER],
                            req[self.GLB_SETTING_SMTP_PORT],
                            req[self.GLB_SETTING_SMTP_USERNAME],
                            req[self.GLB_SETTING_SMTP_PASSWORD])

        return HTTP_OK_STR,HTTP_OK

    def _global_setting_get(self):
        result={}
        glb_setting=self.db.global_setting()
        if glb_setting:
            result[self.GLB_SETTING_EMAIL]=glb_setting[0]
            result[self.GLB_SETTING_SMTP_SERVER]=glb_setting[1]
            result[self.GLB_SETTING_SMTP_PORT]=glb_setting[2]
            result[self.GLB_SETTING_SMTP_USERNAME]=glb_setting[3]
            result[self.GLB_SETTING_SMTP_PASSWORD]=glb_setting[4]

        return jsonify(result),HTTP_OK

    def _global_setting(self):
        if request.method=='GET':
            return self._global_setting_get()
        else:
            return self._global_setting_set()

    def run(self):
        LOG.info('rest server run at %s:%d'%(self.conf.rest_server_address(),
                self.conf.rest_server_port()))

        self.app.run(self.conf.rest_server_address(),
                     self.conf.rest_server_port(),
                     True)
