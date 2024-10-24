#ifndef FRMREGISTER_H
#define FRMREGISTER_H

#include <QWidget>
#include <QLineEdit>
#include <QPushButton>
#include <QVBoxLayout>
#include <QLabel>
#include <QMessageBox>

class FrmRegister : public QWidget {
    Q_OBJECT

public:
    explicit FrmRegister(QWidget *parent = nullptr);
    ~FrmRegister();

private:
    void initForm();  // 初始化界面
    void initText();  // 设置文本
    void initAction(); // 绑定事件

signals:
    void registered();  // 自定义注册信号
    void loginSuccessful(); // 登录成功信号

private slots:
    void onRegisterButtonClicked();
    void onLoginClicked();

private:
    QLineEdit *usernameEdit;
    QLineEdit *passwordEdit;
    QPushButton *loginButton;
    QPushButton *cancelButton;
};

#endif // FRMREGISTER_H
