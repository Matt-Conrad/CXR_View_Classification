package trainer

import (
	"CxrClassify/configHandler"
	"CxrClassify/databaseHandler"
	"CxrClassify/runnable"
	"fmt"
	"log"
	"os"

	"github.com/lib/pq"
	"github.com/sjwhitworth/golearn/base"
	"github.com/sjwhitworth/golearn/evaluation"
	"github.com/sjwhitworth/golearn/knn"
	"gonum.org/v1/gonum/mat"
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

	sqlQuery := "SELECT file_name, hor_profile, vert_profile FROM " + t.ConfigHandler.GetTableName("features") + " ORDER BY file_path ASC;"

	profileResults, _ := t.DatabaseHandler.ExecuteQuery(t.DatabaseHandler.Connection, sqlQuery)

	fileNames := []string{}
	rawData := mat.NewDense(t.Expected_num_files, 400, nil)
	fileIndex := 0
	for profileResults.Next() {
		var fileName string
		var horProfile []float64
		var vertProfile []float64

		profileResults.Scan(&fileName, pq.Array(&horProfile), pq.Array(&vertProfile))
		fileNames = append(fileNames, fileName)

		fullProfile := append(horProfile, vertProfile...)
		fullProfile = append(fullProfile)
		rawData.SetRow(fileIndex, fullProfile)
		fileIndex++
	}

	instances := base.InstancesFromMat64(t.Expected_num_files, 400, rawData)
	oldInst := base.NewDenseCopy(instances)
	newInst := base.NewDenseInstances()

	// Create some Attributes
	attr := new(base.CategoricalAttribute)
	attr.SetName("Laterality")
	attr.GetSysValFromString("F")
	attr.GetSysValFromString("L")

	// Add the attributes
	newSpecs := make([]base.AttributeSpec, 401)
	oldSpecs := make([]base.AttributeSpec, 400)

	for i, a := range instances.AllAttributes() {
		s, err := oldInst.GetAttribute(a)
		if err != nil {
			panic(err)
		}
		oldSpecs[i] = s
		newSpecs[i] = newInst.AddAttribute(a)
	}

	newSpecs[400] = newInst.AddAttribute(attr)
	classAttr := base.GetAttributeByName(newInst, "Laterality")
	newInst.AddClassAttribute(classAttr)

	// Allocate memory
	// _, rows := newInst.Size()
	newInst.Extend(10)

	// Copy each row from the old one to the new
	oldInst.MapOverRows(oldSpecs, func(v [][]byte, r int) (bool, error) {
		for i, c := range v {
			newInst.Set(newSpecs[i], r, c)
		}
		return true, nil
	})

	// Allocate space
	// newInst.Extend(10)

	// // Write the data
	// newInst.Set(newSpecs[0], 0, newSpecs[0].GetAttribute().GetSysValFromString("1"))

	// Put all labels into a list
	sqlQuery = "SELECT image_view FROM " + t.ConfigHandler.GetTableName("label") + " ORDER BY file_path ASC;"

	// Execute query
	y := []int{}
	labelsResult, _ := t.DatabaseHandler.ExecuteQuery(t.DatabaseHandler.Connection, sqlQuery)
	count := 0
	for labelsResult.Next() {
		var label string
		labelsResult.Scan(&label)

		if label == "F" {
			log.Println("FEFW")
			y = append(y, 0)
			newInst.Set(newSpecs[400], count, newSpecs[400].GetAttribute().GetSysValFromString("F"))

		} else if label == "L" {
			log.Println("ASDF")
			y = append(y, 1)
			newInst.Set(newSpecs[400], count, newSpecs[400].GetAttribute().GetSysValFromString("L"))
		}
		count++
	}

	// log.Println(newInst)

	// rawData2, err := base.ParseCSVToInstances("iris.csv", false)
	// if err != nil {
	// 	panic(err)
	// }

	// // Print a pleasant summary of your data.
	// log.Println(rawData2)

	// //Initialises a new SVM classifier
	// cls, err := linear_models.NewLinearSVC("l1", "l2", true, 1.0, 1e-4)

	cls := knn.NewKnnClassifier("euclidean", "linear", 2)
	//Do a training-test split
	trainData, testData := base.InstancesTrainTestSplit(newInst, 0.33)
	cls.Fit(trainData)

	//Calculates the Euclidean distance and returns the most popular label
	predictions, err := cls.Predict(testData)
	if err != nil {
		panic(err)
	}

	// Prints precision/recall metrics
	confusionMat, err := evaluation.GetConfusionMatrix(testData, predictions)
	if err != nil {
		panic(fmt.Sprintf("Unable to get confusion matrix: %s", err.Error()))
	}
	log.Println(evaluation.GetSummary(confusionMat))
}
