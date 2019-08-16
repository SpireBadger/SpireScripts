# -*- coding: utf-8 -*-
"""
Created on Fri Aug  2 12:07:28 2019

@author: 40004
"""

# Project: Create Service Folder
# Create Date: 08/02/2019
# Last Updated: 08/13/2019
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
    print("Map Document saved to " + svcDir)
except:
    print("Error")
    