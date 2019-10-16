# Project: Load Parcel to Temp
# Create Date: 03/13/2018
# Last Updated: 04/30/2018
# Create by: Robert Domiano
# Purpose: This script takes parcels as a polygon feature class, updates it with the TempParcels shema
#          and enters the creation date, subdivision name, WO number, and lot numbers.
# ArcGIS Version:   10.2
# Python Version:   2.7.5
# Input Variables: inputfc, myws, Lotnumber, subdivisionName, wonumber
# Output: fcUpdate, newFc


#-----------------------------------------------------------------------

#Import modules
import arcpy
import os
import sys
import datetime

# Sets ArcGIS parameter variables
# Workspace variable
myws = arcpy.env.workspace = arcpy.GetParameterAsText(0)
# Parcel Polygon Variable
inputfc = arcpy.GetParameterAsText(1)
# user input subdivision name (string)
subdivision = arcpy.GetParameterAsText(2)
# User input Maximo WO Number (string)
wonumber = arcpy.GetParameterAsText(3)
# Lot numbers from CAD file in point FC
Lotnumber = arcpy.GetParameterAsText(4)
#convert wonumber to an integer
# This is done as the wonumber field in the TempParcels layer schema is an integer
wonumber = int(wonumber)

#Set processing extent to union of inputs. This helps with certain append errors.
arcpy.env.overwriteOutput = True

#-----------------------------------------------------------------------
# Create a template feature class (FC) in the current workspace
# This section will create a new, empty FC with the same schema as TempParcels

# Define the template for the new FC as a variable
template = r'\\gisappser2\GIS_Production\Data\Temp_Parcels_LAC.gdb\TempParcels'

# Get the spatial reference
#  26796 is the code for NAD 1927 State Plane Missouri East FIPS 2401
#  The spatial reference was not pulling from the TempParcels FC so this is a work around
#spatialref = arcpy.SpatialReference(26796)

# Define a temporary name for the template.
TempName = 'AppendToTempParcels'

# If for whatever reason the script needs to be run multiple times due to errors
# then this will delete the template created so it can be re-created
if arcpy.Exists(TempName):
    arcpy.Delete_management(TempName)

# Create the new FC
    # This will be an empty FC with all the attributes from the template, TempParcels
templateNew = arcpy.CreateFeatureclass_management(myws, TempName, "POLYGON", template, "DISABLED", "DISABLED")

# Append the new parcel FC to the newly created template
# fcUpdate now contains the parcel lines and the proper schema
fcUpdate = arcpy.Append_management(inputfc, templateNew, "NO_TEST")

#-----------------------------------------------------------------------
# This next section is somewhat optional. It adds various data to the schema.
# While this doesn't seem necessary, it does make use of some of the schema fields that are usually empty.

# Set fields that will need to be updated by name. This is known since the schema does not change.
state = 'State'
country = 'Country'
date = datetime.datetime.today().date()
datefield = 'CreateDate'

# Create a list of all the field attributes that will be automatically updated without user input
auto = [state, country, datefield]

# Iterate through the new feature class to apply data
# First, create an update cursor
with arcpy.da.UpdateCursor(fcUpdate, auto) as cursor:
    # Next, iterate through each row inside the attributes from auto and input automatic data
    for row in cursor:
        row[0] = 'MO'
        row[1] = 'USA'
        row[2] = date
        cursor.updateRow(row)

# Clean up and delete cursor
del cursor

# Create a list of the field names. Field names are taken from the Schema in fcUpdate
userlist = ['SUBDIVNAME', 'MainWONo']
# Open an update cursor
with arcpy.da.UpdateCursor(fcUpdate, userlist) as cursor:
    # iterate through each row for each field in userlist and then update as follows
    for row in cursor:
        # Each field in the first row, the subdivision field, will have the user input subdivision
        row[0] = subdivision
        # Each field in the second row, the wo number field, will have the user input wo number
        row[1] = wonumber
        # update the row
        cursor.updateRow(row)
# delete the cursor
del cursor

#-----------------------------------------------------------------------

# This next section will iterate through a point file containing lot numbers and input those lot numbers
# into the house number field in our new feature class, fcUpdate

# Make a layer from previously created new feature class
arcpy.MakeFeatureLayer_management(fcUpdate, "Parcels_Temp")

# Establish Field Mapping
# NOTE: This field mapping section is leftover code. I could not get the field mappings to map properly
#  and instead used delete fields as mentioned below. 
fieldMappings = arcpy.FieldMappings()
# Add field map objects for lot numbers (TEXTSTRING) and expected output field (HouseNumber)
fieldMappings.addTable(Lotnumber)
fieldMappings.addTable(fcUpdate)

# Create a list of only fields we want to keep
TemplateList = arcpy.ListFields(fcUpdate)
keeper = ["TEXTSTRING"]
for field in TemplateList:
    keeper.append(field)

# Remove output fields you don't want
# Note: this section doesn't seem to work, which is why Delete Fields is used below.
# If the code can be fixed, it may prove faster.
# for field1 in fieldMappings.fields:
#    if field.name not in keeper:
#        fieldMappings.removeFieldMap(fieldMappings.findFieldMapIndex(field.name))

#fieldmap = fielddMappings.getFieldMap(fieldMappings.findFieldMapIndex("TEXTSTRINGS"))
#fieldmap.addInputField(fcUpdate, "HouseNumber")
#fieldMappings.replaceFieldMap(fieldMappings.findFieldMapIndex("TEXTSTRINGS"),fieldmap)

#Create a name for the spatial join
Joinname = TempName + "_spatial"
# Perform the spatial join
# the field mappings do not seem to work and have been removed. Remnants of the code are left above
# in case it can be improved upon in the future.
newFc = arcpy.SpatialJoin_analysis(fcUpdate, Lotnumber, Joinname, "JOIN_ONE_TO_ONE", "KEEP_ALL")


# Since field mapping didn't work, Calculate Fields is used to add and remove needed fields
arcpy.CalculateField_management(newFc, "HouseNumber",'!TEXTSTRING!', "PYTHON")
arcpy.DeleteField_management(newFc, ["Join_Count", "TARGET_FID", "TEXTSTRING", "TEXT_SIZE", "TEXT_ANGLE"])

#Finally, append the final feature class to the TempParcels layer
# NOTE: This will only work for areas within the boundaries of the TempParcels layer.
arcpy.Append_management(newFc, template, "TEST")

