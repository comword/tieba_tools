#!/usr/bin/env /usr/bin/python3
# -*- coding:utf-8 -*-
import urllib.request
import urllib.parse
import json,re
import os,argparse,imp
from html.parser import HTMLParser

class clawer:
	def __init__(self):
		pass

	def set_page(self,tid,pn):
		params = urllib.parse.urlencode({'kz': tid, 'pn': pn,'is_ajax': 1, 'has_url_param': 0, 'post_type': 'normal'})
		req = urllib.request.Request("https://tieba.baidu.com/mo/q/m"+"?%s" % params)
		req.add_header('User-Agent', 'Mozilla/5.0 (Linux; Android 7.1.1; Nexus 6P Build/N4F26J) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.91 Mobile Safari/537.36')
		req.add_header('Accept', 'application/json')
		return req

	def get_url(self,req):
		with urllib.request.urlopen(req) as f:
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

	def get_title(self,tid):
		req = urllib.request.Request("https://tieba.baidu.com/p/%s" % tid)
		req.add_header('User-Agent', 'Mozilla/5.0 (Linux; Android 7.1.1; Nexus 6P Build/N4F26J) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.91 Mobile Safari/537.36')
		req.add_header('Accept', '"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"')
		with urllib.request.urlopen(req) as f:
			res = f.read().decode('utf-8')
		tmp = re.search('\<title\>(.*?)\<\/title\>',res)
		return tmp.group(1)

class html_helper(HTMLParser):
	def __init__(self):
		HTMLParser.__init__(self)
		self.data = dict()
	def handle_starttag(self, tag, attrs):
		try:
			if tag == "li": #get li data
				for k,v in attrs:
					if k == "tid" or k == "fn":
						self.data[k] = v
			if tag == "img": #get avatar
				for index,item in enumerate(attrs):
					if item[0] == 'alt' and item[1] == '头像':
						self.data["avatar_src"] = attrs[0][1]
		except:
			print("A error happened in processing starttag")
			return
	def handle_data(self, data):
		pass
	def handle_endtag(self, tag):
		pass
	def get_post(self,it):
		self.data["poster_name"] = self.replace_char(self.get_poster(it))
		self.set_flags(it)
		self.data["post_date"] = self.get_posttime(it)
		self.data["m_content"] = self.replace_char(self.get_maincontent(it))
		self.feed(it)
		tmp = self.data
		self.data = dict()
		return tmp
	def get_forumname(self,pg):
		tmp = re.search('\<h.?\>(.*?)\<',pg)
		if tmp != None:
			return tmp.group(1)
		return None
	def get_poster(self,post):
		tmp = re.search('class\=\"user_name\"\>(\S+)\<\/a\>',post)
		if tmp != None:
			return tmp.group(1)
		return None
	def set_flags(self,post):
		tmp = re.search('\<HAVESUBPOST\>',post)
		if tmp != None:
			self.data["fl_SUBPOST"] = True
		else:
			self.data["fl_SUBPOST"] = False
	def get_maincontent(self,post):
		tmp = re.search('\<div\s+?class\=\"content\"\s+?lz\=\".\"\>\s+(.*?)\<\/div\>',post)
		if tmp != None:
			return tmp.group(1)
	def get_posttime(self,post):
		tmp = re.search('\<span\s+?class\=\"list_item_time\"\>(.*?)\<\/span\>',post)
		if tmp != None:
			time = tmp.group(1)
			return time
	def replace_char(self,m_in):
		res = re.sub('\<br\>|\<br\/\>', "\n", m_in)
		res = re.sub('\<a.*?\>|\<\/a>', "", res) # remove link tag
		res = re.sub('\&(amp\;)+', "&", res)
		res = self.unescape(res)
		return res
class tb_spider:
	def __init__(self,procer):
		self.tid = 0
		self.out_p = ""
		self.begin = None
		self.end = None
		f, filename, description = imp.find_module(procer,["."])
		self.procermod = imp.load_module(procer, f, filename, description)
		self.clawer = clawer()
		self.html_parser = html_helper()
		self.writer = self.procermod.writer()

	def get_length(self,pg):
		tmp = re.search(',\"total_page":\d+,', pg )
		return int(re.search('\d+', tmp.group(0) ).group(0))

	def json_filter(self,js):
		tmp = re.sub('\<script\>.*?script\>', '', js) #remove all scripts
		tmp = re.sub('\<style.*?style>', '', tmp) #remove all style
		tmp = re.sub('\<div\s+class=.?\"(?!content|user_name|f|list?).*?\".*?div>', '', tmp) #remove all divs with garbage class
		tmp = re.sub('\<div\s+class=.?\"list.{0,15}?operation.*?div>', '', tmp)
		#tmp = re.sub('data-.{0,10}?=.?(\"|\').*?(\"|\')', '', tmp)
		tmp = re.sub('\<li\s+class=.?\"{0,15}?\".*?li>', '', tmp)
		tmp = re.sub('\s+class\=.?\"(?!content|user_|list_item_top_avatar|list_item_time?).*?\"', '', tmp)
		return tmp

	def download(self):
		req = self.clawer.set_page(self.tid,1)
		pg = self.clawer.get_url(req)
		pg = self.json_filter(pg)
		self.length = self.get_length(pg)
		self.title = self.clawer.get_title(self.tid)
		if self.out_p == None:
			self.out_p = self.title
		if(self.begin == None or self.begin == 0):
			self.begin = 0
		if(self.end == None):
			self.end = self.length + 1
		if(self.end > self.length + 1):
			print("The number of end page is wrong. Max number is %d" % self.length)
			return None
		self.do_down()

	def do_down(self):
		for i in range(self.begin,self.end):
			print("Downloading page %d"%i)
			self.curr_pg = i
			req = self.clawer.set_page(self.tid,(i-1)*30)
			pg = self.clawer.get_url(req)
			pg = self.json_filter(pg)
			html = json.loads(pg)["data"]["html"]
			html = re.sub('\<ul\>.*?\<\/ul>','<HAVESUBPOST>',html)
			html = re.sub('\<a\s+href\=\"javascript\:\;\"\>还有\d+条回复…\<\/a\>','',html)
			forumname = self.html_parser.get_forumname(html)
			m = re.findall('\<li\s+tid=\"\d+\".*?\<\/li\>',html)
			m_all = list()
			for it in m:
				res = self.html_parser.get_post(it)
				if res["fl_SUBPOST"]:
					res = self.proc_subfloor(res,1)
				res = self.writer.w_process(res)
				m_all.append(res)
			self.writer.go_writer(m_all,self)

	def proc_subfloor(self,data,pg):
		f_data = json.loads(self.clawer.get_subfloor(self.tid,data["tid"],pg))
		total_page = f_data["data"]["page"]["total_page"]
		f_pg = f_data["data"]["floor_html"]
		m = re.findall('\<li\s+pid.*?\<\/li>',f_pg)
		if "subfloors" in data:
			res = data["subfloors"]
		else:
			res = list()
		for it in m:
			d = dict()
			tmp = re.search('\<span class\=\"floor_content\"\>\s+(.*?)\<\/span>',it)
			if tmp != None:
				d["m_content"] = self.html_parser.replace_char(tmp.group(1))
			tmp = re.search('\"un\"\:\"(.*?)\"',it)
			if tmp != None:
				d["poster_name"] = tmp.group(1)
			tmp = re.search('\<span\s+class\=\"list_item_time\"\>\s+(.*?)\<\/span\>',it)
			if tmp != None:
				d["post_date"] = tmp.group(1)
			res.append(d)
		data["subfloors"] = res
		if pg < total_page:
			self.proc_subfloor(data,pg+1)
		return data

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
	if args.begin != None:
		D.begin = int(args.begin)
	if args.end != None:
		D.end = int(args.end)+1
	print("Begin downloading...")
	D.download()
