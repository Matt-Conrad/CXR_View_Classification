package storer

import (
	"CxrClassify/configHandler"
	"CxrClassify/databaseHandler"
	"CxrClassify/runnable"
	"encoding/json"
	"io/ioutil"
	"log"
	"os"
	"path/filepath"
	"strconv"
	"strings"

	"github.com/suyashkumar/dicom"
	"github.com/suyashkumar/dicom/pkg/tag"
)

type Storer struct {
	runnable.Runnable

	_ func() `constructor:"init"`

	MetadataTableName string
	ColumnsInfoName   string
}

func (s *Storer) init() {

}

func (s *Storer) Setup(configHandler *configHandler.ConfigHandler, databaseHandler *databaseHandler.DatabaseHandler) {
	s.SetupRunnable(configHandler, databaseHandler)
}

func (s Storer) Run() {
	// logging set up
	f, err := os.OpenFile("testlogfile", os.O_RDWR|os.O_CREATE|os.O_APPEND, 0666)
	if err != nil {
		log.Fatalf("error opening file: %v", err)
	}
	defer f.Close()
	log.SetOutput(f)

	s.AttemptUpdateText("Storing metadata")
	s.AttemptUpdateProBarBounds(0, 10)

	s.MetadataTableName = s.ConfigHandler.GetTableName("metadata")
	s.ColumnsInfoName = s.ConfigHandler.GetColumnsInfoName()

	if !s.DatabaseHandler.TableExists(s.MetadataTableName) {
		s.DatabaseHandler.AddTableToDb(s.ColumnsInfoName, "elements", s.MetadataTableName)
	}

	s.AttemptUpdateProBarValue(0)

	jsonFile, err := os.Open(s.ColumnsInfoName)
	if err != nil {
		s.AttemptUpdateText("DF")
	}
	defer jsonFile.Close()

	byteValue, _ := ioutil.ReadAll(jsonFile)

	var columnsJson map[string]interface{}
	json.Unmarshal([]byte(byteValue), &columnsJson)

	elements := columnsJson["elements"].(map[string]interface{})

	var storeCount = 0
	err = filepath.Walk(s.ConfigHandler.GetUnpackFolderPath(),
		func(path string, info os.FileInfo, err error) error {

			if err != nil {
				return err
			}

			fileExtension := filepath.Ext(path)

			if fileExtension == ".dcm" {
				dataset, _ := dicom.ParseFile(path, nil)

				for k, v := range elements {
					tagString := v.(map[string]interface{})["tag"].(string)
					tagSlice := strings.Split(tagString, ",")

					groupNameString := strings.Replace(strings.TrimSpace(tagSlice[0]), "0x", "", -1)
					elementNumString := strings.Replace(strings.TrimSpace(tagSlice[1]), "0x", "", -1)

					groupNameInt, _ := strconv.ParseUint(groupNameString, 16, 64)
					elementNumInt, _ := strconv.ParseUint(elementNumString, 16, 64)

					_, err := dataset.FindElementByTag(tag.Tag{Group: uint16(groupNameInt), Element: uint16(elementNumInt)})

					if err == nil {
						dbDatatype := v.(map[string]interface{})["db_datatype"].(string)
						elem, _ := dataset.FindElementByTag(tag.Tag{Group: uint16(groupNameInt), Element: uint16(elementNumInt)})
						if strings.Contains(dbDatatype, "INT") {
							value := elem.Value.String()
							elements[k].(map[string]interface{})["value"] = elem.Value.String()[1 : len(value)-1]
						} else if strings.Contains(dbDatatype, "CHAR") {
							value := elem.Value.String()
							elements[k].(map[string]interface{})["value"] = "'" + elem.Value.String()[1:len(value)-1] + "'"
						}
					} else {
						elements[k].(map[string]interface{})["value"] = "NULL"
					}
				}

				names := []string{"file_name", "file_path"}
				values := []string{"'" + filepath.Base(path) + "'", "'" + path + "'"}

				for k, v := range elements {
					if !v.(map[string]interface{})["calculation_only"].(bool) {
						names = append(names, k)
						values = append(values, v.(map[string]interface{})["value"].(string))
					}
				}

				sqlQuery := "INSERT INTO " + s.MetadataTableName + " (" + strings.Join(names, ", ") + ") VALUES (" + strings.Join(values, ", ") + ");"

				s.DatabaseHandler.ExecuteQuery(s.DatabaseHandler.Connection, sqlQuery)

				storeCount++

				s.AttemptUpdateProBarValue(storeCount)
			}

			return nil
		})
	if err != nil {
		log.Println("FAIL")
	}

	// sqlQuery := elements["patient_orientation"].(map[string]interface{})["db_datatype"].(string)

	// d.ExecuteQuery(d.Connection, sqlQuery)

	s.AttemptUpdateText("Done storing metadata")
	s.Finished()
}

// func (s Storer) CreateSqlQuery(tableName string, elements) {
