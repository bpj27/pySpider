# -*- coding: utf-8 -*-
import os
import re
import urllib
import requests
import time
import random
from multiprocessing.dummy import Pool as ThreadPool

'''
    简易自动翻页功能已经实现
    （bytes）强制转换并存
    urllib.urlopen(某网站，proxyes={'http:':"某代理IP地址:代理的端口"})
    网站：http://www.dbmeinv.com/dbgroup/show.htm?cid=2&pager_offset=1


'''


def spider(url):
	# 读取网页
	n = url.replace("http://www.dbmeinv.com/dbgroup/show.htm?cid=2&pager_offset=","")

	html = urllib.urlopen(url)
	content = html.read()
	html.close()
	# print('now it is reading:', n)
	# 解析网页
	# regex = r'<img style=".*?" src="(.*?)">'
	# pat = re.compile(regex)

	images_code = re.findall('<img class="height_min" .+? src="(.*?)"', content, re.S)
	# fileName = re.findall('<img class="height_min" title="(.*?)" .+?"', content, re.S)
	print("------>IMG  =   ")
	print(images_code)

	if len(images_code) == 0:
		return 0
	else:
		# 下载网页

		i = 0

		for each in images_code:
			path = 'D:\\doubanGirl'
			if os.path.isdir(path)==True:
				pass
			else:
				try:
					os.mkdir(path)
				except IOError,e:
					print(e)
					pass
			if i == len(images_code):
				print("It is Over", n)
				break
			else:
				print('>>>>>>>>now downloading:' + each)
				pic = requests.get(each)
				if n =="1":
					file_name = (bytes)(i)
				else:
					temp = (int(n)-1)*len(images_code)
					file_name = temp+i
				path = path + "\\"
				fp = open(path + str(file_name) + '.jpg', 'wb')
				fp.write(pic.content)
				fp.close()
				i += 1


urls=[]
pool = ThreadPool(2)

for n in range(0, 1000):
	n += 1
	url = 'http://www.dbmeinv.com/dbgroup/show.htm?cid=2&pager_offset=' + bytes(n)
	urls.append(url)
pool.map(spider,urls)
pool.close()
pool.join()
