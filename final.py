## Raster Change Detection Workflow
## John Dees
## Final Project for GISC 3200K
## Professor Miller
## 28 July 2014

## This script will be converted to an ArcMap tool. The purpose of the tool is to take an Area
## of Interest polygon file and two LANDSAT rasters from two time periods as input. It will clip
## both rasters to the area of interest. It will then perform an unsupervised classification on
## both rasters. It will then run a change detection algorithm on the two rasters.
## Outputs include two classified rasters and a change detection raster.

## Import Necessary Modules

import arcpy
import os
from arcpy.sa import *

## Define repeat functions

def clip_it(AOI, raster, date):
    """This function clips file raster to supplied AOI file. It always uses
       AOI extent for clipping extent. Output file will be a TIF image with the
       supplied date as a filename"""
    try:
        arcpy.Clip_management(raster, '#', '{}clip.tif'.format(date), AOI, '0', 'ClippingGeometry')
    except:
        print('Clip Failed')
        print
        print arcpy.GetMessages()
        print
    return

def classify_it(raster, num_class, min_class, samp_int, date):
##    os.mkdir("{}/{}".format(path,date))
    try:
        outUnsupervised = IsoClusterUnsupervisedClassification(raster, num_class, min_class, samp_int)
        outUnsupervised.save("{}/{}class.tif".format(date, date))
        del outUnsupervised
    except:
        print('Classify failed')
        print
        print arcpy.GetMessages()
        print
    
    return
        
    

## Set up workspace

from arcpy import env
env.workspace = "u:/shared/gis/studata/jpdees0754/gitprojects/Final_Project/files"
env.overwriteOutput = True
path = env.workspace

## Prompt user for AOI and LANDSAT Rasters
## Promt user for raster data month and year
AOI = 'AOI.shp'
new_image = 'g2011Clip.img'
new_date = '2011'
old_image = 'g2000Clip.img'
old_date = '2000'
num_class = '5'
min_class_size = '20'
sample_int = '10'



## Clip both rasters to area of interest

clip_it(AOI, new_image, new_date)
clip_it(AOI, old_image, old_date)


## Perform unsupervised classification on raster images

classify_it('{}clip.tif'.format(new_date), num_class, min_class_size, sample_int, new_date)
classify_it('{}clip.tif'.format(old_date), num_class, min_class_size, sample_int, old_date)

## Perfom change detection on classified rasters

new_class = arcpy.Raster("{}class.tif".format(new_date))
old_class = arcpy.Raster("{}class.tif".format(old_date))

outEqualTo = Raster(old_class) == Raster(new_class)
outEqualTo.save("{}_{}_Change.tif".format(old_date,new_date))

