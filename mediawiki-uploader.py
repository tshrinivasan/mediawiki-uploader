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

#wiki_url =  "https://commons.wikimedia.org/w/api.php"

wiki_username = ""
wiki_password = ""


category = ""

try:
	wiki = wikitools.wiki.Wiki(wiki_url)
except:
	print "Can not connect with wiki. Check the URL"


login_result = wiki.login(username=wiki_username,password=wiki_password)

#print "login status = " + str(login_result)
if login_result == True:
	print "Logged in."
else:
	print "Invalid username or password error"
	sys.exit()







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
 #               print metadata
		file_name=(metadata['Xmp.dc.title'].raw_value)['x-default']
 #               print file_name
		caption=(metadata['Xmp.dc.description'].raw_value)['x-default']
 #               print caption
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
	print "Moving the Photo " + image + " to the folder 'uploaded-" + timestamp + "'"

def uploadphoto(image):
	meta = get_file_details(image)	
	
	if meta:
                print "Uploading the Image " + image
		file_name = meta['name']
		caption = meta['caption']
		extension = filetype(image)
                upload_file_name = file_name + "." + extension
                
		image_object=open(image,"r")
		picture=wikitools.wikifile.File(wiki=wiki, title=upload_file_name)
        	picture.upload(fileobj=image_object,comment=caption, ignorewarnings=True)
        

		page_name = file_name.replace(" ","_")

		page = wikitools.Page(wiki, "File:" + page_name + "." + extension, followRedir=True)
#		wikidata = "=={{int:filedesc}}=={{Information|description={{en|1= " + caption + "}}|source={{own}}|author=[[User:" + wiki_username + "|" + wiki_username + "]]}}=={{int:license-header}}=={{self|cc-by-sa-3.0}}[[Category:" + category + "]] [[Category:Uploaded with MediawikiUploader]]"

                wikidata = """=={{int:filedesc}}==
{{Information
|description={{en|1= """ + caption + """}}
|source={{own}}
|author= [[User:""" + wiki_username + "|" + wiki_username + """]]
|permission=
|other versions=
}}

=={{int:license-header}}==
{{self|cc-by-sa-4.0}}

[[Category:Uploaded with MediawikiUploader]]

"""

                if len(category.strip()) > 2:
                        wikidata = wikidata + "\n" + "[[Category:" + category + "]]"

		page.edit(text=wikidata)

                print "Image URL = " +  wiki_url.split('/w')[0] + "/wiki/File:" + page_name + "." + extension 

		move_photo(image)
		
for photo in listing:
	if filetype(photo) in ['JPG','jpg','GIF','gif','png','PNG']:
		uploadphoto(photo)
		



