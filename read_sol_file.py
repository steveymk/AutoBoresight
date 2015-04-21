#!/usr/bin/env python
#-*- coding:utf-8 -*-

###########################################################
# This file has been created by ARSF Data Analysis Node and
# is licensed under the GPL v3 Licence. A copy of this
# licence is available to download with this file.
###########################################################

#Basic code to read a sol file - can be run standalone or imported as a library
#This is provided as is and there is no warranty or guarantee it works
#The python numpy library is required to run

import argparse
import numpy
import sys
import os

###########################################################################
# Get a list of the sol header types
# This is the definition of a SOL record header
###########################################################################
def sol_header_types():
   """Function sol_header_types

      Get a list of the sol header types

      Arguments:

      Returns: list of the data types in the header of a sol record
   """
   return  [   ("preamble_0", numpy.uint8),
               ("preamble_1", numpy.uint8),
               ("message_length", numpy.uint16),
               ("version", numpy.uint8),
               ("data_version", numpy.uint8),
               ("source_id", numpy.uint8),
               ("destination_id", numpy.uint8),
               ("status", numpy.uint8),
               ("reserved", numpy.uint8),
               ("transaction_id", numpy.uint16),
               ("message_id", numpy.int16),
               ("time_type", numpy.uint8),
               ("time_type_2", numpy.uint8),
               ("gps_week_number", numpy.uint16),
               ("time", numpy.float64),
               ("time_2", numpy.float64),
               ("header_checksum", numpy.uint8) ]

###########################################################################
# Get a list of the sol record types
# This is the definition of a SOL data record
###########################################################################
def sol_record_types():
   """Function sol_record_types

      Get a list of the sol record types

      Arguments:

      Returns: list of the data types in a sol record
   """
   return [ ("datum", numpy.uint16),
            ("solution_origin", numpy.uint16),
            ("solution_level", numpy.uint16),
            ("solution_status", numpy.uint8),
            ("lat", numpy.float64),
            ("lon", numpy.float64),
            ("alt", numpy.float64),
            ("standard_deviation_latitude", numpy.float32),
            ("standard_deviation_longitude", numpy.float32),
            ("standard_deviation_height", numpy.float32),
            ("roll", numpy.float64),
            ("pitch", numpy.float64),
            ("heading", numpy.float64),
            ("standard_deviation_roll", numpy.float32),
            ("standard_deviation_pitch", numpy.float32),
            ("standard_deviation_true_heading", numpy.float32),
            ("nsspeed", numpy.float64),
            ("ewspeed", numpy.float64),
            ("vertspeed", numpy.float64),
            ("standard_deviation_north_velocity", numpy.float32),
            ("standard_deviation_east_velocity", numpy.float32),
            ("standard_deviation_up_velocity", numpy.float32),
            ("roll_rate", numpy.float64),
            ("pitch_rate", numpy.float64),
            ("heading_rate", numpy.float64),
            ("geoid_undulation", numpy.float32),
            ("geoid_model", numpy.uint8),
            ("padding", numpy.int8),
            ("crc32", numpy.int32) ]

###########################################################################
# Get a numpy data type for a sol record
# This is the header followed by data record
###########################################################################
def sol_data_type():
   """Function sol_data_type

      Get a numpy data type for a sol record

      Arguments:

      Returns: numpy data type for a sol header and record
   """
   return numpy.dtype(sol_header_types()+sol_record_types())

###########################################################################
# Read a sol file into a numpy array.
# This is the function that reads the SOL file and returns the data as a
# numpy array
###########################################################################
def readSol(filename):
   """Function readSol

      Read a sol file into a numpy array.

      Arguments:
               filename: string of filename to read into a numpy array

      Returns: 2-d numpy array of sol data
   """

   if not isinstance(filename, str):
      raise TypeError("argument 1 to readSol must be a string")
   #end if
   data_type=sol_data_type()
   record_length=numpy.empty(0, dtype=data_type).itemsize
   header_length_noCheck=numpy.empty(0,
                            dtype=numpy.dtype(sol_header_types()[:-1])).itemsize
   #Calculate checksum for first record. This is done again later on the whole
   #data set. This is just here so if it is clearly rubbish I don't read the
   #whole file into memory
   fd=open(filename, 'r')
   header_size=numpy.empty(0, dtype=numpy.dtype(sol_header_types())).itemsize
   header=fd.read(header_size)
   fd.close()
   #Calculate the checksum
   checksum = 0
   #Do a cumulative bitwise xor on all elements of the header bytearray
   for byte in bytearray(header[:-1]):
      # ^ means xor
      checksum ^= byte
   #end for
   if checksum != ord(header[header_size-1]):
      raise IOError("Header checksum does not match")
   #end if

   #Read file into memory, is a numpy array of tuples (not really tuples, these
   #are mutable, it looks like a tuple though)
   sol_data=numpy.fromfile(filename, dtype=data_type)
   #Check that the header checksum is correct for all records
   #The checksum is the bitwise xor of all elements in the header excluding the
   #checksum itself.
           #Do a bitwise xor on all header records, want to reduce along axis 1
           #to give an array of checksums
   if (not (numpy.bitwise_xor.reduce(
           #numpy.view gives the view of the array in the given data type,
           #and becuase we are doing a bitwise xor needs to be in unsigned 8bit
           #integers
                                     #reshape the array so that it is in records
           sol_data.view(numpy.uint8).reshape(sol_data.shape[0], record_length)\
                                    #Want just the header records up to the
                                    #checksum
                                    [:, :header_length_noCheck], axis=1)\
         ==\
          #Check that the checksums are correct
          sol_data['header_checksum']).all()):
      raise IOError("Header checksum does not match, may not be a sol file")
   #end if
   return sol_data

###########################################################################
# Function to get the navData array index with a closest value to 'value'
# in the column described by 'index'. e.g. index='time'
###########################################################################
def getArrayIndex(navData,index,value):
   """Function getArrayIndex

      Get the index of the navData array that contains the record with the nearest
      value to 'value'
   """

   return numpy.abs(navData[index]-value).argmin()


###########################################################################
# This will be run if the library is used "stand alone" on the command line
###########################################################################
if __name__=='__main__':
   #Get the input arguments
   parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
   parser.add_argument('--input','-i',help ='Input SOL file to read',default="",metavar="<solfile>")
   parser.add_argument('--output','-o',help ='Output TXT file to write',default="",metavar="<txtfile>")
   parser.add_argument('--parse','-p',default=["time","lat","lon","alt","roll","pitch","heading"],help ='Elements of sol file to write out. This is \
                                a space separated list of keywords in the sol_header_types and sol_record_types within this script. To get a \
                                list of the possible keywords use the keyword list, i.e. "--parse list"',nargs='+',metavar="keyword")
   parser.add_argument('--limits','-l',type=float,default=[float('-inf'),float('inf')],nargs=2,\
                        help="Only output records whose time value falls within the given limits.",metavar="time")
   parser.add_argument('--closest','-c',type=float,default=None,nargs='+',\
                        help="Print out the full records that have closest time value to the given time(s).",metavar="time")
   commandline=parser.parse_args()

   if 'list' in commandline.parse:
      print "Found 'list' in parse string - will write out keywords and exit..."
      for item in sol_record_types():
         print item[0]
      for item in sol_header_types():
         print item[0]
      sys.exit(0)

   #check the sol file exists - exit if not
   if not os.path.exists(commandline.input):
      print "%s the input file cannot be found - are you sure it exists?"%commandline.input
      sys.exit(1)

   #Check limits are sane - exit if not
   if commandline.limits[1] <= commandline.limits[0]:
      print "Upper limit should be higher than lower limit."
      sys.exit(1)

   #read in the sol file - an arry with each row as a record
   soldata=readSol(commandline.input)

   #if closest has been specified only run these and then exit
   if commandline.closest is not None:
      for ctime in commandline.closest:
         print "Record closest to given time of %f is:\n"%ctime,soldata[getArrayIndex(soldata,'time',ctime)],'\n'
      sys.exit(0)

   #Now trim the data down depending on the given time limits
   trimmed_data=soldata[numpy.where(soldata['time'] > commandline.limits[0])]
   trimmed_data=trimmed_data[numpy.where(trimmed_data['time'] < commandline.limits[1])]

   #Get the parse strings from the command line
   ziplist=[]
   for e in commandline.parse:
      ziplist.append(trimmed_data[e])

   #Now do some extracting on the file and
   #write out the data to a text file
   try:
      outfile=open(commandline.output,'w')
   except Exception,e:
      print >> sys.stderr, "Error opening the output file: %s"%str(e)
      sys.exit(1)

   #Write out the element names to be written - eg the csv column names
   outfile.write(",".join(commandline.parse)+'\n')
   #For each item in the zipped elements to be written out
   for dataout in  zip(*ziplist):
      #write out the data item to the file described by outfile
      outfile.write(str(dataout).strip('()')+'\n')



