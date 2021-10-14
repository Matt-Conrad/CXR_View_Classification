package configHandler

import (
	"expectedSizes"
	"os"
	"path/filepath"
	"strings"

	"gopkg.in/ini.v1"
)

type ConfigHandler struct {
	configFilename string
	configFile     ini.File
}

func NewConfigHandler(configFilename string) *ConfigHandler {
	c := new(ConfigHandler)
	c.configFilename = configFilename
	c.readConfigFile()
	c.prepConfigIni()
	return c
}

func (c ConfigHandler) Close() {
	c.configFile.SaveTo("test.ini") // change to c.configFilename
}

func (c ConfigHandler) getSection(sectionName string) ini.Section {
	return *c.configFile.Section(sectionName)
}

func (c ConfigHandler) getSetting(sectionName, settingName string) string {
	section := c.getSection(sectionName)
	return section.Key(settingName).String()
}

func (c ConfigHandler) setSetting(sectionName, settingName, value string) {
	c.configFile.Section(sectionName).Key(settingName).SetValue(value)
}

func (c ConfigHandler) prepConfigIni() {
	c.setUrl(expectedSizes.SourceUrl[c.GetDatasetType()])
	c.setParentFolder()
	c.setCsvName()
	c.setColumnsInfoName()
}

func (c *ConfigHandler) readConfigFile() {
	if _, err := os.Stat(c.configFilename); err == nil {
		// path/to/whatever exists
		cfg, _ := ini.Load(c.configFilename)
		c.configFile = *cfg
	}
}

func (c ConfigHandler) setUrl(url string) {
	c.setSetting("misc", "url", url)
}

func (c ConfigHandler) setParentFolder() {
	path, _ := os.Getwd()
	c.setSetting("misc", "parent_folder", path)
}

func (c ConfigHandler) setCsvName() {
	c.setSetting("misc", "csv_filename", "image_labels.csv")
}

func (c ConfigHandler) setColumnsInfoName() {
	c.setSetting("misc", "columns_info_name", "columns_info.json")
}

func (c ConfigHandler) GetDbInfo() ini.Section {
	return c.getSection("postgresql")
}

func (c ConfigHandler) GetTableName(table string) string {
	return c.getSetting("table_names", table)
}

func (c ConfigHandler) GetUrl() string {
	return c.getSetting("misc", "url")
}

func (c ConfigHandler) GetTgzFilename() string {
	url := c.GetUrl()
	basename := filepath.Base(url)
	return basename
}

func (c ConfigHandler) GetTgzFilePath() string {
	return c.PrependParentPath(c.GetTgzFilename())
}

func (c ConfigHandler) GetDatasetName() string {
	basename := c.GetTgzFilename()
	nameWithoutExt := strings.TrimSuffix(basename, filepath.Ext(basename))
	return nameWithoutExt
}

func (c ConfigHandler) GetUnpackFolderPath() string {
	return c.PrependParentPath(c.GetDatasetName())
}

func (c ConfigHandler) GetColumnsInfoName() string {
	return c.getSetting("misc", "columns_info_name")
}

func (c ConfigHandler) GetColumnsInfoPath() string {
	return c.PrependParentPath(c.GetColumnsInfoName())
}

func (c ConfigHandler) GetCsvName() string {
	return c.getSetting("misc", "csv_filename")
}

func (c ConfigHandler) GetCsvPath() string {
	return c.PrependParentPath(c.GetCsvName())
}

func (c ConfigHandler) GetDatasetType() string {
	return c.getSetting("dataset_info", "dataset")
}

func (c ConfigHandler) GetParentFolder() string {
	return c.getSetting("misc", "parent_folder")
}

func (c ConfigHandler) GetLogLevel() string {
	return c.getSetting("logging", "level")
}

func (c ConfigHandler) GetConfigFilename() string {
	return c.configFilename
}

func (c ConfigHandler) GetConfigFilePath() string {
	return c.PrependParentPath(c.GetConfigFilename())
}

func (c ConfigHandler) PrependParentPath(fsItem string) string {
	strArr := []string{c.GetParentFolder(), fsItem}
	return strings.Join(strArr, "\\")
}
