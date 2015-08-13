'''
    This file was just used to clean up the raw artist_list.txt file that I created from
    this wiki page: https://en.wikipedia.org/wiki/Old_Master

    If I add more artists, I can use this to clean it up again.
'''
import sys
import random
'''
fh = open('artist_list.txt')
newFile = open('newArtList.txt', 'w')
for line in fh.readlines():
    #print(line)
    name  = list()
    name = line.split('(')
    print(name[0].strip(), '\n')
    name[0] = name[0].strip()
    name[0] = name[0] + '\n'
    newFile.write(name[0])
    #print(line)
'''
'''
f = open('newArtList.txt')
for artistNames in f.readlines():
    #print(artistNames)
    print('in')
    #print(random.choice(artistNames))
line = f.readlines()
#print('lines: ', line[2])
print('pick one')
#print(random.choice(line))
f.close()

with open('newArtList.txt') as f:
    for line in f:
        print(line)
    print(random.choice(line))
'''
with open('newArtList.txt', 'r') as f:
    artistNames = f.readlines()
    name = random.choice(artistNames)
    print(name)
    print(random.choice(artistNames))
