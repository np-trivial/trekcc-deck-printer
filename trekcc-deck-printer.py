from lxml import html
import requests
#import csv
#import io
import re
import os
import shutil
from PIL import Image
import tempfile
import sys


if __name__ == '__main__':

	
	try:
		url = sys.argv[1]
		#print(url)
		urlmatch = re.match("https?\:\/\/(www.)?trekcc.org/.*deckID\=(\d+)",url)
		decknamesafe = urlmatch.group(2)
		#print(decknamesafe)
	except:
		print("Invalid URL")
		exit(1)

	# https://www.trekcc.org/decklists/index.php?deckID=41504&mode=download
	page = requests.get(url)
	#tree = html.fromstring(page.content)
	#links = re.findall("(\dx)?\s*\<a\s+href=\"(http:\/\/trekcc.org\/\de\/index\.php\?cardID=\d+)",page.text)
	#decknamesafe="41504"
	
	t = html.fromstring(page.content)
	deckname = t.xpath("//h2/text()")[0]
	decknamesafe = re.sub("[^\w]","_",deckname)
	print(deckname)
	print(decknamesafe)
	
	try:
		os.mkdir(decknamesafe)
	except FileExistsError:
		pass

	for qty, cardurl in re.findall("(\d+x)?\s*\<a\s+href=\"(http:\/\/trekcc.org\/\de\/index\.php\?cardID=\d+)",page.text):
		foo = re.match("\d+",qty)
		if foo:
			qty = int(foo.group())
		else:
			qty = 1
		print(qty , "|" , cardurl)
		 
		# follow card URL
		cardpage = requests.get(cardurl)
		cardpagetree = html.fromstring(cardpage.content)
		imgurl = cardpagetree.xpath('//a[@href="javascript:history.go(-1)"]//img')[0].attrib['src']
		#print(imgurl[0].attrib['src'])
		print(imgurl)
		filename = re.search("\/([^/]+)$",imgurl).group(1)
		print(filename)
		imgcontent = requests.get(imgurl)
		image_file = tempfile.TemporaryFile()
		image_file.write(imgcontent.content)
		my_image = Image.open(image_file)
		#my_image = my_image.convert(mode="CMYK")
		my_image = my_image.resize((825,1125),resample=Image.LANCZOS)
		for i in range(qty):
			#dest_file = open(decknamesafe + "/" + str(i) + "_" + filename, "wb")
			#dest_file.write(imgcontent.content)
			#shutil.copyfileobj(imgcontent.content, dest_file)
			#dest_file.close()
			my_image.save(decknamesafe + "/" + str(i) + "_" + filename)

		#image_url = re.findall("https?:\/\/www.trekcc.org\/\de\/cardimages\/[^/]+",cardpage.text)
		#print("cardurl: " , image_url)
		# download image
		# https://www.trekcc.org/2e/cardimages/STVE-EN43004.jpg
		#break
