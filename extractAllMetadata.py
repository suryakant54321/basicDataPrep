#-----------------------------------------------------
# This script helps to create basic directory structure 
# for Time Series analysis using YATSM
# Ref YATSM :https://github.com/ceholden/yatsm
# ----------------------------------------------------
# Script Name: extractAllMetadata.py
# Author: Suryakant Sawant (suryakant54321@gmail.com)
#
# Previous step
# 1. Download required reflectance data from USGS espa site
#	extract >> stack >> subset 
#	using extractAll.py 
# Steps	
# 1. Create list of all scenes (for reference)
# 2. Download only metadata for each scene 
#	(this is optional. Only to explore 
#	additional functions of YATSM)
#
# 3. set the directory path in subsequent lines
#	(Line: 31, 33, 43, 44, 52 and 53)
# 4. the script will create the necessairy folder 
#	structure for your time series analysis
#
# Note: I am trying to make it more simple. 
# 	It may take some time. :(
#-----------------------------------------------------
#!/bin python2
import os, re, gdal
import shutil, time
# Your project path
os.chdir("/media/opengeo-vm/surya2/5_timeSeriesAnalysis")
# metadata path
metaDir = "0_sourceData/allMetadata"
def extract(metaDir):
	allFiles = os.listdir(metaDir) 
	count = 0
	for i in allFiles:
		if i.endswith(".gz"):
			out = re.split("-",i)
			extractedDir = out[0]
			print ("processing %s")%(i)
			# extract directory (may not need to change)
			newDir = ("sudo mkdir 1_extract/%s")%(extractedDir) 
			extracT = ("sudo tar -xvf %s/%s -C 1_extract/%s/")%(metaDir, i, extractedDir)  
			#print (newDir, extracT)		
			os.system(newDir) # new dir is cerated
			os.system(extracT) # extraction executes here
			print ("copying files into %s")%(extractedDir)
			#time.sleep(1)
			# path to subset directory. The script extractAll.py has done this
			# change accordingly
			srcFile = ("3_subset/subset_%s.tif")%(extractedDir)	
			dstFile = ("1_extract/%s/subset_%s.tif")%(extractedDir, extractedDir)			
			shutil.copy(srcFile, dstFile)
			count = count+1
			print ("File %s of %s complete")%(count, len(allFiles))
#--
extract(metaDir)
#
