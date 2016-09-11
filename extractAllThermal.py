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
# To do
# 1. Extract thermal data
# 2. subset thermal data
# 3. Stack thermal data with original data
#!/bin python2
import os, re, gdal
import shutil, time
# Your project path
print (os.getcwd())
os.chdir("/home/agrolab/Desktop/tc_work/rasterData/proc/")
print (os.getcwd())
# Select only TOA Band for perticular list of files
def selectTOA(outFiles):
	filEid = "NULL"
	for filE in outFiles:
		if (filE[0:3] == "LE7"):
			if filE.endswith("_band6.tif"):
				filEid = filE
		elif (filE[0:3] == "LT5"):
			if filE.endswith("_band6.tif"):
				filEid = filE
		elif (filE[0:3] == "LC8"):
			if filE.endswith("_band10.tif"):
				filEid = filE
		else:
			filEid = "NULL"
	#print(filEid)	
	return(filEid)

# data path
dataDir = "0_sourceData/thermal_n_mSAVI"
outDir = "1_extract"
subsetDir = "3_1_subset_thermal"
oldStack = "3_subset"
stackDir = "2_stack"
stTime = time.time()
def inOutDir(dataDir, outDir):
	SHPpath = "4_shapeFiles/subsetLayer/ProjLuLcSelTaluk.shp"
	allFiles = os.listdir(dataDir) 
	count = 0
	stTime = time.time()
	for i in allFiles:
		try:
			if i.endswith(".gz"):
				out = re.split("-",i)
				extractedDir = out[0]
				#print ("processing %s")%(i)
				# extract directory (may not need to change)
				newDir = ("mkdir %s/%s")%(outDir, extractedDir) 
				extracT = ("tar -xvf %s/%s -C %s/%s/")%(dataDir, i, outDir, extractedDir)  
				#print (newDir, extracT)		
				os.system(newDir) 					#-- new dir is cerated
				os.system(extracT) 					#-- extraction executes here
				print ("copied files into %s")%(extractedDir)
				# Subset Directory
				# Example
				# commanD = ("sudo gdalwarp -q -cutline %s -crop_to_cutline -of GTiff 2_stack/Stack_%s.tif 3_subset/subset_%s.tif")%(SHPpath, extractedDir, extractedDir)
				outFiles = ("%s/%s")%(outDir, extractedDir)
				try:
					outFiles = os.listdir(outFiles)
					selectBand = selectTOA(outFiles) 		#-- performs new band selection
					commanD = ("sudo gdalwarp -q -cutline %s -crop_to_cutline -of GTiff %s/%s/%s %s/subset_%s.tif")%(SHPpath, outDir, extractedDir, selectBand, subsetDir, extractedDir)
					try:
						#print commanD
						os.system(commanD) 			#-- performs stack
						print ("Subset complete")
						# Stack
						# 1
						#oldStackFile = ("%s/%s/subset_%s.tif")%(oldStack, extractedDir, extractedDir)
						oldStackFile = ("%s/subset_%s.tif")%(oldStack, extractedDir)
						#print (oldStackFile)
						# 2
						newStackDir = ("%s/%s")%(stackDir, extractedDir)
						#If required make new directory
						newStackFile = ("%s/Subset_%s.tif")%(stackDir, extractedDir)
						stackCmd = ("gdal_merge.py -n 0 -a_nodata 0 -separate -of GTiff -o %s %s %s/subset_%s.tif")%(newStackFile, oldStackFile, subsetDir, extractedDir)
						try:
							print (stackCmd)
							os.system(stackCmd)
							print("stack complete ")
							# Delete extracted files
							try:
								delDirPath = ("%s/%s")%(outDir, extractedDir)
								shutil.rmtree(delDirPath)
								print("Deleted extracted files \n ============================= ")
								newTime = time.time()-stTime
								print("This took %s Seconds\n =============================")%(newTime) 
							except:
								print("Failed to delete extracted files")
						except:
							print("Error in stacking %s")%(newStackFile)
					except:
						print ("Error in subsetting %s")%(selectBand)
				except:
					print ("No extracted directory found :( ")
		except KeyboardInterrupt:
			break
#--
inOutDir(dataDir, outDir)
totTime = time.time()-stTime
print("Total Run Time = %s Seconds")%(totTime)
#
