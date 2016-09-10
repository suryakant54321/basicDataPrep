#-----------------------------------------------------
# Ref YATSM :https://github.com/ceholden/yatsm
# ----------------------------------------------------
# Script Name: extractArray.py
# Author: Suryakant Sawant (suryakant54321@gmail.com)
# Date: 20 August 2015
# This script helps to extract data from cache of YATSM :) 
# to increase Time Series analysis capabilities  
# 
# 1. Read all chache files (.npz)
# 2. Extract usable information
# 	band number, date, reflectance
# 3. Write csv file with pixel details 
#	convention used for output files
#	<pixel ID>_<Shape>.csv 
#
# 	simple ! is it !! ?? :) 
# 4. Now you can use output and process it with 
# 	Python / R / Spreadsheets / Matlab
#
# Note: If you are successful in running TSTools / YATSM
#	in QGIS(i.e.  
#		https://github.com/ceholden/TSTools or 
#		https://github.com/ceholden/yatsm
#
#	I am trying to make it more simple. 
#	Some sections are hard coded (marked with #--*--)
#-----------------------------------------------------
#!/bin python2
import os, re, gdal
import numpy as np
import shutil, time
# To Do : plot values on the fly :)
#import * from pylab
#import matplotlib	
#
# Your project path
os.chdir("/media/opengeo-usb/surya2")				#--*--
# cache path
cacheDir = "suryaWork/work/8_thermalData/4_tsData/cache" 	#--*--
csvPath = "suryaWork/work/8_thermalData/6_TimeSeriesOutput" 	#--*--
def extract(cacheDir, csvPath):
	#print (cacheDir)	
	allFiles = os.listdir(cacheDir) 
	count = 0
	for zipAray in allFiles:
		#print(zipAray)
		if zipAray.endswith(".npz"):
			filePath = ("%s/%s")%(cacheDir, zipAray)
			a = np.load(filePath)
			print("==========================\n \
			Processing new %s File ")%(zipAray)
			print ("Keys = %s")%(a.keys())
			# ['image_0', 'data_0']
			metData = a['image_0']
			print("datatype of key image_0 = %s")%(metData.dtype)
			""" 
			[('filename', 'O'), ('path', 'O'), ('id', 'O'), 
			('date', 'O'), ('ordinal', '<u4'), ('doy', '<u2')]
			"""
			print ("Sample Key image_0 = %s")%(metData[0])
			"""
			('subset_LT51450451990031.tif', '<folder path>/subset_LT51450451990031.tif', 
			'LT51450451990031', datetime.datetime(1990, 1, 31, 0, 0), 726498L, 31)
			"""
			data = a['data_0']
			print ("Number of arrays/Bands in data = %s")%(len(data))
			print ("Number of observations for a band = %s")%(len(data[0]))
			print ("shape of data array = ");print(data.shape)
			# Fun Starts here :)
			tData = np.transpose(data)
			print ("New shape of data array = ");print(tData.shape)
			#***
			fNames = []
			dateTime = []
			ordDay = []
			for i in range(0,len(metData)):
    				fNames.append(metData[i][2])	#--*--
    				dateTime.append(metData[i][3])	#--*--
    				ordDay.append(metData[i][4])	#--*--			
			fNames = np.asarray(fNames, dtype=np.str)
			dateTime = np.asarray(dateTime, dtype=np.str)
			ordDay = np.asarray(ordDay, dtype=np.str)
			numRows = len(fNames)
			fNames = fNames.reshape(numRows,1)
			dateTime = dateTime.reshape(numRows,1)
			ordDay = ordDay.reshape(numRows,1)
			#***
			# concatenate all arrays. This (#*** to #***) can be done in much better and faster way :)
			allMet = np.concatenate((fNames, dateTime, ordDay, tData), axis=1)
			print("New array shape = ")			
			print(allMet.shape)
			jj = allMet.shape
			csvFile = re.split('_',zipAray) # x1121y1090_i0n388b8.npz
			csvFile = ("%s_r%sc%s.csv")%(csvFile[0],jj[0], jj[1])
			csvFile = ("%s/%s")%(csvPath, csvFile)
			np.savetxt(csvFile, allMet, delimiter=',', fmt='%19s', header='name, date, ordate, b, g, r, nir, swir1, swir2, cfmask, thermal')
			#print ("Array %s available")%(zipAray) 
#--
extract(cacheDir, csvPath)
#
