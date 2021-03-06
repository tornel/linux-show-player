##########################################
# Copyright 2012-2014 Ceruti Francesco & contributors
#
# This file is part of LiSP (Linux Show Player).
##########################################

from PyQt5 import QtCore
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QGridLayout, \
    QDoubleSpinBox, QLabel, QComboBox, QStyledItemDelegate

from lisp.gst.elements.fade import Fade
from lisp.ui.settings.section import SettingsSection


class FadeSettings(SettingsSection):

    NAME = "Fade"
    ELEMENT = Fade

    FadeOut = {'Linear': QIcon.fromTheme('fadeout_linear'),
               'Quadratic': QIcon.fromTheme('fadeout_quadratic'),
               'Quadratic2': QIcon.fromTheme('fadeout_quadratic2')}

    FadeIn = {'Linear': QIcon.fromTheme('fadein_linear'),
              'Quadratic': QIcon.fromTheme('fadein_quadratic'),
              'Quadratic2': QIcon.fromTheme('fadein_quadratic2')}

    def __init__(self, size, Id, parent=None):
        super().__init__(size, parent)

        self.id = Id

        self.box = QWidget(self)
        self.box.setGeometry(0, 0, self.width(), 240)

        self.verticalLayout = QVBoxLayout(self.box)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)

        # FadeIn
        self.groupFadeIn = QGroupBox(self.box)
        self.fadeInLayout = QGridLayout(self.groupFadeIn)

        self.fadeInSpin = QDoubleSpinBox(self.groupFadeIn)
        self.fadeInSpin.setMaximum(3600)
        self.fadeInLayout.addWidget(self.fadeInSpin, 0, 0)

        self.fadeInLabel = QLabel(self.groupFadeIn)
        self.fadeInLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.fadeInLayout.addWidget(self.fadeInLabel, 0, 1)

        self.fadeInCombo = QComboBox(self.groupFadeIn)
        self.fadeInCombo.setItemDelegate(QStyledItemDelegate())
        for key in sorted(self.FadeIn.keys()):
            self.fadeInCombo.addItem(self.FadeIn[key], key)
        self.fadeInLayout.addWidget(self.fadeInCombo, 1, 0)

        self.fadeInExpLabel = QLabel(self.groupFadeIn)
        self.fadeInExpLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.fadeInLayout.addWidget(self.fadeInExpLabel, 1, 1)

        self.verticalLayout.addWidget(self.groupFadeIn)

        # FadeOut
        self.groupFadeOut = QGroupBox(self.box)
        self.fadeOutLayout = QGridLayout(self.groupFadeOut)

        self.fadeOutSpin = QDoubleSpinBox(self.groupFadeOut)
        self.fadeOutSpin.setMaximum(3600)
        self.fadeOutLayout.addWidget(self.fadeOutSpin, 0, 0)

        self.fadeOutLabel = QLabel(self.groupFadeOut)
        self.fadeOutLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.fadeOutLayout.addWidget(self.fadeOutLabel, 0, 1)

        self.fadeOutCombo = QComboBox(self.groupFadeOut)
        self.fadeOutCombo.setItemDelegate(QStyledItemDelegate())
        for key in sorted(self.FadeOut.keys()):
            self.fadeOutCombo.addItem(self.FadeOut[key], key)
        self.fadeOutLayout.addWidget(self.fadeOutCombo, 1, 0)

        self.fadeOutExpLabel = QLabel(self.groupFadeOut)
        self.fadeOutExpLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.fadeOutLayout.addWidget(self.fadeOutExpLabel, 1, 1)

        self.verticalLayout.addWidget(self.groupFadeOut)

        self.retranslateUi()

    def retranslateUi(self):
        self.groupFadeIn.setTitle("Fade In")
        self.fadeInLabel.setText("Time (sec)")
        self.fadeInExpLabel.setText("Exponent")
        self.groupFadeOut.setTitle("Fade Out")
        self.fadeOutLabel.setText("Time (sec)")
        self.fadeOutExpLabel.setText("Exponent")

    def get_configuration(self):
        conf = {self.id: {}}

        checkable = self.groupFadeIn.isCheckable()

        if not (checkable and not self.groupFadeIn.isChecked()):
            conf[self.id]["fadein"] = self.fadeInSpin.value()
            conf[self.id]["fadein_type"] = self.fadeInCombo.currentText()
        if not (checkable and not self.groupFadeOut.isChecked()):
            conf[self.id]["fadeout"] = self.fadeOutSpin.value()
            conf[self.id]["fadeout_type"] = self.fadeOutCombo.currentText()

        return conf

    def set_configuration(self, conf):
        if self.id in conf:
            conf = conf[self.id]

            self.fadeInSpin.setValue(conf["fadein"])
            i = sorted(self.FadeIn.keys()).index(conf["fadein_type"])
            self.fadeInCombo.setCurrentIndex(i)

            self.fadeOutSpin.setValue(conf["fadeout"])
            i = sorted(self.FadeOut.keys()).index(conf["fadeout_type"])
            self.fadeOutCombo.setCurrentIndex(i)

    def enable_check(self, enable):
        self.groupFadeIn.setCheckable(enable)
        self.groupFadeIn.setChecked(False)

        self.groupFadeOut.setCheckable(enable)
        self.groupFadeOut.setChecked(False)
