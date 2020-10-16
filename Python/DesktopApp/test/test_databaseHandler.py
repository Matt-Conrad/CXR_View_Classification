import pytest
import psycopg2
import psycopg2.extensions

class TestDatabaseHandler:
    @pytest.fixture(autouse=True)
    def initDatabaseHandler(self, databaseHandler):
        self.dbHandler = databaseHandler

    def test_openConnection(self):
        connection = self.dbHandler.openConnection()
        dbInfo = self.dbHandler.configHandler.getDbInfo()
        assert connection.info.dbname == dbInfo["database"]
        assert connection.info.host == dbInfo["host"]
        assert connection.info.port == int(dbInfo["port"])
        assert connection.info.user == dbInfo["user"]
        assert connection.info.password == dbInfo["password"]

    def test_closeConnection(self):
        connection = self.dbHandler.openConnection()
        self.dbHandler.closeConnection(connection)
        assert connection.info.status == 1 # connection bad 

    def test_dbExists(self):
        assert not self.dbHandler.dbExists("asdlkfjasdf")
        assert self.dbHandler.dbExists(self.dbHandler.configHandler.getDbInfo()["database"])
    
    def test_tableExists(self):
        connection = self.dbHandler.openConnection()
        cursor = connection.cursor()
        cursor.execute("CREATE TABLE test (column1 INTEGER);")
        assert self.dbHandler.tableExists("test")
        cursor.execute("DROP TABLE test;")
        assert not self.dbHandler.tableExists("test")

    def test_countRecords(self):
        connection = self.dbHandler.openConnection()
        cursor = connection.cursor()
        assert self.dbHandler.countRecords("test") == 0
        cursor.execute("CREATE TABLE test (column1 INTEGER);")
        assert self.dbHandler.countRecords("test") == 0
        for i in range(10):
            cursor.execute("INSERT INTO test (column1) VALUES (%s);", (i,))
        assert self.dbHandler.countRecords("test") == 10

    def test_dropTable(self):
        connection = self.dbHandler.openConnection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM information_schema.tables WHERE table_name=\'test\';")
        assert cursor.fetchone() is None
        cursor.execute("CREATE TABLE test (column1 INTEGER);")
        cursor.execute("SELECT * FROM information_schema.tables WHERE table_name=\'test\';")
        assert cursor.fetchone() is not None
        self.dbHandler.dropTable("test")
        cursor.execute("SELECT * FROM information_schema.tables WHERE table_name=\'test\';")
        assert cursor.fetchone() is None

