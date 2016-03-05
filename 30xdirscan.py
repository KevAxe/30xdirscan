#!/usr/bin/env python
# -*- encoding:utf-8 -*-
# author: KevAxe
# email: kevaxe@qq.com

import httplib
import threading
import Queue
import urllib
import optparse

wordlist_file = "big.txt" #字典文件
#extensions = [".php",".bak",".orig",".inc"]
resume = None
user_agent = "Mozilla/5.0 (X11; Linux x86_64; rv:19.0) Gecko/20100101 Firefox/19.0"
#httplib.HTTPConnection.debuglevel = 1

#加载字典，返回队列
def build_wordlist(wordlist_file):
	fd = open(wordlist_file,"rb")
	raw_words = fd.readlines()
	fd.close()

	found_resume = False
	words = Queue.Queue()

	for word in raw_words:
		word = word.rstrip()

		if resume is not None:
			if found_resume:
				words.put(word)

			else:
				if word == resume:
					found_resume = True
					print "Resuming wordlist from: %s" % resume
		else:
			words.put(word)

	return words
#目录爆破
def dir_bruter(word_queue,extensions=None):
	while not word_queue.empty():
		attempt = word_queue.get()
		attempt_list = []

		attempt_list.append("/%s" % attempt)

		#将想要暴力的扩展名加入字典
		if extensions:
			for extension in extensions:
				attempt_list.append("/%s%s" % (attempt,extension))

		#迭代我们要尝试的文件列表
		for brute in attempt_list:
			content = urllib.quote(brute)
			headers = {}
			headers["User-Agent"] = user_agent
			try:
				conn = httplib.HTTPConnection(host = url, port = 80,timeout = 10)
				conn.request(method = 'GET',url = sub_content + content,headers = headers)
				res = conn.getresponse()
				brute_url = 'http://' + url + sub_content + content
				if res.status != 404:
					if str(res.status)[0:2] == '30':
						for item in res.getheaders():
							#print item
							if item[0] == 'location' and item[1] ==  brute_url + '/':
								print '[%s]:%s' % (res.status,item[1])
					#else:
					#	print '[%s]:%s' % (res.status,brute_url)
				conn.close()
			except Exception,e:
				print e,":",brute_url
if __name__ == '__main__':
	parser = optparse.OptionParser('usage: %prog [options] argv')
	parser.add_option('-u','--url',dest='url',type='string',help='Your target url,e.g. www.kevaxe.com')
	parser.add_option('-s','--sub_content',dest='sub_content',default=None,type='string',help='sub_content of target url,e.g. /admin')
	parser.add_option('-t','--threads',dest='threads',default=10,type='int',help='Threads num,default:10')

	(options,args) = parser.parse_args()
	#print options
	#print args
	url = options.url
	sub_content = options.sub_content
	threads = options.threads
	extensions = args

	word_queue = build_wordlist(wordlist_file)

	for i in range(threads):
		t = threading.Thread(target=dir_bruter,args=(word_queue,extensions,))
		t.start()



