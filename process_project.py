'''
Created on 29 Jan 2021

@author: thomasgumbricht

'''

# Standard library imports

from os import path

from sys import exit

# Third party imports

from base64 import b64encode, b64decode

import netrc

import psycopg2

# Package application imports

from geoimagine.params import JsonParams

from geoimagine.ancillary import ProcessAncillary

from geoimagine.dem import ProcessDEM

from geoimagine.npproc import ProcessNumpy

from geoimagine.layout import ProcessLayout

from geoimagine.timeseries import ProcessTimeSeries

from geoimagine.updatedb import ProcessUpdateDB

from geoimagine.modis import ProcessModis, ProcessModisEase2N

from geoimagine.copernicus import ProcessCopernicus

from geoimagine.smap import ProcessSmap

from geoimagine.ktgrass import ProcessGRASS, ProcessGRASSDEM

from geoimagine.grace import ProcessGrace

from geoimagine.userproj import ProcessUserProj

from geoimagine.region import ProcessRegion

from geoimagine.ktgdal import ProcessGDAL

from geoimagine.export import ProcessExport

from geoimagine.postgresdb import ManageLayout, ManageAncillary, ManageSMAP
from geoimagine.postgresdb import ManageMODIS, ManageModisPolar, ManageUserProj
from geoimagine.postgresdb import ManageRegion, ManageGDALcomps

#from geoimagine.params import Composition, RegionLayer, RasterLayer

from geoimagine.postgresdb.compositions import SelectCompleteComp

from geoimagine.postgresdb.region import CommonRegions

from geoimagine.postgresdb.session import CommonSearch

class PGsession(CommonRegions, CommonSearch):
    """Connect to postgres server"""

    def __init__(self, query):
        """Connect to selected database"""

        query['pswd'] = b64decode(query['pswd']).decode('ascii')

        conn_string = "host='localhost' dbname='%(db)s' user='%(user)s' password='%(pswd)s'" %query

        self.conn = psycopg2.connect(conn_string)

        self.cursor = self.conn.cursor()

        self.name = 'processSetup'
        
        self.verbose = 2

        CommonRegions.__init__(self)
        
        CommonSearch.__init__(self)

    def _SetSystem(self,system):
        '''
        '''

        self.system = system

    def _DictToSelect(self, queryD):
        '''
        Converts a dictionary to Select statement
        '''
        selectL = []
        for key in queryD:
            #statement = key operator value
            statement = ' %(col)s %(op)s \'%(val)s\'' %{'col':key.replace('#',''), 'op':queryD[key]['op'], 'val':queryD[key]['val']}
            selectL.append(statement)
        self.select_query = "WHERE %(where)s" %{'where':' AND '.join(selectL)}
        return self.select_query

    def _SelectRootProcess(self,queryD):
        '''
        '''
        self.cursor.execute("SELECT rootprocid, minuserstratum FROM process.subprocesses WHERE subprocid = '%(subprocid)s';" %queryD)

        record = self.cursor.fetchone()

        return record

    def _SelectUserCred(self, queryD):
        '''
        '''

        sql = "SELECT userid, usercat, stratum FROM userlocale.users WHERE userid = '%(user)s';" %queryD

        self.cursor.execute(sql)

        self.userid, self.usercat, self.stratum = self.cursor.fetchone()

    def _SelectTractDefRegion(self, queryD):
        '''
        '''
        #First check if this region is itself a defregion

        sql = "SELECT regionid FROM regions.defregions WHERE regionid = '%(tract)s';" %queryD

        self.cursor.execute(sql)

        rec = self.cursor.fetchone()

        if rec != None:

            return (rec[0], 'D')

        sql = "SELECT parentid FROM regions.tracts WHERE tractid = '%(tract)s';" %queryD

        self.cursor.execute(sql)

        rec = self.cursor.fetchone()

        if rec == None:

            return rec

        return (rec[0], 'T')

    def _SelectRegionTiles(self, queryD, paramL):
        '''
        '''
        
        queryD['cols'] = " ,".join(paramL)
        
        sql = "SELECT %(cols)s FROM %(schema)s.regions WHERE regionid = '%(regionid)s';" %queryD

        self.cursor.execute(sql)
        
        return self.cursor.fetchall()
        

    def _SelectProcessSystem(self, queryD, paramL):
        ''' Select system for this process
        '''

        queryD['cols'] = " ,".join(paramL)

        sql = "SELECT %(cols)s FROM process.procsys WHERE subprocid = '%(subprocid)s' and system = '%(system)s';" %queryD

        self.cursor.execute(sql)

        record = self.cursor.fetchone()

        if record == None:

            sql = "SELECT srcsystem, dstsystem, srcdivision, dstdivision FROM process.procsys WHERE subprocid = '%(subprocid)s' and system = '*';" %queryD

            self.cursor.execute( sql )

            record = self.cursor.fetchone()

            if record == None:

                sql = "SELECT system FROM process.procsys WHERE subprocid = '%(subprocid)s';" %queryD

                self.cursor.execute( sql )

                records = self.cursor.fetchall()

                exitstr = 'EXITING, unidentified process system in projects.process_session.PGssssion._SelectProcessSystem for ‰%(subprocid)s\n    available systems include: ' %queryD
                
                recs = [x[0] for x in records]
                
                exitstr += ','.join(recs)

                exit (exitstr)

        return dict(zip(paramL,record))

    def _SingleSearchOld(self,queryD, paramL,  table, schema, pq = False):
        #self._GetTableKeys(schema, table)
        selectQuery = {}
        for item in queryD:

            if isinstance(queryD[item],dict):
                #preset operator and value
                selectQuery[item] = queryD[item]
            else:
                selectQuery[item] = {'op':'=', 'val':queryD[item]}
        wherestatement = self._DictToSelect(selectQuery)
        cols =  ','.join(paramL)
        selectQuery = {'schema':schema, 'table':table, 'select': wherestatement, 'cols':cols}

        query = "SELECT %(cols)s FROM %(schema)s.%(table)s %(select)s" %selectQuery
        if pq:
            print ('SingleSearch query',query)
        self.cursor.execute(query)
        self.records = self.cursor.fetchone()
        return self.records

    def _MultiSearchOld(self,queryD, paramL, schema, table):
        ''' Select multiple records from any schema.table
        '''

        selectQuery = {}
        for item in queryD:

            if isinstance(queryD[item],dict):
                #preset operator and value
                selectQuery[item] = queryD[item]
            else:
                selectQuery[item] = {'op':'=', 'val':queryD[item]}
        wherestatement = self._DictToSelect(selectQuery)

        if len(paramL) == 1:
            cols = paramL[0]
        else:
            cols =  ','.join(paramL)
            
        selectQuery = {'schema':schema, 'table':table, 'select': wherestatement, 'cols':cols}
        
        query = "SELECT %(cols)s FROM %(schema)s.%(table)s %(select)s" %selectQuery

        self.cursor.execute(query)

        self.records = self.cursor.fetchall()

        return self.records

    def _RetrieveLayerComp(self, queryD, searchItemL):
        '''
        '''

        return SelectCompleteComp(self, self.system, queryD, searchItemL)

    def _Close(self):

        self.cursor.close()

        self.conn.close()


def DbConnect(db):
    '''
    '''
    # the HOST must exist in the .netrc file in the users home directory
    HOST = 'karttur'

    # Retrieve login and password from the .netrc file
    secrets = netrc.netrc()

    # Authenticate username, account and password
    username, account, password = secrets.authenticators( HOST )

    # Encode the password before sending it
    password = b64encode(password.encode())

    # Create a query dictionary for connecting to the Postgres server
    query = {'db':db, 'user':username, 'pswd':password}

    return query

def SetupProcesses(docpath, projFN, db):
    '''
    Setup processes
    '''

    srcFP = path.join(path.dirname(__file__),docpath)

    projFPN = path.join(srcFP,projFN)

    # Get the full path to the project text file
    dirPath = path.split(projFPN)[0]

    if not path.exists(projFPN):

        exitstr = 'EXITING, project file missing: %s' %(projFPN)

        exit( exitstr )

    infostr = 'Processing %s' %(projFPN)

    print (infostr)

    # Open and read the text file linking to all json files defining the project
    with open(projFPN) as f:

        jsonL = f.readlines()

    # Clean the list of json objects from comments and whithespace etc
    jsonL = [path.join(dirPath,x.strip())  for x in jsonL if len(x) > 10 and x[0] != '#']

    # Get the user and password for connecting to the db
    query = DbConnect(db)

    # Connect to the Postgres Server
    session = PGsession(query)

    ProcPar = JsonParams(session)

    processL = []

    #Loop over all json files and create Schemas and Tables
    for jsonObj in jsonL:
        
        print ('    ',jsonObj)

        processL.append( ProcPar._JsonObj(jsonObj) )

    # Close the db connection for getting processes and user
    session._Close()

    for processD in processL:

        for k in range(len(processD)):

            print ('    ',k, processD[k])

            if processD[k]['PP'].rootprocid == 'ManageProject':

                session = ManageUserProj(db)

                ProcessUserProj(processD[k]['PP'], session)

                session._Close()
                
            elif processD[k]['PP'].rootprocid == 'ManageRegion':

                session = ManageRegion(db)

                ProcessRegion(processD[k]['PP'], session)

                session._Close()

            elif processD[k]['PP'].rootprocid == 'LayoutProc':

                session = ManageLayout(db)

                ProcessLayout(processD[k]['PP'], session)

                session._Close()

            elif processD[k]['PP'].rootprocid == 'Ancillary':

                session = ManageAncillary(db)

                ProcessAncillary(processD[k]['PP'], session)
                
            elif processD[k]['PP'].rootprocid == 'Export':

                session = ManageAncillary(db)

                ProcessExport(processD[k]['PP'], session)

                session._Close()


            elif processD[k]['PP'].rootprocid == 'UpdateDb':

                session = ManageAncillary(db)

                ProcessUpdateDB(processD[k]['PP'], session)

                session._Close()
                
            elif processD[k]['PP'].rootprocid == 'DemProc':

                session = ManageAncillary(db)

                ProcessDEM(processD[k]['PP'], session)

                session._Close()
                
            elif processD[k]['PP'].rootprocid == 'GrassProc':

                session = ManageAncillary(db)

                ProcessGRASS(processD[k]['PP'], session)

                session._Close()
                
            elif processD[k]['PP'].rootprocid == 'GrassDemProc':

                session = ManageAncillary(db)

                ProcessGRASSDEM(processD[k]['PP'], session)

                session._Close()
                
            elif processD[k]['PP'].rootprocid == 'NumpyProc':

                session = ManageAncillary(db)

                ProcessNumpy(processD[k]['PP'], session)

                session._Close()
                
            elif processD[k]['PP'].rootprocid == 'Tiling':

                session = ManageGDALcomps(db)

                ProcessGDAL(processD[k]['PP'], session)

                session._Close()
                
            elif processD[k]['PP'].rootprocid == 'Translate':

                session = ManageGDALcomps(db)

                ProcessGDAL(processD[k]['PP'], session)

                session._Close()
                
            elif processD[k]['PP'].rootprocid == 'Reproject':

                session = ManageGDALcomps(db)

                ProcessGDAL(processD[k]['PP'], session)

                session._Close()

            elif processD[k]['PP'].rootprocid == 'SmapProc':

                session = ManageSMAP(db)

                ProcessSmap(processD[k]['PP'], session)

                session._Close()

            elif processD[k]['PP'].rootprocid == 'GraceProc':

                session = ManageAncillary(db)

                ProcessGrace(processD[k]['PP'], session)

                session._Close()

            elif processD[k]['PP'].rootprocid == 'MODISProc':

                session = ManageMODIS(db)

                ProcessModis(processD[k]['PP'], session)

                session._Close()
                
            elif processD[k]['PP'].rootprocid == 'USGSProc':

                session = ManageMODIS(db)

                ProcessModis(processD[k]['PP'], session)

                session._Close()

            elif processD[k]['PP'].rootprocid == 'CopernicusProc':

                session = ManageMODIS(db)

                ProcessCopernicus(processD[k]['PP'], session)

                session._Close()
                
            elif processD[k]['PP'].rootprocid == 'ModisPolar':

                session = ManageModisPolar(db)

                ProcessModisEase2N(processD[k]['PP'], session)

                session._Close()

            elif processD[k]['PP'].rootprocid == 'TimeSeries':

                system =  processD[k]['PP'].procsys.srcsystem

                if system == 'ancillary':

                    session = ManageAncillary(db)

                else:

                    exitstr = 'EXITING - add system %s to process.project.ProcessProject for TimeSeries db manager' %(system)

                    exit( exitstr )

                ProcessTimeSeries(processD[k]['PP'], session)

                session._Close()

            else:
                exitstr = 'Process lacking in process.project.SetupProcess: %s' %(processD[k]['PP'].rootprocid)
                exit ( exitstr )
