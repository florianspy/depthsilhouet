#Afterwards use the following python script to crop areas where no depth information was available because sensor for depth and rgb do not overlap 
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import glob, os
import time
import cv2
import fnmatch
rgb='~/Downloads/KTP/DatasetsRGB/'
rgb = os.path.expanduser(rgb)
depth='~/Downloads/KTP/DatasetsDepth/'
depth = os.path.expanduser(depth)
folder =[depth+"ArcTag",depth+"RotTag",depth+"StillTag",depth+"TransTag",rgb+"ArcAbend",rgb+"ArcNacht",rgb+"ArcTag",rgb+"RotAbend",rgb+"RotNacht",rgb+"RotTag",rgb+"StillAbend",rgb+"StillNacht",rgb+"StillTag",rgb+"TransAbend",rgb+"TransNacht",rgb+"TransTag"]
for i in range(len(folder)):
	#https://stackoverflow.com/questions/15589517/how-to-crop-an-image-in-opencv-using-python 
	print "starting with "+folder[i]
	for file in glob.glob(folder[i] +'/*.pgm'):
		file_with_ext = os.path.basename(file)
		filename, file_extension = os.path.splitext(file_with_ext)		
		image = cv2.imread(file, cv2.IMREAD_UNCHANGED)
		crop = image[37:430+37, 33:570+33]
		cv2.imwrite(file[:-len(file_extension)]+'.png',crop)
	for file in glob.glob(folder[i] +'/*.jpg'):
		file_with_ext = os.path.basename(file)
		filename, file_extension = os.path.splitext(file_with_ext)		
		image = cv2.imread(file)
		crop = image[37:430+37, 33:570+33]
		cv2.imwrite(file[:-len(file_extension)]+'.png',crop)
	print "done with "+folder[i]