'''
Created on 23 feb. 2018

@author: thomasgumbricht
'''

from geoimagine.kartturmain.readXMLprocesses import ReadXMLProcesses, RunProcesses

if __name__ == "__main__":
    
    verbose = True
    
    #TRMM_transfer_YYYYMMDD transfers the TRMM data
    #projFN = '/Users/thomasgumbricht/Dropbox/projects/geoimagine_mbpro/USERS/karttur/TRMM/TRMM_transfer_20181201.txt'
    
    #projFN = '/Users/thomasgumbricht/Dropbox/projects/geoimagine_mbpro/USERS/karttur/TRMM/TRMM_20181104.txt'
    #projFN = '/Users/thomasgumbricht/Dropbox/projects/geoimagine_mbpro/USERS/karttur/TRMM/TRMM_graph_20181214.txt'
    projFN ='doc/TRMM/trmm_20190216.txt'
    
    procLL = ReadXMLProcesses(projFN,verbose)

    RunProcesses(procLL,verbose)