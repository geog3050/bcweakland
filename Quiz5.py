import arcpy
folder = 'C:/Users/bcweakland/Downloads/airports'
arcpy.env.workspace = folder
fc = 'airports'
fields = ['FEATURE', 'TOT_ENP']
arcpy.management.AddField(fc, 'buffer', 'LONG')
fields.append('buffer')
with arcpy.da.UpdateCursor(fc, fields) as cursor:
    for row in cursor:
        if row[0] == 'Airport' and row[1] > 10000:
            row[2] = 15000
        elif row[0] == 'Airport' and row[1] <= 10000:
            row[2] = 10000
        elif row[0] == 'Seaplane Base' and row[1] > 1000:
            row[2] = 7500
