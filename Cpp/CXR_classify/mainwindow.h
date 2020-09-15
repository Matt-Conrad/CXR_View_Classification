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

class AppController;

class MainWindow : public QMainWindow
{
    Q_OBJECT
public:
    MainWindow(AppController * controller);

private:
    AppController * controller;

    QString buttonsList[6] = {"downloadBtn", "unpackBtn", "storeBtn", "featureBtn", "labelBtn", "classifyBtn"};

    QStackedWidget * widgetStack;
    QWidget * mainWidget = nullptr;

    void fillWindow();
    void initGuiState();

public slots:
    void stage1_ui();
    void stage2_ui();
    void stage3_ui();
    void stage4_ui();
    void stage5_ui();
    void stage6_ui();

    void connectToDashBoard(Stage *);
    void disableAllStageButtons();
    void enableStageButton(quint64);
    void updateProBarBounds(quint64, quint64);
    void updateProBarValue(quint64);
    void updateText(QString);

};

#endif // MAINAPPLICATION_H
