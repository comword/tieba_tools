#!/usr/bin/env /usr/bin/python3
# -*- coding:utf-8 -*-
import urllib.request
import urllib.parse
import json,re
import os,yaml,argparse,imp

class clawer:
	def __init__(self):
		pass

	def set_page(self,tid,pn):
		self.params = urllib.parse.urlencode({'kz': tid, 'pn': pn,'is_ajax': 1, 'has_url_param': 0, 'post_type': 'normal'})
		self.req = urllib.request.Request("https://tieba.baidu.com/mo/q/m"+"?%s" % self.params)
		self.req.add_header('User-Agent', 'Mozilla/5.0 (Linux; Android 7.1.1; Nexus 6P Build/N4F26J) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.91 Mobile Safari/537.36')
		self.req.add_header('Accept', 'application/json')

	def get_url(self):
		with urllib.request.urlopen(self.req) as f:
			res = f.read().decode('utf-8')
		return res

	def get_subfloor(self,tid,pid,fpn):
		params = urllib.parse.urlencode({'kz': tid, 'pid': pid, 'fpn': fpn,'is_ajax': 1, 'has_url_param': 0})
		req = urllib.request.Request("https://tieba.baidu.com/mo/q/flr?%s" % params)
		req.add_header('User-Agent', 'Mozilla/5.0 (Linux; Android 7.1.1; Nexus 6P Build/N4F26J) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.91 Mobile Safari/537.36')
		req.add_header('Accept', 'application/json')
		with urllib.request.urlopen(req) as f:
			res = f.read().decode('utf-8')
		return res

class tb_spider:
	def __init__(self,procer):
		self.tid = 0
		self.out_p = ""
		self.split = 0
		f, filename, description = imp.find_module(procer,["."])
		self.procermod = imp.load_module(procer, f, filename, description)
		self.clawer = clawer()
		self.processor = self.procermod.processor(clawer)
		self.writer = self.procermod.writer()

	def get_length(self,pg):
		tmp = re.search(',\"total_page":\d+,', pg )
		return int(re.search('\d+', tmp.group(0) ).group(0))

	def json_filter(self,js):
		tmp = re.sub('\<script\>.*?script\>', '', js) #remove all scripts
		tmp = re.sub('\<style.*?style>', '', tmp) #remove all style
		tmp = re.sub('\<div\s+class=.?\"(?!content|user_name|list?).*?\".*?div>', '', tmp) #remove all divs with garbage class
		tmp = re.sub('\<div\s+class=.?\"list.{0,15}?operation.*?div>', '', tmp)
		tmp = re.sub('data-.{0,10}?=.?(\"|\').*?(\"|\')', '', tmp)
		tmp = re.sub('\<li\s+class=.?\"{0,15}?\".*?li>', '', tmp)
		return tmp

	def download(self):
		self.clawer.set_page(self.tid,1)
		pg = self.clawer.get_url()
		pg = self.json_filter(pg)
		self.length = self.get_length(pg)
		print(json.loads(pg))
		if(self.begin == None or self.begin == 0):
			self.begin = 1
		if(self.end == None):
			self.end = self.length
		if(self.end > self.length):
			print("The number of end page is wrong. Max number is %d" % self.length)
			return None

	def do_down(self):
		for i in range(self.begin,self.end):
			pass

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("tid",type=int,help="the tid of a post")
	parser.add_argument("-o","--out",help="the out directory")
	parser.add_argument("-b","--begin",help="the begin page")
	parser.add_argument("-e","--end",help="the end page")
	parser.add_argument("-s","--split",help="split the output based on the number of posts.")
	parser.add_argument("-t","--type",help="the processing type",required=True)
	args = parser.parse_args()
	D = tb_spider(args.type)
	D.tid = args.tid
	D.split = args.split
	D.out_p = args.out
	D.begin = args.begin
	D.end = args.end
	print("Begin downloading...")
	D.download()