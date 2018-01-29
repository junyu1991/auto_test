#!/usr/bin/env python
#!encoding:utf-8
#@auth:yujun
#@date:2018-01-25

import getopt
import os
import json
import sys
import urlparse
import datetime
import re

import requests

class URL:
    ''''
    Save the request info.
    '''

    def __init__(self,url,header={},data={}):
        self._url=url
        self._header=header
        self._data=self._handle_data(data)

    def _handle_data(self,data):
        '''
        Process the data from json file,turn the dict data to tuple data.
        return tuple
        '''
        result=[]
        for k in data.iterkeys():
            value=data.get(k)
            if isinstance(value,list):
                for v in value:
                    result.append((k,v))
            else:
                result.append((k,value))
        return tuple(result)
                
            
    
    def get_url(self):
        return self._url
    def get_header(self):
        return self._header
    def get_data(self):
        return self._data

    def __str__(self):
        return "%s\t%s\t%s" % (str(self._url),str(self._header),str(self._data))

def get_post_urls(json_data,method_name='post'):
    '''
    Get url configed in json file
    method_name:get or post
    '''
    post_dict=json_data.get(method_name)
    result=[]
    for key in post_dict.iterkeys():
        url=key
        header=post_dict.get(key).get('header')
        data=post_dict.get(key).get('data')
        print data
        result.append(URL(url,header,data))

    return result


def get_regx():
    return re.compile('(?<=parent\.submitCallBack).*(?=;)')


def get_json_data(json_file):
    if os.path.exists(json_file):
        with open(json_file,'rb') as f:
            json_data=json.load(f)
        return json_data
    else:
        print("Json file not exists")
        sys.exit(-1)

def save_result(save_data):
    '''
    Save the response(headers,status_code,response content) to the file.
    The file path:./result/host/uri.txt (uri=path.replace('/','_'),eg:/test/test -> test_test)
    save_data:The requests.models.Response
    '''
    url=urlparse.urlsplit(save_data.url)
    save_path=os.curdir
    host=url.netloc.replace(':',"_")
    uri=url.path.replace('/','_')
    save_path=os.path.join(save_path,"result")
    save_path=os.path.join(save_path,host)
    save_path=os.path.join(save_path,uri)
    if not os.path.exists(save_path):
        print save_path
        os.makedirs(save_path)
    file_name=os.path.join(save_path,datetime.datetime.now().strftime("%Y-%m-%d-%H_%M_%S")+'.txt')
	
    print("Saving data to file :%s" % file_name)
    
    with open(file_name,'wb') as f:
        f.write(save_data.url+"\t"+str(save_data.status_code))
        f.write("\n")
        f.write(str(save_data.headers))
        f.write("\n")
        f.write(save_data.text.encode('UTF-8'))
    print("\n"*3)
    re_result=get_regx().search(save_data.text)
    if re_result:
        print re_result.group()

def post_url(url_list):
    '''
    Send Post request
    url_list:The list of URL class
    '''
    for U in url_list:
        print("Send post requests %s" % U.get_url())
        print U
        #print U.get_data()
        r=requests.post(url=U.get_url(),data=U.get_data(),headers=U.get_header())
        save_result(r)

def get_url_data(url_list):
    '''
    Send GET request
    '''
    for U in url_list:
        print("Send get requests %s" % U.get_url())
        r=requests.get(url=U.get_url(),params=U.get_data(),headers=U.get_header())
        save_result(r)

def usage():
    usage='''
        python httptool.py -c [json config file,default ./data/url.json]
                           -m [choose the method to send data,which configed in json file,post:the post url data;get: the get url data;all: send all requests configed in json file]
                           -h/--help usage()
        '''
    print(usage)

def main():
    opts,args=getopt.getopt(sys.argv[1:],'hc:m:',['help'])
    json_file="./data/url.json"
    method='post'
    for opt,value in opts:
        if opt=='-c':
            json_file=value
        if opt=='-m':
            method=str(value).lower()
            
    print json_file
    if(method=='post'):
        post_url(get_post_urls(get_json_data(json_file)))
    elif(method=='get'):
        get_url_data(get_post_urls(get_json_data(json_file),'get'))

if __name__=='__main__':
    main()
    
