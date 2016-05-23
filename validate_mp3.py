import os
import fnmatch
import commands

#install=commands.getoutput('sudo apt-get install mp3val')


mp3_list = []

def scan(musicfile):
	  scan=commands.getoutput('mp3val '+ '"' + (musicfile) + '"' + ' -lout.log')
	  print(scan)
	  


for root, dirnames, filenames in os.walk('/home/roger/Music'):
    for filename in fnmatch.filter(filenames, '*.mp3'):
        mp3_list.append(os.path.join(root,filename ))


for musicfile in mp3_list:
	scan(musicfile)
	
	


