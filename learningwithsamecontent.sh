#!/bin/bash
func(){
	echo "xterm -e \"$1\" &"
	echo "process_id=$!"
	echo "wait $process_id"

	xterm -e "$1" &
	process_id=$!
	wait $process_id
}

# Paths to darknet where you put your data
path_darknet=$HOME'/Documents/darknet-yolov4/'
# dataset name capital letters for evalfoldername which is part of foldername lower case letters for evalname which is part of the filenames
evalname='evl20001'
evalfoldername='EVL20001'
# typefolder contain capital letters while type only have lower, [rgb -> RGB, pink -> Pink, depthweit -> DepthWeit, depth -> Depth, depthnah -> DepthNah ...]
type='rgb'
typefolder='RGB'
#path to the evalfoldername relative to yolo
foldername='Paper/KTP/'

# Path to .cfg files (will be 'TestAutomate/Median/k/')
path_folders=$foldername$evalfoldername'/'$typefolder'/'	

# In [path_folders]
# Name of the .cfg file in [path_folders]
cfg_filename=$evalname'_'$type	

eval_Valid_filename=${evalname}'_'$type	
eval_Tag_filename=${evalname}'_'$type'_testTag'		# Name of the eval .txt file
eval_Abend_filename=${evalname}'_'$type'_testAbend'
eval_Nacht_filename=${evalname}'_'$type'_testNacht'
eval_Schwarz_filename=${evalname}'_'$type'_testSchwarz'

data_filename=${evalname}'_'$type'_data'			# Name of the .data file
echo $path_folders

# Von einschließelich
split_from=1
# Bis einschließelich
split_to=3

for ((s=$split_from; s<=$split_to; s++)); do	
		START_TIME=$SECONDS
		echo "----------------- TRAIN -----------------------------"
		train="./darknet detector train ${path_folders}Split-${s}/${data_filename}.data ${path_folders}Split-${s}/${cfg_filename}.cfg darknet53.conv.74 -gpus 0,1 -dont_show -map"
		func "${train}"
		sleep 1
		echo "----------------- Vaild final -----------------------------"
		test="./darknet detector test ${path_folders}Split-${s}/${data_filename}.data ${path_folders}Split-${s}/${cfg_filename}.cfg ${path_folders}Split-${s}/Backup/${cfg_filename}_final.weights -thresh 0.5 -dont_show -ext_output < ${path_folders}Split-${s}/fold${s}${f}valid.txt > ${path_folders}Split-${s}/results_${eval_Valid_filename}_fold${s}${f}valid_final_Split_${s}.txt"
		func "${test}"
		sleep 1
		echo "----------------- Vaild best -----------------------------"
		test="./darknet detector test ${path_folders}Split-${s}/${data_filename}.data ${path_folders}Split-${s}/${cfg_filename}.cfg ${path_folders}Split-${s}/Backup/${cfg_filename}_best.weights -thresh 0.5 -dont_show -ext_output < ${path_folders}Split-${s}/fold${s}${f}valid.txt > ${path_folders}Split-${s}/results_${eval_Valid_filename}_fold${s}${f}valid_best_Split_${s}.txt"
		func "${test}"
		sleep 1
		echo "----------------- Tag final -----------------------------"
		test="./darknet detector test ${path_folders}Split-${s}/${data_filename}.data ${path_folders}Split-${s}/${cfg_filename}.cfg ${path_folders}Split-${s}/Backup/${cfg_filename}_final.weights -thresh 0.5 -dont_show -ext_output < ${path_folders}Split-${s}/${eval_Tag_filename}.txt > ${path_folders}Split-${s}/results_${eval_Tag_filename}_final_Split_${s}.txt"
		func "${test}"
		sleep 1
		echo "------------------ Abend final -----------------------------"
		test="./darknet detector test ${path_folders}Split-${s}/${data_filename}.data ${path_folders}Split-${s}/${cfg_filename}.cfg ${path_folders}Split-${s}/Backup/${cfg_filename}_final.weights -thresh 0.5 -dont_show -ext_output < ${path_folders}Split-${s}/${eval_Abend_filename}.txt > ${path_folders}Split-${s}/results_${eval_Abend_filename}_final_Split_${s}.txt"
		func "${test}"
		sleep 1
		echo "------------------ Nacht final -----------------------------"
		test="./darknet detector test ${path_folders}Split-${s}/${data_filename}.data ${path_folders}Split-${s}/${cfg_filename}.cfg ${path_folders}Split-${s}/Backup/${cfg_filename}_final.weights -thresh 0.5 -dont_show -ext_output < ${path_folders}Split-${s}/${eval_Nacht_filename}.txt > ${path_folders}Split-${s}/results_${eval_Nacht_filename}_final_Split_${s}.txt"
		func "${test}"
		sleep 1
		# echo "------------------ Schwarz final -----------------------------"
		# test="./darknet detector test ${path_folders}Split-${s}/${data_filename}.data ${path_folders}Split-${s}/${cfg_filename}.cfg ${path_folders}Split-${s}/Backup/${cfg_filename}_final.weights -thresh 0.5 -dont_show -ext_output < ${path_folders}Split-${s}/${eval_Schwarz_filename}.txt > ${path_folders}Split-${s}/results_${eval_Schwarz_filename}_final_Split_${s}.txt"
		# func "${test}"
		# sleep 1
		echo "----------------- Tag best -----------------------------"
		test="./darknet detector test ${path_folders}Split-${s}/${data_filename}.data ${path_folders}Split-${s}/${cfg_filename}.cfg ${path_folders}Split-${s}/Backup/${cfg_filename}_best.weights -thresh 0.5 -dont_show -ext_output < ${path_folders}Split-${s}/${eval_Tag_filename}.txt > ${path_folders}Split-${s}/results_${eval_Tag_filename}_best_Split_${s}.txt"
		func "${test}"
		sleep 1
		echo "------------------ Abend best -----------------------------"
		test="./darknet detector test ${path_folders}Split-${s}/${data_filename}.data ${path_folders}Split-${s}/${cfg_filename}.cfg ${path_folders}Split-${s}/Backup/${cfg_filename}_best.weights -thresh 0.5 -dont_show -ext_output < ${path_folders}Split-${s}/${eval_Abend_filename}.txt > ${path_folders}Split-${s}/results_${eval_Abend_filename}_best_Split_${s}.txt"
		func "${test}"
		sleep 1
		echo "------------------ Nacht best -----------------------------"
		test="./darknet detector test ${path_folders}Split-${s}/${data_filename}.data ${path_folders}Split-${s}/${cfg_filename}.cfg ${path_folders}Split-${s}/Backup/${cfg_filename}_best.weights -thresh 0.5 -dont_show -ext_output < ${path_folders}Split-${s}/${eval_Nacht_filename}.txt > ${path_folders}Split-${s}/results_${eval_Nacht_filename}_best_Split_${s}.txt"
		func "${test}"
		sleep 1
		# echo "------------------ Schwarz best -----------------------------"
		# test="./darknet detector test ${path_folders}Split-${s}/${data_filename}.data ${path_folders}Split-${s}/${cfg_filename}.cfg ${path_folders}Split-${s}/Backup/${cfg_filename}_best.weights -thresh 0.5 -dont_show -ext_output < ${path_folders}Split-${s}/${eval_Schwarz_filename}.txt > ${path_folders}Split-${s}/results_${eval_Schwarz_filename}_best_Split_${s}.txt"
		# func "${test}"
		# sleep 1

		echo "-------------------- writeParameters -------------------------"
		write="python3 writeParameters.py -path='${path_darknet}${path_folders}Split-${s}/'"
		func "${write}"
		sleep 1
		echo "-------------------- Move ---------------------------"
		mv ${path_darknet}chart.png ${path_darknet}${path_folders}Split-${s}/chart.png
		sleep 1
		echo "---------------------------------------------------"
		ELAPSED_TIME=$(($SECONDS - $START_TIME))
		echo "$(($ELAPSED_TIME/60)) min $(($ELAPSED_TIME%60)) sec"  
done


##########################################################################################################################################
##########################################################################################################################################
##########################################################################################################################################
##########################################################################################################################################
##########################################################################################################################################
##########################################################################################################################################
##########################################################################################################################################
##########################################################################################################################################
##########################################################################################################################################
##########################################################################################################################################
##########################################################################################################################################
##########################################################################################################################################
##########################################################################################################################################
##########################################################################################################################################
##########################################################################################################################################
##########################################################################################################################################
##########################################################################################################################################

# Paths
type='depthweit'
typefolder='DepthWeit'
path_folders=$foldername$evalfoldername'/'$typefolder'/'		# Path to .cfg files (will be 'TestAutomate/Median/k/')

# In [path_folders]
# Name of the .cfg file in [path_folders]
cfg_filename=${evalname}'_'$type		
eval_Valid_filename=${evalname}'_'$type''	
eval_Tag_filename=${evalname}'_'$type'_testTag'		# Name of the eval .txt file
eval_Abend_filename=${evalname}'_'$type'_testAbend'
eval_Nacht_filename=${evalname}'_'$type'_testNacht'
eval_Schwarz_filename=${evalname}'_'$type'_testSchwarz'

data_filename=${evalname}'_'$type'_data'			# Name of the .data file

# Von einschließelich
split_from=1
# Bis einschließelich
split_to=1




for ((s=$split_from; s<=$split_to; s++)); do
		START_TIME=$SECONDS
		echo "----------------- TRAIN -----------------------------"
		train="./darknet detector train ${path_folders}Split-${s}/${data_filename}.data ${path_folders}Split-${s}/${cfg_filename}.cfg darknet53.conv.74 -gpus 0,1 -dont_show -map"
		func "${train}"
		ELAPSED_TIME=$(($SECONDS - $START_TIME))
		echo "$(($ELAPSED_TIME/60)) min $(($ELAPSED_TIME%60)) sec"  
		sleep 1
		echo "----------------- Vaild final -----------------------------"
		test="./darknet detector test ${path_folders}Split-${s}/${data_filename}.data ${path_folders}Split-${s}/${cfg_filename}.cfg ${path_folders}Split-${s}/Backup/${cfg_filename}_final.weights -thresh 0.5 -dont_show -ext_output < ${path_folders}Split-${s}/fold${s}${f}valid.txt > ${path_folders}Split-${s}/results_${eval_Valid_filename}_fold${s}${f}valid_final_Split_${s}.txt"
		func "${test}"
		sleep 1
		echo "----------------- Vaild best -----------------------------"
		test="./darknet detector test ${path_folders}Split-${s}/${data_filename}.data ${path_folders}Split-${s}/${cfg_filename}.cfg ${path_folders}Split-${s}/Backup/${cfg_filename}_best.weights -thresh 0.5 -dont_show -ext_output < ${path_folders}Split-${s}/fold${s}${f}valid.txt > ${path_folders}Split-${s}/results_${eval_Valid_filename}_fold${s}${f}valid_best_Split_${s}.txt"
		func "${test}"
		sleep 1
		echo "----------------- Tag final -----------------------------"
		test="./darknet detector test ${path_folders}Split-${s}/${data_filename}.data ${path_folders}Split-${s}/${cfg_filename}.cfg ${path_folders}Split-${s}/Backup/${cfg_filename}_final.weights -thresh 0.5 -dont_show -ext_output < ${path_folders}Split-${s}/${eval_Tag_filename}.txt > ${path_folders}Split-${s}/results_${eval_Tag_filename}_final_Split_${s}.txt"
		func "${test}"
		sleep 1
		echo "----------------- Tag best -----------------------------"
		test="./darknet detector test ${path_folders}Split-${s}/${data_filename}.data ${path_folders}Split-${s}/${cfg_filename}.cfg ${path_folders}Split-${s}/Backup/${cfg_filename}_best.weights -thresh 0.5 -dont_show -ext_output < ${path_folders}Split-${s}/${eval_Tag_filename}.txt > ${path_folders}Split-${s}/results_${eval_Tag_filename}_best_Split_${s}.txt"
		func "${test}"
		sleep 1
		echo "-------------------- writeParameters -------------------------"
		write="python3 writeParameters.py -path='${path_darknet}${path_folders}Split-${s}/'"
		func "${write}"
		sleep 1
		echo "-------------------- Move ---------------------------"
		mv ${path_darknet}chart.png ${path_darknet}${path_folders}Split-${s}/chart.png
		sleep 1
		echo "---------------------------------------------------"
		ELAPSED_TIME=$(($SECONDS - $START_TIME))
		echo "$(($ELAPSED_TIME/60)) min $(($ELAPSED_TIME%60)) sec"  
done


# Von einschließelich
split_from=2
# Bis einschließelich
split_to=2




for ((s=$split_from; s<=$split_to; s++)); do
		START_TIME=$SECONDS
		echo "----------------- TRAIN -----------------------------"
		train="./darknet detector train ${path_folders}Split-${s}/${data_filename}.data ${path_folders}Split-${s}/${cfg_filename}.cfg darknet53.conv.74 -gpus 0,1 -dont_show -map"
		func "${train}"
		ELAPSED_TIME=$(($SECONDS - $START_TIME))
		echo "$(($ELAPSED_TIME/60)) min $(($ELAPSED_TIME%60)) sec"  
		sleep 1
		echo "----------------- Vaild final -----------------------------"
		test="./darknet detector test ${path_folders}Split-${s}/${data_filename}.data ${path_folders}Split-${s}/${cfg_filename}.cfg ${path_folders}Split-${s}/Backup/${cfg_filename}_final.weights -thresh 0.5 -dont_show -ext_output < ${path_folders}Split-${s}/fold${s}${f}valid.txt > ${path_folders}Split-${s}/results_${eval_Valid_filename}_fold${s}${f}valid_final_Split_${s}.txt"
		func "${test}"
		sleep 1
		echo "----------------- Vaild best -----------------------------"
		test="./darknet detector test ${path_folders}Split-${s}/${data_filename}.data ${path_folders}Split-${s}/${cfg_filename}.cfg ${path_folders}Split-${s}/Backup/${cfg_filename}_best.weights -thresh 0.5 -dont_show -ext_output < ${path_folders}Split-${s}/fold${s}${f}valid.txt > ${path_folders}Split-${s}/results_${eval_Valid_filename}_fold${s}${f}valid_best_Split_${s}.txt"
		func "${test}"
		sleep 1
		echo "----------------- Tag final -----------------------------"
		test="./darknet detector test ${path_folders}Split-${s}/${data_filename}.data ${path_folders}Split-${s}/${cfg_filename}.cfg ${path_folders}Split-${s}/Backup/${cfg_filename}_final.weights -thresh 0.5 -dont_show -ext_output < ${path_folders}Split-${s}/${eval_Tag_filename}.txt > ${path_folders}Split-${s}/results_${eval_Tag_filename}_final_Split_${s}.txt"
		func "${test}"
		sleep 1
		echo "----------------- Tag best -----------------------------"
		test="./darknet detector test ${path_folders}Split-${s}/${data_filename}.data ${path_folders}Split-${s}/${cfg_filename}.cfg ${path_folders}Split-${s}/Backup/${cfg_filename}_best.weights -thresh 0.5 -dont_show -ext_output < ${path_folders}Split-${s}/${eval_Tag_filename}.txt > ${path_folders}Split-${s}/results_${eval_Tag_filename}_best_Split_${s}.txt"
		func "${test}"
		sleep 1
		echo "-------------------- writeParameters -------------------------"
		write="python3 writeParameters.py -path='${path_darknet}${path_folders}Split-${s}/'"
		func "${write}"
		sleep 1
		echo "-------------------- Move ---------------------------"
		mv ${path_darknet}chart.png ${path_darknet}${path_folders}Split-${s}/chart.png
		sleep 1
		echo "---------------------------------------------------"
		ELAPSED_TIME=$(($SECONDS - $START_TIME))
		echo "$(($ELAPSED_TIME/60)) min $(($ELAPSED_TIME%60)) sec"  