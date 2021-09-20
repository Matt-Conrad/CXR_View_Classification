package main

import (
	"CxrClassify/configHandler"
	// "fmt"
)

func main() {
	var c *configHandler.ConfigHandler = configHandler.NewConfigHandler("config.ini")

	(*c).GetTgzFilename()
	defer (*c).Close()
	// fmt.Println((*c).GetSetting("misc", "parent_folder"))
}
