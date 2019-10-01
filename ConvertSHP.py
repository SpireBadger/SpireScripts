# Project: Convert Shapefiles
# Create Date: 08/16/2019
# Last Updated: 08/16/2019
# Create by: Robert Domiano
# Purpose: Convert all shapefiles in a folder to a target geodatabase
# ArcGIS Version:   10.2
# Python Version:   2.7.5
# Input Variables: currentDir, outputWS
# Output: 

# Import modules
import arcpy

# Enter workspace directory
currentDir = raw_input("Copy Shapefile Folder Path here: ")
outputWS = raw_input("Copy GDB path here: ")

# Make directories readable
revDir = "r'" + currentDir + "'"
revOutput = "r'" + outputWS + "'"

# Set environment workspace
arcpy.env.workspace = currentDir
arcpy.env.overwriteOutput = True

# create list of shapefiles
shpList = arcpy.ListFeatureClasses()

# Iterate through shapefiles and export them to geodatabase
for shp in shpList:
    print shp
    arcpy.FeatureClassToGeodatabase_conversion(shp, outputWS)
    
del shp