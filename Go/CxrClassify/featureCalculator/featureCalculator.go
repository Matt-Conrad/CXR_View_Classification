package featureCalculator

import (
	"CxrClassify/configHandler"
	"CxrClassify/databaseHandler"
	"CxrClassify/runnable"
	"fmt"
	"image"
	"image/png"
	"log"
	"math"
	"os"
	"path/filepath"
	"strconv"
	"strings"
	"time"

	"github.com/suyashkumar/dicom"
	"github.com/suyashkumar/dicom/pkg/tag"
	"gocv.io/x/gocv"
)

type FeatureCalculator struct {
	runnable.Runnable

	featTableName string

	_ func() `constructor:"init"`
}

func (f *FeatureCalculator) init() {

}

func (f *FeatureCalculator) Setup(configHandler *configHandler.ConfigHandler, databaseHandler *databaseHandler.DatabaseHandler) {
	f.featTableName = configHandler.GetTableName("features")
	f.SetupRunnable(configHandler, databaseHandler)
}

func (f FeatureCalculator) Run() {
	k, err := os.OpenFile("testlogfile", os.O_RDWR|os.O_CREATE|os.O_APPEND, 0666)
	if err != nil {
		log.Fatalf("error opening file: %v", err)
	}
	defer k.Close()
	log.SetOutput(k)

	log.Printf("Calculating features from images")

	f.AttemptUpdateText("Calculating features")
	f.AttemptUpdateProBarBounds(0, f.Expected_num_files)

	f.DatabaseHandler.AddTableToDb(f.ConfigHandler.GetColumnsInfoName(), "features_list", f.featTableName)

	f.AttemptUpdateProBarValue(0)
	sqlQuery := "SELECT file_path FROM " + f.ConfigHandler.GetTableName("metadata") + ";"
	rows, _ := f.DatabaseHandler.ExecuteQuery(f.DatabaseHandler.Connection, sqlQuery)

	var filePath string
	if err == nil {
		count := 0
		for rows.Next() {
			log.Printf("Calculating for image number: %d File: %s", count+1, filePath)
			err = rows.Scan(&filePath)
			if err == nil {
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

				// bounds := pixelData.Bounds()
				// width, height := bounds.Max.X, bounds.Max.Y

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

				time.Sleep(time.Second)

				imageUnsigned := gocv.IMRead("tmp.png", gocv.IMReadAnyDepth)

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
				defer imageFloat.Close()
				imageUnsigned.ConvertTo(&imageFloat, gocv.MatTypeCV32F)

				imageFloat.DivideFloat(float32(highestPossibleIntensity)) // Conversion loses precision

				imageFloatFlat := imageFloat.Reshape(1, 1)
				imageNormSorted := gocv.NewMatWithSize(imageFloatFlat.Rows(), imageFloatFlat.Cols(), gocv.MatTypeCV32F)
				gocv.Sort(imageFloatFlat, &imageNormSorted, gocv.SortAscending)

				nPixels := float32(imageUnsigned.Rows() * imageUnsigned.Cols())

				firstIndex := int(0.01 * nPixels)
				ninenineIndex := int(0.99 * nPixels)

				firstPercentile := imageNormSorted.GetFloatAt(0, firstIndex)
				nineninePercentile := imageNormSorted.GetFloatAt(0, ninenineIndex)

				// Perform the contrast stretch
				enhancedImage := imageFloat.Clone()
				enhancedImage.SubtractFloat(firstPercentile)
				enhancedImage.DivideFloat(nineninePercentile - firstPercentile)

				for i := 0; i < enhancedImage.Rows(); i++ {
					for j := 0; j < enhancedImage.Cols(); j++ {

						if enhancedImage.GetFloatAt(i, j) < firstPercentile {
							// log.Printf("Float: %f", enhancedImage.GetFloatAt(i, j))
							enhancedImage.SetFloatAt(i, j, 0.0)
						} else if enhancedImage.GetFloatAt(i, j) > nineninePercentile {
							// log.Printf("Float: %f", enhancedImage.GetFloatAt(i, j))
							enhancedImage.SetFloatAt(i, j, 1.0)
						}

					}
				}

				// Calculate the median
				enhancedImageFlat := enhancedImage.Reshape(1, 1)
				enhancedImageSort := gocv.NewMatWithSize(enhancedImageFlat.Rows(), enhancedImageFlat.Cols(), gocv.MatTypeCV32F)
				gocv.Sort(enhancedImageFlat, &enhancedImageSort, gocv.SortAscending)
				medianIndex := int(0.50 * nPixels)
				median := enhancedImageSort.GetFloatAt(0, medianIndex)

				// min, max, _, _ := gocv.MinMaxLoc(enhancedImageFlat)

				// log.Printf("Min: %f, Max: %f", min, max)
				// log.Println(median)

				// Threshold the image at median
				enhancedImageDouble := gocv.NewMat()
				defer enhancedImageDouble.Close()
				enhancedImage.ConvertTo(&enhancedImageDouble, gocv.MatTypeCV32F)
				imageBinarized := gocv.NewMatWithSize(enhancedImage.Rows(), enhancedImage.Cols(), gocv.MatTypeCV32F)
				gocv.Threshold(enhancedImageDouble, &imageBinarized, median, 1.0, gocv.ThresholdBinary)

				// Crop image
				points := gocv.NewMat()
				gocv.FindNonZero(imageBinarized, &points)
				pointVec := gocv.NewPointVectorFromMat(points)
				bb := gocv.BoundingRect(pointVec)

				imageCropped := gocv.NewMat()
				if pointVec.Size() > 0 {
					imageCropped = enhancedImageDouble.Region(bb)
				} else {
					log.Println("ERROR")
				}

				// window := gocv.NewWindow("Hello")
				// window.IMShow(imageCropped)
				// window.WaitKey(0)

				// Scale image
				scalePercent := 0.5
				newWidth := int(float64(imageCropped.Cols()) * scalePercent)
				newHeight := int(float64(imageCropped.Rows()) * scalePercent)

				imageDownsize := gocv.NewMatWithSize(newHeight, newWidth, gocv.MatTypeCV64F)
				gocv.Resize(imageCropped, &imageDownsize, image.Pt(newWidth, newHeight), 0.5, 0.5, gocv.InterpolationArea)

				imageResize := gocv.NewMatWithSize(200, 200, gocv.MatTypeCV64F)
				gocv.Resize(imageDownsize, &imageResize, image.Pt(200, 200), 0, 0, gocv.InterpolationArea)

				horProfile := gocv.NewMatWithSize(1, 200, gocv.MatTypeCV64F)
				gocv.Reduce(imageResize, &horProfile, 0, gocv.ReduceAvg, gocv.MatTypeCV64F)

				vertProfile := gocv.NewMatWithSize(200, 1, gocv.MatTypeCV64F)
				gocv.Reduce(imageResize, &vertProfile, 1, gocv.ReduceAvg, gocv.MatTypeCV64F)

				// Create SQL Query

				log.Printf("Storing the calculated features into the database.")

				horVecString := []string{}
				vertVecString := []string{}

				for i := 0; i < 200; i++ {
					horVecString = append(horVecString, fmt.Sprint(enhancedImage.GetFloatAt(0, i)))
					vertVecString = append(vertVecString, fmt.Sprint(enhancedImage.GetFloatAt(i, 0)))
				}

				sqlQuery := "INSERT INTO " + f.ConfigHandler.GetTableName("features") + " (file_name, file_path, hor_profile, vert_profile) VALUES ('" + filepath.Base(filePath) + "', '" + filePath + "', '{" + strings.Join(horVecString, ", ") + "}', '{" + strings.Join(vertVecString, ", ") + "}');"

				connection := f.DatabaseHandler.OpenConnection(false)

				f.DatabaseHandler.ExecuteQuery(connection, sqlQuery)

				connection.Close()

				// cv::Mat imageCropped;
				// if (!points.empty()) {
				// 	imageCropped = imageFloat(bb);
				// } else {
				// 	imageCropped = imageFloat;
				// }

				// log.Println(median)
			}
			count++
		}
	}

	log.Println("Done calculating features from images")

	f.AttemptUpdateText("Done calculating features")
	f.AttemptUpdateProBarValue(f.DatabaseHandler.CountRecords(f.featTableName))
	f.Finished()
}
