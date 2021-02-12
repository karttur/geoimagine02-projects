'''
Created on 19 Feb 2019

@author: thomasgumbricht
'''

# Standard library imports

from os.path import join

# Package application imports

from geoimagine.projects import SetupProcesses

if __name__ == "__main__":
    
    prodDB = 'geoimagine'   
        
    projPath = join ('doc','smap')
    
    projFN ='smap_20210201.txt'
    
    #projFN ='smap-waterbodies-adjust_20190416.txt'
  
    procLL = SetupProcesses(projPath, projFN, prodDB)
    