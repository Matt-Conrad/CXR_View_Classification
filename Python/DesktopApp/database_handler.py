"""Module contains functions that are basic and common DB operations."""
import os
import sys
import json
import logging
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
# This line is so modules using this package as a submodule can use this.
sys.path.append(os.path.dirname(os.path.abspath(__file__)).replace('\\', '/'))
#

class DatabaseHandler:
    def __init__(self, configHandler):
        self.configHandler = configHandler
        self.dbInfo = self.configHandler.getDbInfo()
        
        self.default_connection = self.openConnection(open_default=True)
        self.default_connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        self.default_cursor = self.openCursor(self.default_connection)

        if not self.db_exists(self.dbInfo["database"]):
            self.create_new_db(self.dbInfo["database"])

        self.connection = self.openConnection()
        self.connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        self.retrieveCursor = self.openCursor(self.connection)
        self.storeCursor = self.openCursor(self.connection) 
        self.countCursor = self.openCursor(self.connection)

    def openConnection(self, open_default=False):
        params = self.dbInfo.copy()
        if open_default:
            params['database'] = 'postgres'
        return psycopg2.connect(**params)

    def openCursor(self, connection):
        return connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

    def closeConnection(self):
        try:
            logging.info('Closing connection')
            self.retrieveCursor.close()
            self.storeCursor.close()
        except (psycopg2.DatabaseError) as error:
            logging.warning(error)
        finally:
            if self.connection is not None:
                self.connection.close()
                logging.info('Connection closed')

    def closeCursor(self, cursor):
        try:
            logging.info('Closing connection')
            cursor.close()
        except (psycopg2.DatabaseError) as error:
            logging.warning(error)
        finally:
            if self.conn is not None:
                self.conn.close()
                logging.info('Connection closed')

    def check_server_connection(self):
        """Check the connection to a PostgreSQL DB server."""
        logging.info('Running test for server connection')
        self.executeQuery(self.default_cursor, 'SELECT version()')
        db_version = self.default_cursor.fetchone()
        logging.info('PostgreSQL database version: %s', db_version)

    def db_exists(self, db_name):
        """Check the existence of a DB in a PostgreSQL DB server."""
        result = None
        sql_query = 'SELECT datname FROM pg_catalog.pg_database WHERE datname=\'' + db_name + '\''
        self.executeQuery(self.default_cursor, sql_query)
        if self.default_cursor.fetchone() is None:
            result = False
        else:
            result = True
        return result

    def table_exists(self, table_name):
        """Check the existence of a table in a DB in a PostgreSQL DB server."""
        result = None
        try:
            # execute a statement
            sql_query = "SELECT * FROM information_schema.tables WHERE table_name=%s"
            self.retrieveCursor.execute(sql_query, (table_name,))
            if self.retrieveCursor.fetchone() is None:
                result = False
            else:
                result = True
            logging.info('Table %s exists: %s', table_name, result)
        except (psycopg2.DatabaseError) as error:
            logging.debug(str(error).rstrip())
        return result

    def count_records(self, table_name):
        """Checks the count of records in the table in a DB in a PostgreSQL DB server."""
        logging.debug('Counting the number of records in table %s in DB %s ', table_name, self.dbInfo['database'])
        result = None
        try:
            # execute a statement
            sql_query = 'SELECT COUNT(*) FROM ' + table_name + ';'
            self.countCursor.execute(sql_query, (table_name,))
            result = self.countCursor.fetchone()[0]
        except (psycopg2.DatabaseError) as error:
            logging.warning(error)
        return result

    def drop_table(table_name):
        """Drop a table in the desired DB."""
        logging.info('Attempting to drop table')
        self.executeQuery(self.storeCursor, 'DROP TABLE ' + table_name + ';')

    def add_table_to_db(self, table_name, columns_info, section_name):
        """Add a table to the desired DB."""
        logging.info('Attempting to add table to DB')

        # Open the json with the list of elements we're interested in
        with open(columns_info) as file_reader:
            elements_json = json.load(file_reader)
        elements = elements_json[section_name]

        # Make the SQL query
        sql_query = 'CREATE TABLE ' + table_name + ' (' + os.linesep + \
            'file_name VARCHAR(255) PRIMARY KEY,' + os.linesep + \
            'file_path VARCHAR(255),' + os.linesep
        for element_name in elements:
            if not elements[element_name]['calculation_only']:
                sql_query = sql_query + element_name + ' ' + elements[element_name]['db_datatype'] \
                    + ',' + os.linesep
        margin_to_remove = -1 * (len(os.linesep) + 1)
        sql_query = sql_query[:margin_to_remove] + ');'
        self.executeQuery(self.storeCursor, sql_query)

    # TODO: Rewrite this function to be more flexible
    def create_new_db(self, db_name):
        """Create a new DB."""
        logging.info('Attempting to create a new DB')
        self.executeQuery(self.default_cursor, 'CREATE DATABASE ' + db_name + ';')

    def import_image_label_data(self):
        """Import data into a table in the desired DB."""
        logging.info('Attempting to import table to DB')

        # Open the json with the list of elements we're interested in
        with open(self.configHandler.getColumnsInfoPath()) as file_reader:
            elements_json = json.load(file_reader)
        elements = elements_json['labels']

        # Make the SQL query
        sql_query = 'COPY ' + self.configHandler.getTableName('label') + '(file_name, file_path, '
        for element_name in elements:
            if not elements[element_name]['calculation_only']:
                sql_query = sql_query + element_name + ','
        sql_query = sql_query[:-1] + ') FROM \'' + self.configHandler.getParentFolder() + "/" + self.configHandler.getCsvPath() + '\' DELIMITER \',\' CSV HEADER;'

        self.executeQuery(self.storeCursor, sql_query)
    
    def executeQuery(self, cursor, query):
        try:
            cursor.execute(query)
        except (psycopg2.DatabaseError) as error:
            logging.warning(error)

