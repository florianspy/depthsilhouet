mport glob, os
import random
import math
import sys,re
import shutil
#path to folder where the split folders should be created the first needs slash in front of it the second must not!
nameevl='/lab6'
nameevlfolder='Lab6'
#where to find cfg file
cfgpath=os.path.expanduser('~/Desktop/lab6_10000.cfg')
#path to where the output of this script should be stored
leng=os.path.expanduser('~/Desktop/'+nameevlfolder)
#path to where our split and other txt files relative to the yolo folder have to be put, e.g. the output of this script
stor='Master/'+nameevlfolder+'/'
directorylist =['Pink','RGB','Depth','DepthWeit','DepthNah']
txtlist =['pink','rgb','depth','depthweit','depthnah']
subname=[['Abend','Nacht','Tag','Schwarz'],['Abend','Nacht','Tag'],['Tag'],['Tag'],['Tag']]
#subversions other than Tag
daytime =['Abend', 'Nacht']
percentagetest=20
percentagetrain=70
s=20
#file containing all data of the dataset
alltxtpath =  os.path.expanduser('~/Downloads/ichbinmegageil/pink_alles.txt')

#in this script two files pink_allestrain and pink_allestest will be created and they contain the train and test dataimage paths
testTXTPATH = leng+'/pink_allestest.txt'
trainTXTPath = leng+'/pink_allestrainvalid.txt'
#variable for storing the directorynames of the labels
directory=[]
#variable for storing the directorynames for the storage folders
directory_data=[]
try:
    os.mkdir(leng) 
except OSError:
    print(leng)
for m in range(0,len(directorylist)):
    try:
        os.mkdir(leng+'/'+directorylist[m]) 
    except OSError:
        print(leng+directorylist[m])
for y in range(0,len(directorylist)):
    directory.append(leng+'/'+directorylist[y]+'/')
    directory_data.append(stor+directorylist[y]+'/')
index=0
testtxtstring=''
traintxtstrin=''
#stratification
with open(alltxtpath) as allFile:  
    #read in linewise
    for numLabel, lineLabel in enumerate(allFile, 1):
        if index%10 <= percentagetest/10-1:
            testtxtstring=testtxtstring+lineLabel
        else :
            traintxtstrin=traintxtstrin+lineLabel
        index=index+1
with open(testTXTPATH, 'w') as testFile:
    testFile.write(testtxtstring)
    testFile.close()
with open(trainTXTPath, 'w') as trainFile:
    trainFile.write(traintxtstrin)
    trainFile.close()   


foldtrain=[[[]]]
foldvalid=[[[]]]
for d in range(0, len(directory)):
    if d > 0:
        foldtrain.append([[]])
        foldvalid.append([[]])
    for si in range(1,s+1):
        if si > 1:
            foldtrain[d].append([])
            foldvalid[d].append([])       
        name = directory[d]+'Split-'+str(si)+'/fold'+str(si)+'train.txt'
        nameval = directory[d]+'Split-'+str(si)+'/fold'+str(si)+'valid.txt'
        foldtrain[d][si-1].append(name)
        foldvalid[d][si-1].append(nameval)        
        try:
            os.mkdir(directory[d]+'Split-'+str(si))                   
            #print("Directory " , directory[d]+'Split-'+str(s)+'-'+ str(x) ,  " Created ")   
        except OSError:
            print("Directory " , directory[d]+'Split-'+str(si),  " already exists")
        try:
            os.mkdir(directory[d]+'Split-'+str(si)+'/Backup')       
            #print("Directory " , directory[d]+'Split-'+str(s)+'-'+ str(x)+'/Backup' ,  " Created ")   
        except OSError:
            print("Directory " , directory[d]+'Split-'+str(si)+'/Backup' ,  " already exists")
        #create the names file
        with open(directory[d]+'Split-'+str(si)+'/names.names', 'w') as writi:
            writi.write('Person')
            writi.close()             
        strData = \
            'classes = 1\n\
train = '+directory_data[d]+'Split-'+str(si)+'/fold'+str(si)+'train.txt\n\
valid = '+directory_data[d]+'Split-'+str(si)+'/fold'+str(si)+'valid.txt\n\
names = '+directory_data[d]+'Split-'+str(si)+'/names.names\n\
backup = '+directory_data[d]+'Split-'+str(si)+'/Backup/'
            #write the data file
        with open(directory[d]+'Split-'+str(si)+nameevl +directorylist[d].lower()+ '_data.data', 'w') as dataFile:
                dataFile.write(strData)
       
print foldtrain
for i in range(len(directorylist)):
    for u in range(len(subname[i])):
        testtxtstring=''
        with open(testTXTPATH) as allFile: 
             for numLabel, lineLabel in enumerate(allFile, 1):
                subsit=re.sub(r'Tag',subname[i][u],lineLabel)
                subsit=re.sub(r'Pink',directorylist[i],subsit)                
                testtxtstring=testtxtstring+subsit
        if re.search("Depth",directorylist[i]):
                testtxtstring=re.sub(r'rgb.png','depth.png',testtxtstring)
        #create the files for testing in the split folders
        for si in range(1,s+1):           
                filename=directory[i]+'Split-'+str(si)+nameevl+txtlist[i]+'_test'+subname[i][u]+'.txt'
                with open(filename, 'w') as writi:
                    writi.write(testtxtstring)
                    writi.close()  
                #create cfg files
                try:
                    #print(cfgpath,directory[i]+'Split-'+str(si)+'-'+ str(index)+nameevl+txtlist[i]+'.cfg')
                    shutil.copy2(cfgpath,directory[i]+'Split-'+str(si)+nameevl+txtlist[i]+'.cfg')   
                except OSError:
                    print("cfg already exists")   
arrTrain = [[]]
num_lines_all = sum(1 for line in open(trainTXTPath))
print(num_lines_all, 'lines count all')
num_lines_fold = num_lines_all
print(num_lines_fold, 'lines count fold')
datapoints=0
previousname=''
firstelement = 0
# ---------------------------------------------------- shuffle train.txt in arrTrain
with open(trainTXTPath) as trainFile:    
    for numTrain, lineTrain in enumerate(trainFile, 1):
        linesplit = []
        for t in lineTrain.split('/'):
            try:
                linesplit.append(t)
            except ValueError:
                pass
        if linesplit[len(linesplit)-2] == previousname or firstelement == 0:
            firstelement = 1
            arrTrain[datapoints].append(lineTrain)
        else :
            datapoints=datapoints+1
            arrTrain.append([])
            arrTrain[datapoints].append(lineTrain)
        previousname=linesplit[len(linesplit)-2]

#fshuffel
for ind in range(0,datapoints+1):    
	random.shuffle(arrTrain[ind])   
#put all in one file

# print("picture of which the following number will be used for training")
# print(sumall*(percentagetrain*100.0/(100-percentagetest))/100.0)
print len(arrTrain),datapoints
for si in range(0,s):      
  
    #every pink, etc gets the same data
    for d in range(0, len(directory)): 
            with open(foldtrain[d][si][0], 'w') as foldtrainFile:
                with open(foldvalid[d][si][0], 'w') as foldvalFile:  
                    for ind in range(0,datapoints+1):  
                        for m in xrange(0,len(arrTrain[ind])):
                            if m<len(arrTrain[ind])*(percentagetrain*100.0/(100-percentagetest))/100.0:
                                new=re.sub(r'DatasetsPink','Datasets'+directorylist[d],str(arrTrain[ind][m]))
                                if re.search("Depth",new):
                                    new2=re.sub(r'rgb.png','depth.png',new)
                                    new=new2
                                foldtrainFile.write(new)
                            else:   
                                new=re.sub(r'DatasetsPink','Datasets'+directorylist[d],str(arrTrain[ind][m]))
                                if re.search("Depth",new):
                                    new2=re.sub(r'rgb.png','depth.png',new)
                                    new=new2
                                foldvalFile.write(new)
                                # if None == re.search("Depth",new):
                                #     for time in daytime:         
                                #         dummy = strFold[m].replace('Tag', time)
                                #         new=re.sub(r'DatasetsPink','Datasets'+directorylist[d],dummy)
                                #         foldvalFile.write(new)  
                                                 
print "done"