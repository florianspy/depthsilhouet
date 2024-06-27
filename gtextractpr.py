import glob, os
import shutil
import sys,re
from PIL import Image

# This script reads all the txt files from 'txtPath' from the pink folder, creates from these the ground truth files for the other 4
# and then writes these Bounding Boxes to the result file 'resultFile' in the different folders
# Also it converts the YOLO format from the txt file to 'left_x top_y width height' format.
#files with 4 letter extension will not work!
# labelPAth is the path where to find the gt
labelPath =os.path.expanduser('~/Documents/darknet-yolov4/Paper/KTP/DatasetsPink/')
evaluationname='evl20001'
evalnamecaps='EVL20001'
#where to find the files which contain the information of which we want to have ground truth for
evaltxtpath=os.path.expanduser('~/Documents/results'+evaluationname)
#where to write the gt files to
resultxtpath=os.path.expanduser('~/Documents/results'+evaluationname)

#pink must be first!
variants =['pink','rgb','depth','depthweit','depthnah']
variantpathnames=['Pink','RGB','Depth','DepthWeit','DepthNah']
#the order of these has to match with the order of variants do not change it t
subvariants=[['Tag','Abend','Nacht'],['Tag','Abend','Nacht'],['Tag'],['Tag'],['Tag']]
im_width = 570
im_height = 430
# multi_subfolder describes how many subfolder should stay.
# 0 = imageName.jpg
# 1 = firstSubfolder/imageName.jpg
# 2 = secondSubfolder/firstSubfolder/imageName.jpg
multi_subfolder = 1
objectClass0 = 'Person'
objectClass = '0'
k=5
s=1
string = ''
filename = []
lineArray = []
stringful = ''
for si in range(1,s+1):
    for f in range(1,k+1):
        #we need this file cause we want to find out for which files we need labels
        dataTXT=[]
        resultTXT=[[]]        
        #containing gt for the valids
        dataTXT.append(evaltxtpath+'/Pink/Split-'+str(si)+'-'+str(f)+'/fold'+str(si)+str(f)+'valid.txt')
        #as gt files are same for all no need for using all the below files contain the gtinfo for the test
        for subindex in range(0,len(subvariants[0])):
                dataTXT.append(evaltxtpath+'/Pink/Split-'+str(si)+'-'+str(f)+'/'+evaluationname+'_'+variants[0]+'_test'+subvariants[0][subindex]+'.txt')
        for index in range(0,len(variants)):
             if index > 0:
                resultTXT.append([])
             #gt file for fold
             resultTXT[index].append(resultxtpath+'/'+variantpathnames[index]+'/Split-'+str(si)+'-'+str(f)+'/gt_'+variants[index]+'_fold'+str(si)+str(f)+'valid.txt')
             #if you want to do this only for pink set write 1 instead of len(variants)       
             for subindex in range(0,len(subvariants[index])):
                resultTXT[index].append(resultxtpath+'/'+variantpathnames[index]+'/Split-'+str(si)+'-'+str(f)+'/gt_'+variants[index]+'_test'+str(si)+str(f)+subvariants[index][subindex]+'.txt')
        print (resultTXT)
        # m walks through all label files including those for all subvariants but depth etc do not have all subvariants so these cases need special handling 
        for m in range(0,len(dataTXT)): 
            with open(dataTXT[m]) as evalFile: 
                for numEval, lineEval in enumerate(evalFile, 1):                
                    linesplit = []
                    for t in lineEval.split('/'):
                        try:
                            linesplit.append(t)
                        except ValueError:
                            pass
                    if multi_subfolder == 0:
                        filename = linesplit[len(linesplit)-1]
                    if multi_subfolder == 1:
                        filename = linesplit[len(linesplit)-2] + '/' + linesplit[len(linesplit)-1]
                    if multi_subfolder == 2:
                        filename = linesplit[len(linesplit)-3] + '/' + linesplit[len(linesplit)-2] + '/' + linesplit[len(linesplit)-1]                
                    # Delete the '\n' from the end of filename
                    filename = filename.strip('\n')
                    # Delete the file extension like '.jpg' .png but it has to have 3 letters! files with 4 letter extension will not work
                    filename = filename[:len(filename)-4]
                    #Tag Abend Nacht have the same labels so we can just use the file for Tag for everything but depth pictures do not use them so we have to separate
                    nwfd=0      
                    if None != re.search(subvariants[0][1],filename):
                        nwfd=1
                        filename=re.sub(r'Abend','Tag',filename)
                    if None != re.search(subvariants[0][2],filename):
                        nwfd=1                  
                        filename=re.sub(r'Nacht','Tag',filename)
                    # Open the corresponding image to get the width and height of the image which
                    #im = Image.open(imagePath + filename + '.png')
                    #im_width, im_height, im.size
                    #stringful is used to store information for cases with subvariants
                    #string for those without
                    #this procedure is essential because the valid file from which we extract the gt also contains data about subvariants of Nacht,Abend
                    #which those without subversions only Tag will not need, this is why as soon we find one filename which 
                    #get the name of the image and store it into string/stringful 
                    if nwfd == 0:
                    	string += 'Enter Image Path: ' + lineEval.strip('\n') + ': Predicted in 17.000000 milli-seconds.' + '\n'
                    stringful += 'Enter Image Path: ' + lineEval.strip('\n') + ': Predicted in 17.000000 milli-seconds.' + '\n'
                    #get all the labels for this image
                    with open(labelPath + filename + '.txt') as labelFile:
                        for numLabel, lineLabel in enumerate(labelFile, 1):
                            lineArray = []
                            for t in lineLabel.split():
                                try:
                                    lineArray.append(t)
                                except ValueError:
                                    pass
                            left_x = int((float(lineArray[1]) * im_width) - (float(lineArray[3]) * im_width) / 2)
                            top_y = int((float(lineArray[2]) * im_height) - (float(lineArray[4]) * im_height) / 2)
                            width = int(float(lineArray[3]) * im_width)
                            height = int(float(lineArray[4]) * im_height)
                            stringful += 'Person: 100% (left_x: '+str(left_x)+' top_y: '+str(top_y)+' width: '+str(width)+' height: '+str(height)+')\n'
                            if nwfd == 0:
                                   string += 'Person: 100% (left_x: '+str(left_x)+' top_y: '+str(top_y)+' width: '+str(width)+' height: '+str(height)+')\n'
                    labelFile.close()
            #print(stringful)
            for index in range(0,len(variants)):
		#print m,index
		#because in this case we have depth,depthweit which only have one subvariant while pink and rgb have several and there text will be more
		if len(subvariants[index])>1:
		        with open(resultTXT[index][m], 'w') as resultFile:
				resultFile.write(stringful)		        
		else:
			#because this loop takes care of subvariants but depth etc has only one and therefore no results files need to be stored for other subversions
			#the +1 is essential here because m is walking through all variants
			if len(subvariants[index])+1> m:
				with open(resultTXT[index][m], 'w') as resultFile:
					resultFile.write(string)
	    string = ''
            stringful=''