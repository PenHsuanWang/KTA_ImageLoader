import xml.etree.ElementTree as ET
import math
import os
import time
import sys
import re
import datetime
import py7zr
from pathlib import Path


from shutil import copyfile
import shutil

sourceDir = "E:\\Work_Willy\\ImageLoader_TestDataSource\\Image_LotKTA222_Original"
testingHomeDir = "D:\\ImageLoader_test\\"
destRootDir = testingHomeDir+"test_nestForder_OV1"
#destRootDir = "Z:\\Public\\KTA_ImageLoaderTest\\test_nestForder"
#destRootDir = "Y:\\Public\\KTA_ImageLoaderTest\\test_nestForder"
#destRootDir = "X:\\Public\\imageloader_test\\test_nestForder"
#destRootDir = "C:\\Users\\willy\\Desktop\\testingImageGen\\test_nestForder"
inFiles = os.listdir(sourceDir)

#mimicFilesGenVirtualTime = datetime.datetime.strptime('23:56:00:000000 07/31/2019', '%H:%M:%S:%f %m/%d/%Y')

try:
	#====================================#
	# Try to create the folder,          #
	# Pass, if the folder already exist. #
	#====================================#
	os.makedirs(destRootDir)
except:
	pass


for i in range (1,100):

	mimicFilesGenVirtualTime = datetime.datetime.strptime('00:00:00:000000 08/01/2019', '%H:%M:%S:%f %m/%d/%Y') + datetime.timedelta(seconds = (i-1)*7*60)

	serialNumber = "%05d" %i
	productName = "PROD"+str(serialNumber)
	recipeName = "RECIPE"+str(serialNumber)
	lotIDName  = "LOT"+str(serialNumber)
	folderTimeStemp = datetime.datetime.now().strftime("%m%d%y.%H%M%S.%f")[:-3]


	#===================================================
	# Mode 1, the case of all file export to dir folder 
	#===================================================
	#destDir = destRootDir

	
	#==============================================================================
	# Mode 2, the case of folder base on folder named "<lotID>_"+"DatetimeFormate"
	#==============================================================================
	#destDir = destRootDir+"\\lot"+str(serialNumber)+"_"+folderTimeStemp

	
	#========================================================
	# Mode 3, the case of folder in the sub-folder structure 
	#========================================================	
	#destDir = destRootDir+"\\"+productName+"\\"+recipeName+"\\"+lotIDName

	#=========================================================================================#
	# Mode 4 ~ 6, need to create a temp dir, to store the temp for diring archiving the files #
	#=========================================================================================#
	tempDir = testingHomeDir+"temp"
	destDir = tempDir+"\\lot"+str(serialNumber)+"_"+folderTimeStemp

	'''
	======================================================================
	Remove folders !!!
	In case that number of folders is over than 20, remove the oldest one
	======================================================================
	'''
	
	'''
	folders = os.listdir(destRootDir)
	#folders.sort(key=lambda x: os.path.getmtime(os.path.join(destRootDir, x)))
	#oldest_file = min(folders, key=lambda x: os.path.getctime(os.path.join(destRootDir, x)))
	
	if len(folders) > 20 :
		#oldest_file = min([os.path.join(destRootDir,d) for d in os.listdir(destRootDir)], key=os.path.getmtime)
		oldest_file = min(folders, key=lambda x: os.path.getctime(os.path.join(destRootDir, x)))
		print('Remove: '+destRootDir+"\\"+oldest_file)
		shutil.rmtree(destRootDir+"\\"+oldest_file)
	'''

	#======================#
	# End of remove folder #
	#======================#

	print("Folder "+destDir+" created")

	genFilesStartTime = datetime.datetime.now()
	print("Start to generate files at: "+genFilesStartTime.strftime("%H:%M:%S"))

	print(str(len(inFiles))+" files found")
	fileCount = 0

	# Add at 09/30
	# Fitting for new CXMT requirment, create folder for certain timestemp

	try:
		os.makedirs(destDir)
	except:
		pass

	for f in inFiles:

		fileCount+=1

		k = math.floor((fileCount/(len(inFiles)))*100) + 1      
		progressBar = '>'*math.floor((fileCount/(len(inFiles)))*100)+' '*(100-k)
		sys.stdout.write('\r'+progressBar+'[%s%%]'%(math.floor((fileCount/(len(inFiles)))*100))+'(%s'%(fileCount)+'/%s'%(len(inFiles))+')' )
		sys.stdout.flush()

		if os.path.splitext(f)[1] == '.xml' :
			#----------------------------------------------------------------------------------------------------------------------------------------#
			# For saving the files to remote disk, it took more than 5 mins, thus time delta -240 seconds to prevent files time over than kdata time #
			#----------------------------------------------------------------------------------------------------------------------------------------#
			thisFilesTime = mimicFilesGenVirtualTime + datetime.timedelta(seconds = 0.12*fileCount)

			inputXML_tree = ET.parse(sourceDir+"\\"+f)
			inputXML_tree.getroot()

			ProductElementLotID = inputXML_tree.find("LotId")
			ProductElementLotID.text = lotIDName

			ProductElementRecipe = inputXML_tree.find("RecipeName")
			ProductElementRecipe.text = recipeName

			ProductElementTime = inputXML_tree.find("DateAndTime")
			ProductElementTime.text = str(thisFilesTime.strftime('%H:%M:%S:%f')[:-3])+' '+str(thisFilesTime.strftime('%m/%d/%Y'))
			
			#ProductElementSlotID = inputXML_tree.find("SlotNumber")
			#ProductElementSlotID.text = str(int(ProductElementSlotID.text) + 10)

			ProductElementWaferID = inputXML_tree.find("WaferId")
			#ProductElementWaferID.text = "WaferAAA"+ProductElementSlotID.text
			

			#=======================================================#
			# Mode 1 or 2, Saving all the file into the same folder #
			#=======================================================#
			inputXML_tree.write(destDir+"\\"+"MEASUREMENT_INNER_"+lotIDName+"_"+str(thisFilesTime.strftime('%m%d%y.%H%M%S.%f')[:-3])+".xml")
			copyfile(sourceDir+"\\LotKTA222_TIF\\"+os.path.splitext(f)[0]+".tif", destDir+"\\"+"MEASUREMENT_INNER_"+lotIDName+"_"+str(thisFilesTime.strftime('%m%d%y.%H%M%S.%f')[:-3])+".tif")
			
			#--------------------------------#
			# Save as Measurement outer type #
			#--------------------------------#
			ProductElementImageType = inputXML_tree.find("ImageType")
			ProductElementImageType.text = "Acquisition Outer"
			inputXML_tree.write(destDir+"\\"+"MEASUREMENT_OUTER_"+lotIDName+"_"+str(thisFilesTime.strftime('%m%d%y.%H%M%S.%f')[:-3])+".xml")
			copyfile(sourceDir+"\\LotKTA222_TIF\\"+os.path.splitext(f)[0]+".tif", destDir+"\\"+"MEASUREMENT_OUTER_"+lotIDName+"_"+str(thisFilesTime.strftime('%m%d%y.%H%M%S.%f')[:-3])+".tif")
			
			#====================#
			# End of Mode 1 or 2 #
			#====================#


			#===========================================================#
			# Mode3, seperate image into 2 slot id(identified by wafer) #
			#===========================================================#
			'''
			if "WAFER01" in ProductElementWaferID.text:
				# Add in 7/30 
				if not Path(destDir+"\\WAFER01").exists() :
					os.makedirs(destDir+"\\WAFER01")
				#inputXML_tree.write(destDir+"\\WAFER01\\"+lotIDName+"_"+re.sub("LotKTA222(\\S+)_", "", f))
				#copyfile(sourceDir+"\\LotKTA222_TIF\\"+os.path.splitext(f)[0]+".tif", destDir+"\\WAFER01\\"+lotIDName+"_"+re.sub("LotKTA222(\\S+)_", "", os.path.splitext(f)[0])+".tif")
				#=========================================#
				# use system time to create new file name #
				#=========================================#
				inputXML_tree.write(destDir+"\\WAFER01\\"+"MEASUREMENT_INNER_"+lotIDName+"_"+str(thisFilesTime.strftime('%m%d%y.%H%M%S.%f')[:-3])+".xml")
				copyfile(sourceDir+"\\LotKTA222_TIF\\"+os.path.splitext(f)[0]+".tif", destDir+"\\WAFER01\\"+"MEASUREMENT_INNER_"+lotIDName+"_"+str(thisFilesTime.strftime('%m%d%y.%H%M%S.%f')[:-3])+".tif")

			elif "WAFER02" in ProductElementWaferID.text:
				#Add in 7/30
				if not Path(destDir+"\\WAFER02").exists() :
					os.makedirs(destDir+"\\WAFER02")
				#inputXML_tree.write(destDir+"\\WAFER02\\"+lotIDName+"_"+re.sub("LotKTA222(\\S+)_", "", f))
				#copyfile(sourceDir+"\\LotKTA222_TIF\\"+os.path.splitext(f)[0]+".tif", destDir+"\\WAFER02\\"+lotIDName+"_"+re.sub("LotKTA222(\\S+)_", "", os.path.splitext(f)[0])+".tif")
				#=========================================#
				# use system time to create new file name #
				#=========================================#
				inputXML_tree.write(destDir+"\\WAFER02\\"+"MEASUREMENT_INNER_"+lotIDName+"_"+str(thisFilesTime.strftime('%m%d%y.%H%M%S.%f')[:-3])+".xml")
				copyfile(sourceDir+"\\LotKTA222_TIF\\"+os.path.splitext(f)[0]+".tif", destDir+"\\WAFER02\\"+"MEASUREMENT_INNER_"+lotIDName+"_"+str(thisFilesTime.strftime('%m%d%y.%H%M%S.%f')[:-3])+".tif")
			'''
			#===============#
			# End of Mode 3 #
			#===============#

			#========================#
			# End of files iteration #
			#========================#
			time.sleep(0)


	#======================================#
	#shutil.register_archive_format('7zip', py7zr.pack_7zarchive, description='7zip archive')
	#shutil.make_archive(destDir, '7zip', destDir)

	#========================================#
	# Mode to archive all files into 7z file #
	#========================================#
	archive = py7zr.SevenZipFile(destDir+'.7z', 'w')
	archive.writeall(destDir, 'lot'+str(serialNumber)+'_'+folderTimeStemp)
	archive.close()
	shutil.move(destDir+'.7z', destRootDir+"\\lot"+str(serialNumber)+"_"+folderTimeStemp+'.7z')
	#===================================#
	# End of archive files into 7z file #
	#===================================#



	genFilesFinishedTime = datetime.datetime.now()
	print("finished, at : "+genFilesFinishedTime.strftime("%H:%M:%S") + "  Total consumed time:"+str((genFilesFinishedTime-genFilesStartTime).seconds))

	#mimicFilesGenVirtualTime = mimicFilesGenVirtualTime+datetime.timedelta(seconds = 7*60)
	#mimicFilesGenVirtualTime = datetime.datetime.strptime('23:56:00:000000 07/31/2019', '%H:%M:%S:%f %m/%d/%Y') + datetime.timedelta(seconds = i*7*60)


	time.sleep(0)