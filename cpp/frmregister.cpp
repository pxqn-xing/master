#include "frmregister.h"
#include "qthelper.h" // 这里可以导入你自己的Qt辅助函数
#include "appinit.h"

FrmRegister::FrmRegister(QWidget *parent) : QWidget(parent) {
    this->initForm();
    this->initText();
    this->initAction();
    QtHelper::setFormInCenter(this); // 将窗口居中
}

FrmRegister::~FrmRegister() {
    // 任何需要的资源释放
}

void FrmRegister::initForm() {
    QLabel *usernameLabel = new QLabel("用户名:", this);
    QLabel *passwordLabel = new QLabel("密码:", this);

    usernameEdit = new QLineEdit(this);
    passwordEdit = new QLineEdit(this);
    passwordEdit->setEchoMode(QLineEdit::Password);

    // 设置默认用户名和密码
    usernameEdit->setText("admin");
    passwordEdit->setText("admin");

    loginButton = new QPushButton("登录", this);
    cancelButton = new QPushButton("取消", this);

    QVBoxLayout *layout = new QVBoxLayout(this);
    layout->addWidget(usernameLabel);
    layout->addWidget(usernameEdit);
    layout->addWidget(passwordLabel);
    layout->addWidget(passwordEdit);
    layout->addWidget(loginButton);
    layout->addWidget(cancelButton);

    setLayout(layout);
    setWindowTitle("登录学生信息管理系统");
    resize(400, 300); // 调整窗口大小
}

void FrmRegister::initText() {
    // 设置窗口标题或其他静态文本
    setWindowTitle("登录 - 学生信息管理系统");
}

void FrmRegister::initAction() {
    // 绑定按钮点击事件
    connect(loginButton, &QPushButton::clicked, this, &FrmRegister::onLoginClicked);
    connect(cancelButton, &QPushButton::clicked, this, [=]() {
        close(); // 取消操作时关闭窗口
    });
}

void FrmRegister::onRegisterButtonClicked() {
    // 添加注册逻辑
    emit registered();  // 发射注册信号
}

void FrmRegister::onLoginClicked() {
    QString username = usernameEdit->text();
    QString password = passwordEdit->text();

    // 验证用户名和密码
    if (username == "admin" && password == "admin") {
        emit loginSuccessful(); // 发出登录成功信号
    } else {
        QMessageBox::warning(this, "登录失败", "用户名或密码不正确！");
    }
}
