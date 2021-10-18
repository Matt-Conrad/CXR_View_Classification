package unpacker

import (
	"CxrClassify/configHandler"
	"CxrClassify/runnable"
	"archive/tar"
	"compress/gzip"
	"io"
	"os"
)

type Unpacker struct {
	runnable.Runnable

	_ func() `constructor:"init"`

	FolderAbsPath string
}

func (u *Unpacker) init() {

}

func (u *Unpacker) Setup(configHandler *configHandler.ConfigHandler) {
	u.SetupRunnable(configHandler)
	u.FolderAbsPath = u.ConfigHandler.GetUnpackFolderPath()
}

func (u Unpacker) Run() {
	u.AttemptUpdateText("Unpacking images")
	u.AttemptUpdateProBarBounds(0, 10)
	u.AttemptUpdateProBarValue(0)

	r, err := os.Open(u.ConfigHandler.GetTgzFilePath())
	if err != nil {
		u.AttemptUpdateText("error")
	}
	u.ExtractTarGz(r)

	u.AttemptUpdateProBarValue(10) //TODO: Change to use countDcms()
	u.AttemptUpdateText("Images unpacked")
	u.Finished()
}

func (u Unpacker) ExtractTarGz(gzipStream io.Reader) {
	uncompressedStream, err := gzip.NewReader(gzipStream)
	if err != nil {
		u.AttemptUpdateText("ExtractTarGz: NewReader failed")
	}

	tarReader := tar.NewReader(uncompressedStream)

	for true {
		header, err := tarReader.Next()

		if err == io.EOF {
			break
		}

		if err != nil {
			u.AttemptUpdateText("ExtractTarGz: Next() failed: %s")
		}

		switch header.Typeflag {
		case tar.TypeDir:
			if err := os.Mkdir(header.Name, 0755); err != nil {
				u.AttemptUpdateText("ExtractTarGz: Mkdir() failed: %s")
			}
		case tar.TypeReg:
			outFile, err := os.Create(header.Name)
			if err != nil {
				u.AttemptUpdateText("ExtractTarGz: Create() failed: %s")
			}
			if _, err := io.Copy(outFile, tarReader); err != nil {
				u.AttemptUpdateText("ExtractTarGz: Copy() failed: %s")
			}
			outFile.Close()

		default:
			u.AttemptUpdateText("ExtractTarGz: uknown type: %s in %s")
		}

	}
}

func (u *Unpacker) countDcms() int {
	return 0
}
