#!/usr/bin/env /usr/bin/python3
# -*- coding:utf-8 -*-
import os
import re
import urllib

class writer:
	def __init__(self):
		pass

	def w_process(self,dics):
		c = dics["m_content"]
		c = re.sub("\<\/?(span).*?\>","",c)
		c = re.sub("\n","<br/>",c)
		tmp = re.search("data-url\=\'(.*?)\'\>",c)
		if tmp != None:
			imgsrc = tmp.group(1)
			c = re.sub("\<div.*?data-url\=\'(.*?)\'\>","<img src='%s'>" % imgsrc,c)
		dics["m_content"] = c
		return dics

	def go_writer(self,lists,conf):
		out = os.path.join(os.getcwd(),conf.out_p)
		if not os.path.isdir(out):
			os.makedirs(out)
		if conf.split == None:
			f = open(os.path.join(out,str(conf.curr_pg)+".html"), 'w')
			f.write('''<!DOCTYPE html>
<html lang="cn">
<head>
  <meta charset="utf-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>%(title)s</title>
</head>
<body>
''' % {"title": conf.title+"_"+str(conf.curr_pg)})
			for post in lists:
				f.write("""
<div style=\"border-bottom: 1px solid #eaebec;\">
	<div style=\"float: left;\">
		<img src=\"%(ava_src)s\" alt=\"头像\" width=\"40\" height=\"40\"/>
	</div>
	<div>%(username)s<br/>%(fn)s楼 %(time)s</div>
	<div>%(content)s</div>
</div>\n""" % {"ava_src":post["avatar_src"],"time":post["post_date"],"fn":post["fn"],"username":post["poster_name"],"content":post["m_content"]})
			f.write("</body></html>")
