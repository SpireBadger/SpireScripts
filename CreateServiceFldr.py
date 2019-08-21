# Project: Create Service Folder
# Create Date: 08/02/2019
# Last Updated: 08/16/2019
# Create by: Robert Domiano
# Purpose: This script creates a folder for new service installs
# ArcGIS Version:   10.2
# Python Version:   2.7.5
# Input Variables: wo, streeet, address, path
# Output: newmxd, svcDir

# Import system modules
import os
import arcpy

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
    print("Directory ", fldrName, " Created ")
    os.mkdir(svcDir + "/" + "CAD")
    print("Sub-Directory for CAD SHP Created.")
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
try:
    mxd = arcpy.mapping.MapDocument(r"\\gisappser2\Engineering_GIS\Domiano_Robert\ServiceInstall\svcTemplate.mxd")
    newmxd = os.path.join(svcDir, fldrName + ".mxd")
    mxd.saveACopy(newmxd)
    print("Map Document saved to {0} as {1}".format(svcDir, newmxd))
except:
    print("Error")
    
# Locate all text elements
#print(newmxdPath)
newmxd2 = arcpy.mapping.MapDocument(newmxd)
totalAddress = address + " " + street
for elm in arcpy.mapping.ListLayoutElements(newmxd2, "TEXT_ELEMENT"):
    if elm.name == "Address":
        elm.text = totalAddress
        print("Address has been changed to {0}.".format(totalAddress))
    if elm.name == "WO":
        elm.text = str(wo)
        print("Work order has been changed to {0}.".format(wo))
        
arcpy.RefreshActiveView()
newmxd2.save()
del elm, newmxd2  

    