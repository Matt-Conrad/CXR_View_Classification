package manualLabeler

import (
	"CxrClassify/configHandler"
	"CxrClassify/databaseHandler"
	"CxrClassify/runnable"
)

type ManualLabeler struct {
	runnable.Runnable

	_ func() `constructor:"init"`

	count int

	labelTableName string

	// imageList pqxx::result
	// record pqxx::result::const_iterator
}

func (m *ManualLabeler) init() {

}

func (m *ManualLabeler) Setup(configHandler *configHandler.ConfigHandler, databaseHandler *databaseHandler.DatabaseHandler) {
	m.SetupRunnable(configHandler, databaseHandler)
	m.count = 0
	m.labelTableName = m.ConfigHandler.GetTableName("label")
}

func (m ManualLabeler) Run() {
	m.AttemptUpdateText("Please manually label images")
	m.AttemptUpdateProBarBounds(0, m.Expected_num_files)

	// m.DatabaseHandler.AddTableToDb(m.ConfigHandler.GetColumnsInfoName(), "labels", m.labelTableName)

	// displayNextImage

	// for m.count < m.Expected_num_files {

	// }

	m.AttemptUpdateText("Image labeling complete")
	m.AttemptUpdateProBarValue(m.count)
	m.Finished()
}
