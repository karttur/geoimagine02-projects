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
        
    projPath = join ('doc','regions')
    
    projFN ='regions_link_20210304.txt'
      
    procLL = SetupProcesses(projPath, projFN, prodDB)