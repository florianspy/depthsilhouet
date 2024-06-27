import glob
import os
import matplotlib.pyplot as plt
import sys # for sys.exit()
import numpy as np
import matplotlib
import matplotlib.gridspec as gridspec
import argparse
import csv

# This reads Script reads all Ground Truth Bounding Boxes from 'gtPathFile' and all Prediction Bounding Boxes from
# 'predPathFile'. Then it compares a pred-BB with all gt-BB and takes the best match.

# multi_subfolder describes how many subfolder should stay. 
# 0 = imageName.jpg
# 1 = firstSubfolder/imageName.jpg
# 2 = secondSubfolder/firstSubfolder/imageName.jpg
multi_subfolder = 1
# -----------------------------------------------------------
# ---- Function to get Intersection over Union

# Source: https://www.pyimagesearch.com/2016/11/07/intersection-over-union-iou-for-object-detection/
def bb_intersection_over_union(boxA, boxB):
    # determine the (x, y)-coordinates of the intersection rectangle
    xA = max(boxA[0], boxB[0])
    yA = max(boxA[1], boxB[1])
    xB = min(boxA[2], boxB[2])
    yB = min(boxA[3], boxB[3])
 
    # compute the area of intersection rectangle
    interArea = max(0, xB - xA ) * max(0, yB - yA )

    # compute the area of both the prediction and ground-truth
    # rectangles
    boxAArea = (boxA[2] - boxA[0] ) * (boxA[3] - boxA[1] )
    boxBArea = (boxB[2] - boxB[0] ) * (boxB[3] - boxB[1] )
    
    # compute the intersection over union by taking the intersection
    # area and dividing it by the sum of prediction + ground-truth
    # areas - the interesection area
    iou = interArea / float(boxAArea + boxBArea - interArea)
 
    # return the intersection over union value
    return iou

# Enter Image Path: results/TestImages/0004.jpg: Predicted in 17.116000 milli-seconds.
# Person: 98%   (left_x:   -2   top_y:  100   width:  353   height:  351)
def getBoundingBoxesFromTXT(path, storage):
    with open(path) as myFile:
        
        for num, line in enumerate(myFile, 1):

            # If line is 'Enter ... image ... /../imageName.jpg then save the filename

            if line[0] == 'E':
                
                linesplit = []
                for t in line.split('/'):
                    try:
                        linesplit.append(t)
                    except ValueError:
                        pass

                # Check for MultiSubfolders
                if multi_subfolder == 0:
                    filename = linesplit[len(linesplit)-1].rsplit('.png', 1)[0]
                if multi_subfolder == 1:
                    filename = linesplit[len(linesplit)-2] + '/' + linesplit[len(linesplit)-1].rsplit('.png', 1)[0]
                if multi_subfolder == 2:
                    filename = linesplit[len(linesplit)-3] + '/' + linesplit[len(linesplit)-2] + '/' + linesplit[len(linesplit)-1].rsplit('.png', 1)[0]

            
            # If line is 'Person' then store the Bounding Boxes int the Element with the 
            # corresponding Name.  Format Person: 82%   (left_x:   250   top_y:  77   width:  211   height:  264)
            # [['TestImages/0002', ['82', '250', '77', '211', '264'], [BB2], [BB2], ...], ['TestImages/0000', [BB]], ... ]
            if line[0] == 'P':
                linesplit = []
                for t in line.split():
                    try:
                        linesplit.append(t)
                    except ValueError:
                        pass
                if 'depth' in filename:
                    filename = filename.replace('depth', 'rgb')
                # Person: 98%   (left_x:   -2   top_y:  100   width:  353   height:  351)
                storage.append([filename,[linesplit[1][:(len(linesplit[1])-1)], linesplit[3], linesplit[5], linesplit[7], linesplit[9][:(len(linesplit[9])-1)]]])                
    myFile.close() 

def getParameterValue(line):
    line2 = line.split('=')
    return line2[len(line2)-1].rstrip('\n')


class mAP(object):
    def __init__(self, predPathFile, gtPathFile): 
        self.predPathFile = predPathFile; self.gtPathFile = gtPathFile
        self.title, ext = os.path.splitext(os.path.basename(self.predPathFile)); self.type = ''; self.version = ''; self.mode = ''
        self.total_num_pred = 0; self.total_num_gt = 0
        self.pred = []; self.gt = []; self.conf = []
        self.TP = [0 for x in range(10)]; self.FP = [0 for x in range(10)]; self.FN = [0 for x in range(10)] 
        self.recall = []; self.precision = []; self.precisionOriginal = [[]]*10
        self.area = [[0 for col in range(101)] for row in range(10)]; self.area_mean = [0 for col in range(10)]; self.area_mean_complete = 0
        self.batch = 0; self.subdivisions = 0; self.width = 0; self.height = 0; self.learning_rate = 0; self.max_batches = 0
        # Check if files exists, if not then exit the script
        if not os.path.exists(predPathFile):
            print(predPathFile + ' doesn\'t exists and the script will be terminated.')
            sys.exit(0)
        if not os.path.exists(gtPathFile):
            print(gtPathFile + ' doesn\'t exists and the script will be terminated.')
            sys.exit(0)
        # Read the Path files and store it in ['imageName', [Percentage, left_x, top_y, width, height]], ['imageName', [...]], ...
        # [['rgb000681', ['100', '345', '201', '62', '187']], ['rgb000681', ['100', '192', '223', '85', '174']], ... ]
        getBoundingBoxesFromTXT(self.predPathFile, self.pred)
        getBoundingBoxesFromTXT(self.gtPathFile, self.gt)
        self.total_num_pred = len(self.pred)
        self.total_num_gt = len(self.gt)
        self.getParameters()
        self.sortingPred()
        self.determine()
        self.interpolate()
        self.calculateArea()

    def getParameters(self):
    # ---- Get all Learning parameters 
        with open(self.predPathFile) as myFile:
            for num, line in enumerate(myFile, 1):
                if 'batch=' in line:
                    self.batch= getParameterValue(line)
                elif 'subdivisions=' in line:
                    self.subdivisions= getParameterValue(line)
                elif 'width=' in line:
                    self.width= getParameterValue(line)
                elif 'height=' in line:
                    self.height= getParameterValue(line)
                elif 'learning_rate=' in line:
                    self.learning_rate= getParameterValue(line)
                elif 'max_batches' in line:
                    self.max_batches= getParameterValue(line)        
        if 'pink' in self.title:
            self.type = 'Pink'
        if 'rgb' in self.title:
            self.type = 'RGB'
        if 'depth' in self.title:
            self.type = 'Depth'
        self.version = self.title.replace('zgzgvz', '')
        self.version = self.version.replace('Tag', '')
        self.version = self.version.replace('Abend', '')
        self.version = self.version.replace('Nacht', '')
        self.version = self.version.replace('Schwarz', '')
        if 'Tag' in self.title:
            self.mode = 'Tag'
        if 'Abend' in self.title:
            self.mode = 'Abend'
        if 'Nacht' in self.title:
            self.mode = 'Nacht'
        if 'Schwarz' in self.title:
            self.mode = 'Schwarz'    
        if 'valid' in self.title:
            self.mode = 'valid'  
        if not self.batch:  
            print("Batch Parameter not found.")                                 
        if not self.subdivisions:   
            print("Subdivisions Parameter not found.")  
        if not self.width:  
            print("Width Parameter not found.") 
        if not self.height: 
            print("Height Parameter not found.")
        if not self.learning_rate:  
            print("Learning_Rate Parameter not found.")
        if not self.max_batches:    
            print("Max_Batches Parameter not found.")   
    def sortingPred(self):
    # ---- Sort the Pred Bounding Boxes to the lowest confidence score -> reverse it -> sort the pred BBs with the
    # ---- same Confidence Score in alphabetical order 
        for i in range(0, self.total_num_pred):
            for j in range(0, self.total_num_pred-i-1):

                if (int(self.pred[j][1][0]) > int(self.pred[j + 1][1][0])):  
                    pred_temp = self.pred[j]  
                    self.pred[j]= self.pred[j + 1]  
                    self.pred[j + 1]= pred_temp  

        # Reverse the list 
        self.pred.reverse()
        for p in self.pred:
            self.conf.append(p[1][0])

    def determine(self):
    # ---- Determine TP, FP and FN 
        for x in range(10):
            gtDummy = list(self.gt)
            #gt = []
            #getBoundingBoxesFromTXT(gtPathFile, gt)
            self.recall.append([])
            self.precision.append([])
            # Cycle through all Prediction Bounding Boxes
            for predIndex, predBB in enumerate(self.pred):
                detected = 0; z = -1; iou_result = 0
                #print(predIndex, predBB)
                # Convert   left_x - top_y - width - height
                # To        Xmin - Ymin - Xmax - Ymax
                boxPred = []
                boxPred.append(int(predBB[1][1])) # Xmin
                boxPred.append(int(predBB[1][2])) # Ymin
                boxPred.append(int(predBB[1][1]) + int(predBB[1][3])) # Xmax
                boxPred.append(int(predBB[1][2]) + int(predBB[1][4])) # Ymax
                # Cycle through all Ground Truth Bounding Boxes
                for gtIndex, gtBB in enumerate(gtDummy):                    
                    # Check if predBB and gtBB are from the same image
                    if predBB[0] == gtBB[0]:
                        # Convert   left_x - top_y - width - height
                        # To        Xmin - Ymin - Xmax - Ymax
                        boxGT = []
                        boxGT.append(int(gtBB[1][1])) # Xmin
                        boxGT.append(int(gtBB[1][2])) # Ymin
                        boxGT.append(int(gtBB[1][1]) + int(gtBB[1][3])) # Xmax
                        boxGT.append(int(gtBB[1][2]) + int(gtBB[1][4])) # Ymax                        
                        # Calculate Intersection over Union
                        iou = bb_intersection_over_union(boxGT, boxPred)
                        # If iou is over 0.5 and iou ist the best iou for this GT Box       
                        if (iou > iou_result) and (iou > (0.5 + (0.05*x))):
                            iou_result = iou
                            detected = 1
                            z = gtIndex                        
                        # Try it with the next Ground Truth Box
                # If GT Box was predicted correctly
                if detected == 1:
                    self.TP[x] = self.TP[x] + 1
                    #iouall += (iou / len(gtLine))
                    gtDummy.remove(gtDummy[z])
                else :
                    self.FP[x] = self.FP[x] + 1
                self.recall[x].append(self.TP[x]*1.0 / self.total_num_gt*1.0)
                self.precision[x].append(self.TP[x]*1.0 / (self.TP[x]+self.FP[x])*1.0)
            self.FN[x] = len(gtDummy)

    def interpolate(self):
    # ---- Interpolate the precision
        for x in range(10):
            self.precisionOriginal[x] = list(self.precision[x])

        for x in range(10):
            # Interpolate the precision
            for recIndex, rec in enumerate(self.recall[x]):     
                maxPrecision = 0; detected = False  
                for y in range (recIndex, len(self.recall[x])):
                    if (self.precision[x][recIndex] < self.precision[x][y]) and (self.precision[x][y] > maxPrecision):
                        maxPrecision = self.precision[x][y]
                        detected = True
                        
                if detected == True:
                    self.precision[x][recIndex] = maxPrecision
                detected = False

    def calculateArea(self):
        # Cycle through the ten IoU values
        for x in range(10): 
            # Cycle through the 101 mAP COCO recall values 
            for y in range(0,101):
                index=-1
                # Check which recall value has the lowest distance to the specific
                # mAP COCO recall value 
                if ((y*0.01) < self.recall[x][0]):
                    index=0
                else:
                    for recIndex in range(0,len(self.recall[x])):   
                        if recIndex+1 < len(self.recall[x]):
                            if ((y*0.01) == self.recall[x][recIndex]):
                                index=recIndex                            
                                break  
                            if ((y*0.01) > self.recall[x][recIndex]) and ((y*0.01) <= self.recall[x][recIndex+1]):
                                index=recIndex+1                            
                                break    
                if index == -1:
                    self.area[x][y] = 0
                else:
                    self.area[x][y] = self.precision[x][index]
            # Compute the mean of the mAP COCO precision values
            self.area_mean[x] = np.mean(self.area[x])
        # Create a list with 100 values from 0-1
        array101 = []
        for x in range(0,101):
           array101.append(x*1.0/100)
        self.area_mean_complete = np.mean(self.area_mean)
        #print(self.area_mean_complete)
        #print(area_mean)
        #print(area_mean_complete)

def main():
# Pink
# RGB
# Depth
# DepthNah
# depthWeit
    evalname='evl1'
    nameevlfolder='EVL1'
    stor=os.path.expanduser('~/Documents/darknet-yolov4/Paper/KTP/'+nameevlfolder+'/')
    directorylist =['Pink','DepthNah','RGB','Depth','DepthWeit']
    txtlist =['pink','depthnah','rgb','depth','depthweit']
    subname=[['Abend','Nacht','Tag'],['Tag'],['Abend','Nacht','Tag'],['Tag'],['Tag']]
    gtPathFile=[]
    folder_dir=[]
    #change only this line if you want another stuff
    s=1
    k=2
    selected=1
    gtPathFile.append(stor+directorylist[selected]+'/Split-'+str(s)+'-'+str(k)+'/gt_'+txtlist[selected]+'_fold'+str(s)+str(k)+'valid.txt')
    folder_dir.append(stor+directorylist[selected]+'/Split-'+str(s)+'-'+str(k)+'/results_'+evalname+'_'+txtlist[selected]+'_fold'+str(s)+str(k)+'valid_best_Split_'+str(s)+'_'+str(k)+'*.txt')
    selected=0
    gtPathFile.append(stor+directorylist[selected]+'/Split-'+str(s)+'-'+str(k)+'/gt_'+txtlist[selected]+'_fold'+str(s)+str(k)+'valid.txt')
    folder_dir.append(stor+directorylist[selected]+'/Split-'+str(s)+'-'+str(k)+'/results_'+evalname+'_'+txtlist[selected]+'_fold'+str(s)+str(k)+'valid_best_Split_'+str(s)+'_'+str(k)+'*.txt')
    
    print(gtPathFile)
    print(folder_dir)
    a = 'w+'
    filenamecsv='testsolo.csv'
    if os.path.isfile(filenamecsv):
        os.remove(filenamecsv)
        print(filenamecsv, "File was deleted and a new one will be created.")
    mAP_list = []
    version_list = []
    for x in range(len(gtPathFile)):
        
        # Append mAP objects to 'mAP_list' and count the objects --ResultsLabMedian
        for files in glob.glob(folder_dir[x]):
            print(files + ' will be read in.')
            mAP_list.append(mAP(files, gtPathFile[x]))
    for mAP_Object in mAP_list:
        print(mAP_Object)
        print('total_num_pred', mAP_Object.total_num_pred)
        print('total_num_gt', mAP_Object.total_num_gt)
        print('mAP', mAP_Object.area_mean_complete)
        print('TP', mAP_Object.TP)
        print('FP', mAP_Object.FP)
        print('FN', mAP_Object.FN)
        print("-----")
    with open(filenamecsv, 'w', newline='') as csvfile:
        fieldnames = ['Name', 'Type', 'mAP', 'Iteration', 'LearningRate', \
        '.50', '.55', '.60', '.65', '.70', '.75', '.80', '.85', '.90', '.95']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')
        writer.writeheader()
        for mAP_Object in mAP_list:
            writer.writerow({'Name': mAP_Object.title, 
                'Type': mAP_Object.type, \
                'mAP': "{:.2f}".format(round(mAP_Object.area_mean_complete,5)*100), \
                'Iteration': mAP_Object.max_batches, \
                'LearningRate': mAP_Object.learning_rate, \
                '.50': "{:.2f}".format(round(mAP_Object.area_mean[0],4)*100), \
                '.55': "{:.2f}".format(round(mAP_Object.area_mean[1],4)*100), \
                '.60': "{:.2f}".format(round(mAP_Object.area_mean[2],4)*100), \
                '.65': "{:.2f}".format(round(mAP_Object.area_mean[3],4)*100), \
                '.70': "{:.2f}".format(round(mAP_Object.area_mean[4],4)*100), \
                '.75': "{:.2f}".format(round(mAP_Object.area_mean[5],4)*100), \
                '.80': "{:.2f}".format(round(mAP_Object.area_mean[6],4)*100), \
                '.85': "{:.2f}".format(round(mAP_Object.area_mean[7],4)*100), \
                '.90': "{:.2f}".format(round(mAP_Object.area_mean[8],4)*100), \
                '.95': "{:.2f}".format(round(mAP_Object.area_mean[9],4)*100) \
                })
if __name__ == "__main__":
    main()