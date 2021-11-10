package trainer

import (
	"CxrClassify/configHandler"
	"CxrClassify/databaseHandler"
	"CxrClassify/runnable"
	"log"
	"os"
)

type Trainer struct {
	runnable.Runnable

	_ func() `constructor:"init"`
}

func (t *Trainer) init() {

}

func (t *Trainer) Setup(configHandler *configHandler.ConfigHandler, databaseHandler *databaseHandler.DatabaseHandler) {
	t.SetupRunnable(configHandler, databaseHandler)
}

func (t Trainer) Run() {
	k, err := os.OpenFile("testlogfile", os.O_RDWR|os.O_CREATE|os.O_APPEND, 0666)
	if err != nil {
		log.Fatalf("error opening file: %v", err)
	}
	defer k.Close()
	log.SetOutput(k)

	t.AttemptUpdateText("Training classifier")
	t.AttemptUpdateProBarBounds(0, t.Expected_num_files)
	t.AttemptUpdateProBarValue(0)
}
