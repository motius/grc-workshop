#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: IteratingVariableOverTime
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
from gnuradio import blocks
from gnuradio import gr
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
import numpy as np
import time
import threading

from gnuradio import qtgui

class IteratingVariableOverTime(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "IteratingVariableOverTime")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("IteratingVariableOverTime")
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

        self.settings = Qt.QSettings("GNU Radio", "IteratingVariableOverTime")

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
        self.modulo_base = modulo_base = 1000
        self.amp_probe_function = amp_probe_function = 0
        self.index_var_modulo = index_var_modulo = int(amp_probe_function/modulo_base)
        self.index_var = index_var = amp_probe_function
        self.samp_rate = samp_rate = int(32000/1)
        self.pickle_mat = pickle_mat = np.load('/Applications/GNURadio-comp/projects/01_FunKI_GRC_repo/01_channelModels/python_util/vector_from_mat/vector.npy')[index_var]
        self.maximum_index = maximum_index = 2000
        self.index_var_qtgui_label_0 = index_var_qtgui_label_0 = index_var_modulo
        self.index_var_qtgui_label = index_var_qtgui_label = index_var

        ##################################################
        # Blocks
        ##################################################
        self.signProbe = blocks.probe_signal_s()
        self.qtgui_time_sink_x_1 = qtgui.time_sink_c(
            1024, #size
            samp_rate, #samp_rate
            "", #name
            1 #number of inputs
        )
        self.qtgui_time_sink_x_1.set_update_time(0.10)
        self.qtgui_time_sink_x_1.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_1.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_1.enable_tags(True)
        self.qtgui_time_sink_x_1.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_1.enable_autoscale(False)
        self.qtgui_time_sink_x_1.enable_grid(False)
        self.qtgui_time_sink_x_1.enable_axis_labels(True)
        self.qtgui_time_sink_x_1.enable_control_panel(False)
        self.qtgui_time_sink_x_1.enable_stem_plot(False)


        labels = ['Signal 1', 'Signal 2', 'Signal 3', 'Signal 4', 'Signal 5',
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
                if (i % 2 == 0):
                    self.qtgui_time_sink_x_1.set_line_label(i, "Re{{Data {0}}}".format(i/2))
                else:
                    self.qtgui_time_sink_x_1.set_line_label(i, "Im{{Data {0}}}".format(i/2))
            else:
                self.qtgui_time_sink_x_1.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_1.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_1.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_1.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_1.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_1.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_1_win = sip.wrapinstance(self.qtgui_time_sink_x_1.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_time_sink_x_1_win)
        self.qtgui_number_sink_0_0 = qtgui.number_sink(
            gr.sizeof_short,
            0,
            qtgui.NUM_GRAPH_NONE,
            1
        )
        self.qtgui_number_sink_0_0.set_update_time(0.00)
        self.qtgui_number_sink_0_0.set_title('Live_value: Index')

        labels = ['', '', '', '', '',
            '', '', '', '', '']
        units = ['', '', '', '', '',
            '', '', '', '', '']
        colors = [("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"),
            ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black")]
        factor = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]

        for i in range(1):
            self.qtgui_number_sink_0_0.set_min(i, -1)
            self.qtgui_number_sink_0_0.set_max(i, 1)
            self.qtgui_number_sink_0_0.set_color(i, colors[i][0], colors[i][1])
            if len(labels[i]) == 0:
                self.qtgui_number_sink_0_0.set_label(i, "Data {0}".format(i))
            else:
                self.qtgui_number_sink_0_0.set_label(i, labels[i])
            self.qtgui_number_sink_0_0.set_unit(i, units[i])
            self.qtgui_number_sink_0_0.set_factor(i, factor[i])

        self.qtgui_number_sink_0_0.enable_autoscale(False)
        self._qtgui_number_sink_0_0_win = sip.wrapinstance(self.qtgui_number_sink_0_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_number_sink_0_0_win, 0, 0, 1, 1)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.index_vector = blocks.vector_source_s(np.arange(maximum_index), True, 1, [])
        self._index_var_qtgui_label_0_tool_bar = Qt.QToolBar(self)

        if None:
            self._index_var_qtgui_label_0_formatter = None
        else:
            self._index_var_qtgui_label_0_formatter = lambda x: eng_notation.num_to_str(x)

        self._index_var_qtgui_label_0_tool_bar.addWidget(Qt.QLabel('Index Var_modulo' + ": "))
        self._index_var_qtgui_label_0_label = Qt.QLabel(str(self._index_var_qtgui_label_0_formatter(self.index_var_qtgui_label_0)))
        self._index_var_qtgui_label_0_tool_bar.addWidget(self._index_var_qtgui_label_0_label)
        self.top_grid_layout.addWidget(self._index_var_qtgui_label_0_tool_bar, 2, 0, 1, 1)
        for r in range(2, 3):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._index_var_qtgui_label_tool_bar = Qt.QToolBar(self)

        if None:
            self._index_var_qtgui_label_formatter = None
        else:
            self._index_var_qtgui_label_formatter = lambda x: eng_notation.num_to_str(x)

        self._index_var_qtgui_label_tool_bar.addWidget(Qt.QLabel('Acquired_index_var:' + ": "))
        self._index_var_qtgui_label_label = Qt.QLabel(str(self._index_var_qtgui_label_formatter(self.index_var_qtgui_label)))
        self._index_var_qtgui_label_tool_bar.addWidget(self._index_var_qtgui_label_label)
        self.top_grid_layout.addWidget(self._index_var_qtgui_label_tool_bar, 1, 0, 1, 1)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.blocks_vector_to_stream_0 = blocks.vector_to_stream(gr.sizeof_gr_complex*1, 64)
        self.blocks_vector_source_x_0 = blocks.vector_source_c(np.ones(len(pickle_mat)), True, 64, [])
        self.blocks_throttle_1 = blocks.throttle(gr.sizeof_short*1, samp_rate,True)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_vcc(pickle_mat)
        def _amp_probe_function_probe():
            while True:

                val = self.signProbe.level()
                try:
                    self.set_amp_probe_function(val)
                except AttributeError:
                    pass
                time.sleep(1.0 / (samp_rate))
        _amp_probe_function_thread = threading.Thread(target=_amp_probe_function_probe)
        _amp_probe_function_thread.daemon = True
        _amp_probe_function_thread.start()




        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_vector_to_stream_0, 0))
        self.connect((self.blocks_throttle_1, 0), (self.qtgui_number_sink_0_0, 0))
        self.connect((self.blocks_throttle_1, 0), (self.signProbe, 0))
        self.connect((self.blocks_vector_source_x_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.blocks_vector_to_stream_0, 0), (self.qtgui_time_sink_x_1, 0))
        self.connect((self.index_vector, 0), (self.blocks_throttle_1, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "IteratingVariableOverTime")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_modulo_base(self):
        return self.modulo_base

    def set_modulo_base(self, modulo_base):
        self.modulo_base = modulo_base
        self.set_index_var_modulo(int(self.amp_probe_function/self.modulo_base))

    def get_amp_probe_function(self):
        return self.amp_probe_function

    def set_amp_probe_function(self, amp_probe_function):
        self.amp_probe_function = amp_probe_function
        self.set_index_var(self.amp_probe_function)
        self.set_index_var_modulo(int(self.amp_probe_function/self.modulo_base))

    def get_index_var_modulo(self):
        return self.index_var_modulo

    def set_index_var_modulo(self, index_var_modulo):
        self.index_var_modulo = index_var_modulo
        self.set_index_var_qtgui_label_0(self._index_var_qtgui_label_0_formatter(self.index_var_modulo))

    def get_index_var(self):
        return self.index_var

    def set_index_var(self, index_var):
        self.index_var = index_var
        self.set_index_var_qtgui_label(self._index_var_qtgui_label_formatter(self.index_var))
        self.set_pickle_mat(np.load('/Applications/GNURadio-comp/projects/01_FunKI_GRC_repo/01_channelModels/python_util/vector_from_mat/vector.npy')[self.index_var])

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.blocks_throttle_1.set_sample_rate(self.samp_rate)
        self.qtgui_time_sink_x_1.set_samp_rate(self.samp_rate)

    def get_pickle_mat(self):
        return self.pickle_mat

    def set_pickle_mat(self, pickle_mat):
        self.pickle_mat = pickle_mat
        self.blocks_multiply_const_vxx_0.set_k(self.pickle_mat)
        self.blocks_vector_source_x_0.set_data(np.ones(len(self.pickle_mat)), [])

    def get_maximum_index(self):
        return self.maximum_index

    def set_maximum_index(self, maximum_index):
        self.maximum_index = maximum_index
        self.index_vector.set_data(np.arange(self.maximum_index), [])

    def get_index_var_qtgui_label_0(self):
        return self.index_var_qtgui_label_0

    def set_index_var_qtgui_label_0(self, index_var_qtgui_label_0):
        self.index_var_qtgui_label_0 = index_var_qtgui_label_0
        Qt.QMetaObject.invokeMethod(self._index_var_qtgui_label_0_label, "setText", Qt.Q_ARG("QString", self.index_var_qtgui_label_0))

    def get_index_var_qtgui_label(self):
        return self.index_var_qtgui_label

    def set_index_var_qtgui_label(self, index_var_qtgui_label):
        self.index_var_qtgui_label = index_var_qtgui_label
        Qt.QMetaObject.invokeMethod(self._index_var_qtgui_label_label, "setText", Qt.Q_ARG("QString", self.index_var_qtgui_label))





def main(top_block_cls=IteratingVariableOverTime, options=None):

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
