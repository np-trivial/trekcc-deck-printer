from lxml import html
import requests
import re
import os
import shutil
from PIL import Image
import tempfile
import sys


if __name__ == '__main__':

	
	try:
		url = sys.argv[1]
		urlmatch = re.match("https?\:\/\/(www.)?trekcc.org/.*deckID\=(\d+)",url)
		decknamesafe = urlmatch.group(2)
	except:
		print("Invalid URL")
		exit(1)

	page = requests.get(url)
	
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
		print(imgurl)
		filename = re.search("\/([^/]+)$",imgurl).group(1)
		imgcontent = requests.get(imgurl)
		image_file = tempfile.TemporaryFile()
		image_file.write(imgcontent.content)
		my_image = Image.open(image_file)
		# omitted because this conversion worked poorly. 
		#TODO: revisit CMYK conversion
		#my_image = my_image.convert(mode="CMYK")
		my_image = my_image.resize((825,1125),resample=Image.LANCZOS)
		for i in range(qty):
			my_image.save(decknamesafe + "/" + str(i) + "_" + filename)

