# Project: Create Service Folder
# Create Date: 08/02/2019
# Last Updated: 08/21/2019
# Create by: Robert Domiano
# Purpose: This script creates a folder for new service installs
# ArcGIS Version:   10.2
# Python Version:   2.7.5
# Input Variables: wo, streeet, address, path
# Output: newmxd, svcDir, mxd

# Import system modules
import os
import arcpy

# Determine which template to use
while True:
    tpe = raw_input("Commercial or Residential? (C/R): ")
    tpe = tpe.lower()
    if tpe == "r":
        mxd = arcpy.mapping.MapDocument(r"\\gisappser2\Engineering_GIS\Domiano_Robert\ServiceInstall\svcTemplate.mxd")
        print("Using the Residential Template.")
        break
    if tpe == "c":
        mxd = arcpy.mapping.MapDocument(r"\\gisappser2\Engineering_GIS\Domiano_Robert\ServiceInstall\svcTemplate_Commercial.mxd")
        print("Using the Commercial Template.")
        break
    else:
        print("Invalid input. Please enter C for Commercial or R for \
              Residential.")
        
# Ask user for Wo information        
wo = raw_input("WO Number: ")
street = raw_input("Street: ")
address = raw_input("Address: ")


# Set path for new service folder
path = r'\\gisappser2\Engineering_GIS\Domiano_Robert\Services'

# Create field name for GDB, Folder, and new MXD
fldrName = str(street + "_" + address + "_" + wo)


# Create the service folder with a sub-folder for CAD
# Try/Excet used for test purposes
try:
    svcDir = path + "/" + fldrName
    os.mkdir(svcDir)
    # print("Directory ", fldrName, " Created ")
    os.mkdir(svcDir + "/" + "CAD")
    # print("Sub-Directory for CAD SHP Created.")
# Except if folder already exists
except IOError:
    print("Directory already exists.")
    
# Create blank geodatabase [for future CAD files]    
try:
    arcpy.CreateFileGDB_management(svcDir, fldrName)
    print("Geodatabase successfully created.")
    
except:
    print("Geodatabase Unable to be created.")
    
# Copy the service MXD to create a new, blank service install mxd.
# Determine which template to use
    
try:
    newmxd = os.path.join(svcDir, fldrName + ".mxd")
    mxd.saveACopy(newmxd)
    # print("Map Document saved to {0} as {1}".format(svcDir, newmxd))
except:
    print("Error")
    
# Locate all text elements
#print(newmxdPath)
newmxd2 = arcpy.mapping.MapDocument(newmxd)
totalAddress = address + " " + street
# Loop through the layout elements, then replace with the user input info.
for elm in arcpy.mapping.ListLayoutElements(newmxd2, "TEXT_ELEMENT"):
    if elm.name == "Address":
        elm.text = totalAddress
        print("Address has been changed to {0}.".format(totalAddress))
    if elm.name == "WO":
        elm.text = str(wo)
        print("Work order has been changed to {0}.".format(wo))

#Store changes       
arcpy.RefreshActiveView()
newmxd2.save()
# clean up variables
del elm, newmxd2, path, newmxd, svcDir
del street, totalAddress, tpe, wo, address, fldrName

    