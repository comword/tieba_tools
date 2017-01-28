#!/usr/bin/env /usr/bin/python3
# -*- coding:utf-8 -*-
import urllib.request
import urllib.parse
import os,yaml
import argparse

TOKEN_URL = "https://passport.baidu.com/v2/api/?getapi&tpl=mn&apiver=v3"
LOGIN_URL = "https://passport.baidu.com/v2/api/?login"

reg_token = re.compile("\"token\"\s+:\s+\"(\w+)\"")

class login_col:
    def __init__(self):
        pass
    def login_withpassword(self,uname,password):
        sign_url = 'http://c.tieba.baidu.com/c/c/forum/sign'
    def _make_sign_request(tieba, fid, tbs, BDUSS):
        sign_url = 'http://c.tieba.baidu.com/c/c/forum/sign'
        sign_request = urllib.parse.urlencode({"BDUSS": BDUSS, "_client_id": "03-00-DA-59-05-00-72-96-06-00-01-00-04-00-4C-43-01-00-34-F4-02-00-BC-25-09-00-4E-36", "_client_type":
                        "4", "_client_version": "1.2.1.17", "_phone_imei": "540b43b59d21b7a4824e1fd31b08e9a6", "fid": fid, "kw": tieba, "net_type": "3", 'tbs': tbs})
        sign_request = sign_request.encode('UTF-8')
        sign_request = urllib.Request(sign_url, sign_request)
        sign_request.add_header("Content-Type", "application/x-www-form-urlencoded")
        return sign_request

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
