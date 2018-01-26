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

import requests

class URL:
    ''''
    Save the request info.
    '''

    def __init__(self,url,header={},data={}):
        self._url=url
        self._header=header
        self._data=data
    def get_url(self):
        return self._url
    def get_header(self):
        return self._header
    def get_data(self):
        return self._data

    def __str__(self):
        return "%s\t%s\t%s" % (str(self._url),str(self._header),str(self._data))

def get_post_urls(json_data):
    post_dict=json_data.get('post')
    result=[]
    for key in post_dict.iterkeys():
        url=key
        header=post_dict.get(key).get('header')
        data=post_dict.get(key).get('data')
        result.append(URL(url,header,data))

    return result

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

def post_url(url_list):
    '''
    Send Post request
    url_list:The list of URL class
    '''
    for U in url_list:
        print("Post data to %s" % U.get_url())
        print U
        r=requests.post(url=U.get_url(),data=U.get_data(),headers=U.get_header())
        save_result(r)

def main():
    opts,args=getopt.getopt(sys.argv[1:],'hc:d:',['help'])
    json_file="./data/url.json"
    for opt,value in opts:
        if opt=='-c':
            json_file=value
    print json_file
    post_url(get_post_urls(get_json_data(json_file)))

if __name__=='__main__':
    main()
    
