# testing s3
import yaml
import os
import tinys3
import datetime

S3_ACCESS_KEY = ""
S3_SECRET_KEY = ""
# For scope - I had to move the assignment of the yaml variables to here from loadConfigs()
f = open("hourlyArt.yaml", 'r+')
datamap = yaml.load(f)
#f.close()

S3_ACCESS_KEY = datamap['S3_ACCESS_KEY']
S3_SECRET_KEY = datamap['S3_SECRET_KEY']
# close file - then reopen for writing
f.close()


conn = tinys3.Connection(S3_ACCESS_KEY,S3_SECRET_KEY)
ttime = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")

# Uploading a single file
f = open('2015_08_11_18_35_24_image.png','rb')
conn.upload('2015_08_11_18_35_24_image.png',f,'hourlyart', public=True)
f.close()
