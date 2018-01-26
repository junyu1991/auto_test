#!encoding:utf-8

class RequestInfo:
    '''
    Store the request info which configed in .json file
    The json example like this:
    "example":{
		"path1":{
			"root_url":"",
			"logon":{
				"method":"post",
				"url":"",
				"random_img_url":"",
				"param":{
					"param1":"",
					"param2":"",
					"param3":"",
					"param4":""
				}
			},
			"headers":{
				"Referer":"",
				"User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
			}
		}
    }
    '''

    def __init__(self,request_name,root_url,logon,header,request_list):
        self._request_name=request_name
        self._root_url=root_url
        self._logon=logon
        slef._header=header
        self._request_list=request_list

    def get_root_url(self):
        return self._root_url

    def get_header(self):
        return self._header
