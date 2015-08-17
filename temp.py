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
from time import sleep
import shutil

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

f = open("hourlyArt.yaml", 'w+')
#datamap = yaml.load(f)

# update post_number
post_number += 1
datamap['post_number'] = post_number

yaml.dump( datamap, f, default_flow_style=False )
f.close()


# Take the file of artists, read it, and pick a random artist name
'''
with open('newArtList.txt', 'w') as f:
    artistNames = f.readlines()
    print(random.choice(artistNames))
'''
with open('newArtList.txt', 'r') as f:
    artistNames = f.readlines()
    name = random.choice(artistNames)
    print(name)
    #print(random.choice(artistNames))

#


parsedData = []
#req = requests.get('https://www.googleapis.com/customsearch/v1?q=ANDREOLI&key=AIzaSyDDCEIWAf_ryCpO-pyKiQpRhBT_DtS6QmY&cx=015442808760036436136:sbdsxirnsiy&searchType=image&fileType=jpg&imgSize=large&alt=json')
# the one below works great
req = requests.get('https://www.googleapis.com/customsearch/v1?cx=015442808760036436136%3Asbdsxirnsiy&q=' + name + '&fields=items(image%2Clink%2Ctitle)&key=AIzaSyDDCEIWAf_ryCpO-pyKiQpRhBT_DtS6QmY&searchType=image&fileType=jpg&imgSize=large')

#req = requests.get('https://www.googleapis.com/customsearch/v1?cx=015442808760036436136:iv4zccg18bu&q=ANDREOLI&fields=items(image%2Clink%2Ctitle)&key=AIzaSyDDCEIWAf_ryCpO-pyKiQpRhBT_DtS6QmY&searchType=image&fileType=jpg&imgSize=large')
jsonList = []
jsonList.append(json.loads(req.content.decode('utf-8')))
searchData = {}
resultPic = {}

imageList = list()
titleList = list()

# Need to check if the image is empty - if so - start over
for data in jsonList:
    searchData['this'] = data['items']
    for each in searchData['this']:
        #print(each['title'])
        #print(each['link'])
        imageList.append(each['link'])
        titleList.append(each['title'])
        #resultPic['image_link'] = each['link']
        #resultPic['image_title'] = each['title']
    #print(imageList)
    #print(titleList)
    random_index = randrange(0,len(imageList))
    print('choice:')
    image = imageList[random_index]
    title = titleList[random_index]
    print( image )
    print( title )

# download the image
    # Download the image:
    filename = None
    print( 'Downloading %s' % image)
    filein = urllib.request.urlopen(image)
    try:
        newImage = filein.read(5000000)
    except Exception as e:
        print ("Downloading error: " , e)
    except MemoryError: # I sometimes get this exception. Why ?
        print('Memory Error ', e)

    filein.close()
        # Check it.

'''
    if len(image)==0:
        return None  # Sometimes flickr returns nothing.
    if len(image)==5000000:
        return None  # Image too big. Discard it.
    if image.startswith('GIF89a'):
        return None # "This image is not available" image.
        '''

    # Save to disk.
if not filename:
    filename = 'newImage.jpg' #url[url.rindex('/')+1:]
fileout = open(filename,'w+b')
fileout.write(newImage)
fileout.close()

# Now start processing...
os.system("startProcessing.bat")

#os.system("processing-java --sketch=" + processing_location + " --output=" + processing_location + "\HourlyArtBuild --force --run")
#os.system("processing-java --sketch=" + processing_location + " --output=" + processing_location + "\HourlyArtBuild --force --run")
print("Done with processing")
sleep(10)

print(os.getcwd())
# rename the files
ttime = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
# original
os.rename('newImage.jpg', ttime + '_image.jpg')
# new
os.rename('newImage.png', ttime + '_image.png')
# gif
#os.rename('newImage.gif', ttime + '_image.gif')
shutil.copyfile('newImage.gif', ttime + '_image.gif')

# ok - have picture, name - now put it on S3
# Creating a simple connection
conn = tinys3.Connection(S3_ACCESS_KEY,S3_SECRET_KEY)

# Uploading a single file
f = open(ttime + '_image.png','rb')
conn.upload(ttime + '_image.png',f,'hourlyart', public=True)
f.close()

f = open(ttime + '_image.jpg','rb')
#conn.upload(ttime + '_image.jpg',f,'hourlyart', public=True)
f.close()

# upload gif
f = open(ttime + '_image.gif','rb')
conn.upload(ttime + '_image.gif',f,'hourlyart', public=True)
f.close()

os.remove(ttime + '_image.jpg')
os.remove(ttime + '_image.png')
os.remove(ttime + '_image.gif')

# Now create the WP post
# template: https://s3.amazonaws.com/hourlyart/2015_08_11_19_09_07_image.png
imageTemplate = 'https://s3.amazonaws.com/hourlyart/'
postNewImage = imageTemplate + ttime + '_image.png'
postOriginalImage = imageTemplate + ttime + '_image.jpg'
postGif = imageTemplate + ttime + '_image.gif'


# Now create the WP post
tags = '#hourlyart #generative #generativeart #art #artistsontumblr'

message_html = """
The original:
</br>
<img src=""" + image + """ width="450" height="503" class="alignnone" />

The transformed image:
</br>
<img src=""" + postNewImage + """ width="450" height="503" class="alignnone" />

The transformation:
[caption width="450" align="alignnone"]<img src=""" + postGif + """ width="450" height="503" alt="gif" class /> gif[/caption]


[tags """ + tags + """]
[publicize twitter]
"""

server = smtplib.SMTP('smtp.gmail.com:587')
server.ehlo()
server.starttls()

server.login(gmail_user_name, gmail_pass_word)
msg = MIMEMultipart('alternative')
#msg = MIMEMultipart()
markHtml = MIMEText(message_html, 'html')
msg.attach(markHtml)

msg['Subject'] = 'HourlyArt Post #' + str(post_number) + " " + title
me = gmail_user_name
msg['From'] = me
msg['To'] = wp_email
#msg['Body'] = markHtml

#msg.preamble = tags
print( markHtml )
print( msg['Subject'] )

#img = MIMEImage(open('newImage.png',"rb").read(), _subtype="png")
#img.add_header('Content-Disposition', 'attachment; filename="newImage.png"')
#msg.attach(img)

server.sendmail(me, wp_email, msg.as_string())
server.quit()
