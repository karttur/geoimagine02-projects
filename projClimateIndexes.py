'''
Created on 5 Apr 2019

@author: thomasgumbricht
'''

#from geoimagine.kartturmain.readXMLprocesses import ReadXMLProcesses, RunProcesses


from params.paramsjson import Params

from geoImagineMain import EvaluateProcesses

#from os.path import dirname, realpath, join 
import os

if __name__ == "__main__":
        
    projFNL = []
    projFNL.append('doc/ClimateIndexes/json/climateIndex-0100_import-NOAA.json')
    #projFNL.append('doc/ClimateIndexes/json/climateIndex-0100_import-co2records.json')
    #projFNL.append('doc/ClimateIndexes/json/climateIndexes-0800_plot.json')

    dir_path = os.path.dirname(os.path.realpath(__file__))
    
    for projFN in projFNL:
        
        projFPN = os.path.join(dir_path, projFN)
        
        print ('running project file:', projFPN)

        projParams = Params(projFPN)
        
        EvaluateProcesses(projParams)