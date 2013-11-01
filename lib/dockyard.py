import os, sys, json, re
import sqlite3
from dict2table import *

def curs2dict(cursor):
    
    field_names = [d[0].lower() for d in cursor.description]
    rows = []

    for row in cursor.fetchall():
        rows.append(dict(zip(field_names, row)))

    return rows

class Dockyard(object):
    
    conn = None
    dockyardConfig = None
    dockerImageFactory = None
    docker = None

    def __init__(self, docker=None, dockyardConfig=None, dockerImageFactory=None):
        self.connect()
        self.dockyardConfig = dockyardConfig
        self.dockerImageFactory = dockerImageFactory
        self.docker = docker
        
    def connect(self):
        self.conn = sqlite3.connect('dockyard.db')

    def init(self):

        # Recreate database
        os.remove('dockyard.db')
        self.connect()

        cursor = self.conn.cursor()

        # Table to keep track of dockyards
        cursor.execute('''CREATE TABLE active_dockyards
                     ( id INTEGER PRIMARY KEY, identifier TEXT)''')

        # Table to keep track of each dockyard's dockers
        cursor.execute('''CREATE TABLE active_dockyard_containers
                     ( id INTEGER PRIMARY KEY, dockyard_id INTEGER, image_name TEXT, hash TEXT)''')

    def list(self):
        activeDockyardsCursor = self.conn.cursor().execute('SELECT * FROM active_dockyards')
        dockyardHeaders = [d[0].lower() for d in activeDockyardsCursor.description]  

        activeDockyardsDict = curs2dict(activeDockyardsCursor)
        for activeDockyard in activeDockyardsDict:

            dockyardDockersCursor = self.conn.cursor().execute('SELECT * FROM active_dockyard_containers WHERE dockyard_id = ?', (activeDockyard['id'],))
            dockerHeaders = [d[0].lower() for d in dockyardDockersCursor.description]
            dockerAsciiTable = format_as_table(curs2dict(dockyardDockersCursor), dockerHeaders, dockerHeaders)
            dockerAsciiTable = "\n" + re.sub(re.compile('^', re.MULTILINE), '\t\1', dockerAsciiTable)
            activeDockyard['dockers'] = dockerAsciiTable

        dockyardHeaders.append('dockers')

        print format_as_table(activeDockyardsDict, dockyardHeaders, dockyardHeaders)


    def start(self, dockyardName):
        print "Assembling [%s] dockyard" % dockyardName

        cursor = self.conn.cursor()
        cursor.execute('''INSERT INTO active_dockyards values (NULL,?)''', (dockyardName,))
        rowId = cursor.lastrowid

        for containerConfig in self.dockyardConfig['dockyards'][dockyardName]['containers']:
            
            dockerImage = self.dockerImageFactory.imageFromConfig(containerConfig)

            for i in range(0, dockerImage.getInstances()):
                containerId = self.docker.runByConfiguration(dockerImage)
                cursor.execute('''INSERT INTO active_dockyard_containers VALUES (NULL, ?, ?, ?)''', (rowId, containerConfig['image'], containerId))

        self.conn.commit()



    def stop(self, identifier):

        # Lookup the dockyard from identified
        try:
            id = int(identifier)
            cursor = self.conn.cursor().execute('SELECT * FROM active_dockyards WHERE id = ?', (id,))
        except ValueError:
            cursor = self.conn.cursor().execute('SELECT * FROM active_dockyards WHERE identifier = ?', (identifier,))

        rows = curs2dict(cursor)
        if len(rows) == 0:
            raise Exception("Identifier [%s] does not match a name or id." % identifier)

        for row in rows:
            if row:
                print "Disassembling [%(id)s:%(identifier)s] dockyard" % row
                
                # Kill the containers
                cursor = self.conn.cursor().execute('SELECT * FROM active_dockyard_containers WHERE dockyard_id = ?', (row['id'],))
                for container in curs2dict(cursor):
                    self.docker.killContainerById(container['hash'])

                # Delete container references
                rowsAffected = 0
                cursor = self.conn.cursor().execute('DELETE FROM active_dockyard_containers WHERE dockyard_id = ?', (row['id'],))
                rowsAffected = rowsAffected + cursor.rowcount                
                
                # Delete the dockyard reference                
                cursor = self.conn.cursor().execute('DELETE FROM active_dockyards WHERE id = ?', (row['id'],))
                rowsAffected = rowsAffected + cursor.rowcount                
                
                print "%d rows affected." % rowsAffected
                self.conn.commit()

            else:
                raise Exception("No active dockyard with identifier [%s]" % identifier)

        








