package databaseHandler

import (
	"CxrClassify/configHandler"
	"database/sql"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"os"

	_ "github.com/lib/pq"
)

type DatabaseHandler struct {
	DefaultConnection *sql.DB
	Connection        *sql.DB

	configHandler *configHandler.ConfigHandler

	host     string
	port     string
	database string
	user     string
	password string
}

func NewDatabaseHandler(configHandler *configHandler.ConfigHandler) *DatabaseHandler {
	d := new(DatabaseHandler)
	d.configHandler = configHandler

	dbInfo := d.configHandler.GetDbInfo()

	d.host = dbInfo.Key("host").String()
	d.port = dbInfo.Key("port").String()
	d.database = dbInfo.Key("database").String()
	d.user = dbInfo.Key("user").String()
	d.password = dbInfo.Key("password").String()

	d.DefaultConnection = d.OpenConnection(true)

	if !d.DbExists() {
		d.CreateNewDb()
	}

	d.Connection = d.OpenConnection(false)

	return d
}

func (d DatabaseHandler) Close() {
	d.CloseConnection(d.DefaultConnection)
	d.CloseConnection(d.Connection)
}

func (d DatabaseHandler) OpenConnection(openDefault bool) *sql.DB {
	var params string
	if openDefault {
		params = fmt.Sprintf("host=%s port=%s dbname=postgres user=%s password=%s sslmode=disable", d.host, d.port, d.user, d.password)
	} else {
		params = fmt.Sprintf("host=%s port=%s dbname=%s user=%s password=%s sslmode=disable", d.host, d.port, d.database, d.user, d.password)
	}

	// TODO: replace DATABASE with parameter
	log.Println("Opening connection to DB: %s", "DATABASE")

	db, err := sql.Open("postgres", params)
	if err != nil {
		log.Fatal(err)
	}

	return db
}

func (d DatabaseHandler) CloseConnection(connection *sql.DB) {
	log.Println("Closing connection")
	// TODO: add check for connection being nil
	connection.Close()
}

func (d DatabaseHandler) CheckServerConnection() {
	_, err := d.ExecuteQuery(d.Connection, "SELECT version()")
	if err == nil {
		fmt.Println("Server is connected")
	} else {
		fmt.Println("Server is not connected")
	}
}

func (d DatabaseHandler) CreateNewDb() {
	log.Println("Attempting to drop a new DB")
	sqlQuery := fmt.Sprintf("CREATE DATABASE %s;", d.database)
	d.ExecuteNonTransQuery(d.DefaultConnection, sqlQuery)
}

func (d DatabaseHandler) dropDb() {
	log.Println("Attempting to drop a DB")
	// TODO: add logic
}

func (d DatabaseHandler) DbExists() bool {
	sqlQuery := fmt.Sprintf("SELECT datname FROM pg_catalog.pg_database WHERE datname='%s'", d.database)

	var datname string
	rows, err := d.ExecuteQuery(d.DefaultConnection, sqlQuery)

	if err == nil {
		if rows.Next() {
			err = rows.Scan(&datname)
		}
	}

	// TODO: replace RESULT with rows string conversion
	log.Println("DB named %s existence: %s", datname, "RESULT")

	if datname == d.database {
		return true
	} else {
		return false
	}
}

func (d DatabaseHandler) TableExists(tableName string) bool {
	sqlQuery := fmt.Sprintf("SELECT table_name FROM information_schema.tables WHERE table_name='%s'", tableName)

	var version string

	rows, err := d.ExecuteQuery(d.Connection, sqlQuery)

	if err == nil {
		if rows.Next() {
			err = rows.Scan(&version)
		}
	}

	if version == "" {
		log.Println("Table %s does not exist", tableName)
		return false
	} else {
		// TODO: replace RESULT with rows string conversion
		log.Println("Table %s exists: %s", tableName, "RESULT")
		return true
	}
}

func (d DatabaseHandler) AddTableToDb(columnsInfo, section, tableName string) {
	log.Println("Attempting to add table")
	jsonFile, err := os.Open(columnsInfo)

	if err != nil {
		fmt.Println(err)
	}
	fmt.Println("Successfully Opened users.json")

	defer jsonFile.Close()

	byteValue, _ := ioutil.ReadAll(jsonFile)

	var columnsJson map[string]interface{}
	json.Unmarshal([]byte(byteValue), &columnsJson)

	elements := columnsJson[section].(map[string]interface{})

	sqlQuery := fmt.Sprintf("CREATE TABLE %s (file_name VARCHAR(255) PRIMARY KEY, file_path VARCHAR(255)", tableName)

	for k, v := range elements {
		sqlQuery += (", " + k + " " + v.(map[string]interface{})["db_datatype"].(string))
	}
	sqlQuery += ");"

	d.ExecuteQuery(d.Connection, sqlQuery)
}

func (d DatabaseHandler) CountRecords(tableName string) int {
	var count int

	rows, err := d.ExecuteQuery(d.Connection, "SELECT COUNT(*) FROM "+tableName+";")

	if err == nil {
		if rows.Next() {
			err = rows.Scan(&count)
		}
	}

	return count
}

func (d DatabaseHandler) dropTable(dbName string) {
	log.Println("Attempting to create a new DB")
	// TODO: add logic
	log.Println("Dropped table: TABLE_NAME")
}

func (d DatabaseHandler) ExecuteQuery(connection *sql.DB, query string) (*sql.Rows, error) {
	rows, err := connection.Query(query)
	return rows, err
}

func (d DatabaseHandler) ExecuteNonTransQuery(connection *sql.DB, query string) sql.Result {
	result, err := connection.Exec(query)
	if err == nil {
		log.Println("No error")
	} else {
		log.Println("Error")
	}
	return result
}
