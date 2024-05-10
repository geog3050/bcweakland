import arcpy

# Check workspace and ensure csv table is stored in the same folder
print(arcpy.env.workspace)

# Convert the coordinate data in the csv file into a table within my geodatabase
arcpy.conversion.TableToTable("tortoise.csv", "S:/2024_Spring/GEOG_3050/STUDENT/bcweakland/FinalProject/FinalProject.gdb", "tortoise")

# Define input table and output feature class names
input_table = "tortoise"
tortoisefc = "tortoise_path"

# Create an empty point fc
arcpy.management.CreateFeatureclass(arcpy.env.workspace, tortoisefc, "POINT")

# Add X and Y fields to the fc
arcpy.management.AddField(tortoisefc, "X", "DOUBLE")
arcpy.management.AddField(tortoisefc, "Y", "DOUBLE")

# Create insert cursor for the shapefile
cursor = arcpy.da.InsertCursor(tortoisefc, ["SHAPE@", "X", "Y"])

# Iterate over rows in the input table and create points
with arcpy.da.SearchCursor(input_table, ["X", "Y"]) as search_cursor:
    for row in search_cursor:
        x = row[0]
        y = row[1]
        point = arcpy.Point(x, y)
        cursor.insertRow([point, x, y])

# Clean up
del cursor

# Define the projection of the layer as UM40, WKID is 32640
arcpy.management.DefineProjection(tortoisefc, arcpy.SpatialReference(32640))

# Add change in x and y coordinates to shapefile
arcpy.management.AddField(tortoisefc, "Delta_X", "DOUBLE")
arcpy.management.AddField(tortoisefc, "Delta_Y", "DOUBLE")

#Initialize variables
totaldx = 0
totaldy = 0
count = 0

# Calculate change in coordinates
with arcpy.da.UpdateCursor(tortoisefc, ['X', 'Y', 'Delta_X', 'Delta_Y']) as cursor:
    previous_x, previous_y = None, None
    for row in cursor:
        X, Y = row[0], row[1]
        if previous_x is not None or previous_y is not None:
            delta_x = X - previous_x
            delta_y = Y - previous_y
            row[2] = delta_x
            row[3] = delta_y
            cursor.updateRow(row)
            
            # Record values to calculate average 
            totaldx += abs(delta_x)
            totaldy += abs(delta_y)
            count += 1
        
        previous_x, previous_y = X, Y

#calculate average change in coordinates
avg = ((totaldx/count)+(totaldx/count))/2

# Behavior classification: Define rules based on change in x and y coordinates
def classify_behavior(delta_x, delta_y):
    if delta_x or delta_y != None:
        displacement = (abs(delta_x)+abs(delta_y))/2
        if displacement < 0.05*avg:
            return 'Resting'
        elif displacement < 0.2*avg:
            return 'Foraging'
        else:
            return 'Traveling'
    else:
        return None

# Create a new field to store behavior classifications
arcpy.management.AddField(tortoisefc, 'Behavior', 'TEXT')

# Calculate behavior classifications based on change in x and y coordinates
with arcpy.da.UpdateCursor(tortoisefc, ['Delta_X', 'Delta_Y', 'Behavior']) as cursor:
    for row in cursor:
        delta_x, delta_y = row[0], row[1]
        behavior = classify_behavior(delta_x, delta_y)
        row[2] = behavior
        cursor.updateRow(row)

# Aggregate points
arcpy.cartography.AggregatePoints(tortoisefc, "points_of_interest", "0.75 meters")

# Wanted to use DBC but could not get code to run. It would go for 15+ minutes without giving output
# arcpy.stats.DensityBasedClustering(tortoisefc, "output_cluster_fc", "HDBSCAN", 50)


