#ifndef SIGNALS_H
#define SIGNALS_H

#include <QObject>
#include <QString>
#include <QPixmap>

class Signals : public QObject
{
    Q_OBJECT
public:
    Signals();

signals:
    void finished();
    void attemptUpdateProBarValue(quint64);
    void attemptUpdateProBarBounds(quint64, quint64);
    void attemptUpdateText(QString);
    void attemptUpdateImage(QPixmap);
};

#endif // SIGNALS_H
