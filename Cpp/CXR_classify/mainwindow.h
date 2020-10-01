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

#include <string>
#include <filesystem>
#include "downloadstage.h"
#include "unpackstage.h"
#include "storestage.h"
#include "featurecalculatorstage.h"
#include "labelstage.h"
#include "trainstage.h"
#include "confighandler.h"
#include "databasehandler.h"

#include "spdlog/spdlog.h"
#include "spdlog/sinks/basic_file_sink.h"

class MainWindow : public QMainWindow
{
    Q_OBJECT
public:
    MainWindow();
    ~MainWindow();

private:
    std::shared_ptr<spdlog::logger> logger;
    ConfigHandler * configHandler;
    DatabaseHandler * dbHandler;

    QString buttonsList[6] = {"downloadBtn", "unpackBtn", "storeBtn", "featureBtn", "labelBtn", "trainBtn"};

    QStackedWidget * widgetStack;
    QWidget * mainWidget = nullptr;

    Stage * currentStage;

    void fillWindow();
    void initGuiState();

    void connectToDashboard(Runnable *);
    void disableAllStageButtons();
    void enableStageButton(quint64);
    void configureLogging();

private slots:
    void clearCurrentStage();
    void firstPage();
    void secondPage();

public slots:
    void downloadStageUi();
    void unpackStageUi();
    void storeStageUi();
    void calcFeatStageUi();
    void labelStageUi();
    void trainStageUi();

    void updateProBarBounds(quint64, quint64);
    void updateProBarValue(quint64);
    void updateText(QString);
    void updateImage(QPixmap);
};

#endif // MAINAPPLICATION_H
