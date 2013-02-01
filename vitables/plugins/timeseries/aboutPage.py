#!/usr/bin/env python2
# -*- coding: utf-8 -*-

#       Copyright (C) 2008-2013 Vicent Mas. All rights reserved
#
#       This program is free software: you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation, either version 3 of the License, or
#       (at your option) any later version.
#
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#
#       You should have received a copy of the GNU General Public License
#       along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#       Author:  Vicent Mas - vmas@vitables.org

"""
This module provides a widget with the full description of the plugin.

The module allows for configuring the plugin too.

The widget is displayed when the plugin is selected in the Preferences
dialog selector tree.
"""

__docformat__ = 'restructuredtext'

import os.path
import ConfigParser
import datetime

from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4.uic import loadUiType

import vitables.utils


translate = QtGui.QApplication.translate


# This method of the PyQt4.uic module allows for dinamically loading user 
# interfaces created by QtDesigner. See the PyQt4 Reference Guide for more
# info.
Ui_TimeFormatterPage = \
    loadUiType(os.path.join(os.path.dirname(__file__), 
    'timeformatter_page.ui'))[0]


class AboutPage(QtGui.QWidget, Ui_TimeFormatterPage):
    """
    Widget for describing and customising the Time series plugin.

    By loading UI files at runtime we can:

        - create user interfaces at runtime (without using pyuic)
        - use multiple inheritance, MyParentClass(BaseClass, FormClass)

    This widget is inserted as a page in the stacked widget of the
    Preferences dialog when the Time series item is clicked in the
    selector tree.

    :Parameters:

    - `title`: the dialog title
    - `info`: information to be displayed in the dialog
    - `action`: string with the editing action to be done, Create or Rename
    """

    def __init__(self, desc, parent=None):
        """A widget for describing and customising the timeseries plugin.

        :Parameters:

            - `desc`: a dictionary with the plugin description
            -`parent`: the sctaked widget of the Preferences dialog
        """

        # Makes the dialog and gives it a layout
        super(AboutPage, self).__init__(parent)
        self.setupUi(self)

        self.version_le.setText(desc['version'])
        self.module_name_le.setText(desc['module_name'])
        self.folder_le.setText(desc['folder'])
        self.author_le.setText(desc['author'])
        self.desc_te.setText(desc['about_text'])

        # Configuration section of the page
        self.save_button = self.buttons_box.button(QtGui.QDialogButtonBox.Save)
        self.save_button.setText('Save format')

        # Setup initial configuration
        config = ConfigParser.RawConfigParser()
        def_tformat = '%c' 
        try:
            config.read(\
                os.path.join(os.path.dirname(__file__), u'time_format.ini'))
            self.tformat = config.get('Timeseries', 'strftime')
        except (IOError, ConfigParser.Error):
            self.tformat = def_tformat

        self.tformat_editor.setText(self.tformat)
        today = datetime.datetime.today().strftime(self.tformat)
        self.today_label.setText(today)

        self.save_button.clicked.connect(self.saveFormat)


    def eventFilter(self, w, e):
        """Event filter for the dialog.
        """

        if self.tformat_editor.hasFocus():
            if e.type() == 6:
                if e.key() in (QtCore.Qt.Key_Enter, QtCore.Qt.Key_Return):
                    self.applyFormat()
                    return True
        return QtGui.QWidget.eventFilter(self, w, e)


    def applyFormat(self):
        """
        Check the current time format.

        The time format currently entered in the line editor is applied to the
        sample label showing the today date. If the result is that expected by
        user then she can click safely the OK button. Otherwhise she should try
        another time format.
        """

        today = datetime.datetime.today().strftime(self.tformat_editor.text())
        self.today_label.clear()
        self.today_label.setText(today)




    def saveFormat(self):
        """Slot for saving the entered time format.
        """

        config = ConfigParser.RawConfigParser()
        filename = os.path.join(os.path.dirname(__file__), u'time_format.ini')
        config.read(filename)
        config.set(\
            'Timeseries', 'strftime', self.tformat_editor.text())
        with open(filename, 'wb') as ini_file:
            config.write(ini_file)
