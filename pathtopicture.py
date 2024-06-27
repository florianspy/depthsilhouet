import glob, os
# Creates from a Dataset a train, test and evaluation file with the paths of
# the images for learning with YOLO.
# Dir of the images
#parameter
evalname="ichbinmegageil"
directory =os.path.expanduser("~/Documents/darknet-yolov4/Master/DatasetsPink")


# Create and/or truncate train.txt and test.txt
folder=os.path.expanduser("~/Downloads/"+evalname)
os.mkdir(folder) 
filename =folder+"/pink_alles.txt"
file_eval = open(filename, 'w')
for pathAndFilename in glob.glob(directory + "/Labor1Tag/*rgb.png"):
 	print(pathAndFilename)
	title, ext = os.path.splitext(os.path.basename(pathAndFilename))
	file_eval.write(directory + "/Labor1Tag/" + title + '.png' + "\n")
for pathAndFilename in glob.glob(directory + "/Labor2Tag/*rgb.png"):
	print(pathAndFilename)
	title, ext = os.path.splitext(os.path.basename(pathAndFilename))
	file_eval.write(directory + "/Labor2Tag/" + title + '.png' + "\n")
for pathAndFilename in glob.glob(directory + "/Labor3Tag/*rgb.png"):
	print(pathAndFilename)
	title, ext = os.path.splitext(os.path.basename(pathAndFilename))
	file_eval.write(directory + "/Labor3Tag/" + title + '.png' + "\n")
for pathAndFilename in glob.glob(directory + "/Labor4Tag/*rgb.png"):
	print(pathAndFilename)
	title, ext = os.path.splitext(os.path.basename(pathAndFilename))
	file_eval.write(directory + "/Labor4Tag/" + title + '.png' + "\n")
for pathAndFilename in glob.glob(directory + "/Labor5Tag/*rgb.png"):
	print(pathAndFilename)
	title, ext = os.path.splitext(os.path.basename(pathAndFilename))
	file_eval.write(directory + "/Labor5Tag/" + title + '.png' + "\n")
for pathAndFilename in glob.glob(directory + "/Gang1Tag/*rgb.png"):
	print(pathAndFilename)
	title, ext = os.path.splitext(os.path.basename(pathAndFilename))
	file_eval.write(directory + "/Gang1Tag/" + title + '.png' + "\n")
for pathAndFilename in glob.glob(directory + "/Gang2Tag/*rgb.png"):
	print(pathAndFilename)
	title, ext = os.path.splitext(os.path.basename(pathAndFilename))
	file_eval.write(directory + "/Gang2Tag/" + title + '.png' + "\n")
for pathAndFilename in glob.glob(directory + "/Gang3Tag/*rgb.png"):
	print(pathAndFilename)
	title, ext = os.path.splitext(os.path.basename(pathAndFilename))
	file_eval.write(directory + "/Gang3Tag/" + title + '.png' + "\n")
for pathAndFilename in glob.glob(directory + "/Gang4Tag/*rgb.png"):
	print(pathAndFilename)
	title, ext = os.path.splitext(os.path.basename(pathAndFilename))
	file_eval.write(directory + "/Gang4Tag/" + title + '.png' + "\n")
for pathAndFilename in glob.glob(directory + "/Gang5Tag/*rgb.png"):
	print(pathAndFilename)
	title, ext = os.path.splitext(os.path.basename(pathAndFilename))
	file_eval.write(directory + "/Gang5Tag/" + title + '.png' + "\n")
for pathAndFilename in glob.glob(directory + "/Gang6Tag/*rgb.png"):
	print(pathAndFilename)
	title, ext = os.path.splitext(os.path.basename(pathAndFilename))
	file_eval.write(directory + "/Gang6Tag/" + title + '.png' + "\n")
for pathAndFilename in glob.glob(directory + "/Gang7Tag/*rgb.png"):
	print(pathAndFilename)
	title, ext = os.path.splitext(os.path.basename(pathAndFilename))
	file_eval.write(directory + "/Gang7Tag/" + title + '.png' + "\n")
for pathAndFilename in glob.glob(directory + "/Gang8Tag/*rgb.png"):
	print(pathAndFilename)
	title, ext = os.path.splitext(os.path.basename(pathAndFilename))
	file_eval.write(directory + "/Gang8Tag/" + title + '.png' + "\n")
for pathAndFilename in glob.glob(directory + "/Gang9Tag/*rgb.png"):
	print(pathAndFilename)
	title, ext = os.path.splitext(os.path.basename(pathAndFilename))
	file_eval.write(directory + "/Gang9Tag/" + title + '.png' + "\n")
for pathAndFilename in glob.glob(directory + "/Frau1Tag/*rgb.png"):
	print(pathAndFilename)
	title, ext = os.path.splitext(os.path.basename(pathAndFilename))
	file_eval.write(directory + "/Frau1Tag/" + title + '.png' + "\n")
for pathAndFilename in glob.glob(directory + "/Flo1Tag/*rgb.png"):
	print(pathAndFilename)
	title, ext = os.path.splitext(os.path.basename(pathAndFilename))
	file_eval.write(directory + "/Flo1Tag/" + title + '.png' + "\n")