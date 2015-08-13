import yaml
import smtplib
import urllib
import os
import sys
#import urllib2
import requests
import json
import codecs
import pprint
import random
from random import randrange
import tinys3
import datetime

# Here are the email package modules we'll need
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
#from twython import Twython

# config vals
gmail_user_name = ""
gmail_pass_word = ""
tumblr_email = ""
random_word = ""
api_key = ""
api_secret = ""
oauth_token = ""
oauth_token_secret = ""
S3_ACCESS_KEY = ""
S3_SECRET_KEY = ""
wp_email = ""

# For scope - I had to move the assignment of the yaml variables to here from loadConfigs()
f = open("hourlyArt.yaml", 'r+')
datamap = yaml.load(f)
#f.close()

gmail_user_name = datamap['gmail_user_name']
gmail_pass_word = datamap['gmail_user_pass']
flickr_api_key = datamap['flickr_api_key']
flickr_api_secret = datamap['flickr_api_secret']
tumblr_email = datamap['tumblr_email']
post_number = datamap['post_number']
processing_location = datamap['processing_location']
api_key = datamap['api_key']
api_secret = datamap['api_secret']
oauth_token = datamap['oauth_token']
oauth_token_secret = datamap['oauth_token_secret']
S3_ACCESS_KEY = datamap['S3_ACCESS_KEY']
S3_SECRET_KEY = datamap['S3_SECRET_KEY']
wp_email = datamap['wp_email']
# close file - then reopen for writing
f.close()

#f = open("hourlyArt.yaml", 'w+')
#datamap = yaml.load(f)

f.close()



postNewImage = "bal"
postOriginalImage = "bal"
postGif = "bal"


# Now create the WP post
message_html = """
The original:
</br>
<img src=""" + postOriginalImage + """ width="450" height="503" class="alignnone" />

The transformed image:
</br>
<img src=""" + postNewImage + """ width="450" height="503" class="alignnone" />

The transformation:
[caption width="450" align="alignnone"]<img src=""" + postGif + """ width="450" height="503" alt="gif" class /> gif[/caption]
"""
server = smtplib.SMTP('smtp.gmail.com:587')
server.ehlo()
server.starttls()

server.login(gmail_user_name, gmail_pass_word)
msg = MIMEMultipart('alternative')
#msg = MIMEMultipart()
markHtml = MIMEText(message_html, 'html')
msg.attach(markHtml)

msg['Subject'] = 'HourlyArt Post #' + str(post_number)
me = gmail_user_name
msg['From'] = me
msg['To'] = wp_email
#msg['Body'] = markHtml
tags = '#hourlyart #generative #generativeart #art #artistsontumblr #' + random_word.rstrip()
#msg.preamble = tags
print( markHtml )
print( msg['Subject'] )

#img = MIMEImage(open('newImage.png',"rb").read(), _subtype="png")
#img.add_header('Content-Disposition', 'attachment; filename="newImage.png"')
#msg.attach(img)

server.sendmail(me, wp_email, msg.as_string())
server.quit()
