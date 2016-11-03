#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Charles.Ferguson
#
# Created:     02/11/2016
# Copyright:   (c) Charles.Ferguson 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------



class ForceExit(Exception):
    pass

def PrintMsg(msg, severity=0):
    # Adds tool message to the geoprocessor
    #
    #Split the message on \n first, so that if it's multiple lines, a GPMessage will be added for each line
    try:
        for string in msg.split('\n'):
            #Add a geoprocessing message (in case this is run as a tool)
            if severity == 0:
                arcpy.AddMessage(string)

            elif severity == 1:
                arcpy.AddWarning(string)

            elif severity == 2:
                arcpy.AddError(" \n" + string)

    except:
        pass



def errorMsg():
    try:
        tb = sys.exc_info()[2]
        tbinfo = traceback.format_tb(tb)[0]
        theMsg = tbinfo + " \n" + str(sys.exc_type)+ ": " + str(sys.exc_value)
        PrintMsg(theMsg, 2)

    except:
        PrintMsg("Unhandled error in errorMsg method", 2)
        pass

import sys, os, arcpy, random, traceback

arcpy.env.addOutputsToMap = True

try:

    #delete the layer if it exists
    if arcpy.Exists("random_sample"):
        arcpy.management.Delete("random_sample")

    inFeats = arcpy.GetParameterAsText(0)
    sSize = arcpy.GetParameterAsText(1)

    desc = arcpy.Describe(inFeats)
    #cPath = desc.catalogPath

    #get the oid field name to use in cursor
    oidFld = desc.OIDFieldName

    #create a container to grab the list of oids
    oidList = list()


    #oidStr = ''

    #grab all the oids to the container
    with arcpy.da.SearchCursor(inFeats, oidFld) as rows:
        for row in rows:
            #oidStr = oidStr + "'" + str(row[0]) + ",'"
            oidList.append(row[0])



    #oidStr = oidStr[:-1]

    #get the random selection
    theSample = random.sample(oidList, int(sSize))

    #make a where_clause with the list
    wc = '"' + oidFld + '" IN' + str(theSample).replace("[", "(").replace("]", ")")


    #add it to the map document
    mxd = arcpy.mapping.MapDocument("CURRENT")
    df = mxd.activeDataFrame
    arcpy.management.MakeFeatureLayer(inFeats, "random_sample", where_clause = wc )
    arcpy.mapping.Layer("random_sample")


except:
    errorMsg()







