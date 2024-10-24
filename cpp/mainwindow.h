#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QTableWidget>
#include <QVBoxLayout>
#include <QPushButton>
#include <QWidget>

class MainWindow : public QMainWindow {
    Q_OBJECT

public:
    MainWindow(QWidget *parent = nullptr);

private:
    QTableWidget *tableWidget;
    QPushButton *addButton;
    QPushButton *previousButton;
    QPushButton *nextButton;
};

#endif // MAINWINDOW_H
