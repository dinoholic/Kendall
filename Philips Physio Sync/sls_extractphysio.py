#!/usr/bin/python
# Extract physio files from SLU Philips .log format
# Usage:
# sls_extractphysio filename lengthofprotocol
#
# todo: figure out how to extract length of protocol, in secs, from some other
# information source
import sys,csv, os, re, string

# sampling frequency of physio on SLU scanner is 500hz
samplingFreq = 500

def usage():
   print "usage: sls_extractphysio filename lengthOfProtocol"
   print "       filename is name of .log file"
   print "       lengthOfProtocol is the length, in seconds of corresponding"
   print "          scan"
   sys.exit(1);


if (len(sys.argv) != 3 ):
   usage(); # will exit

    
filename = sys.argv[1]
lenOfProtocol = int(sys.argv[2])
   

# read in physio, using any combination of whitespace as delimeter
physiodat = csv.reader(open(filename), delimiter=' ', skipinitialspace=True)

endlines = []  
for row in physiodat:
      firstchar = row[0][0];
      if (firstchar != "#"): # skip # as comment character
           code = row[9]
           if (int(code) == 20): # hex code 20 is end of scan
              endlines.append(physiodat.line_num) # save the line number
# we are done, now check to see if there was only one end scan character
if (len(endlines) == 0):
   print "Error - no end of scan code found."
   sys.exit(1)
if (len(endlines) > 1):
   print >> sys.stderr, "Warning - there should only be one end scan character."
   print >> sys.stderr,  "In this file, there are ", len(endlines)
   print >> sys.stderr, "Using the last - check your physio data"
   end =int(endlines[len(endlines)-1])
else:
   end = int(endlines[0])
# if we get here, that means there is one end of line marker, and we just
# need to print out that many lines back
# first, reopen the file

start = end - samplingFreq*lenOfProtocol
if (start < 0):
  print "Error - not enough lines for the specified length of protocol"
  sys.exit(1);
physiodat = csv.reader(open(filename), delimiter=' ', skipinitialspace=True)
f = open(filename, "r") # reopen the file
x = f.readlines() # read in the whole file
for i in range(start,end): # for the subset we care about
    print x[i].strip() # print it, stripping newline characters

  
