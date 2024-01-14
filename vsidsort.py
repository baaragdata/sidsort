'''
###  sidsort2.py
###  SID Data sort
###      by
###  Rupert Powell
###    Jan 2016
###  Minor edits by Andrew Lutley
###    Feb 2020
###
###**************************
###  Install python 3.x from here: https://www.python.org/downloads/
###  then from the command prompt type the following:
###
###  Usage: py sidsort2.py

###  Make sure to set the directories up before hitting run.

###**************************
###  v0.2b Added Colin Clements file types
###  v2.0a Added GUI and a few other features RGP
###  v2.1a Resolved YY and YYYY date formatting RGP
###  v2.2a Added csv files section
###
###**************************
'''
import os, datetime, time
import shutil
from tkinter import *
from tkinter import ttk, StringVar
from tkinter.filedialog import askdirectory

version = '2.2a'
Names = (
        'JCook',
        'CClements',
        'ALutley',
        'AThomas'
        )
version = '2.0a'
folders = {'input':"./", 'output':"./"}
labels={}

class Application:
    
    def __init__(self, parent):
        self.parent = parent
        parent.title( "vSIDSORT {}".format(version))
        self.GUI()
        self.SkippedFiles = []
        
    def GUI(self):
        
        self.InputLabel = ttk.Label(self.parent, text = "Input folder")
        self.InputLabel.grid(column=1, row=0, sticky='w')
        self.InputButton = ttk.Button(self.parent, text='Select input folder', width=20, command= lambda : self.GetFolder('input'))
        self.InputButton.grid(column=0, row=0)
        
        self.OutputLabel = ttk.Label(self.parent, text ="Output folder")
        self.OutputLabel.grid(column=1, row=1, sticky='w')
        self.OutputButton = ttk.Button(self.parent, text='Select output folder', width=20, command= lambda : self.GetFolder('output'))
        self.OutputButton.grid(column=0, row=1)
        
        self.ObserverName = StringVar()
        self.NameSelect = ttk.Combobox(self.parent, width = 30 , textvariable = self.ObserverName)
        self.NameSelect['values'] = Names
        self.NameSelect.current(0)
        self.NameSelect.grid(column=1, row=2, sticky='w')
        
        self.ObserverLabel = ttk.Label(self.parent, text ="Observer's Name")
        self.ObserverLabel.grid(column=0, row=2)
        
        labels['input']=self.InputLabel
        labels['output'] =self.OutputLabel
        
        self.RunButton = ttk.Button(self.parent, text='Run', width=20, command= self.Sort)
        self.RunButton.grid(column=0, row=4, sticky='s')
        
        self.S = Scrollbar(root)
        self.Messages = Text(self.parent, height=40, width=150)
        self.S.grid(column=2, row=4, sticky='ns')
        self.Messages.grid(column=1, row=4, columnspan=True)
        self.S.config(command=self.Messages.yview)
        self.Messages.config(yscrollcommand=self.S.set)
        self.Messages.bind('<Button-3>',self.rClicker, add='')
        
        self.style = ttk.Style()
        self.style.theme_use("vista") # classic,default,clam,winnative,vista,xpnative,alt  

    def rClicker(self, e):
        ''' right click context menu for all Tk Entry and Text widgets'''
        
        try:
            def rClick_All(e, apnd=0):
                e.widget.event_generate('<Control-a>')
                
            def rClick_Copy(e, apnd=0):
                e.widget.event_generate('<Control-c>')
    
            def rClick_Cut(e):
                e.widget.event_generate('<Control-x>')

            e.widget.focus()
    
            nclst=[
                   (' Select All', lambda e=e: rClick_All(e)),
                   (' Cut', lambda e=e: rClick_Cut(e)),
                   (' Copy', lambda e=e: rClick_Copy(e)),
                   ]
    
            rmenu = Menu(None, tearoff=0, takefocus=0)
    
            for (txt, cmd) in nclst:
                rmenu.add_command(label=txt, command=cmd)
    
            rmenu.tk_popup(e.x_root+40, e.y_root+10,entry="0")
        except TclError:
            print(' - rClick menu, something wrong')
            pass
        return "break"              
    
    def rClickbinder(self, r):
        ''' binder for the right click menu '''

        try:
            for b in [ 'Text', 'Entry', 'Listbox', 'Label']: #
                r.bind_class(b, sequence='<Button-3>', func=self.rClicker, add='')
        except TclError:
            print(' - rClickbinder, something wrong') 


    def CopyFile(self):
        '''
        Rename the file to meet the following specification:
        The VLF Data Repository naming convention is UTYYYYMMDD[0HHSS]_VLF_[Name].[Suffix]
        '''
        # Make sure the skipped file list is cleared
        self.SkippedFiles.clear()
        # Get the filenames from the input directory
        FileNames = os.listdir(folders['input'])
        # numfiles stores how many files are copied
        numfiles = 0
        # Loop through all the names and process them - including all subdirectories
        for subdir, dirs, files in os.walk(folders['input']):
            for file in files:
                suffix = file[-3:]
                # only process .dat file types, skip any other non .dat files
                if suffix == 'dat':            
                    longyear = file[0:4]
                    year = file[2:4]
                    month = file[4:6]
                    date = file[6:8]
                    # make the new directory path based on the file information
                    NewDir = '{0}/{1}/{2}{3}/{2}{3}{4}'.format(folders['output'], longyear, year, month, date)
                    # check the directory exists and if it does not then create it
                    if not os.path.exists(NewDir):
                        os.makedirs(NewDir)    
                    
                    # Create the new file name
                    # NewFileName = 'UT{0}{1}{2}_VLF_{3}.dat'.format(year, month, date, name)
                    # Edited by AJL to concert filename to long year format, for conformity to SPD file convention
                    NewFileName = 'UT{0}{1}{2}_VLF_{3}.dat'.format(longyear, month, date, self.ObserverName.get())
                    
                    # copy the file to the new directory so long as it does not already exist
                    if not os.path.isfile('{}/{}'.format(NewDir, NewFileName)):
                        numfiles += 1
                        # copy and rename the file to the new location
                        shutil.copy(os.path.join(subdir, file), '{}/{}'.format(NewDir, NewFileName))
                        self.Messages.insert(END, '{} >> {} copied to {}\n'.format(file, NewFileName, NewDir))
                    else:
                        self.Messages.insert(END, '{0}/{1} - File already exists!\n'.format( NewDir, NewFileName))
                elif suffix == 'spd':
                    NewFileName = '{}_VLF_{}.spd'.format(file[2:-4], self.ObserverName.get())
                    # Detect either YY or YYYY date format
                    if file[2:4] == '20':
                        year = '{}'.format(file[2:6])
                        NewFileName = "UT{}".format(NewFileName)
                        month = file[6:8]
                        date = file[8:10]
                    else:                    
                        year = '20{}'.format(file[2:4])
                        NewFileName = "UT20{}".format(NewFileName)
                        month = file[4:6]
                        date = file[6:8]
                    # make the new directory path based on the file information
                    NewDir = '{0}/{1}/{2}{3}/{2}{3}{4}'.format(folders['output'], year, year[-2:], month, date)
                    # check the directory exists and if it does not then create it
                    if not os.path.exists(NewDir):
                        os.makedirs(NewDir)    
                                  
                    # copy the file to the new directory so long as it does not already exist
                    if not os.path.isfile('{}/{}'.format(NewDir, NewFileName)):
                        numfiles += 1
                        # copy and rename the file to the new location
                        shutil.copy(os.path.join(subdir, file), '{}/{}'.format(NewDir, NewFileName))
                        self.Messages.insert(END, '{} >> {} copied to {}\n'.format(file, NewFileName, NewDir))
                    else:
                        self.Messages.insert(END, '{0}/{1} - File already exists!\n'.format( NewDir, NewFileName))
                    
                    pass
                elif suffix == 'xml':
                    '''
                        File example for Andrew Thomas: Staribus4ChannelLogger_RawData_20190101_000021.xml
                    '''
                    FilenameParts = file.split('_')
                    NewFileName = 'UT{}_{}_{}_{}_VLF_{}.xml'.format(FilenameParts[2], FilenameParts[3][:-4],
                                                               FilenameParts[0], FilenameParts[1], self.ObserverName.get())
                    #print(NewFileName)
                    year = '{}'.format(FilenameParts[2][2:4])
                    month = FilenameParts[2][4:6]
                    date = FilenameParts[2][6:8]
                    # make the new directory path based on the file information
                    NewDir = '{0}/20{1}/{2}{3}/{2}{3}{4}'.format(folders['output'], year, year, month, date)
                    # check the directory exists and if it does not then create it
                    if not os.path.exists(NewDir):
                        os.makedirs(NewDir)    
                                  
                    # copy the file to the new directory so long as it does not already exist
                    if not os.path.isfile('{}/{}'.format(NewDir, NewFileName)):
                        numfiles += 1
                        # copy and rename the file to the new location
                        shutil.copy(os.path.join(subdir, file), '{}/{}'.format(NewDir, NewFileName))
                        self.Messages.insert(END, '{} >> {} copied to {}\n'.format(file, NewFileName, NewDir))
                elif suffix == 'csv':
                    '''
                        Example file: UT20110307_UKRAA_Rx_VLF_SDawes.csv
                    '''
                    NewFileName = file
                    #print(NewFileName)
                    year = file[2:6]
                    month = file[6:8]
                    date = file[8:10]
                    # make the new directory path based on the file information
                    NewDir = '{0}/{1}/{2}{3}/{2}{3}{4}'.format(folders['output'], year, year[-2:], month, date)
                    # check the directory exists and if it does not then create it
                    if not os.path.exists(NewDir):
                        os.makedirs(NewDir)    
                                  
                    # copy the file to the new directory so long as it does not already exist
                    if not os.path.isfile('{}/{}'.format(NewDir, NewFileName)):
                        numfiles += 1
                        # copy and rename the file to the new location
                        shutil.copy(os.path.join(subdir, file), '{}/{}'.format(NewDir, NewFileName))
                        self.Messages.insert(END, '{} >> {} copied to {}\n'.format(file, NewFileName, NewDir))                        
                    else:
                        self.Messages.insert(END, '{0}/{1} - File already exists!\n'.format( NewDir, NewFileName))
                    
                    pass
                else:
                    # not a .dat or .spd file!
                    #self.Messages.insert(END, '{} skipped\n'.format(file))
                    self.SkippedFiles.append(file)
            
        return numfiles

    def GetFolder(self, folder_type, event=None):
        '''
            Folder type is 'input' or 'output'
        '''
        folders[folder_type] = askdirectory(initialdir="",
                               title = "Choose the input directory."
                               )
        labels[folder_type].config(text=folders[folder_type])
        self.Messages.insert(END, "{} folder set to {}\n".format(folder_type.capitalize(), folders[folder_type]))
        #Using try in case user types in unknown file or closes without choosing a file.

    def Sort(self):
        self.Messages.insert(END, 'SORTING for {}...\n'.format(self.ObserverName.get()))
        #Messages.insert(END, 'From: {} \nTo: {}\n'.format(folders['input'], folders['output']))
        #Messages.insert(END, 'For: {}\n'.format(Name.get()))
        StartTime = time.time()
        self.Messages.insert(END, 'Sidsort version {} started {}\n'.format(version, datetime.datetime.now().time()))
        
        # make sure the input directory exists
        if folders['input'] and os.path.isdir(folders['input']) is True:
            self.Messages.insert(END, 'Sorting files in {}\n'.format(folders['input']))
        else:
            self.Messages.insert(END, 'Input Directory does not exist: {}\n'.format(folders['input']))
            return
        if not folders['output']:
            self.Messages.insert(END, 'Output Directory blank!\n')
            return
        self.Messages.insert(END, 'Outputting renamed files in {}\n'.format(folders['output']))
        if not os.path.exists(folders['output']):
            self.Messages.insert(END, "Output directory doesn't exist so creating it....\n")
            os.makedirs(folders['output'])    
        
        # call the copy function and get back the number of files copied    
        numfiles = self.CopyFile()
        # log any skipped files
        if len(self.SkippedFiles):
            self.Messages.insert(END, 'Skipped Files = {}\n'.format(len(self.SkippedFiles)))
            self.WriteSkippedReport()
        else:
            self.Messages.insert(END, 'No Skipped Files\n')
        # get the time now in order to calculate how long it all took
        EndTime = time.time()
        self.Messages.insert(END, 'Sidsort finished at {}\n'.format(datetime.datetime.now().time()))
        self.Messages.insert(END, 'Files copied = {} in {:.3f} seconds\n'.format(numfiles, EndTime-StartTime))
        
        ### END OF THE SCRIPT - RETURN TO THE COMMAND PROMPT ###
        

    def ClearText(self, event=None):
        self.Messages.delete('1.0', END)

    def WriteSkippedReport(self):
        ReportName = 'skipreport.log'
        self.Messages.insert(END, 'Skipped File report = {}/{}\n'.format(folders['input'], ReportName))
        with open('{}{}'.format(folders['input'], ReportName), mode='wt', encoding='utf-8') as myfile:
            myfile.write('\n'.join(self.SkippedFiles))
        

if __name__ == '__main__':
    root = Tk()
    app = Application(root)
    root.mainloop()
    