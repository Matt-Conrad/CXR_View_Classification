#include <QApplication>
#include "appcontroller.h"
#include "confighandlers.h"

int main(int argc, char **argv) {
    QApplication app(argc, argv);

    AppController appController = AppController();

    return app.exec();
}


//#include "dcmtk/dcmimgle/dcmimage.h"
//#include <iostream>
//using namespace std;

//int main()
//{
//    DicomImage * image = new DicomImage("/home/matthew/Documents/CXR_Classification/Cpp/build-CXR_classify-Desktop_Qt_5_9_8_GCC_64bit-Debug/NLMCXR_subset_dataset/1/1_IM-0001-3001.dcm");
//    cout << image->getHeight() << endl;

//    delete image;
//    return 0;
//}
