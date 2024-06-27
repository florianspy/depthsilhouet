import glob, os
import random
import math
import sys,re
import shutil

evalu='lab6'
#name of the subfolder 
capevalu='Lab6'
#folder containing the resutls
source='~/Documents/darknet-yolov4/Master/'+capevalu+'/'
source =os.path.expanduser(source)
#Pink should be the first
directorylist =['Pink','RGB','Depth','DepthWeit','DepthNah']
# chart has to be second name! and fold the first
files=['results__fold','chart','results_'+evalu+'_']
dest='~/Documents/results'+evalu+'/'
dest =os.path.expanduser(dest)
s=20

filenames=[[]]
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
			try:
				os.mkdir(dest+'/'+directorylist[i]+'/Split-'+str(si))  
			except OSError:
				print("Directory already exists")
count=0
#this is necessary to put all folders of one Datasetsplit in the directory-variable behind each other
for y in range(0,len(directorylist)):
	if y >0:
		filenames.append([])
	for si in range(1,s+1):
		    arr = os.listdir(source+directorylist[y]+'/Split-'+str(si))
		    for ls in range(0,len(arr)):
				if arr[ls] != 'Backup':	
					filenames[y].append('Split-'+str(si)+'/'+arr[ls])

for d in range(0, len(directorylist)):
	for si in range(1,s+1):
			for fil in range(0,len(filenames[d])):
				shutil.copy2(source+directorylist[d]+'/'+filenames[d][fil],dest+directorylist[d]+'/'+filenames[d][fil])