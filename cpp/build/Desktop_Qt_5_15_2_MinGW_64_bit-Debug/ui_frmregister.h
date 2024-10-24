/********************************************************************************
** Form generated from reading UI file 'frmregister.ui'
**
** Created by: Qt User Interface Compiler version 5.15.2
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_FRMREGISTER_H
#define UI_FRMREGISTER_H

#include <QtCore/QVariant>
#include <QtWidgets/QApplication>
#include <QtWidgets/QDialog>
#include <QtWidgets/QDialogButtonBox>

QT_BEGIN_NAMESPACE

class Ui_frmregister
{
public:
    QDialogButtonBox *buttonBox;

    void setupUi(QDialog *frmregister)
    {
        if (frmregister->objectName().isEmpty())
            frmregister->setObjectName(QString::fromUtf8("frmregister"));
        frmregister->resize(400, 300);
        buttonBox = new QDialogButtonBox(frmregister);
        buttonBox->setObjectName(QString::fromUtf8("buttonBox"));
        buttonBox->setGeometry(QRect(30, 240, 341, 32));
        buttonBox->setOrientation(Qt::Orientation::Horizontal);
        buttonBox->setStandardButtons(QDialogButtonBox::StandardButton::Cancel|QDialogButtonBox::StandardButton::Ok);

        retranslateUi(frmregister);
        QObject::connect(buttonBox, SIGNAL(accepted()), frmregister, SLOT(accept()));
        QObject::connect(buttonBox, SIGNAL(rejected()), frmregister, SLOT(reject()));

        QMetaObject::connectSlotsByName(frmregister);
    } // setupUi

    void retranslateUi(QDialog *frmregister)
    {
        frmregister->setWindowTitle(QCoreApplication::translate("frmregister", "Dialog", nullptr));
    } // retranslateUi

};

namespace Ui {
    class frmregister: public Ui_frmregister {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_FRMREGISTER_H
