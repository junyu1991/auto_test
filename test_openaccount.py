#!/usr/bin/env python
#!encoding:utf-8

import requests
from httptool import *

def send_post(U):
    conn=requests.session()
    #get cookie from first request
    resp=conn.post(url=U.get_url(),data=U.get_data(),headers=U.get_header())
    print("The first request header:%s" % str(resp.request.headers))
    print("Get Set-Cookie header:%s" % (resp.headers.get('set-cookie')))

    ''''
    Use the new cookie to post data.
    '''

    #send ask message request
    print("Sending asking message post.....")
    mobile=raw_input('The mobile:')
    message_url="http://172.16.2.90:6710/uic-front/firmManage/firm/getMobileCode.action?mobile=%s&t=0.883366231799672" % mobile
    message_data={"mobile":mobile,"t":"0.883366231799672"}
    print("The mobile phone number:%s " % message_data.get('mobile'))
    message_resp=conn.post(url=message_url,data=message_data,headers=U.get_header())
    print("The new cookie: %s " % message_resp.request.headers.get('cookie'))
    print("Send message post \t %d " % message_resp.status_code)

    register_data=U.get_data()
    register_data['htmlCode']=raw_input("The varify code:")
    register_data['entity.mobile']=message_data.get('mobile')
    register_data['entity.userID']=raw_input("The user name:")

    register_resp=conn.post(url=U.get_url(),data=register_data,headers=U.get_header())
    print("Send register post \t %d " % register_resp.status_code)

    save_result(register_resp)
    print(register_resp.text)


if __name__=='__main__':

    json_file="./data/url.json"
    url_list=get_post_urls(get_json_data(json_file));
    send_post(url_list[0])
    
