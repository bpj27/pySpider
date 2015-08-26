# -*- coding: utf-8 -*-


__author__ = 'Administrator'
# 用来爬取X-art图片
# 最终目标分析：
# 	三层网页：main --> album --> single
import os
import re
import urllib
import requests
import sys

# 网页解析器
def UrlOpen(url):
	html = urllib.urlopen(url)
	content = html.read();
	html.close()
	return content


# 下载图片
def saveImg(pic, each, n):
	fileName = n
	# fp = open('H:\\Xart\\' + each + '\\' + str(fileName) + '.jpg', 'wb')
	# fp.write(pic.content)
	# fp.close()
	path = 'H:\\Xart\\' + each + '\\' + str(fileName) + '.jpg'
	urllib.urlretrieve(pic, path, reporthook=report)


# 下载进度显示器
def report(count, blockSize, totalSize):
	percent = int(count * blockSize * 100 / totalSize)
	sys.stdout.write("\r%d%%" % percent + ' complete')
	sys.stdout.flush()


urlMain = "http://www.xartbeauties.com/photos/"
contentMain = UrlOpen(urlMain)

# print(contentMain)

# 正则解析
# 目标：<a href="http://www.xartbeauties.com/galleries/aubrey-in-domination--part-i-8387.html" title="Aubrey in Domination - Part I">

urlAlbum = re.findall('<a href="http://www.xartbeauties.com/galleries/(.*?)" title=.*?"', contentMain, re.S)
# print(len(urlAlbum))

for each in urlAlbum:
	n = 1
	urlEach = "http://www.xartbeauties.com/galleries/" + each
	# 决定在X-art大文件里按照Album名称分文件夹保存(python里成为目录用os.mkdir)
	albumFileName = each.replace(".html", "")
	pathDir = "H:\\Xart\\" + albumFileName

	if os.path.isdir(pathDir) == True:
		pass
	else:
		os.mkdir(pathDir)

	# 突然发现目标其实就是单个Album地址01-END.html,所以很简单的可以直接找到单个图片地址
	temp = urlEach.replace(".html", "/")
	if n < 10:
		urlSingle = temp + "0" + str(n) + ".html"
	else:
		urlSingle = temp + str(n) + ".html"
	# 合集已经找到，再解析一次
	picContent = UrlOpen(urlSingle)
	# 目标：<img src="http://images.xartbeauties.com/source_galleries/x-art_james_deen_aubrey_domination_part_i-med/01.jpg"
	# border="0" alt="X-Art" id="galleryimage" height="657">

	imgList = re.findall('<img src="(.*?)" b.+? alt="X-Art" id="galleryimage" .+?', picContent, re.S)
	pic = imgList[0]

	saveImg(pic, albumFileName, n)
	n = n + 1
	# 暂停下
	raw_input()
