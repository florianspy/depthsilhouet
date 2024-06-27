#Script for bringing silhouttes to depth 
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import glob, os
import time
import cv2
import fnmatch

folder = ["ArcTag","RotTag","StillTag","TransTag"]
rgb='~/Downloads/KTP/DatasetsRGB/'
depth='~/Downloads/KTP/DatasetsDepth/'
img_path_saved = '~/Downloads/KTP/'

img_path_saved =os.path.expanduser(img_path_saved)
for fl in range(len(folder)):
	img_path = rgb+folder[fl]+'/'
	img_path = os.path.expanduser(img_path)
	depthimg_path =depth+folder[fl]+'/'
	depthimg_path = os.path.expanduser(depthimg_path)	
	counter = 0
	counterall = len(fnmatch.filter(os.listdir(img_path), '*.jpg'))
	xyapproach=1
	removecontours=1	
	for file in glob.glob(img_path +'*.png'):
		file_with_ext = os.path.basename(file)
		filename, file_extension = os.path.splitext(file_with_ext)
		# Check if filename begins with 'rgb'
		img_rgb = file_with_ext
		img_number = ''.join([n for n in filename if n.isdigit()])
		#for KTP_dataset_images
		img_depth = depthimg_path+filename+'.png'
		print(img_rgb)
		print(img_depth)
		# Read the Depth image
		depth = cv2.imread(img_depth,  cv2.IMREAD_UNCHANGED)
		depthorg=depth.copy()
		#depthorg = cv2.imread(img_path + img_depth,  cv2.IMREAD_UNCHANGED)
		#depth = cv2.imread(img_depth, cv2.IMREAD_GRAYSCALE)
		#print(depth)
		thresh = depthorg.max()
		print(thresh)
		# ------------------------------------------------------------------------------
		depthorgui8=depth.copy()
		height, width = depth.shape
		#print(width, 'width') # 480
		#print(height, 'height') # 640

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
					depth[y][x] = max(depth[y][x-1], depth[y+zy][x+z])
				    if (x==(width-1)):
					depth[y][x]= depth[y][x-1]
		depthfilterui8=depth.copy()
		depthfilterorgui8=depth.copy()
		cv2.normalize(depth, depth, 0, 255, cv2.NORM_MINMAX)
		depth = cv2.convertScaleAbs(depth)
		#print(type(depth[0,0]))
		depth = cv2.medianBlur(depth, 5)
		depth_canny = cv2.Canny(depth, 30, 100, 3)
		_,contours, hierarchy = cv2.findContours(depth_canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
		depthcloseui8=depthorg.copy()   
		depthorgui8=depthorg.copy()
		depthfarui8=depthorg.copy()

		if removecontours == 1:     
			for i in range(len(contours)):
				#x,y,w,h = cv2.boundingRect(contours[i])
				for l in range(len(contours[i])):
					#this will remove horizontal lines with no values smaller than 470 so regular contours 					#will still remain intact
					if contours[i][l][0][1]>470 and l < len(contours[i]):
						#contours[i][l][0][0]=500
						contours[i][l][0][1]=500					

				cv2.drawContours(depthcloseui8, contours,i, 0, 4) # Nah
				cv2.drawContours(depthfarui8, contours,i, (thresh*2), 4)# Weit
		
		cv2.normalize(depthorgui8, depthorgui8, 0, 255, cv2.NORM_MINMAX)  
		cv2.normalize(depthcloseui8, depthcloseui8, 0, 255, cv2.NORM_MINMAX) 
		cv2.normalize(depthfarui8, depthfarui8, 0, 255, cv2.NORM_MINMAX)
		depthorgui8 = cv2.convertScaleAbs(depthorgui8)
		depthcloseui8 = cv2.convertScaleAbs(depthcloseui8)
		depthfarui8 = cv2.convertScaleAbs(depthfarui8)
		depthorgui8c3=cv2.merge((depthorgui8,depthorgui8,depthorgui8))
		depthcloseui8c3 =cv2.merge((depthcloseui8,depthcloseui8,depthcloseui8))		
		depthfarui8c3=cv2.merge((depthfarui8,depthfarui8,depthfarui8))
		names=['DatasetsDepthC3/','DatasetsDepthNah/','DatasetsDepthWeit/']
		cv2.imwrite(img_path_saved + names[0] + folder[fl] + '/' + filename+'.png', depthorgui8c3) # Depth
		cv2.imwrite(img_path_saved + names[1] + folder[fl] + '/' + filename+'.png', depthcloseui8c3) # DepthNah
		cv2.imwrite(img_path_saved + names[2] + folder[fl] + '/' + filename+'.png', depthfarui8c3) # DepthWeit
		#print(len(depthorgui8c3.shape), len(depthcloseui8c3.shape), len(depthfarui8c3.shape))
		print('Depth', depthorgui8c3[230,230,0],depthorgui8c3[230,230,1],depthorgui8c3[230,230,2])
		print('DepthNah', depthcloseui8c3[230,230,0],depthcloseui8c3[230,230,1],depthcloseui8c3[230,230,2])
		print('DepthWeit', depthfarui8c3[230,230,0],depthfarui8c3[230,230,1],depthfarui8c3[230,230,2])
		counter += 1
		print(counter, counterall)