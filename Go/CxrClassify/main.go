package main

import (
	"CxrClassify/configHandler"
	"CxrClassify/databaseHandler"
	"fmt"
)

func main() {
	var c *configHandler.ConfigHandler = configHandler.NewConfigHandler("config.ini")
	var d *databaseHandler.DatabaseHandler = databaseHandler.NewDatabaseHandler(c)

	fmt.Println(d.CountRecords("test"))

	defer (*d).Close()
	defer (*c).Close()
	// fmt.Println((*c).GetSetting("misc", "parent_folder"))
}
