#The below script will create the folders we use for learning but the pink and the depthnah folders will not be filled with data because they require other steps. This script also creates pink_alles.txt 
#name of the folders to be created
Foldernames=(Arc Rot Still Trans)
#where to get the files from
Folderlist=(~/Downloads/KTP_dataset_images/images/Arc ~/Downloads/KTP_dataset_images/images/Rotation ~/Downloads/KTP_dataset_images/images/Still ~/Downloads/KTP_dataset_images/images/Translation)
#which folders to create
varnames=(DatasetsRGB DatasetsPink DatasetsDepth DatasetsDepthNah DatasetsDepthWeit)
numvars=${#varnames[@]}
numnames=${#Foldernames[@]}
#where the folders should be created
defname="$HOME/Downloads/KTP2"
#path relative to yolo folder where later (in another script) the images of this dataset be copied to 
despathrelyolo="$HOME/Documents/darknet-yolov4/Paper/KTP/"
#name of pink_alles.txt file
pnka=$defname/pink_alles.txt

rm $pnka
mkdir ${defname}
for ((idx=0; idx<$numvars; idx++))
do 
mkdir "${defname}/${varnames[idx]}"
done
for ((idx=0; idx<$numnames; idx++))
do    
  for ((idx2=0; idx2<$numvars; idx2++))
  do 
    mkdir "${defname}/${varnames[idx2]}/${Foldernames[idx]}Tag"
  done	
	mkdir "${defname}/DatasetsRGB/${Foldernames[idx]}Abend"
	mkdir "${defname}/DatasetsRGB/${Foldernames[idx]}Nacht"
	mkdir "${defname}/DatasetsPink/${Foldernames[idx]}Abend"
	mkdir "${defname}/DatasetsPink/${Foldernames[idx]}Nacht"
	mkdir "${defname}/DatasetsPink/${Foldernames[idx]}Schwarz"
done

for ((idx=0; idx<$numnames; idx++))
do
  for file in `find ${Folderlist[idx]}/depth -maxdepth 1 -type f -name "*.pgm"`;do
   filename=$(basename "$file") 
   cp $file ${defname}/DatasetsDepth/${Foldernames[idx]}Tag/$filename
   echo "copying"$filename
  done
  for file in `find ${Folderlist[idx]}/rgb -maxdepth 1 -type f -name "*.jpg"`;do
   filename=$(basename "$file") 
   cp $file ${defname}/DatasetsRGB/${Foldernames[idx]}Tag/$filename
   cp $file ${defname}/DatasetsRGB/${Foldernames[idx]}Abend/$filename
   cp $file ${defname}/DatasetsRGB/${Foldernames[idx]}Nacht/$filename
   echo "$despathrelyolo/DatasetsPink/${Foldernames[0]}Tag/$filename">>$pnka
   echo "copying"$filename
  done
done
echo "finished moving files"
for ((idx=0; idx<$numnames; idx++))
do
       cd ${defname}/DatasetsRGB/${Foldernames[idx]}Abend
       for file in `find ${defname}/DatasetsRGB/${Foldernames[idx]}Abend -maxdepth 1 -type f -name "*.jpg"`;do
		      filename=$(basename "$file") 
		      mogrify $filename -brightness-contrast -40x-40 $filename
          echo "processed $file"
       done
       cd ..
       cd ${defname}/DatasetsRGB/${Foldernames[idx]}Nacht
       for file in `find ${defname}/DatasetsRGB/${Foldernames[idx]}Nacht -maxdepth 1 -type f -name "*.jpg"`;do
            		filename=$(basename "$file") 
            		mogrify $filename -brightness-contrast -65x-65 $filename
                echo "processed $file"
       done          
       cd ..
done