package manualLabeler

import (
	"CxrClassify/configHandler"
	"CxrClassify/databaseHandler"
	"CxrClassify/runnable"
	"database/sql"
	"fmt"
	"image/png"
	"log"
	"os"
	"strconv"

	"github.com/suyashkumar/dicom"
	"github.com/suyashkumar/dicom/pkg/tag"
)

type ManualLabeler struct {
	runnable.Runnable

	_ func() `constructor:"init"`

	count int

	labelTableName string

	imageList *sql.Rows
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
	k, err := os.OpenFile("testlogfile", os.O_RDWR|os.O_CREATE|os.O_APPEND, 0666)
	if err != nil {
		log.Fatalf("error opening file: %v", err)
	}
	defer k.Close()
	log.SetOutput(k)

	m.queryImageList()

	m.AttemptUpdateText("Please manually label images")
	m.AttemptUpdateProBarBounds(0, m.Expected_num_files)

	// m.DatabaseHandler.AddTableToDb(m.ConfigHandler.GetColumnsInfoName(), "labels", m.labelTableName)

	m.displayNextImage()

	// for m.count < m.Expected_num_files {

	// }

	// m.AttemptUpdateText("Image labeling complete")
	// m.AttemptUpdateProBarValue(m.count)
	// m.Finished()
}

func (m *ManualLabeler) queryImageList() {
	sqlQuery := "SELECT file_path FROM " + m.ConfigHandler.GetTableName("metadata") + " ORDER BY file_path;"

	m.imageList, _ = m.DatabaseHandler.ExecuteQuery(m.DatabaseHandler.Connection, sqlQuery)

	// defer m.imageList.Close()
}

func (m *ManualLabeler) displayNextImage() {
	m.AttemptUpdateText("Image count: " + strconv.Itoa(m.count))
	m.AttemptUpdateProBarValue(m.DatabaseHandler.CountRecords(m.ConfigHandler.GetTableName("label")))

	var filePath string
	if m.count < m.Expected_num_files {
		m.imageList.Next()
		m.imageList.Scan(&filePath)

		dataset, err := dicom.ParseFile(filePath, nil)
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

		fileObj, err := os.Create(fmt.Sprintf("tmp.png"))
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
	}
}
