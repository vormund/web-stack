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

    def __init__(self):
        self.connect()

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
        cursor.execute('''CREATE TABLE dockyard_dockers
                     ( id INTEGER PRIMARY KEY, dockyard_id INTEGER, image_name TEXT, hash TEXT)''')

    def list(self):
        activeDockyardsCursor = self.conn.cursor().execute('SELECT * FROM active_dockyards')
        dockyardHeaders = [d[0].lower() for d in activeDockyardsCursor.description]  

        activeDockyardsDict = curs2dict(activeDockyardsCursor)
        for activeDockyard in activeDockyardsDict:

            dockyardDockersCursor = self.conn.cursor().execute('SELECT * FROM dockyard_dockers WHERE dockyard_id = ?', (activeDockyard['id'],))
            dockerHeaders = [d[0].lower() for d in dockyardDockersCursor.description]
            dockerAsciiTable = format_as_table(curs2dict(dockyardDockersCursor), dockerHeaders, dockerHeaders)
            dockerAsciiTable = "\n" + re.sub(re.compile('^', re.MULTILINE), '\t\1', dockerAsciiTable)
            activeDockyard['dockers'] = dockerAsciiTable

        dockyardHeaders.append('dockers')

        print format_as_table(activeDockyardsDict, dockyardHeaders, dockyardHeaders)


    def start(self, dockyardName):
        dockyardConfigs = json.load(open('dockyard.json'))

        print "Assembling [%s] dockyard" % dockyardName

        cursor = self.conn.cursor()
        cursor.execute('''INSERT INTO active_dockyards values (NULL,?)''', (dockyardName,))
        rowId = cursor.lastrowid

        for imageConfig in dockyardConfigs['dockyard'][dockyardName]['image']:
            cursor.execute('''INSERT INTO dockyard_dockers VALUES (NULL, ?, ?, ?)''', (rowId, imageConfig['image'], 'hash'))
            #print image

        self.conn.commit()



        for dockyardConfig in dockyardConfigs['dockyard'][dockyardName]:
            #print dockyardConfig
            pass


    def stop(self, identifier):

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
                
                rowsAffected = 0
                cursor = self.conn.cursor().execute('DELETE FROM active_dockyards WHERE id = ?', (row['id'],))
                rowsAffected = rowsAffected + cursor.rowcount
                
                cursor = self.conn.cursor().execute('DELETE FROM dockyard_dockers WHERE dockyard_id = ?', (row['id'],))
                rowsAffected = rowsAffected + cursor.rowcount
                
                print "%d rows affected." % rowsAffected
                self.conn.commit()

            else:
                raise Exception("No active dockyard with identifier [%s]" % identifier)

        








