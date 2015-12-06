import wikitools
import poster
import pyexiv2
import os
import shutil
import sys
import time
import datetime

ts = time.time()
timestamp  = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d-%H-%M-%S')


wiki_url = "MediaWiki API url here"

#Example: http://commons.wikimedia.org/w/api.php

wiki_username = "USER NAME HERE"
wiki_password = "PASSWORD HERE"


category = ""

try:
	wiki = wikitools.wiki.Wiki(wiki_url)
except:
	print "Can not connect with wiki. Check the URL"


try:
	wiki.login(username=wiki_username,password=wiki_password)

except:
	print "Invalid Username or Password"

path = './'

listing = os.listdir(path)

def filetype(file):
	return file.split(".")[-1]

def filename(file):
	return file.split(".")[-2]


def get_file_details(image):
	try:
		metadata = pyexiv2.ImageMetadata(image)
		metadata.read()
                print metadata
		file_name=(metadata['Xmp.dc.title'].raw_value)['x-default']
                print file_name
		caption=(metadata['Xmp.dc.description'].raw_value)['x-default']
                print caption
		file_meta = {'name':file_name,'caption':caption}
		return file_meta

                
	except:
		print "No tag is set for the image " + image	
		exit	

	

def move_photo(image):
	source = image
	destination = "./uploaded-"+ timestamp + "/" + image

	if os.path.isdir("uploaded-" + timestamp):
		shutil.move(source,destination)
	else:
		os.mkdir("uploaded-" + timestamp)
		shutil.move(source,destination)		
	print "Moving the Photo " + image + " to the folder 'uploaded-'" + timestamp

def uploadphoto(image):
	meta = get_file_details(image)	
	
	if meta:
		file_name = meta['name']
		caption = meta['caption']
		extension = filetype(image)
                upload_file_name = file_name + "." + extension
                
		image_object=open(image,"r")
		picture=wikitools.wikifile.File(wiki=wiki, title=file_name)
        	picture.upload(fileobj=image_object,comment=caption, ignorewarnings=True)
		print "Uploaded the Image " + file_name

		page_name = file_name.replace(" ","_")

		page = wikitools.Page(wiki, "File:" + page_name + "." + extension, followRedir=True)
		wikidata = "=={{int:filedesc}}=={{Information|description={{en|1= " + caption + "}}|source={{own}}|author=[[User:" + wiki_username + "|" + wiki_username + "]]}}=={{int:license-header}}=={{self|cc-by-sa-3.0}}[[Category:" + category + "]] [[Category:Uploaded with MediawikiUploader]]"

		page.edit(text=wikidata)

		move_photo(image)
		
for photo in listing:
	if filetype(photo) in ['JPG','jpg','GIF','gif','png','PNG']:
		uploadphoto(photo)
		



