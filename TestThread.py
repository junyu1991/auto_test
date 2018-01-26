#!/usr/bin/env python
#!encoding:utf-8

import threading
import requests


class TestThread(threading.Thread):
    '''
    A AutoTestThread.
    '''

    def __init__(self,thread_name,thread_id,request_info):
        '''
        thread_name:thread name
        thread_id:thread id
        request_info:The request info ,Class RequestInfo which store root_url,
                     logn dict,request header and request list all configed in
                     .json file
        '''
        threading.Thread.__init__(self)
        self._thread_name=thread_name
        self._thread_id=thread_id
        self._request_info=request_info
        self._conn=request.session()

    def update_cookie(self):
        '''
        Get Cookie by request the root url
        '''
        root_url=self._request_info.get_root_url()
        self._conn.get(url=root_url,headers=self._request_info.get_header())

    def logon(self):
        '''
        Post the logon  request
        '''
        header=self._request_info.get_header()
        logon_url=header.get('url')
        
        
    
    def run(self):
        
