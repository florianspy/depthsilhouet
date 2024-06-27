#Script for conversion to pink be careful if your depth image has the 3 channels at this stage instead of just one the script will produce bad results. 
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import glob, os,re
import time
import cv2
import fnmatch
#for epfl
#img_path_saved = '~/Downloads/epfl/DatasetsPink/Corr1Tag/'
#for ktp
#the folders with the following names have same depth images
additonalwithsamedepth=["Abend","Nacht"]
folder =["ArcTag","RotTag","StillTag","TransTag"]
folderdepth =["ArcTag","RotTag","StillTag","TransTag"]
for i in range(len(folder)):
	img_path_saved = '~/Downloads/KTP/DatasetsPink/'+folder[i]+'/'
	img_path_saved =os.path.expanduser(img_path_saved)
	#for KTP_dataset_images
	img_path = '~/Downloads/KTP/DatasetsRGB/'+folder[i]+'/'
	depthimg_path = '~/Downloads/KTP/DatasetsDepth/'+folderdepth[i]+'/'
	#for mensa_seq
	#img_path = '~/Downloads/mensa_seq0_1.1/rgb/'
	#for freiburg adatpive
	#img_path = '/home/irobot/Downloads/Images/'
	img_path = os.path.expanduser(img_path)
	depthimg_path = os.path.expanduser(depthimg_path)
	counter = 0
	counterall = len(fnmatch.filter(os.listdir(img_path), '*.png'))
	removecontours=1
	#1=xy 0=x -1=not
	xyapproach=1
	#for file in glob.glob(img_path +'rgb*.png'):
	#for KTP_dataset_images
	#for file in glob.glob(img_path +'1339066241.733630743.jpg'):
	#for mensa_seq
	#for file in glob.glob(img_path +'seq0_0000_0.ppm'):
	# for freiburg adatpive
	for file in glob.glob(img_path +'*.png'):
		file_with_ext = os.path.basename(file)
		filename, file_extension = os.path.splitext(file_with_ext)
		#print filename,file_extension
		img_rgb = file_with_ext
		img_number = ''.join([n for n in filename if n.isdigit()])
		#for KTP_dataset_images
		img_depth = depthimg_path+filename+'.png'
		# for freiburg adatpive
		#img_depth = filename+'d.png'
		print(img_rgb)
                #stores the paths to where the data is to be written to
		add=[]
		for i in range(len(additonalwithsamedepth)):
                        #this removes Tag from the filepath name and replaces it with the subvariants
			add.append(img_path[:-4]+additonalwithsamedepth[i]+'/'+filename+'.png')
		print(img_depth)
		# Read image in bgr 
		bgr = cv2.imread(img_path + img_rgb)
		# Convert image from bgr to rgb
		rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
		addrgb=[]
		for i in range(len(additonalwithsamedepth)):
			bgr = cv2.imread(add[i])
			addrgb.append(cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB))
			# Read the Depth image
		depth = cv2.imread(img_depth,  cv2.IMREAD_UNCHANGED)
		# ------------------------------------------------------------------------------
		height, width = depth.shape
		#print(width, 'width') # 480
		#print(height, 'height') # 640
		print("---- removing shadows -----")
		# depth[height][width] # depth[479][639]
		if xyapproach == 1:
			for y in range(height): # 0 - 479
			    #print(x)
			    for x in range(width): # 0 - 639
				if (depth[y][x]==0):
				    z = 0 
				    zy = 0
				    while ((depth[y][x+z]==0) and (depth[y+zy][x]==0)):
					#print(y, x)                       
					if((x+z)<(width-1)):
					     z = z+1
					#exceeded                        
					if((y+zy)<(height-1)):
					     zy = zy + 1
					if (y+zy)>=(height-1) and ((x+z)>=(width-1)):
					    break
				    if(depth[y+zy][x]==0):
					zy=0
				    if(depth[y][x+z]==0):
					z=0   
				    if (x==0):
					depth[y][x] = depth[y+zy][x+z]
				    if ((x>0) and (x<(width-1))):
                                        %WE CAN use this formula because we set zy or z to zero if we found something
					depth[y][x] = max(depth[y][x-1], depth[y+zy][x+z])
				    if (x==(width-1)):
					depth[y][x] = depth[y][x-1]

		if xyapproach == 0:
			for y in range(height): # 0 - 479
			    #print(x)
			    for x in range(width): # 0 - 639
				#print(x)
				if (depth[y][x][0]==0):
				    z = 1
				    while (((x+z)<(width-1)) and (depth[y][x+z][0]==0)):
					#print(y, x)
					z = z+1
				    if (x==0):
					depth[y][x][0] = depth[y][x+z][0]
				    if ((x>0) and (x<(width-1))):
					depth[y][x][0] = max(depth[y][x-1][0], depth[y][x+z][0])
				    if (x==(width-1)):
					depth[y][x][0] = depth[y][x-1][0]
		#print("-----??-------")
		print("---- Normalize -----")
		cv2.normalize(depth, depth, 0, 255, cv2.NORM_MINMAX)
		#depth8 = depth/255
		print("-----Convert----")
		depth = cv2.convertScaleAbs(depth)
		#print(type(depth[0,0]))
		depth = cv2.medianBlur(depth, 5)
		depth_canny = cv2.Canny(depth, 30, 100, 3)
		_,contours, hierarchy= cv2.findContours(depth_canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
		if removecontours == 1:     
			for i in range(len(contours)):
				#x,y,w,h = cv2.boundingRect(contours[i])
				for l in range(len(contours[i])):
					#this will remove horizontal lines with no values smaller than 470 so regular contours 				#will still remain intact
					if contours[i][l][0][1]>470 and l < len(contours[i]):
						#contours[i][l][0][0]=500
						contours[i][l][0][1]=500					
				cv2.drawContours(rgb, contours,i, (255, 0, 255), 4)
				for m in range(len(additonalwithsamedepth)):
					cv2.drawContours(addrgb[m], contours,i, (255, 0, 255), 4)
		else:
			cv2.drawContours(rgb, contours,-1, (255, 0, 255), 4)	
                #this stores for Tag
		plt.imsave(img_path_saved + filename + '.png', rgb, format='png')
                #this for the other subvariants
		for i in range(len(additonalwithsamedepth)):
			add[i]=re.sub('DatasetsRGB','DatasetsPink',add[i])
			plt.imsave(add[i], addrgb[i], format='png')
		counter += 1
		print(counter, counterall)