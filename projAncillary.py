'''
Created on 4 Mar 2021

@author: thomasgumbricht
'''

# Standard library imports

from os.path import join

# Package application imports

from geoimagine.projects import SetupProcesses

if __name__ == "__main__":
    
    prodDB = 'geoimagine'   
        
    projPath = join ('doc','importAncillary')
    
    projFN ='Import_ancillary_20210317.txt'
      
    procLL = SetupProcesses(projPath, projFN, prodDB)