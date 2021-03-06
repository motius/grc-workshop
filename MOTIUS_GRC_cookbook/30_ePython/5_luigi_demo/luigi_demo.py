#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: luigi_demo
# Author: JI
# GNU Radio version: 3.8.2.0

from distutils.version import StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

from PyQt5 import Qt
from gnuradio import eng_notation
from gnuradio import qtgui
from gnuradio.filter import firdes
import sip
from gnuradio import analog
from gnuradio import gr
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
import epy_do_luigi

from gnuradio import qtgui

class luigi_demo(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "luigi_demo")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("luigi_demo")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "luigi_demo")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 32000
        self.mult_val = mult_val = 1
        self.add_val = add_val = 0.1

        ##################################################
        # Blocks
        ##################################################
        self._mult_val_tool_bar = Qt.QToolBar(self)
        self._mult_val_tool_bar.addWidget(Qt.QLabel('mutl' + ": "))
        self._mult_val_line_edit = Qt.QLineEdit(str(self.mult_val))
        self._mult_val_tool_bar.addWidget(self._mult_val_line_edit)
        self._mult_val_line_edit.returnPressed.connect(
            lambda: self.set_mult_val(eng_notation.str_to_num(str(self._mult_val_line_edit.text()))))
        self.top_grid_layout.addWidget(self._mult_val_tool_bar)
        self._add_val_tool_bar = Qt.QToolBar(self)
        self._add_val_tool_bar.addWidget(Qt.QLabel('add' + ": "))
        self._add_val_line_edit = Qt.QLineEdit(str(self.add_val))
        self._add_val_tool_bar.addWidget(self._add_val_line_edit)
        self._add_val_line_edit.returnPressed.connect(
            lambda: self.set_add_val(eng_notation.str_to_num(str(self._add_val_line_edit.text()))))
        self.top_grid_layout.addWidget(self._add_val_tool_bar)
        self.qtgui_time_sink_x_1 = qtgui.time_sink_f(
            100, #size
            samp_rate, #samp_rate
            "", #name
            2 #number of inputs
        )
        self.qtgui_time_sink_x_1.set_update_time(0.10)
        self.qtgui_time_sink_x_1.set_y_axis(-2, 2)

        self.qtgui_time_sink_x_1.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_1.enable_tags(True)
        self.qtgui_time_sink_x_1.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_1.enable_autoscale(True)
        self.qtgui_time_sink_x_1.enable_grid(False)
        self.qtgui_time_sink_x_1.enable_axis_labels(True)
        self.qtgui_time_sink_x_1.enable_control_panel(False)
        self.qtgui_time_sink_x_1.enable_stem_plot(False)


        labels = ['Original', 'Postprocessed', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(2):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_1.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_1.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_1.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_1.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_1.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_1.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_1_win = sip.wrapinstance(self.qtgui_time_sink_x_1.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_time_sink_x_1_win)
        self.epy_do_luigi = epy_do_luigi.luigi_blk(mult_var=mult_val, add_var=add_val, luigi_model_path='')
        self.analog_sig_source_x_0 = analog.sig_source_f(samp_rate, analog.GR_COS_WAVE, 1000, 1, 0, 0)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_sig_source_x_0, 0), (self.epy_do_luigi, 0))
        self.connect((self.analog_sig_source_x_0, 0), (self.qtgui_time_sink_x_1, 0))
        self.connect((self.epy_do_luigi, 0), (self.qtgui_time_sink_x_1, 1))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "luigi_demo")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate)
        self.qtgui_time_sink_x_1.set_samp_rate(self.samp_rate)

    def get_mult_val(self):
        return self.mult_val

    def set_mult_val(self, mult_val):
        self.mult_val = mult_val
        Qt.QMetaObject.invokeMethod(self._mult_val_line_edit, "setText", Qt.Q_ARG("QString", eng_notation.num_to_str(self.mult_val)))
        self.epy_do_luigi.mult_var = self.mult_val

    def get_add_val(self):
        return self.add_val

    def set_add_val(self, add_val):
        self.add_val = add_val
        Qt.QMetaObject.invokeMethod(self._add_val_line_edit, "setText", Qt.Q_ARG("QString", eng_notation.num_to_str(self.add_val)))
        self.epy_do_luigi.add_var = self.add_val





def main(top_block_cls=luigi_demo, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    def quitting():
        tb.stop()
        tb.wait()

    qapp.aboutToQuit.connect(quitting)
    qapp.exec_()

if __name__ == '__main__':
    main()
