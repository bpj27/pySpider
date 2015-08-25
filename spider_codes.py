# -*- coding: utf-8 -*-
import re
import urllib
import requests
import time

'''
    简易自动翻页功能已经实现
    （bytes）强制转换并存

'''


def spider(n):
	# 读取网页
	url = 'http://wanimal1983.tumblr.com/page/' + n
	html = urllib.urlopen(url)
	content = html.read()
	html.close()
	print('now it is reading:', n)
	# 解析网页
	# regex = r'<img style=".*?" src="(.*?)">'
	# pat = re.compile(regex)

	images_code = re.findall('<img src="(.*?)"', content, re.S)
	if len(images_code) == 0:
		return 0
	else:
		# 下载网页

		i = 0
		for each in images_code:
			if i == len(images_code):
				print("It is Over", n)
			else:
				print('>>>>>>>>now downloading:' + each)

				pic = requests.get(each)

				file_name = n + (bytes)(i)
				fp = open('H:\\Wannal\\' + str(file_name) + '.jpg', 'wb')
				fp.write(pic.content)
				time.sleep(1)
				fp.close()
				i += 1


n = 3
for n in range(3,100):
	n += 1
	number = (bytes)(n)
	spider(number)
	time.sleep(1)
