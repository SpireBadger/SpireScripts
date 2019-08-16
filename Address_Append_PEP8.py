# Project: Load Parcel to Temp
# Create Date: 03/13/2018
# Last Updated: 08/16/2019
# Create by: Robert Domiano
# Purpose: This script takes parcels as a polygon feature class, updates it
#          with the TempParcels schema
#          and enters the following variables:
#          creation date, subdivision name, WO number, and lot numbers.
# ArcGIS Version:   10.2
# Python Version:   2.7.5
# Input Variables: inputfc, myws, Lotnumber, subdivisionName, wonumber, Address
# Output: fcUpdate, newFc, newFc2


# -----------------------------------------------------------------------

# Import modules
import arcpy
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
# Add Address number
Address = arcpy.GetParameterAsText(5)
# convert wonumber to an integer
wonumber = int(wonumber)


# Set processing extent to union of inputs.
# This helps with certain append errors.
arcpy.env.overwriteOutput = True

# -----------------------------------------------------------------------
# Create a template feature class (FC) in the current workspace
# This section will create a new, empty FC with the same schema as TempParcels

# Define the template for the new FC as a variable
template = r'\\gisappser2\GIS_Production\Data\Temp_Parcels_LAC.gdb\TempParcels'


# Define a temporary name for the template.
TempName = 'AppendToTempParcels'

# If for whatever reason the script needs to be run multiple times
# due to errors then this will delete the template created
# so it can be re-created
if arcpy.Exists(TempName):
    arcpy.Delete_management(TempName)

# Create the new FC
# This will be an empty FC with all the
# attributes from the template, TempParcels
templateNew = arcpy.CreateFeatureclass_management(myws, TempName, "POLYGON",\
                                                  template, "DISABLED",\
                                                  "DISABLED")

# Append the new parcel FC to the newly created template
# fcUpdate now contains the parcel lines and the proper schema
fcUpdate = arcpy.Append_management(inputfc, templateNew, "NO_TEST")

# -----------------------------------------------------------------------
# This next section is somewhat optional. It adds various data to the schema.
# While this doesn't seem necessary, it does make use
# of some of the schema fields that are usually empty.

# Set fields that will need to be updated by name.
# This is known since the schema does not change.
state = 'State'
country = 'Country'
date = datetime.datetime.today().date()
datefield = 'CreateDate'

# Create a list of all the field attributes that will
# be automatically updated without user input
auto = [state, country, datefield]

# Iterate through the new feature class to apply data
# First, create an update cursor
with arcpy.da.UpdateCursor(fcUpdate, auto) as cursor:
    # Next, iterate through each row inside the attributes
    # from auto and input automatic data
    for row in cursor:
        row[0] = 'MO'
        row[1] = 'USA'
        row[2] = date
        cursor.updateRow(row)

# Clean up and delete cursor
del cursor

# Create a list of the field names.
# Field names are taken from the Schema in fcUpdate
userlist = ['SUBDIVNAME', 'MainWONo']
# Open an update cursor
with arcpy.da.UpdateCursor(fcUpdate, userlist) as cursor:
    # iterate through each row for each field in userlist and then update
    for row in cursor:
        # Each field in the first row,
        # the subdivision field, will have the user input subdivision
        row[0] = subdivision
        # Each field in the second row,
        # the wo number field, will have the user input wo number
        row[1] = wonumber
        # update the row
        cursor.updateRow(row)
# delete the cursor
del cursor

# -----------------------------------------------------------------------

# Iterate through a point file containing lot numbers and input those
# lot numbers into the lot number field in our new feature class, fcUpdate

# Make a layer from previously created new feature class
arcpy.MakeFeatureLayer_management(fcUpdate, "Parcels_Temp")


# Create a name for the spatial join
Joinname = TempName + "_spatial"
# Perform the spatial join
newFc = arcpy.SpatialJoin_analysis(fcUpdate, Lotnumber, Joinname, \
                                   "JOIN_ONE_TO_ONE", "KEEP_ALL")


# Calculate fields, remove unwanted fields
arcpy.CalculateField_management(newFc, "SiteLot_No", '!TEXTSTRING!', "PYTHON")
arcpy.DeleteField_management(newFc, ["Join_Count", "TARGET_FID", "TEXTSTRING",\
                                     "TEXT_SIZE", "TEXT_ANGLE"])

# Create a name for the address relevant spatial join
Joinname2 = TempName + "_spatial2"

# Unlike Lot Numbers, Addresses are not always stored in the TEXTSTRING field.
# As a result, iterate through whatever point FC to look for an alternative
# in place of TEXTSTRING.

addressFields = arcpy.ListFields(Address)
for field in addressFields:
    if field.name.lower() == 'number':
        arcpy.AlterField_management(Address, field.name, 'TEXTSTRING')
del field

# Perform Spatial Join for Address Numbers
newFc2 = arcpy.SpatialJoin_analysis(newFc, Address, Joinname2,\
                                    "JOIN_ONE_TO_ONE", "KEEP_ALL")

# Delete leftover fields
arcpy.CalculateField_management(newFc2, "HouseNumber", '!TEXTSTRING!',\
                                "PYTHON")
arcpy.DeleteField_management(newFc2, ["Join_Count", \
                                      "TARGET_FID", "TEXTSTRING", \
                                      "TEXT_SIZE", "TEXT_ANGLE"])

# Finally, append the final feature class to the TempParcels layer
# This will only work for areas within the boundaries of the TempParcels layer.
arcpy.Append_management(newFc2, template, "TEST")

arcpy.RefreshActiveView()
