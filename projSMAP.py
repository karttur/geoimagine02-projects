'''
Created on 19 Feb 2019

@author: thomasgumbricht
'''

#from geoimagine.kartturmain.readXMLprocesses import ReadXMLProcesses, RunProcesses
from os.path import join

from projects import SetupProcesses

if __name__ == "__main__":
    
    prodDB = 'geoimagine'   
    
    #projFN ='/full/path/to/smap_20190221.txt'
    
    projPath = join ('doc','smap')
    
    projFN ='smap_20210201.txt'
    
    #projFN ='doc/SMAP/smap-waterbodies-adjust_20190416.txt'
  
    procLL = SetupProcesses(projPath, projFN, prodDB)

    #RunProcesses(procLL,verbose)
    