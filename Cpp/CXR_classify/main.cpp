#include <QApplication>
#include "appcontroller.h"

int main(int argc, char **argv) {
    QApplication app(argc, argv);

    AppController appController = AppController();

    return app.exec();
}



