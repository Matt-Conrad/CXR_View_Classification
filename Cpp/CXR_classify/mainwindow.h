#ifndef MAINAPPLICATION_H
#define MAINAPPLICATION_H

#include <QMainWindow>
#include <QWidget>
#include <QPushButton>
#include <QGridLayout>
#include <QLabel>
#include <QProgressBar>

class AppController;

class MainWindow : public QMainWindow
{
    Q_OBJECT
public:
    MainWindow(AppController * controller);

private:
    AppController * controller;

    QWidget * centralWidget = nullptr;

    void fillWindow();
    void initGuiState();

public slots:
    void stage1_ui();
    void stage2_ui();
    void stage3_ui();
    void stage4_ui();
    void stage5_ui();
    void stage6_ui();

    void startDashboard(QString, quint64, quint64);
    void updateProBarBounds(quint64, quint64);
    void updateProBarValue(quint64);
    void updateText(QString);

};

#endif // MAINAPPLICATION_H
