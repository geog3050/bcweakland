###################################################################### 
# Edit the following function definition, replacing the words
# 'name' with your name and 'hawkid' with your hawkid.
# 
# Note: Your hawkid is the login name you use to access ICON, and not
# your firsname-lastname@uiowa.edu email address.
# 
# def hawkid():
#     return(["Caglar Koylu", "ckoylu"])
###################################################################### 
def hawkid():
    return(["Ben Weakland", "bcweakland"])

###################################################################### 
# Problem 1: 20 Points
#
# Given a csv file import it into the database passed as in the second parameter
# Each parameter is described below:

# csvFile: The absolute path of the file should be included (e.g., C:/users/ckoylu/test.csv)
# geodatabase: The workspace geodatabase
###################################################################### 
def importCSVIntoGeodatabase(csvFile, geodatabase):
    import arcpy
    output_tbl = "my_table"
    arcpy.CreateTable_management(geodatabase, output_tbl)
    arcpy.TableToTable_conversion(csvFile, geodatabase, output_tbl)

##################################################################################################### 
# Problem 2: 80 Points Total
#
# Given a csv table with point coordinates, this function should create an interpolated
# raster surface, clip it by a polygon shapefile boundary, and generate an isarithmic map

# You can organize your code using multiple functions. For example,
# you can first do the interpolation, then clip then equal interval classification
# to generate an isarithmic map

# Each parameter is described below:

# inTable: The name of the table that contain point observations for interpolation       
# valueField: The name of the field to be used in interpolation
# xField: The field that contains the longitude values
# yField: The field that contains the latitude values
# inClipFc: The input feature class for clipping the interpolated raster
# workspace: The geodatabase workspace

# Below are suggested steps for your program. More code may be needed for exception handling
#    and checking the accuracy of the input values.

# 1- Do not hardcode any parameters or filenames in your code.
#    Name your parameters and output files based on inputs. For example,
#    interpolated raster can be named after the field value field name 
# 2- You can assume the input table should have the coordinates in latitude and longitude (WGS84)
# 3- Generate an input feature later using inTable
# 4- Convert the projection of the input feature layer
#    to match the coordinate system of the clip feature class. Do not clip the features yet.
# 5- Check and enable the spatial analyst extension for kriging
# 6- Use KrigingModelOrdinary function and interpolate the projected feature class
#    that was created from the point feature layer.
# 7- Clip the interpolated kriging raster, and delete the original kriging result
#    after successful clipping. 
#################################################################################################################### 
def krigingFromPointCSV(inTable, valueField, xField, yField, inClipFc, workspace = "assignment3.gdb"):
    import arcpy
    from arcpy.sa import *
    try:
        # Set the workspace
        arcpy.env.workspace = workspace

        # Generate an input feature layer using inTable
        input_feature = arcpy.management.MakeXYEventLayer(inTable, xField, yField, "input_feature_lyr")

        # Convert the projection of the input feature layer to match the clip feature class
        arcpy.management.Project(input_feature, "input_feature_projected", inClipFc.spatialReference)

        # Check and enable the spatial analyst extension for kriging
        if arcpy.CheckExtension("Spatial") == "Available":
            arcpy.CheckOutExtension("Spatial")
        else:
            raise arcpy.ExecuteError("Spatial Analyst Extension is not available.")

        # Interpolate using KrigingModelOrdinary
        out_kriging = Kriging("input_feature_projected", valueField, KrigingModelOrdinary())

        # Clip the interpolated raster
        out_clipped = arcpy.management.Clip(out_kriging, "", "out_clipped", inClipFc)

        # Generate isarithmic map using equal interval classification
        out_raster_classified = arcpy.sa.Slice(out_clipped, 5, "EQUAL_INTERVAL")

        # Delete the original kriging result
        arcpy.management.Delete(out_kriging)

        return out_raster_classified

    except arcpy.ExecuteError:
        arcpy.AddError(arcpy.GetMessages(2))
        return None

######################################################################
# MAKE NO CHANGES BEYOND THIS POINT.
######################################################################
if __name__ == '__main__' and hawkid()[1] == "hawkid":
    print('### Error: YOU MUST provide your hawkid in the hawkid() function.')
