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
# Problem 1 (20 Points)
#
# This function reads all the feature classes in a workspace, and
# prints the number of feature classes by each shape type. For example,
# polygon: 3, polyline: 2, point: 4

###################################################################### 
import arcpy

def printNumberOfFeatureClassesByShapeType(workspace):
    arcpy.env.workspace = workspace
    
    feature_classes = arcpy.ListFeatureClasses()
    
    shape_type_count = {}
    
    for fc in feature_classes:
        desc = arcpy.Describe(fc)
        shape_type = desc.shapeType

        if shape_type not in shape_type_count:
            shape_type_count[shape_type] = 0
        
        shape_type_count[shape_type] += 1
        
    for shape_type, count in shape_type_count.items():
        print(f"{shape_type}: {count}")

###################################################################### 
# Problem 2 (20 Points)
#
# This function reads all the feature classes in a workspace, and
# prints the coordinate systems for each file

###################################################################### 
def printCoordinateSystems(workspace):
    arcpy.env.workspace = workspace
    
    feature_classes = arcpy.ListFeatureClasses()
    
    for fc in feature_classes:
        spatial_ref = arcpy.Describe(fc).spatialReference
        
        if spatial_ref.name == "Unknown":
            print("{} has an unknown spatial reference".format(fc))
        else:
            print("{} : {}".format(fc, spatial_ref.name))

###################################################################### 
# Problem 3 (60 Points)
#
# Given two feature classes in a workspace:
# check whether their coordinate systems are
# the same, and if not convert the projection of one of them to the other.
# If one of them has a geographic coordinate system (GCS) and the other has
# a projected coordinate system (PCS), then convert the GCS to PCS. 

###################################################################### 
def autoConvertProjections(fc1, fc2, workspace):
    arcpy.env.workspace = workspace
    
    coord_sys_fc1 = arcpy.Describe(fc1).spatialReference
    coord_sys_fc2 = arcpy.Describe(fc2).spatialReference
    
    if coord_sys_fc1.name != coord_sys_fc2.name:
    
        if coord_sys_fc1.type == 'Geographic' and coord_sys_fc2.type == 'Projected':
            arcpy.Project_management(fc1, fc1 + "_projected", coord_sys_fc2)
            print(f"Coordinate system of {fc1} converted to match {fc2}.")
            
        elif coord_sys_fc1.type == 'Projected' and coord_sys_fc2.type == 'Geographic':
            arcpy.Project_management(fc2, fc2 + "_projected", coord_sys_fc1)
            print(f"Coordinate system of {fc2} converted to match {fc1}.")
            
        else:
            arcpy.Project_management(fc2, fc2 + "_new_projection", coord_sys_fc1)
            print(f"Coordinate system of {fc2} converted to match {fc1}.")
            
    elif coord_sys_fc1.name == coord_sys_fc2.name:
        print("Coordinate systems are already the same.")
        
    else:
        print("Error, one or both coordinate systems are unknown or undefined.")
        
    pass

######################################################################
# MAKE NO CHANGES BEYOND THIS POINT.
######################################################################
if __name__ == '__main__' and hawkid()[1] == "hawkid":
    print('### Error: YOU MUST provide your hawkid in the hawkid() function.')
