#include "mainwindow.h"

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent) {

    // 创建表格部件
    tableWidget = new QTableWidget(this);
    tableWidget->setColumnCount(8); // 设置列数
    tableWidget->setHorizontalHeaderLabels({"学号", "学生名称", "学生学院", "学生专业", "学生联系方式","学生家庭住址","学生父母联系方式"});
    tableWidget->setRowCount(30); // 设置行数

    // 添加按钮
    addButton = new QPushButton("增加学生信息", this);
    previousButton = new QPushButton("上一页", this);
    nextButton = new QPushButton("下一页", this);

    // 布局
    QVBoxLayout *layout = new QVBoxLayout();
    layout->addWidget(tableWidget);
    layout->addWidget(addButton);
    layout->addWidget(previousButton);
    layout->addWidget(nextButton);

    QWidget *centralWidget = new QWidget(this);
    centralWidget->setLayout(layout);
    setCentralWidget(centralWidget);
    setWindowTitle("学生信息管理平台");
}
