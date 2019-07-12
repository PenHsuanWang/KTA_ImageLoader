import xml.etree.ElementTree as ET
import math
import os
import time
import sys
import re
import datetime


from shutil import copyfile

sourceDir = "C:\\Work_Willy\\ImageLoader_test\\Image_LotKTA222_Original"
destRootDir = "E:\\ImageLoader_test\\test_nestForder"
#destRootDir = "Z:\\Public\\KTA_ImageLoaderTest"
inFiles = os.listdir(sourceDir)

mimicFilesGenStartTime = datetime.datetime.strptime('00:00:00:000000 07/01/2018', '%H:%M:%S:%f %m/%d/%Y')

for i in range (12,15):

	serialNumber = "%05d" %i
	productName = "PROD"+str(serialNumber)
	recipeName = "RECIPE"+str(serialNumber)
	lotIDName  = "LOT"+str(serialNumber)

	destDir = destRootDir+"\\"+productName+"\\"+recipeName+"\\"+lotIDName
	os.makedirs(destDir+"\\WAFER01")
	os.makedirs(destDir+"\\WAFER02")

	
	print("Folder "+destDir+" created")

	genFilesStartTime = datetime.datetime.now()
	print("Start to generate files at: "+genFilesStartTime.strftime("%H:%M:%S"))

	copyfile("C:\\Work_Willy\\ImageLoader_test\\ImageLoaderTesting_KData\\"+lotIDName+".kdata", destDir+"\\WAFER01\\"+lotIDName+".kdata")
	copyfile("C:\\Work_Willy\\ImageLoader_test\\ImageLoaderTesting_KData\\"+lotIDName+".kdata", destDir+"\\WAFER02\\"+lotIDName+".kdata")

	print(str(len(inFiles))+" files found")
	fileCount = 0

	# To fixed the time in XML
	timeShiftedValue = -3600 + (300*(i-1))

	#if i%3 == 1 :
	#	timeShiftedValue = -300 # shifted -5 mins
	#elif i%3 == 2 :
	#	timeShiftedValue = 0 # shifted -5 mins
	#elif i%3 == 0 :
	#	timeShiftedValue = 300 # shifted -5 mins

	for f in inFiles:
		
		fileCount+=1

		k = math.floor((fileCount/(len(inFiles)))*100) + 1      
		progressBar = '>'*math.floor((fileCount/(len(inFiles)))*100)+' '*(100-k)
		sys.stdout.write('\r'+progressBar+'[%s%%]'%(math.floor((fileCount/(len(inFiles)))*100))+'(%s'%(fileCount)+'/%s'%(len(inFiles))+')' )
		sys.stdout.flush()

		if os.path.splitext(f)[1] == '.xml' :

			
			currentTime = datetime.datetime.now()
			outputDate = currentTime - datetime.timedelta(days = 365)

			inputXML_tree = ET.parse(sourceDir+"\\"+f)
			inputXML_tree.getroot()

			ProductElementLotID = inputXML_tree.find("LotId")
			ProductElementLotID.text = lotIDName

			ProductElementRecipe = inputXML_tree.find("RecipeName")
			ProductElementRecipe.text = recipeName

			ProductElementTime = inputXML_tree.find("DateAndTime")
			#print(ProductElementTime.text)
			measureDatetime = datetime.datetime.strptime(ProductElementTime.text, '%H:%M:%S:%f %m/%d/%Y')
			#print(timeShiftedValue)
			shiftedMeasureDatetime = measureDatetime+datetime.timedelta(seconds = timeShiftedValue)
			ProductElementTime.text = str(shiftedMeasureDatetime.strftime('%H:%M:%S:%f')[:-3])+' '+str(shiftedMeasureDatetime.strftime('%m/%d/%Y'))
			#print(ProductElementTime.text)
			

			ProductElementWaferID = inputXML_tree.find("WaferId")
			
			if "WAFER01" in ProductElementWaferID.text:
				#inputXML_tree.write(destDir+"\\WAFER01\\"+lotIDName+"_"+re.sub("LotKTA222(\\S+)_", "", f))
				#copyfile(sourceDir+"\\LotKTA222_TIF\\"+os.path.splitext(f)[0]+".tif", destDir+"\\WAFER01\\"+lotIDName+"_"+re.sub("LotKTA222(\\S+)_", "", os.path.splitext(f)[0])+".tif")
				#=========================================#
				# use system time to create new file name #
				#=========================================#
				inputXML_tree.write(destDir+"\\WAFER01\\"+"MEASUREMENT_INNER_"+lotIDName+"_"+str(outputDate.strftime('%m%d%y.%H%M%S.%f')[:-3])+".xml")
				copyfile(sourceDir+"\\LotKTA222_TIF\\"+os.path.splitext(f)[0]+".tif", destDir+"\\WAFER01\\"+"MEASUREMENT_INNER_"+lotIDName+"_"+str(outputDate.strftime('%m%d%y.%H%M%S.%f')[:-3])+".tif")

			elif "WAFER02" in ProductElementWaferID.text:
				#inputXML_tree.write(destDir+"\\WAFER02\\"+lotIDName+"_"+re.sub("LotKTA222(\\S+)_", "", f))
				#copyfile(sourceDir+"\\LotKTA222_TIF\\"+os.path.splitext(f)[0]+".tif", destDir+"\\WAFER02\\"+lotIDName+"_"+re.sub("LotKTA222(\\S+)_", "", os.path.splitext(f)[0])+".tif")
				#=========================================#
				# use system time to create new file name #
				#=========================================#
				inputXML_tree.write(destDir+"\\WAFER02\\"+"MEASUREMENT_INNER_"+lotIDName+"_"+str(outputDate.strftime('%m%d%y.%H%M%S.%f')[:-3])+".xml")
				copyfile(sourceDir+"\\LotKTA222_TIF\\"+os.path.splitext(f)[0]+".tif", destDir+"\\WAFER02\\"+"MEASUREMENT_INNER_"+lotIDName+"_"+str(outputDate.strftime('%m%d%y.%H%M%S.%f')[:-3])+".tif")


			time.sleep(0.1)

	genFilesFinishedTime = datetime.datetime.now()
	print("finished, at : "+genFilesFinishedTime.strftime("%H:%M:%S") + "  Total consumed time:"+str((genFilesFinishedTime-genFilesStartTime).seconds))

	time.sleep(120)