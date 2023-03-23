""" This program will take a list of rotation measure maps and a list of rotation measures (as .csv files) and apply a fitting routine to these
 Written by Alex Woodfinden, April 2018
 """
###############################################

#need files rmMaps.csv, rmModels.csv, must be ran from within casa, used casa version 4.7 for this


#imports
import os,sys,csv,math
import matplotlib.pyplot as plt
from astropy.io import fits
import numpy as np
import datetime
import shutil
import matplotlib.patches as patches
plt.ioff()#turns interactive plotting off (plot only displayed if plt.show() is called)

#Global variables
m2f="MapleToFits.py"#maple to fits python file make sure it is a modified version that accepts the parameters at the top as an external file

#print startTime
startTime=datetime.datetime.now()
print startTime

#check needed files exist
if os.path.exists(m2f) != True:
	print "Maple to fits file does not exist"
	sys.exit(0)
if os.path.exists("rmMaps.csv") != True:
	print "Rotation measure maps (observed) list with bbox values file does not exist"
	sys.exit(0)
if os.path.exists("rmModelsCombined.csv") != True:
	print "Rotation measure model file does not exist"
	sys.exit(0)
if os.path.exists("mediansCombined.txt") == True:
    print "Medians file already exists, delete this to run the fitting routines."
    sys.exit(0)
else:
	os.system("touch mediansCombined.txt")

#import rm Maps and Models
with open("rmMaps.csv", 'r') as fp:
    reader = csv.reader(fp, delimiter=',')
    maps = [row for row in reader]

with open("rmModelsCombined.csv", 'r') as fp:
    reader = csv.reader(fp, delimiter=',')
    models = [row for row in reader]


os.mkdir("ImagesCombined")#if you need to restart comment out this line
#create directory system to work in
for ii in maps:
	os.mkdir("./ImagesCombined/" + str(ii[0][:-5]))#if you need to restart comment out this line
	os.mkdir("./Combined-" + str(ii[0])[:-5])#if you need to restart comment out this line
	for jj in models:
		if os.path.exists("./" + str(jj[0])[:-4]):
        shutil.rmtree("./" + str(jj[0])[:-4])
		os.mkdir("./" + str(jj[0])[:-4])
    os.chdir("./" + str(jj[0])[:-4])

		###this is where the working code for the subdirectories should be done

		#copy all needed files
		os.system("cp ../../" + m2f+" ./")
		os.system("cp ../../" + str(ii[0]) + " ./")
		if str(jj[3])=="True":
			os.system("cp ../../csvfiles/" + str(jj[4]) + " ./")
		if str(jj[7])=="True":
			os.system("cp ../../csvfiles/" + str(jj[8]) + " ./")
		if str(jj[11])=="True":
			os.system("cp ../../csvfiles/" + str(jj[12]) + " ./")
		os.system("cp ../../csvfiles/" + str(jj[0]) + " ./")	







		#run mapletofits conversion passing needed parameters to python file
		m2fd=[]
		m2fd.append(ii[0])#fits map file
		m2fd.append(jj[0][:-4]+".fits")#outfile name
		m2fd.append("True")#if overwrite is enabled
		m2fd.append(ii[1])#galaxy diameter in degrees, an expression is okay i.e 15.5arcmin/60 to get degrees
		m2fd.append("True")#if we have data for quadrant 1
		m2fd.append(jj[0])#this is the maple output for quadrant 1 to be converted to fits, must be in csv format
		m2fd.append("False")#whether to flip the input data along the x axis
		m2fd.append("False")#whether to flip the input data along the y axis
		m2fd.append("True")#if we have data for quadrant 2
		if str(jj[3])=="True":
			m2fd.append(jj[4])#this is the maple output for quadrant 2 to be converted to fits, must be in csv format
			m2fd.append(jj[5])#whether to flip the input data along the x axis
			m2fd.append(jj[6])#whether to flip the input data along the y axis
		else:
			m2fd.append(jj[0])#this is the maple output for quadrant 2 to be converted to fits, must be in csv format
			m2fd.append("True")#whether to flip the input data along the x axis
			m2fd.append("False")#whether to flip the input data along the y axis
		m2fd.append("True")#if we have data for quadrant 3
		if str(jj[7])=="True":
			m2fd.append(jj[8])#this is the maple output for quadrant 2 to be converted to fits, must be in csv format
			m2fd.append(jj[9])#whether to flip the input data along the x axis
			m2fd.append(jj[10])#whether to flip the input data along the y axis
		else:
			m2fd.append(jj[0])  #this is the maple output for quadrant 3 to be converted to fits, must be in csv format
			m2fd.append("True")#whether to flip the input data along the x axis
			m2fd.append("True")#whether to flip the input data along the y axis
		m2fd.append("True")#if we have data for quadrant 4
		if str(jj[11])=="True":
			m2fd.append(jj[12])#this is the maple output for quadrant 2 to be converted to fits, must be in csv format
			m2fd.append(jj[13])#whether to flip the input data along the x axis
			m2fd.append(jj[14])#whether to flip the input data along the y axis
		else:
			m2fd.append(jj[0]) #this is the maple output for quadrant 4 to be converted to fits, must be in csv format
			m2fd.append("False")#whether to flip the input data along the x axis
			m2fd.append("True")#whether to flip the input data along the y axis
		m2ff = open('MapleToFitsImports.csv', 'w')
		with m2ff:
    		writer = csv.writer(m2ff)
			for kk in m2fd:
    				writer.writerow([kk])
		execfile(m2f)


		#set scale for all images based of max/min from desired area of map, model images will be shown on same scale
		imscale=imstat(imagename=str(ii[0]),box=str(ii[2])+","+str(ii[3])+","+str(ii[4])+","+str(ii[5]))
		immax=imscale['max'][0]
		immin=imscale['min'][0]
		scalemax=math.fabs(max(immax,immin))


		#perform fitting routine
		### different scaling methods here.  Only one method should be ran, others should be commented out.
		immath(imagename=[str(ii[0][:-5]) + ".im",str(jj[0][:-4]) +".regrid.im"],expr="abs(IM0/IM1)",outfile="divided.im")
		

		###scaling method one, dividing images and taking mean, this method was found to perform best
		scaled=imstat(imagename="divided.im",box=str(ii[2])+","+str(ii[3])+","+str(ii[4])+","+str(ii[5]))['median'][0]
		

		###scaling method two, setting medians to be the same
#		scaled1=imstat(imagename=str(ii[0][:-5]) + ".im",box=str(ii[2])+","+str(ii[3])+","+str(ii[4])+","+str(ii[5]))
#		scaled2=imstat(imagename=str(jj[0][:-4]) + ".regrid.im",box=str(ii[2])+","+str(ii[3])+","+str(ii[4])+","+str(ii[5]))
#		scaled=float(scaled1['median'][0])/float(scaled2['median'][0])
		

		###scaling method three, setting maximum to be the same
#		scaled1=imstat(imagename=str(ii[0][:-5]) + ".im",box=str(ii[2])+","+str(ii[3])+","+str(ii[4])+","+str(ii[5]))
#		scaled2=imstat(imagename=str(jj[0][:-4]) + ".regrid.im",box=str(ii[2])+","+str(ii[3])+","+str(ii[4])+","+str(ii[5]))
#		scaled=float(scaled1['max'][0])/float(scaled2['max'][0])
		###		

        #create residual maps and perform data analysis
		immath(imagename=[str(jj[0][:-4]) + ".regrid.im"],expr="IM0*"+str(scaled),outfile='scaled.im')
		immath(imagename=[str(ii[0][:-5]) + ".im","scaled.im"], expr="IM1-IM0",outfile="residual.im")
		immath(imagename=["residual.im"], expr="abs(IM0)",outfile="absresidual.im")
        
    #AIC calculation
    if os.path.exists("likelihood.im") == True:
        shutil.rmtree("./likelihood.im")
    immath(imagename=["residual.im","N4631_Cband20RMErr_4sig.rotated.im"], expr="(IM0*IM0)/(IM1*IM1)",outfile="likelihood.im")
    lfbox=imstat(imagename="likelihood.im",box=str(ii[2])+","+str(ii[3])+","+str(ii[4])+","+str(ii[5]))
    lf=lfbox['sum'][0]
    npts = lfbox['npts'][0]
    AIC = lf + 2.*4. + 2.*(4.)*(4.-1.)/(npts-4.-1.)

        
        #data analysis
		med=imstat(imagename="residual.im",box=str(ii[2])+","+str(ii[3])+","+str(ii[4])+","+str(ii[5]))
		meda=med['median'][0]
		medb=med['medabsdevmed'][0]
		medc=med['sigma'][0]
		medfile = open('mediansCombined.txt', 'w')
    with medfile:
        writer = csv.writer(medfile)
        writer.writerow([meda])
		    writer.writerow([medc])
		    writer.writerow([AIC])
		med2file = open('../../mediansCombined.txt', 'a')
    with med2file:
        writer = csv.writer(med2file)
		    writer.writerow([ii[0],jj[0]])
        writer.writerow(["median",meda])
		    writer.writerow(["std dev",medc])
        writer.writerow(["AIC",AIC])


		#plot residual image and label median and std dev
		exportfits(imagename='residual.im/',fitsimage='residual.fits')
		hdu = fits.open("residual.fits")[0]
		image_data = hdu.data[0][0]
		ax = plt.subplot(111)#,projection=proj)
		im=ax.imshow(image_data,cmap='coolwarm',vmin=-100.,vmax=100.,origin="lower")#vmin and vmax set to be stand values here, can add vmin and vmax for individual maps later if needed
		plt.colorbar(im)
		rect = patches.Rectangle((int(ii[2]),int(ii[3])),int(ii[4])-int(ii[2]),int(ii[5])-int(ii[3]),fill=False,linewidth=1,edgecolor='r')
		ax.add_patch(rect)
		ax.text(240, 230, 'median = %.2f\n STD  = %.2f\n AIC = %d'% (meda,medc,AIC), style='italic',bbox={'facecolor':'wheat', 'alpha':0.2, 'pad':10})
		ax.plot([int(ii[6]), int(ii[6])], [int(ii[7])-35,int(ii[7])+35], 'k-', lw=1)
		ax.plot([int(ii[6])-50,int(ii[6])+50], [int(ii[7]),int(ii[7])], 'k-', lw=1)
    plt.xlim(int(ii[8]),int(ii[9]))
		plt.ylim(int(ii[10]),int(ii[11]))
		imoutname=str(ii[0])[:-5] +"-"+str(jj[0])[:-4] +"-residual.png"
		plt.savefig(imoutname,bbox_inches="tight")
		os.system("cp -f " + imoutname + " ../../ImagesCombined/" + str(ii[0][:-5]))
		plt.close()



		#plot scaled image and label median and std dev
		exportfits(imagename='scaled.im/',fitsimage='scaled.fits')
		hdu = fits.open("scaled.fits")[0]
		image_data = hdu.data[0][0]
		ax = plt.subplot(111)#,projection=proj)
		med=imstat(imagename="scaled.im",box=str(ii[2])+","+str(ii[3])+","+str(ii[4])+","+str(ii[5]))
		meda=med['median'][0]
		medb=med['medabsdevmed'][0]
		medc=med['sigma'][0]
		im=ax.imshow(image_data,vmin=-1.1*scalemax,vmax=1.1*scalemax,origin="lower",cmap='coolwarm')#vmin and vmax set to be stand values here, can add vmin and vmax for individual maps later if needed
		plt.colorbar(im)
		rect = patches.Rectangle((int(ii[2]),int(ii[3])),int(ii[4])-int(ii[2]),int(ii[5])-int(ii[3]),fill=False,linewidth=1,edgecolor='r')
		ax.add_patch(rect)
		ax.text(240, 230, 'median = %.2f\n MAD = %.2f\n STD  = %.2f'% (meda,medb,medc), style='italic',bbox={'facecolor':'wheat', 'alpha':0.2, 'pad':10})
		ax.plot([int(ii[6]), int(ii[6])], [int(ii[7])-35,int(ii[7])+35], 'k-', lw=1)
		ax.plot([int(ii[6])-50,int(ii[6])+50], [int(ii[7]),int(ii[7])], 'k-', lw=1)
    plt.xlim(int(ii[8]),int(ii[9]))
		plt.ylim(int(ii[10]),int(ii[11]))
		imoutname=str(ii[0])[:-5] +"-"+str(jj[0])[:-4] +"-scaled.png"
		plt.savefig(imoutname,bbox_inches="tight")
		os.system("cp -f " + imoutname + " ../../ImagesCombined/" + str(ii[0][:-5]))
		plt.close()


		###  no code below here for the fitting function
		os.chdir("../")
	os.chdir("../")


	#create image for map file map=ii[0]
	med=imstat(imagename=str(ii[0]),box=str(ii[2])+","+str(ii[3])+","+str(ii[4])+","+str(ii[5]))
	meda=med['median'][0]
  medb=med['medabsdevmed'][0]
	medc=med['sigma'][0]
	hdu = fits.open(ii[0])[0]
  image_data = hdu.data[0][0]
  ax = plt.subplot(111)#,projection=proj)
  im=ax.imshow(image_data,vmin=-1.1*scalemax,vmax=1.1*scalemax,origin="lower",cmap='coolwarm')#vmin and vmax set to be stand values here, can add vmin and vmax for individual maps later if needed
  plt.colorbar(im)
  rect = patches.Rectangle((int(ii[2]),int(ii[3])),int(ii[4])-int(ii[2]),int(ii[5])-int(ii[3]),fill=False,linewidth=1,edgecolor='r')
  ax.add_patch(rect)
  ax.text(240, 230, 'median = %.2f\n STD  = %.2f' % (meda,medc), style='italic',bbox={'facecolor':'wheat', 'alpha':0.2, 'pad':10})
  ax.plot([int(ii[6]), int(ii[6])], [int(ii[7])-35,int(ii[7])+35], 'k-', lw=1)
  ax.plot([int(ii[6])-50,int(ii[6])+50], [int(ii[7]),int(ii[7])], 'k-', lw=1)
  plt.xlim(int(ii[8]),int(ii[9]))
  plt.ylim(int(ii[10]),int(ii[11]))
  imoutname=str(ii[0])[:-5] + ".png"
  plt.savefig(imoutname)
  os.system("cp -f " + imoutname + " ../ImagesCombined/" + str(ii[0][:-5]))
  plt.close()


endTime=datetime.datetime.now()
print "start time = " + str(startTime)
print "end time = " + str(endTime)
print "time taken = " + str(endTime-startTime)
