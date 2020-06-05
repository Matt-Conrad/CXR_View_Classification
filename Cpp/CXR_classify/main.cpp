#include <QApplication>
#include "appcontroller.h"
#include "confighandlers.h"

int main(int argc, char **argv) {
    QApplication app(argc, argv);

    AppController appController = AppController();

    return app.exec();
}
