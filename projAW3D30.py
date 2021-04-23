'''
Created on 2 Mar 2021

@author: thomasgumbricht
'''

# Standard library imports

from os.path import join

# Package application imports

from geoimagine.projects import SetupProcesses

if __name__ == "__main__":
    
    prodDB = 'geoimagine'   
        
    projPath = join ('doc','AW3D30')
    
    projFN ='aw3d30_20210321.txt'
      
    procLL = SetupProcesses(projPath, projFN, prodDB)