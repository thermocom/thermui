#!/usr/bin/python3

import sys
import logging
import os

from PyQt5 import QtCore
from PyQt5.QtWidgets import *

import thermui
import utils
import conftree

class Therm_Main(QWidget):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.ui = thermui.Ui_Form()
        self.ui.setupUi(self)
        envconfname = 'THERM_CONFIG'
        confname = None
        if envconfname in os.environ:
            confname = os.environ[envconfname]
        if not confname:
            QMessageBox.critical(self, "therm",
                                 "No %s in environment" % envconfname)
            sys.exit(1)

        conf = conftree.ConfSimple(confname)
        utils.initlog(conf)
        self.logger = logging.getLogger()
        
        self.datarepo = conf.get('datarepo')
        self.scratchdir = conf.get('scratchdir')
        if not self.datarepo or not self.scratchdir:
            QMessageBox.critical(self, "therm",
                                 "No 'datarepo' or 'scratchdir' in config")
            sys.exit(1)

        self.remotesettingfile = os.path.join(self.datarepo, 'consigne')
        self.myscratchact = os.path.join(self.scratchdir, 'ui')
        self.myscratchdis = os.path.join(self.scratchdir, 'ui-')
        self.ctlscratch = os.path.join(self.scratchdir, 'ctl')
        if not os.path.exists(self.ctlscratch):
            QMessageBox.critical(self, "therm",
                                 "%s not found: controller not active" %
                                 self.ctlscratch)
            sys.exit(1)
        self._refreshTimer = QtCore.QTimer()
        self._refreshTimer.timeout.connect(self._periodic)
        self._refreshTimer.start(15 * 1000.0)

        self._readCtlValues()
        cf = None
        self.localactive = False
        if os.path.exists(self.myscratchact):
            # Local control
            self.localactive = True
            cf = conftree.ConfSimple(self.myscratchact)
        elif os.path.exists(self.myscratchdis):
            cf = conftree.ConfSimple(self.myscratchdis)
        if cf:
            self.localsetting = float(cf.get("localsetting") or 20.5)
        else:
            self.localsetting = 20.5

        if self.localactive:
            self.ui.commandePB.setChecked(True)
            self.on_commandePB_toggled(True)
        else:
            self.ui.commandePB.setChecked(False)
            self.on_commandePB_toggled(False)

        self.ui.dial.setWrapping(True)
        self.lastDialValue = 0
            
        #with open(self.myscratch, 'w') as f:
        #    print("localconsigne = %.2f" % self.lcdCurrent, file=f)

    def _setlocalsetting(self):
        try:
            os.rename(self.myscratchdis, self.myscratchact)
        except:
            pass
        with open(self.myscratchact, 'w') as f:
            print("localsetting = %.2f" % self.localsetting, file=f)

    def _setremotesetting(self):
        try:
            os.rename(self.myscratchact, self.myscratchdis)
        except:
            pass
        
    def _readCtlValues(self):
        cf = conftree.ConfSimple(self.ctlscratch)
        self.measuredtemp = float(cf.get("measuredtemp"))
        self.remotesetting = open(self.remotesettingfile, 'r').read().strip()
        self.remotesetting = float(self.remotesetting)
        
    def _manageUiState(self):
        self._readCtlValues()
        cmdlocal = self.ui.commandePB.isChecked()
        displaysetting = self.ui.displayPB.isChecked()
        if cmdlocal and displaysetting:
            self.ui.dial.setEnabled(True)
        else:
            self.ui.dial.setEnabled(False)
        if displaysetting:
            if cmdlocal:
                self.ui.lcdNumber.display(self.localsetting)
            else:
                self.ui.lcdNumber.display(self.remotesetting)
        else:
            self.ui.lcdNumber.display(self.measuredtemp)

    def on_commandePB_toggled(self, checked):
        self.logger.debug("on_commandePB_toggled: checked %d", checked)
        if checked:
            self.ui.commandePB.setText("Commande\nlocale")
            self._setlocalsetting()
        else:
            self.ui.commandePB.setText("Commande\ndistante")
            self._setremotesetting()
        self._manageUiState()

    def on_displayPB_toggled(self, checked):
        self.logger.debug("on_displayPB_toggled: checked %d", checked)
        if checked:
            self.ui.displayPB.setText("Consigne")
        else:
            self.ui.displayPB.setText("Mesure")
        self._manageUiState()
            
    def on_dial_valueChanged(self, value):
        delta = value - self.lastDialValue
        self.logger.debug("dial: value %d delta %d", value, delta)
        self.lastDialValue = value
        if delta > 90 or delta < -90:
            # Went through 0
            return
        self.localsetting += float(delta)/50.0
        self._setlocalsetting()
        self._manageUiState()

    def _periodic(self):
        self._manageUiState()
        
def main(args):
    app = QApplication(args)

    topwindow = Therm_Main()
    topwindow.show()
    
    sys.exit(app.exec_())


if __name__=="__main__":
    main(sys.argv)
