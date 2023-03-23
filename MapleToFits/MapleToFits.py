"""Python program to convert maple output, as a .csv file, to a fits image.  Uses a template fits image to make maple output match and uses the same header as the template file.  Needs to be ran from within the casa shell (using execfile("MapleToFits.py")), program was tested using casa version 4.7 and python 2.7.  Parameters to change are located at top of file."""
#Created by Alex Woodfinden (a.woodfinden@queensu.ca) Aug 2017
##################### PARAMETERS TO CHANGE #######################
fitsFile="NGC4631_MoraP_RMsynth_RM_4.fits"  #fits file we are making out data look like, we will copy the header and match dimensions 
outfile="spiralexactvne0alla-N.fits"#end with .fits
Overwrite=True #if we should overwrite outfile if it exists
gD=15.5/60.0 #galaxy diameter in degrees (deg = 60*arcmin)
QuadOne=True#if we have data for quadrant 1
mapFileQ1="spiralexactne0alla-N.csv"  #this is the maple output for quadrant 1 to be converted to fits, must be in csv format
rotQ1x=False#whether to flip the input data along the x axis
rotQ1y=False#whether to flip the input data along the y axis
QuadTwo=True#if we have data for quadrant 2
mapFileQ2="spiralexactne0alla-N.csv"  #this is the maple output for quadrant 2 to be converted to fits, must be in csv format
rotQ2x=True#whether to flip the input data along the x axis
rotQ2y=False#whether to flip the input data along the y axis
QuadThree=True#if we have data for quadrant 3
mapFileQ3="spiralexactne0alla-N.csv"  #this is the maple output for quadrant 3 to be converted to fits, must be in csv format
rotQ3x=True#whether to flip the input data along the x axis
rotQ3y=True#whether to flip the input data along the y axis
QuadFour=True#if we have data for quadrant 4
mapFileQ4="spiralexactne0alla-N.csv"  #this is the maple output for quadrant 4 to be converted to fits, must be in csv format
rotQ4x=False#whether to flip the input data along the x axis
rotQ4y=True#whether to flip the input data along the y axis

##################################################################

from astropy.io import fits
import numpy as np
import csv,sys
from astropy.wcs import WCS
from astropy.utils.data import get_pkg_data_filename



#import and unload data
if QuadOne == True:
	mapleDataQ1=[]
	with open(mapFileQ1) as csvfile:
    		reader = csv.reader(csvfile)
    		mapleDataQ1 = list(reader)    
if QuadTwo == True:
	mapleDataQ2=[]
	with open(mapFileQ2) as csvfile:
    		reader = csv.reader(csvfile)
    		mapleDataQ2 = list(reader)    
if QuadThree == True:
	mapleDataQ3=[]
	with open(mapFileQ3) as csvfile:
    		reader = csv.reader(csvfile)
    		mapleDataQ3 = list(reader)    
if QuadFour == True:
	mapleDataQ4=[]
	with open(mapFileQ4) as csvfile:
    		reader = csv.reader(csvfile)
    		mapleDataQ4 = list(reader)    



#check about of data points in each quadrants, assumes quadrants have the same size
if QuadOne == True:
	numYQuad = len(mapleDataQ1)
	numXQuad = len(mapleDataQ1[0])
elif QuadTwo == True:
	numYQuad = len(mapleDataQ2)
	numXQuad = len(mapleDataQ2[0])
elif QuadThree == True:
	numYQuad = len(mapleDataQ3)
	numXQuad = len(mapleDataQ3[0])
elif QuadFour == True:
	numYQuad = len(mapleDataQ4)
	numXQuad = len(mapleDataQ4[0])
else:
	print "At least one quadrant needs to be enabled"
	sys.exit(0)


##rearranges data for each quadrant into shape that can be converted to .fits
arrangeDataQ1=[]
#axis dimensions are the x and y lengths
#axis 2 (y axis) of image
if QuadOne == True:
	for i in range(len(mapleDataQ1)):
   		arrangeDataQ12=[]
    		#axis 1 (x axis) on image
    		for j in range(len(mapleDataQ1[0])):
        		#this is the value of the field when viewed float if exists, blank if not
			try:
        			if str(mapleDataQ1[j][i]) != "Float(undefined)":
					arrangeDataQ12.append(float(mapleDataQ1[j][i]))
				else:
					arrangeDataQ12.append(float('nan'))
			except:
				arrangeDataQ12.append(float('nan'))
	    	if rotQ1x== True:
			arrangeDataQ1.append(arrangeDataQ12[::-1])#reverses the list (flips along x axis for quadrant)
		else:
			arrangeDataQ1.append(arrangeDataQ12)
else:
	for i in range(numYQuad):
		arrangeDataQ12=[]
		for j in range(numXQuad):
			arrangeDataQ12.append(float('nan'))
		arrangeDataQ1.append(arrangeDataQ12)
if rotQ1y==True:
	arrangeDataQ1=arrangeDataQ1[::-1]#flips along y axis
#repeat for other quadrants
arrangeDataQ2=[]
if QuadTwo == True:
	for i in range(len(mapleDataQ2)):
   		arrangeDataQ22=[]
    		#axis 1 (x axis) on image
    		for j in range(len(mapleDataQ2[0])):
        		#this is the value of the field when viewed float if exists, blank if not
			try:
        			if str(mapleDataQ2[j][i]) != "Float(undefined)":
					arrangeDataQ22.append(float(mapleDataQ2[j][i]))
				else:
					arrangeDataQ22.append(float('nan'))
			except:
				arrangeDataQ22.append(float('nan'))
	    	if rotQ2x== True:
			arrangeDataQ2.append(arrangeDataQ22[::-1])#reverses the list (flips along x axis for quadrant)
		else:
			arrangeDataQ2.append(arrangeDataQ22)
else:
	for i in range(numYQuad):
		arrangeDataQ22=[]
		for j in range(numXQuad):
			arrangeDataQ22.append(float('nan'))
		arrangeDataQ2.append(arrangeDataQ22)
if rotQ2y==True:
	arrangeDataQ2=arrangeDataQ2[::-1]#flips along y axis
arrangeDataQ3=[]
if QuadThree == True:
	for i in range(len(mapleDataQ3)):
   		arrangeDataQ32=[]
    		#axis 1 (x axis) on image
    		for j in range(len(mapleDataQ3[0])):
        		#this is the value of the field when viewed float if exists, blank if not
			try:
        			if str(mapleDataQ3[j][i]) != "Float(undefined)":
					arrangeDataQ32.append(float(mapleDataQ3[j][i]))
				else:
					arrangeDataQ32.append(float('nan'))
			except:
				arrangeDataQ32.append(float('nan'))
	    	if rotQ3x== True:
			arrangeDataQ3.append(arrangeDataQ32[::-1])#reverses the list (flips along x axis for quadrant)
		else:
			arrangeDataQ3.append(arrangeDataQ32)
else:
	for i in range(numYQuad):
		arrangeDataQ32=[]
		for j in range(numXQuad):
			arrangeDataQ32.append(float('nan'))
		arrangeDataQ3.append(arrangeDataQ32)
if rotQ3y==True:
	arrangeDataQ3=arrangeDataQ3[::-1]#flips along y axis
arrangeDataQ4=[]

if QuadFour == True:
	for i in range(len(mapleDataQ4)):
   		arrangeDataQ42=[]
    		#axis 1 (x axis) on image
    		for j in range(len(mapleDataQ4[0])):
        		#this is the value of the field when viewed float if exists, blank if not
			try:
        			if str(mapleDataQ4[j][i]) != "Float(undefined)":
					arrangeDataQ42.append(float(mapleDataQ4[j][i]))
				else:
					arrangeDataQ42.append(float('nan'))
			except:
				arrangeDataQ42.append(float('nan'))
	    	if rotQ4x== True:
			arrangeDataQ4.append(arrangeDataQ42[::-1])#reverses the list (flips along x axis for quadrant)
		else:
			arrangeDataQ4.append(arrangeDataQ42)
else:
	for i in range(numYQuad):
		arrangeDataQ42=[]
		for j in range(numXQuad):
			arrangeDataQ42.append(float('nan'))
		arrangeDataQ4.append(arrangeDataQ42)
if rotQ4y==True:
	arrangeDataQ4=arrangeDataQ4[::-1]#flips along y axis


allData=[]
#add the quadrants together
for i in range(numYQuad):
	t = arrangeDataQ3[i]+arrangeDataQ4[i]
	allData.append(t[::-1])
for i in range(numYQuad):
	t = arrangeDataQ2[i]+arrangeDataQ1[i]
	allData.append(t[::-1])

#make data into hdu type
makeFitsDataQ1 = np.array(allData)
hdunew = fits.PrimaryHDU(makeFitsDataQ1)

#copys old fits file header to new fits file header, we will change certain parameters later
hdu1t = fits.open(fitsFile)
hduold = hdu1t[0]
for i in hduold.header:
    #errors in fits header creation may have made empty rows that we need to exclude
    #history and comments also do not copy over well
    #if you get an error about the header it may be a bad field you need to exlude like here.
    if str(i) != "" and str(i) != " " and str(i) != "\n" and str(i) != '' and str(i) != 'COMMENT' and str(i) != 'HISTORY':
        #if string cast to a string to avoid errors
        if type(hduold.header[i]) == str:
            hdunew.header.set(i,str(hduold.header[i]))
        else:
            hdunew.header.set(i,hduold.header[i])

####change coordinate parameters  
ndel1 = gD/(2*numXQuad) #set pixel size
ndel2 = gD/(4*numYQuad) #output given is to galaxy radius in one direction and half radius in y direction, needs to be checked for each input
hdunew.header.set('CDELT1',ndel1)
hdunew.header.set('CDELT2',ndel2)


####set reference pixel to be center of image as per convention
hdunew.header.set("CRPIX1",float(numXQuad)+0.5)#uses center of pixel
hdunew.header.set("CRPIX2",float(numYQuad)+0.5)


#####needs to be a unique outfile name or overwrite set to true
hdunew.writeto(outfile,clobber=Overwrite)

importfits(fitsimage=outfile,imagename=outfile[:-5]+".im",overwrite=Overwrite)
importfits(fitsimage=fitsFile,imagename=fitsFile[:-5]+".im",overwrite=True)#this overwrite could be set to false to be less wasteful but then you get an error if this step has been done before (that can be ignored)
imregrid(imagename=outfile[:-5]+".im",template=fitsFile[:-5]+".im",output=outfile[:-5]+".regrid.im",overwrite=Overwrite)
exportfits(imagename=outfile[:-5]+".regrid.im",fitsimage=outfile[:-5]+".regrid.fits",overwrite=Overwrite)

print("Raw fits output created at " + outfile + " and regridded image to match template file located at " + outfile[:-5] + ".regrid.fits")
