#!/usr/bin/env /usr/bin/python3
# -*- coding:utf-8 -*-
import re,os

class writer:
	def __init__(self):
		pass

	def w_process(self,dics):
		dics.pop("avatar_src")
		c = dics["m_content"]
		c = re.sub("\<\/?(span|div|img|p).*?\>","",c) #remove images
		dics["m_content"] = c
		if "subfloors" in dics:
			d = dics["subfloors"]
			for index,item in enumerate(d):
				d[index]["m_content"] = re.sub("\<\/?(span|div|img|p).*?\>","",item["m_content"]) #remove images
			dics["subfloors"] = d
		return dics

	def go_writer(self,lists,conf):
		out = os.path.join(os.getcwd(),conf.out_p)
		if not os.path.isdir(out):
			os.makedirs(out)
		if conf.split == None: # nature split based on page number
			#print(os.path.join(out,str(conf.curr_pg)+".txt"))
			f = open(os.path.join(out,str(conf.curr_pg)+".txt"), 'w')
			for post in lists:
				f.write("%(time)s %(fn)s楼 %(username)s: %(content)s\n" % {"time":post["post_date"],"fn":post["fn"],"username":post["poster_name"],"content":post["m_content"]})
				if "subfloors" in post:
					for subp in post["subfloors"]:
						f.write("\t%(time)s %(username)s: %(content)s\n" % {"time":subp["post_date"],"username":subp["poster_name"],"content":subp["m_content"]})
			f.close()
