# -*- coding: utf-8 -*-
import os

import re
import chardet
import spynner
import requests
from multiprocessing.dummy import Pool as ThreadPool


# 网页解析器
def analysisHtml(url):
	# browser 类中有一个类方法load，可以用webkit加载你想加载的页面信息。
	# load(是你想要加载的网址的字符串形式)
	# 创建一个浏览器对象
	album = 0
	print('------>当前页面为' + url)
	try:
		browser.load(url=url, tries=5)
		browser.load_jquery(True)
	except spynner.SpynnerTimeout, e:
		print(e)
		pass

	# browser.show()

	# browser 类中有一个成员是html，是页面进过处理后的源码的字符串.
	# 将其转码为UTF-8编码
	content = browser.html.encode("utf-8")

	# 获得单页所有相册集的地址
	# <a class="img js-anchor etag noul" hidefocus="true" target="_blank" href="http://pp.163.com/atao/pp/15608026.html" title="谁为你做的嫁衣">
	urlAlbum = re.findall('<a class="img js-anchor etag noul" hidefocus="true" target.*? href="(.*?)" title=.*?>',
						  content,
						  re.S)
	# print(len(urlAlbum))
	browser.hide()
	while (album <= len(urlAlbum) - 1):
		try:
			browser.load(urlAlbum[album], load_timeout=50, tries=5)
			browser.load_jquery(True)
		except spynner.SpynnerTimeout, e:
			print(e)
			pass

		imgContent = browser.html.encode("utf-8")

		# 获得图片地址集
		u1 = '<img class="z-tag data-lazyload-src" .*? src="(.*?)"'
		imgUrl = re.findall(u1, imgContent, re.S)
		# 获取标题
		# <meta name="description" content="晚·远 by 無小宾摄影">
		u2 = '<meta name="description" content="(.*?)">'
		albumName = re.findall(u2, imgContent, re.S)
		title = albumName[0].replace("\t", "").replace("\n", "").replace("【", "").replace("】", "").replace("《",
																										   "").replace(
			"》", "").replace("&lt;","").replace("&gt;","")
		title = title.rstrip()
		# point = 'by TONNYLAW'
		# isMyAim = title.find(point) #失败是-1
		# 创建目录
		pathAlbum = 'H:/wangyiGirl/' + title.decode('utf-8').encode('gbk')

		if os.path.isdir(pathAlbum) == True:
			pass
		else:
			try:
				# 建立目录
				os.mkdir(pathAlbum)
				# 文件下载
				save(imgUrl, pathAlbum, title)
			except WindowsError, e:
				print(e)
				pass
			except IOError, e:
				print(e)
				pass
		album = album + 1


# 文件下载
def save(imgUrl, pathAlbum, title):
	n = 0
	for img in imgUrl:
		pic = requests.get(img)
		imgPath = pathAlbum + "/" + str(n) + ".jpg"

		if os.path.isfile(imgPath) == True:
			print(title + "--->" + str(n))
			pass
		else:
			print(title + "--->" + str(n))
			fp = open(imgPath, "wb")
			fp.write(pic.content)
			fp.close()
		n = n + 1


browser = spynner.Browser()
browser.create_webview()
print("1:默认    2:黑白    3:日系")
num = raw_input()
initPage = {
	"1": "http://pp.163.com/pp/#p=10&c=-1&m=3&page=",
	"2": "http://pp.163.com/pp/#p=10&c=283&m=3&page=",
	"3": "http://pp.163.com/pp/#p=10&c=285&m=3&page="
}
for n in range(1, 501):
	page = initPage[num] + str(n)
	analysisHtml(page)
browser.close()
