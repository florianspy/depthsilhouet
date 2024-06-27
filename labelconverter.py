import numpy as np
import glob, os
tag = ['Arc_gt2D','Rotation_gt2D','Still_gt2D','Translation_gt2D']
rgb='DatasetsRGB/'
pink='DatasetsPink/'
depth='DatasetsDepth/'
depthnah='DatasetsDepthNah/'
depthfar='DatasetsDepthWeit/'
foldernames=['Arc','Rot','Still','Trans']
subfoldernames=['Abend/','Tag/','Nacht/']
corfolder=[[]]
for u in range(len(foldernames)):
	for o in range(len(subfoldernames)):
		corfolder[u].append(rgb+foldernames[u]+subfoldernames[o])
		corfolder[u].append(pink+foldernames[u]+subfoldernames[o])
	corfolder[u].append(depth+foldernames[u]+'Tag/')
	corfolder[u].append(depthnah+foldernames[u]+'Tag/')
	corfolder[u].append(depthfar+foldernames[u]+'Tag/')
	corfolder.append([])
mainfolder='~/Downloads/KTP/'
mainfolder = os.path.expanduser(mainfolder)
for i in range(len(tag)):
	labelFilePath = '~/Downloads/KTP_dataset_images/ground_truth/' + tag[i] + '.txt'
	labelFilePath = os.path.expanduser(labelFilePath)
	with open(labelFilePath) as labelFile:
	    for numLabel, lineLabel in enumerate(labelFile, 1):
		#print(lineLabel)
		line = lineLabel
		nameList = []
		labelList = []
		for t in lineLabel.split(':'):
		    try:
		        nameList.append(t)
		    except ValueError:
		        break
		name = nameList[0].replace(':', '')
		for t in nameList[1].split(','):
		    try:
		        labelList.append(t)
		    except ValueError:
		        break
		#print(labelList)
		# Delete \r\n from last index
		del labelList[-1]
		#print(labelList)
		# labelList = [' 1 493 136 101 224', ' 4 457 122 124 256']
		# labelList = []
		k=0
		labelLine = []
		for labels in labelList:
		    labelLine.append([0, 0, 0, 0])
		    m=0
		    for t in labels.split(' '):
		        if (m > 1):                
		            try:
		                labelLine[k][m-2]=t
		            except ValueError:
		                break
		        m=m+1
		    k=k+1
		string = ''		
		for labels in labelLine:
		    # [bbox...] = [x y width height] 
		    # x, y: image coordinates of the top-left corner of the person bounding box
		    # width, height: width and height of the person bounding box
		    # crop = image[37:430+37, 33:570+33]
		    bbox = []
		    negx=0
		    negy=0
		    img_w = 570
		    img_h = 430
		    for x in xrange(len(labels)):
		        if(x==0): # x
		            if(int(labels[x])-33<0):
		                bbox.append(0)
		                negx=int(labels[x])-33
		            else:                      
		                bbox.append(int(labels[x])-33)
		        if(x==1): # y
		            if(int(labels[x])-37<0):
		                negy=int(labels[x])-37
		                bbox.append(0)                      
		            else:                      
		                bbox.append(int(labels[x])-37)
		        if(x==2):
		            if(int(labels[x])+negx<0):
		                bbox.append(0)
		            else:
		                limitboxw=int(labels[x])+bbox[0]
		                toomuch=0
		                if(limitboxw>img_w):
		                   toomuch=limitboxw-img_w
		                bbox.append(int(labels[x])+negx-toomuch)
		        if(x==3):
		            if(int(labels[x])+negy<0):
		                bbox.append(0)
		            else:  
		                limitboxh=int(labels[x])+bbox[1]
		                toomuch=0
		                if(limitboxh>img_h):
		                   toomuch=limitboxh-img_h                      
		                bbox.append(int(labels[x])+negy-toomuch)
		    # for x in xrange(len(labels)):
		    #     if(x==0):
		    #         bbox.append(int(labels[x])-33)
		    #     if(x==1):
		    #         bbox.append(int(labels[x])-37)
		    #     if(x==2):
		    #         bbox.append(int(labels[x]))
		    #     if(x==3):
		    #         bbox.append(int(labels[x]))
		    # Image Size
		    img_w = 570
		    img_h = 430
		    # Convert to YOLO
		    # <x> <y> <width> <height> - float values relative to width and height of image, it can be equal from (0.0 to 1.0]
		    # or example: # <x> = <absolute_x> / <image_width> or <height> = <absolute_height> / <image_height>
		    # atention: <x> <y> - are center of rectangle (are not top-left corner)
		    x_yolo = 1.0*(1.0*bbox[0] + bbox[2]/2.0) / (1.0*img_w)
		    y_yolo = 1.0*(1.0*bbox[1] + bbox[3]/2.0) / (1.0*img_h)
		    w_yolo = (1.0*bbox[2]) / (1.0*img_w)
		    h_yolo = (1.0*bbox[3]) / (1.0*img_h)
		    string += ('0 ' + str(x_yolo) + ' ' + str(y_yolo) + ' ' + str(w_yolo) + ' ' + str(h_yolo) + '\n')
		for m in range(len(corfolder[i])):		
			savepath = mainfolder+corfolder[i][m]
			txt = open(savepath + name + ".txt","w+")
			txt.write(string)