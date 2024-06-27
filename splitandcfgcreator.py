import glob, os
import random
import math
import sys,re
import shutil
#path to folder where the split folders should be created the first needs slash in front of it and a trailing _ the second must not!
nameevl='/evl20002_'
nameevlfolder='EVL20002'
#where to find cfg file
cfgpath='$HOME/Desktop/EvalKTPScript/yolo.cfg'
#path to where the output of this script should be stored
leng='$HOME/Desktop/'+nameevlfolder
#path to where our split and other txt files relative to the yolo folder have to be put, e.g. the output of this script, only change stuff before KTP
stor='Paper/KTP/'+nameevlfolder+'/'
#file containing all data of the dataset
alltxtpath =  '/home/irobot/Desktop/EvalKTPScript/pink_alles.txt'
#more parameters for your dataset
directorylist =['Pink','RGB','Depth','DepthWeit','DepthNah']
txtlist =['pink','rgb','depth','depthweit','depthnah']
subname=[['Abend','Nacht','Tag'],['Abend','Nacht','Tag'],['Tag'],['Tag'],['Tag']]
#subversions other than Tag
daytime =['Abend', 'Nacht']
# how many splits and how many shuffel
k=5
s=5

#in this script two files pink_allestrain and pink_allestest will be created and they contain the train and test dataimage paths
testTXTPATH = '/home/irobot/Desktop/EvalKTPScript/pink_allestest.txt'
trainTXTPath = '/home/irobot/Desktop/EvalKTPScript/pink_allestrain.txt'
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
with open(alltxtpath) as allFile:  
    #read in linewise
    for numLabel, lineLabel in enumerate(allFile, 1):
        if index%10 <= 1:
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
        for x in range(1, k+1):
            name = directory[d]+'Split-'+str(si)+'-'+ str(x) + '/fold'+str(si)+str(x)+'train.txt'
            nameval = directory[d]+'Split-'+str(si)+'-'+ str(x) + '/fold'+str(si)+str(x)+'valid.txt'
            foldtrain[d][si-1].append(name)
            foldvalid[d][si-1].append(nameval)
        for x in xrange(1, k+1):
            try:
                os.mkdir(directory[d]+'Split-'+str(si)+'-'+ str(x))                   
                #print("Directory " , directory[d]+'Split-'+str(s)+'-'+ str(x) ,  " Created ")   
            except OSError:
                print("Directory " , directory[d]+'Split-'+str(si)+'-'+ str(x) ,  " already exists")
            try:
                os.mkdir(directory[d]+'Split-'+str(si)+'-'+ str(x)+'/Backup')       
                #print("Directory " , directory[d]+'Split-'+str(s)+'-'+ str(x)+'/Backup' ,  " Created ")   
            except OSError:
                print("Directory " , directory[d]+'Split-'+str(si)+'-'+ str(x)+'/Backup' ,  " already exists")
            #create the names file
            with open(directory[d]+'Split-'+str(si)+'-'+ str(x)+'/names.names', 'w') as writi:
                writi.write('Person')
                writi.close()             
        for x in range(1, k+1):
            strData = \
            'classes = 1\n\
train = '+directory_data[d]+'Split-'+str(si)+'-'+ str(x)+'/fold'+str(si)+str(x)+'train.txt\n\
valid = '+directory_data[d]+'Split-'+str(si)+'-'+ str(x)+'/fold'+str(si)+str(x)+'valid.txt\n\
names = '+directory_data[d]+'Split-'+str(si)+'-'+ str(x)+'/names.names\n\
backup = '+directory_data[d]+'Split-'+str(si)+'-'+ str(x)+'/Backup/'
            #write the data file
            with open(directory[d]+'Split-'+str(si)+'-'+ str(x) +nameevl +directorylist[d].lower()+ '_data.data', 'w') as dataFile:
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
        #create the files for testing in the split folders
        if re.search("Depth",directorylist[i]):
               testtxtstring=re.sub(r'rgb.png','depth.png',testtxtstring)
        for si in range(1,s+1):
            for index in xrange(1, k+1):
                filename=directory[i]+'Split-'+str(si)+'-'+ str(index)+nameevl+txtlist[i]+'_test'+subname[i][u]+'.txt'
                with open(filename, 'w') as writi:
                    writi.write(testtxtstring)
                    writi.close()  
                #create cfg files
                try:
                    #print(cfgpath,directory[i]+'Split-'+str(si)+'-'+ str(index)+nameevl+txtlist[i]+'.cfg')
                    shutil.copy2(cfgpath,directory[i]+'Split-'+str(si)+'-'+ str(index)+nameevl+txtlist[i]+'.cfg')   
                except OSError:
                    print("cfg already exists")   
arrTrain = [[]]
num_lines_all = sum(1 for line in open(trainTXTPath))
print(num_lines_all, 'lines count all')
print(k, 'k')
num_lines_fold = num_lines_all / k
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


for si in range(0,s):
    #for each split shuffel
    for ind in range(0,datapoints+1):    
        random.shuffle(arrTrain[ind])   
    strFold=[]
    for lala in range (0,k):
        strFold.append([])
    cur=0
    #this takes care of spliting our train into the k-folds
    for m in range(0,datapoints+1):
        for l in range(0,len(arrTrain[m])):             
            strFold[cur].append(arrTrain[m][l])
            cur=cur+1
            if cur >= k:
                cur = 0
    print("length of the folds")
    sum=0
    for m in range(0,k):
        sum+=len(strFold[m])
    for i in range(0,k):    
        print(sum-len(strFold[m]))
    #every pink, etc gets the same data
    for d in range(0, len(directory)):      
        
        for i in xrange(0, k): # 1 bis einschliesslich 5  
            with open(foldtrain[d][si][i], 'w') as foldtrainFile:
                with open(foldvalid[d][si][i], 'w') as foldvalFile:
                    for index in xrange(0, k):        
                        for m in xrange(0,len(strFold[index])):
                            if(i != index):
                                new=re.sub(r'DatasetsPink','Datasets'+directorylist[d],str(strFold[index][m]))
                                if re.search("Depth",new):
                                    new2=re.sub(r'rgb.png','depth.png',new)
                                    new=new2
                                foldtrainFile.write(new)
                            else:   
                                new=re.sub(r'DatasetsPink','Datasets'+directorylist[d],str(strFold[index][m]))
                                if re.search("Depth",new):
                                    new2=re.sub(r'rgb.png','depth.png',new)
                                    new=new2
                                foldvalFile.write(new)
                                if None == re.search("Depth",new):
                                    for time in daytime:         
                                        dummy = strFold[i][m].replace('Tag', time)
                                        new=re.sub(r'DatasetsPink','Datasets'+directorylist[d],dummy)
                                        foldvalFile.write(new)                           
print "done"