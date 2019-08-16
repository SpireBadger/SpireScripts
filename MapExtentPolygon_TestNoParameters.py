# Project: Create Map Extent Polygon
# Create Date: 08/03/2018
# Last Updated: 08/06/2018
# Create by: Robert Domiano
# Purpose: This script will take the current map extent to create a polygon in
#           the Map Grid feature class.
#           It then fills in necessary data to use data driven pages.
#        
# ArcGIS Version:   10.2
# Python Version:   2.7.5
# Input Variables: mapGrid, mxd, dataframe, frameExtent, XMAX, XMIN, YMAX, YMIN
#                  point1, point2, point3, point4, array
# Output: polygon

# Import Modules
import arcpy
from arcpy import env
from arcpy import mapping

# Establish current workspace
#env.workspace = arcpy.GetParameterAsText(0)

# Set Map Grid Variable
#mapGrid = arcpy.GetParameterAsText(0)

# Set current map document
mxd = mapping.MapDocument("CURRENT")


#------------------------------
# No parameters are needed to be set while this portion of the script functions
df = arcpy.mapping.ListDataFrames(mxd)[0]
for lyr in arcpy.mapping.ListLayers(mxd, "", df):
    if lyr.name == "MapbookGrid":
        mapGrid = lyr
#----------------------------



# Set the current data frame as a variable
dataframe = mapping.ListDataFrames(mxd, "*")[0]

# Gets the extent of the current data frame
frameExtent = dataframe.extent

# Get the current scale
scale = dataframe.scale

# Store the coordinates of the current extent
XMAX = frameExtent.XMax
XMIN = frameExtent.XMin
YMAX = frameExtent.YMax
YMIN = frameExtent.YMin

# Create points at each of the extent's corners
point1 = arcpy.Point(XMIN, YMIN)
point2 = arcpy.Point(XMIN, YMAX)
point3 = arcpy.Point(XMAX, YMAX)
point4 = arcpy.Point(XMAX, YMIN)

# Put all of these points into an array
array = arcpy.Array()
array.add(point1)
array.add(point2)
array.add(point3)
array.add(point4)

# Create a polygon from the array
polygon = arcpy.Polygon(array)

# Copy the polygon to an existing feature class
# Note: This should be a Temporary polygon as it will replace
# any existing features.
#arcpy.CopyFeatures_management(polygon, mapGrid)

# Append new polygon to the Map grid polygon
arcpy.Append_management(polygon, mapGrid, "NO_TEST")


# This second section updates the attribute table of MapbookGrid for use with
# data driven pages.

# Updates the scale field
with arcpy.da.UpdateCursor(mapGrid, "Scale") as cursor:
    for row in cursor:
        row[0] = scale
        cursor.updateRow(row)
# Clean up data
del cursor, row

# Obtains a count of the current number of rows in mapbookgrid and
# outputs it as an integer
count = int(arcpy.GetCount_management(mapGrid).getOutput(0))


# Add count to the MapGrid variable
# as the total number of pages.
with arcpy.da.UpdateCursor(mapGrid, "SeqId") as cursor:
    for row in cursor:
        row[0] = count + 1
        cursor.updateRow(row)

# Clean up data
del cursor, row

# Creates a list of three more fields to be updated
list = ['PageNumber', 'Previous', 'Next']
# Set page count to 2 for modifying Next and Previous pages
page = 2

# Add the current page number
with arcpy.da.UpdateCursor(mapGrid, list) as cursor:
    for row in cursor:
        row[0] = page
        cursor.updateRow(row)
        page += 1
        # Clean up data
del cursor, row

# Add the next page number
with arcpy.da.UpdateCursor(mapGrid, list) as cursor:
    for row in cursor:
        if row[0] == 2:
            row[1] = None
            cursor.updateRow(row)
        else:
            row[1] = row[0]-1
            cursor.updateRow(row)
# Clean up data
del cursor, row

# Add the previous page number
with arcpy.da.UpdateCursor(mapGrid, list) as cursor:
    for row in cursor:
        if row[0] == (count+1):
            row[2] = None
            cursor.updateRow(row)
        else:
            row[2] = row[0]+1
            cursor.updateRow(row)

# Clean up data
del cursor, row

# Refreshes the view so new polygons show up
arcpy.RefreshActiveView()


