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
        
    projPath = join ('doc','grace')
    
    projFN ='grace_20210212.txt'
      
    procLL = SetupProcesses(projPath, projFN, prodDB)  