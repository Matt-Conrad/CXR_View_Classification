#ifndef MAINAPPLICATION_H
#define MAINAPPLICATION_H

#include <QMainWindow>
#include <QWidget>
#include <QPushButton>
#include <QGridLayout>
#include <QLabel>
#include <QProgressBar>
#include <QStackedWidget>
#include <QVBoxLayout>
#include <QString>
#include <stage.h>
#include <runnable.h>

class AppController;

class MainWindow : public QMainWindow
{
    Q_OBJECT
public:
    MainWindow(AppController * controller);

private:
    AppController * controller;

    QString buttonsList[6] = {"downloadBtn", "unpackBtn", "storeBtn", "featureBtn", "labelBtn", "trainBtn"};

    QStackedWidget * widgetStack;
    QWidget * mainWidget = nullptr;

    void fillWindow();
    void initGuiState();

public slots:
    void downloadStageUi();
    void unpackStageUi();
    void storeStageUi();
    void calcFeatStageUi();
    void labelStageUi();
    void trainStageUi();

    void firstPage();
    void secondPage();

    void connectToDashboard(Runnable *);
    void disableAllStageButtons();
    void enableStageButton(quint64);
    void updateProBarBounds(quint64, quint64);
    void updateProBarValue(quint64);
    void updateText(QString);
    void updateImage(QPixmap);
};

#endif // MAINAPPLICATION_H
