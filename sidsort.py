'''
###  sidsort.py
###  SID Data sort
###      by
###  Rupert Powell
###    Jan 2016
###
###**************************
###  Install python 3.x from here: https://www.python.org/downloads/
###  then from the command prompt type the following:
###
###  Usage: py sidsort.py -i=./input_path -o=./output_path
###  ./ = from the path where the script is located
###  also absolute paths can be used: 
###  py sidsort.py -i=c:\input_path -o=c:\output_path
###  py sidsort.py -h (command line help)
###  Forward and backwards slashes are both acceptable \ and /
###
###**************************
###  v0.2b Added Colin Clements file types
###  v0.3b Few tweeks to filename handling
'''
import os, datetime, time
import argparse
import shutil

version = '0.3b'
name = 'JCook'  # hardcoded for this script but could be passed as a paramitter

# setup the commandline argument handler
parser = argparse.ArgumentParser()
# command line argument to take the input path where the .dat files are
parser.add_argument('-i', '--i', dest = 'indir', default = './', 
                    help = 'Input files directory default is ./')
# command line argument that takes the path where the output files go
parser.add_argument('-o', '--o', dest = 'outdir', default = './', 
                    help = 'Output files directory default is ./')

# create the argument handler object
args = parser.parse_args()

def initialize():
    StartTime = time.time()
    print('Sidsort version {} started {}'.format(version, datetime.datetime.now().time()))
    
    # make sure the input directory exists
    if os.path.isdir(args.indir) is True:
        print('Sorting files in {}'.format(args.indir))
    else:
        print('Input Directory does not exist: {}'.format(args.indir))
        return
    
    print('Outputting renamed files in {}'.format(args.outdir))
    if not os.path.exists(args.outdir):
        print("Output directory doesn't exist so creating it....")
        os.makedirs(args.outdir)    
    
    # call the copy function and get back the number of files copied    
    numfiles = CopyFile()
    # get the time now in order to calculate how long it all took
    EndTime = time.time()
    print('Sidsort finished at {}'.format(datetime.datetime.now().time()))
    print('Files copied = {} in {:.3f} seconds'.format(numfiles, EndTime-StartTime))
    
    ### END OF THE SCRIPT - RETURN TO THE COMMAND PROMPT ###
       
def CopyFile():
    '''
    Rename the file to meet the following specification:
    The VLF Data Repository naming convention is UTYYMMDD[0HHSS]_VLF_[Name].[Suffix]
    '''
    # Get the filenames from the input directory
    FileNames = os.listdir(args.indir)
    # numfiles stores how many files are copied
    numfiles = 0
    # Loop through all the names and process them - including all subdirectories
    for subdir, dirs, files in os.walk(args.indir):
        for file in files:
            suffix = file[-3:]
            # only process .dat file types, skip any other non .dat files
            if suffix == 'dat':            
                longyear = file[0:4]
                year = file[2:4]
                month = file[4:6]
                date = file[6:8]
                # make the new directory path based on the file information
                NewDir = '{0}/{1}/{2}{3}/{2}{3}{4}'.format(args.outdir, longyear, year, month, date)
                # check the directory exists and if it does not then create it
                if not os.path.exists(NewDir):
                    os.makedirs(NewDir)    
                
                # Create the new file name
                NewFileName = 'UT{0}{1}{2}_VLF_{3}.dat'.format(year, month, date, name)
                
                # copy the file to the new directory so long as it does not already exist
                if not os.path.isfile('{}/{}'.format(NewDir, NewFileName)):
                    numfiles += 1
                    # copy and rename the file to the new location
                    shutil.copy(os.path.join(subdir, file), '{}/{}'.format(NewDir, NewFileName))
                    print('{} >> {} copied to {}'.format(file, NewFileName, NewDir))
                else:
                    print('{0}/{1} - File already exists!'.format( NewDir, NewFileName))
            elif suffix == 'spd':                
                NewFileName = '{}_VLF_CClements.spd'.format(file[:-4])
                #print(NewFileName)
                year = file[2:4]
                month = file[4:6]
                date = file[6:8]
                # make the new directory path based on the file information
                longyear = '20{}'.format(year)
                NewDir = '{0}/{1}/{2}{3}/{2}{3}{4}'.format(args.outdir, longyear, year, month, date)
                # check the directory exists and if it does not then create it
                if not os.path.exists(NewDir):
                    os.makedirs(NewDir)    
                              
                # copy the file to the new directory so long as it does not already exist
                if not os.path.isfile('{}/{}'.format(NewDir, NewFileName)):
                    numfiles += 1
                    # copy and rename the file to the new location
                    shutil.copy(os.path.join(subdir, file), '{}/{}'.format(NewDir, NewFileName))
                    print('{} >> {} copied to {}'.format(file, NewFileName, NewDir))
                else:
                    print('{0}/{1} - File already exists!'.format( NewDir, NewFileName))
                
                pass
            else:
                # not a .dat or .spd file!
                print('{} skipped'.format(file))
        
    return numfiles

initialize()
