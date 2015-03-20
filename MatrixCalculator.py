#!/usr/bin/env python
#-*- coding:utf-8 -*-

import argparse
import numpy
import sys
import os
import read_sol_file as sol
import read_sbet_file as sbet
import spy

#Imuangles=[pitch, roll, heading]=np.array([[r11,r12,r13],[r21,r22,r23],[r31,r32,r33]])
#exteriororientation=[w,p,k]=np.array([[a1,a2,a3],[b1,b2,b3],[c1,c2,c3]])
#misalignmentangles=[ex,ey,ez]=np.array([[e11,e12,e13],[e21,e22,e23],[e31,e32,e33]])

#set our sensor and bands to process
#needs to import FOV data, look direction and look slant per instrument
#also needs lever arm offsets (though these should be constant from 2015)
def setFov(sensor):
   if sensor is eagle:
      fovfile=getEagleFov()
   elif sensor is hawk:
      fovfile=getHawkFov()
   elif sensor is fenix:
      fovfile=getFenixFov()
   elif sensor is owl:
      fovfile=getOwlFov()
   
   return fovfile

def flightlineHandler():
   fov=getCentrePixelFov(centrepixel, fovfile)
   adjustments=[]
   stddev=[]
   for flightline in dataset:
      flightlineadjustments=[]
      for scanline in flightline:
         gpstime = getScanlineGpstime(flightline, scanline)
         if solfile:
            #it should be this in flights after 2015
            navinf = sol.getArrayIndex(gpstime)
         else:
            #its going to be sbet
            navinf = sbet.getArrayIndex(gpstime)
         aircraftposition=[navinf.lat,navinf.long]
         attitudeTriangulation(gcps, aircraftposition, Fov, 
         
      adjustments.extend([flightlineadjustments])
   
   numpy.mean(adjustments, axis=0)
   numpy.std(adjustments, axis=0)
   numpy.average(adjustments, axis=0)
   numpy.var(adjustments, axis=0)
   return adjustments

def imuGrabber(navinf):
   imuattitude=[navinf.pitch,navinf.roll,navinf.heading]
   gpsxyz=[navinf]
   
   return imuattitude
         

def attitudeTriangulation(gcps, scanlineposition, projection)
   acceptedgcps
   for gcp in gcps:
      if gcp is outside range of sensible location
         ditch
      else:
         acceptedgcps.extend(gcp)
   given position p(centrepixel proj)
   return triangulatedattitude
   
      
def attitudeComparison(imuattitude, triangulatedattitude, currentadjustments):
   pitchadjust = imuattitude[0] + triangulatedattitude[0]
   rolladjust = imuattitude[1] + triangulatedattitude[1]
   headingadjust = imuattitude[2] + triangulatedattitude[2]
   
   adjustments=[pitchadjust, rolladjust, headingadjust]
   return adjustments
   
def gcpReader(gcpfile):
   if os.path.exists(gcpfile):
      gcps = genfromtxt(gcpfile, delimiter=',', dtype=None)
   else:
      raise Exception
   
   return gcps
   
   
#rotates the sensor frame into the boresight frame
def SframeToBframe(sframe):

#rotates the boresight frame into the mapping frame
def BframtoMframe(bframe):

#brings the matrices into scale
def scaler(matrixtoscale, scale):

def leastSquareAdjustor:
   
def centreGcpIdent(gcplist, navinf):
   

      
      
if __name__=='__main__':
   #Get the input arguments
   parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
   parser.add_argument('--navfile','-n',help ='Input SOL file to read',default="",metavar="<solfile>/<sbetfile>")
   parser.add_argument('--dataset','-d',help ='Input dataset to analyse',default="",metavar="<folder>")
   parser.add_argument('--gcp','-g',help ='Input ground control points file',default="",metavar="<csvfile>")
   parser.add_argument('--output','-o',help ='Output text file for results and variability information',default="",metavar="<txtfile>")
   commandline=parser.parse_args()

   #check the sol/sbet file exists - exit if not
   if not os.path.exists(commandline.navfile):
      print "%s the input file cannot be found - does it exist?"%commandline.input
      sys.exit(1)

   #check the dataset exists - exit if not
   if not os.path.exists(commandline.dataset):
      print "%s the input dataset cannot be found - does it exist?"%commandline.input
      sys.exit(1)
     
   #check the dataset exists - exit if not
   if not os.path.exists(commandline.gcp):
      print "%s the input gcp csv cannot be found - does it exist?"%commandline.input
      sys.exit(1)