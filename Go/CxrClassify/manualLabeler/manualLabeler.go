package manualLabeler

import (
	"CxrClassify/configHandler"
	"CxrClassify/databaseHandler"
	"CxrClassify/runnable"
	"database/sql"
	"image/png"
	"log"
	"math"
	"os"
	"path/filepath"
	"strconv"
	"time"

	"github.com/suyashkumar/dicom"
	"github.com/suyashkumar/dicom/pkg/tag"
	"gocv.io/x/gocv"
)

type ManualLabeler struct {
	runnable.Runnable

	_ func() `constructor:"init"`

	count int

	labelTableName string

	imageList *sql.Rows
	filePath  string
}

func (m *ManualLabeler) init() {

}

func (m *ManualLabeler) Setup(configHandler *configHandler.ConfigHandler, databaseHandler *databaseHandler.DatabaseHandler) {
	m.SetupRunnable(configHandler, databaseHandler)
	m.count = 0
	m.labelTableName = m.ConfigHandler.GetTableName("label")
}

func (m *ManualLabeler) Run() {
	k, err := os.OpenFile("testlogfile", os.O_RDWR|os.O_CREATE|os.O_APPEND, 0666)
	if err != nil {
		log.Fatalf("error opening file: %v", err)
	}
	defer k.Close()
	log.SetOutput(k)

	log.Println("Filling window")

	m.queryImageList()

	m.AttemptUpdateText("Please manually label images")
	m.AttemptUpdateProBarBounds(0, m.Expected_num_files)

	m.DatabaseHandler.AddTableToDb(m.ConfigHandler.GetColumnsInfoName(), "labels", m.labelTableName)

	m.displayNextImage()

	// for m.count < m.Expected_num_files {

	// }

	// log.Println("End of query")
	// m.AttemptUpdateText("Image labeling complete")
	// m.Finished()
}

func (m *ManualLabeler) Frontal() {
	log.Println("Front")
	m.storeLabel("F")
	m.count++
	m.displayNextImage()
}

func (m *ManualLabeler) Lateral() {
	log.Println("Lateral")
	m.storeLabel("L")
	m.count++
	m.displayNextImage()
}

func (m *ManualLabeler) displayNextImage() {
	log.Printf("Image count: %d", m.count)
	m.AttemptUpdateText("Image count: " + strconv.Itoa(m.count))
	m.AttemptUpdateProBarValue(m.DatabaseHandler.CountRecords(m.ConfigHandler.GetTableName("label")))

	if m.count < m.Expected_num_files {
		m.imageList.Next()
		m.imageList.Scan(&(m.filePath))

		dataset, err := dicom.ParseFile(m.filePath, nil)
		if err != nil {
			log.Println(err)
		}

		pixelDataElement, err := dataset.FindElementByTag(tag.PixelData)
		if err != nil {
			log.Println(err)
		}
		pixelDataInfo := dicom.MustGetPixelDataInfo(pixelDataElement.Value)
		frame := pixelDataInfo.Frames[0]

		pixelData, err := frame.GetImage() // Intensity range of 0 - 2^bits_stored

		if err != nil {
			log.Println(err)
		}

		// Save image to transfer to gocv
		fileObj, err := os.Create("tmp.png")
		if err != nil {
			log.Println(err)
		}
		err = png.Encode(fileObj, pixelData)
		if err != nil {
			log.Println(err)
		}
		err = fileObj.Close()
		if err != nil {
			log.Println(err)
		}

		time.Sleep(time.Second)

		imageUnsigned := gocv.IMRead("tmp.png", gocv.IMReadAnyDepth)

		// Image correction for display
		pixelDataElement, err = dataset.FindElementByTag(tag.Tag{Group: 40, Element: 257})
		if err != nil {
			log.Println(err)
		}
		value := pixelDataElement.Value.String()
		value = value[1 : len(value)-1]
		bitsStored, err := strconv.ParseFloat(value, 64)
		if err != nil {
			log.Println(err)
		}

		highestPossibleIntensity := math.Pow(2, bitsStored) - 1

		imageFloat := gocv.NewMat()

		imageUnsigned.ConvertTo(&imageFloat, gocv.MatTypeCV32F)

		imageFloat.DivideFloat(float32(highestPossibleIntensity)) // Conversion loses precision

		imageFloat.MultiplyFloat(float32(255))

		// Save image
		gocv.IMWrite("tmp.png", imageFloat)

		// Miscellaneous code

		// originalImage := gocv.IMRead("tmp.png", gocv.IMReadGrayScale)
		// imageSquare := gocv.NewMatWithSize(300, 300, gocv.MatTypeCV8U)
		// gocv.Resize(originalImage, &imageSquare, image.Pt(300, 300), 0, 0, gocv.InterpolationArea)

		// // bounds := pixelData.Bounds()
		// // width, height := bounds.Max.X, bounds.Max.Y
		// imageData, _ := imageSquare.DataPtrUint8()
		// qImage := gui.NewQImageFromPointer(unsafe.Pointer(&imageData))
		// // gui.NewQImage4(string(imageData), width, height, gui.QImage__Format_Grayscale8)
		// qPixmap := gui.NewQPixmap().FromImage(qImage, 0)
		// // gui.NewQPixmap3("tmp.png", gui.QImage__Format_Grayscale8, nil)

		// qPixmap.Save("TEss", "PNG", -1)
		// m.AttemptUpdateImage(qPixmap)
		// window := gocv.NewWindow("Hello")
		// window.IMShow(imageSquare)
		// window.WaitKey(0)

		m.AttemptUpdateImage("tmp.png")
	} else {
		m.AttemptUpdateText("Image labeling complete")
		m.AttemptUpdateProBarValue(m.count)
		m.Finished()
	}
}

func (m *ManualLabeler) storeLabel(decision string) {
	log.Println("Getting the image list")
	fileName := filepath.Base(m.filePath)
	sqlQuery := "INSERT INTO " + m.labelTableName + "  (file_name, file_path, image_view) VALUES ('" + fileName + "', '" + m.filePath + "', '" + decision + "');"

	m.DatabaseHandler.ExecuteQuery(m.DatabaseHandler.Connection, sqlQuery)
}

func (m *ManualLabeler) queryImageList() {
	log.Println("Storing label")
	sqlQuery := "SELECT file_path FROM " + m.ConfigHandler.GetTableName("metadata") + " ORDER BY file_path;"

	m.imageList, _ = m.DatabaseHandler.ExecuteQuery(m.DatabaseHandler.Connection, sqlQuery)

	// defer m.imageList.Close()
}
