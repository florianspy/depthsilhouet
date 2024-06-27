import glob, os
import random
import math
import sys,re
import shutil
evalu='evl1'
capevalu='EVL1'
source='~/Documents/darknet-yolov4/Paper/KTP/'+capevalu+'/'
source =os.path.expanduser(source)
#Pink should be the first
directorylist =['Pink','RGB','Depth','DepthWeit','DepthNah']
txtlist =['pink','rgb','depth','depthweit','depthnah']
subname=[['Abend','Nacht','Tag'],['Abend','Nacht','Tag'],['Tag'],['Tag'],['Tag']]
# chart has to be second name! and fold the first
files=['results__fold','chart','results_'+evalu+'_']
dest='~/Documents/results'+evalu+'/'
dest =os.path.expanduser(dest)
k=5
s=1

filenames=[[[]]]
try:
	os.mkdir(dest)  
except OSError:
	print("Directory already exists")
for i in range(0, len(directorylist)):
	try:
		os.mkdir(dest+'/'+directorylist[i])  
	except OSError:
		print("Directory already exists")
	for si in range(1,s+1):
		for index in range(1, k+1):
			try:
				os.mkdir(dest+'/'+directorylist[i]+'/Split-'+str(si)+'-'+str(index))  
			except OSError:
				print("Directory already exists")
count=0
#this is necessary to put all folders of one Datasetsplit in the directory-variable behind each other
for y in range(0,len(directorylist)):
	for si in range(1,s+1):
		for index in range(1, k+1):	
		    filenames[y].append([])	 
		    arr = os.listdir(source+directorylist[y]+'/Split-'+str(si)+'-'+str(index))
		    for ls in range(0,len(arr)):
				if arr[ls] != 'Backup':	
					filenames[y][index-1].append('Split-'+str(si)+'-'+str(index)+'/'+arr[ls])
	filenames.append([[]])
for d in range(0, len(directorylist)):
	for si in range(1,s+1):
		for index in range(1, k+1):	
			for fil in range(0,len(filenames[d][index-1])):
				shutil.copy2(source+directorylist[d]+'/'+filenames[d][index-1][fil],dest+directorylist[d]+'/'+filenames[d][index-1][fil])