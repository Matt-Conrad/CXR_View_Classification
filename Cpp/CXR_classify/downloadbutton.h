#ifndef DOWNLOADBUTTON_H
#define DOWNLOADBUTTON_H

#include <QPushButton>
#include <iostream>

class DownloadButton : public QPushButton
{
    Q_OBJECT
public:
    DownloadButton(const char * text);

private slots:
    void test();
};

#endif // DOWNLOADBUTTON_H
