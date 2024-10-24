#include <QApplication>
#include "frmregister.h"
#include "mainwindow.h"

int main(int argc, char *argv[]) {
    QApplication a(argc, argv);  // 正确的参数格式

    FrmRegister loginWindow;
    MainWindow mainWindow;

    // 登录成功后显示主界面
    QObject::connect(&loginWindow, &FrmRegister::loginSuccessful, [&]() {
        mainWindow.show();
        loginWindow.close();
    });

    loginWindow.show();
    return a.exec();
}
