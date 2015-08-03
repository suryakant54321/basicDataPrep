#!/bin python2
import os, re, gdal
import shutil
# description will be added very soon
os.chdir("/media/opengeo-vm/6BC47EF334814001/suryaWork/work/5_timeSeriesAnalysis")
# Extract all
def extract():
	allFiles = os.listdir("0_sourceData/")
	count = 0
	for i in allFiles:
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
		shutil.rmtree(delDirPath)
	except:
		print("error in deleting extracted files")
	##---------
	# subset
	print "start subset"
	SHPpath = "0_sourceData/studyShapeFile/testSite.shp"
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
		os.remove(stackPath)
	except:
		print("error in deteting stacked file Stack_%s.tif")%(extractedDir)
#--
extract()

