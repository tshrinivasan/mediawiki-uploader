# Introduction #

Mediawiki Uploader 0.1

Author: T Shrinivasan
Email: tshrinivasan@gmail.com.


# Details #


Description:

Mediawiki uploader uploads all the files in the current directory to a mediawiki installation.

I created this to contribute to Wikimedia Commons.
http://commons.wikimedia.org



You need the following to use this application.

1. Mediawiki API path
2. Username
3. Password


Provide them in the following variables

1. wiki\_url
2. wiki\_username
3. wiki\_password

Example:
wiki\_url = "http://commons.wikimedia.org/w/api.php"
wiki\_username = "tshrinivasan"
wiki\_password = "MY PASSWORD HERE"

We need to add IPTC tags to the images to add the detailed filename and description.
I use GThumb image viewer in my ubuntu 11.10 machine.

Using this, we can add/edit comments using the following menu
Edit->Comment or Ctrl+M

Filled the values for "Description" and "Title"

These values will be used as description and filename while uploading.

Note: If you do not set the Description and Title using the GThumb viewer, that file wont get uploaded.



After uploaded the files will be moved to a subdirectory named "uploaded".
If any file is missed out in the current directory, this means that the IPTC tags are not set properly.
Use GThumb and set them.




Add your content here.  Format your content with:
  * Text in **bold** or _italic_
  * Headings, paragraphs, and lists
  * Automatic links to other wiki pages