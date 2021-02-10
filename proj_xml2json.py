'''
Created on 21 feb. 2018
@author: thomasgumbricht

'db_setup_class' is used for creating database schemas and tables as defined in xml files.
'db_setup_class' contains a single class 'PGsession'. 
The initiating expects a query dictionary with 
database [db], user [user] and password [pswd] with [pswd] encoded using the base64 package
'''

import xml.etree.cElementTree as ET

import simplejson

from os import path

class Session:
    """Connect to postgres server"""   
    def __init__(self):
        """Connect to selected database"""
        
        pass
                
    def elem_to_internal(self,elem,strip=1):
    
        """Convert an Element into an internal dictionary (not JSON!)."""
    
        d = {}
        for key, value in elem.attrib.items():
            d['@'+key] = value
    
        # loop over subelements to merge them
        for subelem in elem:
            v = self.elem_to_internal(subelem,strip=strip)
            tag = subelem.tag
            value = v[tag]
            try:
                # add to existing list for this tag
                d[tag].append(value)
            except AttributeError:
                # turn existing entry into a list
                d[tag] = [d[tag], value]
            except KeyError:
                # add a new non-list entry
                d[tag] = value
        text = elem.text
        tail = elem.tail
        if strip:
            # ignore leading and trailing whitespace
            if text: text = text.strip()
            if tail: tail = tail.strip()
    
        if tail:
            #d['#tail'] = tail
            pass
        if d:
            # use #text element if other attributes exist
            #if text: d["#text"] = text
            pass
        else:
            # text is the value if no attributes
            d = text or None
        return {elem.tag: d}
    
    
    def internal_to_elem(self, pfsh, factory=ET.Element):
    
        """Convert an internal dictionary (not JSON!) into an Element.
        Whatever Element implementation we could import will be
        used by default; if you want to use something else, pass the
        Element class as the factory parameter.
        """
    
        attribs = {}
        text = None
        tail = None
        sublist = []
        tag = pfsh.keys()
        if len(tag) != 1:
            raise ValueError("Illegal structure with multiple tags: %s" % tag)
        tag = tag[0]
        value = pfsh[tag]
        if isinstance(value,dict):
            for k, v in value.items():
                if k[:1] == "@":
                    attribs[k[1:]] = v
                elif k == "#text":
                    text = v
                elif k == "#tail":
                    tail = v
                elif isinstance(v, list):
                    for v2 in v:
                        sublist.append(self.internal_to_elem({k:v2},factory=factory))
                else:
                    sublist.append(self.internal_to_elem({k:v},factory=factory))
        else:
            text = value
        e = factory(tag, attribs)
        for sub in sublist:
            e.append(sub)
        e.text = text
        e.tail = tail
        return e
    
    
    def elem2json(self,elem, strip=1):
    
        """Convert an ElementTree or Element into a JSON string."""
    
        if hasattr(elem, 'getroot'):
            elem = elem.getroot()
        return simplejson.dumps(self.elem_to_internal(elem,strip=strip))
    
    
    def json2elem(self,json, factory=ET.Element):
    
        """Convert a JSON string into an Element.
        Whatever Element implementation we could import will be used by
        default; if you want to use something else, pass the Element class
        as the factory parameter.
        """
    
        return self.internal_to_elem(simplejson.loads(json), factory)
    
    
    def xml2json(self,xmlstring,strip=1):
    
        """Convert an XML string into a JSON string."""
    
        elem = ET.fromstring(xmlstring)
        return self.elem2json(elem,strip=strip)
    
    
    def json2xml(self,json, factory=ET.Element):
    
        """Convert a JSON string into an XML string.
        Whatever Element implementation we could import will be used by
        default; if you want to use something else, pass the Element class
        as the factory parameter.
        """
    
        elem = self.internal_to_elem(simplejson.loads(json), factory)
        return ET.tostring(elem)
    
    def main(self,input_name):
        
        xmlinput = open(input_name).read()
        
        out = self.xml2json(xmlinput, strip = 0)
        
        output_name = input_name.replace('.xml','.json')
        output_name = output_name.replace('v80','v090')
        file = open(output_name, 'w')
        file.write(out)
        file.close()
        
        
    def _Close(self):
        self.cursor.close()
        self.conn.close()
        
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
    xmlL = [path.join(dirPath,'xml',x.strip())  for x in xmlL if len(x) > 10 and x[0] != '#']
    
    
    session = Session()
    
    for row in xmlL:
        
        print (row)
        
        session.main(row)
        
if __name__ == "__main__":
    
    verbose = True
    
    projFN ='doc/ImportAncillary/Import_NaturalEarth.txt'
    
    projFN ='doc/smap/Import_NaturalEarth.txt'
    
    projFN ='doc/smap/smap_20190416.txt'
  
    ConvertXMLtoJson(projFN)