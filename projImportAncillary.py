'''
Created on 24 Apr 2019

@author: thomasgumbricht
'''

from os import path


def ConvertXMLtoJson(projFPN):
    '''
    Setup schemas and tables
    '''
        
    # Get the full path to the project text file
    dirPath = path.split(projFPN)[0]
    
    # Open and read the text file linking to all json files defining the project
    with open(projFPN) as f:
        
        xmlL = f.readlines()
    
    # Clean the list of json objects from comments and whithespace etc    
    xmlL = [path.join(dirPath,x.strip())  for x in xmlL if len(x) > 10 and x[0] != '#']
    
    for row in xmlL:
        
        print (row)
        
    SNULLE
    
    
if __name__ == "__main__":
    
    verbose = True
    
    projFN ='doc/ImportAncillary/Import_NaturalEarth.txt'
  
    ConvertXMLtoJson(projFN)


