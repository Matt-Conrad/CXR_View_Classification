#include "mainwindow.h"

MainWindow::MainWindow(QWidget *parent) : QMainWindow(parent)
{
    QWidget *central_widget = new QWidget;

    QPushButton *button1 = new QPushButton("One");
    QPushButton *button2 = new QPushButton("Two");
    QPushButton *button3 = new QPushButton("Three");
    QPushButton *button4 = new QPushButton("Four");
    QPushButton *button5 = new QPushButton("Five");
    QPushButton *button6 = new QPushButton("Six");

    QHBoxLayout *upper_buttons = new QHBoxLayout;

    upper_buttons->addWidget(button1);
    upper_buttons->addWidget(button2);
    upper_buttons->addWidget(button3);

    QHBoxLayout *lower_buttons = new QHBoxLayout;

    lower_buttons->addWidget(button4);
    lower_buttons->addWidget(button5);
    lower_buttons->addWidget(button6);

    QVBoxLayout *layout = new QVBoxLayout;

    layout->addLayout(upper_buttons);
    layout->addLayout(lower_buttons);

    central_widget->setLayout(layout);
    setCentralWidget(central_widget);
}
