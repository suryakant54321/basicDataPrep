#-----------------------------------------------------
# This script helps to create basic directory structure 
# for Time Series analysis using YATSM
# Ref YATSM :https://github.com/ceholden/yatsm
# ----------------------------------------------------
# Script Name: extractAll.py
# Author: Suryakant Sawant (suryakant54321@gmail.com)
#
# Step
# 1. Download required reflectance data from USGS espa site
# 2. Create following directory structure	
# 	1_project
#		0_sourceData
#		1_extract
#		2_stack
#		3_subset
#		4_training
#		5_<name as per your need>
# 3. If you wish to subset image to exact boundary of your study area
# 	in 0_sourcedata directory create directory studyShapeFile 
#		add shapefiles 		testSite.shp
#	and for metadata create directory allMetadata 
# 4. execute the script as sudo python extractAll.py
# 	the script will perform following operations
#	a. extract (.gz from 0_sourceData to 1_extract dir) 
#	b. stack extracted bands for Landsat 4, 5, 7 and 8
#		from 1_extract to 2_stack 
#	c. subset stack bands in following order
#		for L4, 5 and 7	>> B1, B2, B3, B4, B5, B7 and Cloud Mask
#		for L 8 	>> B2, B3, B4, B5, B6, B7 and Cloud Mask		
#	d. After completion the script will remove
#		i) 	extracted files
#		ii)	stacked files
#		to preserve all extracted and stacked files 
#		add comment (i.e. #) on line 108 and 133
#	 
# Next Step
# 1. Follow instructions in script extractAllMetadata.py  
# 
# Note: I am trying to make it more simple. 
# 	It may take some time. :(
#-----------------------------------------------------
#!/bin python2
import os, re, gdal
import shutil
# 
os.chdir("/home/agrolab/Desktop/tc_work/rasterData/proc")
# Extract all
def extract():
	allFiles = os.listdir("0_sourceData/")
	count = 0
	for i in allFiles:
		if i.endswith(".gz"):
			out = re.split("-",i)
			extractedDir = out[0]
			print ("processing %s")%(i)
			newDir = ("sudo mkdir 1_extract/%s")%(out[0])
			extracT = ("sudo tar -xvf 0_sourceData/%s -C 1_extract/%s/")%(i, out[0])
			#print (newDir, extracT)		
			os.system(newDir) # new dir is cerated
			os.system(extracT) # extraction executes here
			stackFor(extractedDir)
			count = count+1
			print ("File %s of %s complete")%(count, len(allFiles))
##---------
# Stack Subset and remove intermediate files
def stackFor(extractedDir):
	print ("start stacking")
	l8bandNumbers = ["2","3","4","5","6","7"]
	l7bandNumbers = ["1","2","3","4","5","7"]
	SenNums = ["4","5","7"]
	folPath = ("1_extract/%s")%(extractedDir)
	allFiles = sorted(os.listdir(folPath))
	#print allFiles
	fNames = []
	for files in allFiles:
		senName = files[2]
		maskName = files[-10:-4]
		selFile = re.split(".tif",files)
		selFile = re.split("_sr_band",selFile[0])
		if (maskName == 'cfmask'):		
			fNames.append(files)
			#print maskName
		if (senName=='8'):
			if(selFile[-1] in l8bandNumbers):			
				#print (selFile[-1],senName)
				fNames.append(files)
				#fNames.append(senName)
		if (senName in SenNums):
			if(selFile[-1] in l7bandNumbers):			
				#print (selFile[-1],senName)
				fNames.append(files)
				#fNames.append(senName)
	fNames =[fNames[1],fNames[2],fNames[3],fNames[4],fNames[5],fNames[6],fNames[0]]
	#print fNames	
	#print "New File"
	stackCmd = ("gdal_merge.py -n 0 -a_nodata 0 -separate -of GTiff -o 2_stack/Stack_%s.tif 1_extract/%s/%s 1_extract/%s/%s 1_extract/%s/%s 1_extract/%s/%s 1_extract/%s/%s 1_extract/%s/%s 1_extract/%s/%s")%(extractedDir, extractedDir, fNames[0], extractedDir,fNames[1], extractedDir,fNames[2], extractedDir,fNames[3], extractedDir,fNames[4], extractedDir,fNames[5], extractedDir,fNames[6])
	#print stackCmd
	try:
		os.system(stackCmd)# Stack executes here
		print ("stacking complete")
	except:
		print ("error in stacking files from %s")%(extractedDir)
	##---------
	# remove extracted files
	delDirPath = ("1_extract/%s")%(extractedDir)
	try:
		shutil.rmtree(delDirPath) # :)
		print("deleting extracted files")
	except:
		print("error in deleting extracted files")
	##---------
	# subset
	print "start subset"
	SHPpath = "/home/agrolab/Desktop/tc_work/rasterData/subsetLayer/ProjLuLcSelTaluk.shp"
	# gdal_translate -a_nodata 0 -projwin 8656046.82624 2466649.9095 8732510.15897 2398831.92847 /input/dir/file.tif /output/dir/file.tif
	# xMin,yMin 1974709.37,2118929.96 : xMax,yMax 2046369.22,2180790.55
	# 	
	# 8652749.69515 2462557.66251 8733762.12 2398493.44369
	#commanD = ("sudo gdal_translate -a_nodata 0 -projwin 1974709.37 2180790.55 2046369.22 2118929.96 2_stack/Stack_%s.tif 3_subset/subset_%s.tif")%(extractedDir, extractedDir)
	#commanD = ("sudo gdal_translate -a_nodata 0 -projwin 8652749.69515 2462557.66251 8733762.12 2398493.44369 2_stack/Stack_%s.tif 3_subset/subset_%s.tif")%(extractedDir, extractedDir)	
	commanD = ("sudo gdalwarp -q -cutline %s -crop_to_cutline -of GTiff 2_stack/Stack_%s.tif 3_subset/subset_%s.tif")%(SHPpath, extractedDir, extractedDir)
	#print commanD
	try:
		os.system(commanD)
		print ("subset complete")
	except:
		print ("error in subsetting Stack_%s.tif")%(extractedDir)	
	##---------
	# remove stack file
	stackPath = ("2_stack/Stack_%s.tif")%(extractedDir)
	try:
		os.remove(stackPath) # :)
		print("deteting stacked file stack_%s.tif")%(extractedDir)
	except:
		print("error in deteting stacked file stack_%s.tif")%(extractedDir)
#--
extract()

