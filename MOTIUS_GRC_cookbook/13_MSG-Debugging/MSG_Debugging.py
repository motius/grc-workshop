#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: MSG-Debugging
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
from gnuradio import qtgui
from gnuradio.filter import firdes
import sip
from gnuradio import analog
from gnuradio import blocks
from gnuradio import gr
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio.qtgui import Range, RangeWidget
import epy_block_0_0

from gnuradio import qtgui

class MSG_Debugging(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "MSG-Debugging")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("MSG-Debugging")
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

        self.settings = Qt.QSettings("GNU Radio", "MSG_Debugging")

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
        self.samp_rate = samp_rate = 32000/8
        self.numPoints = numPoints = int(1024/4)
        self.index_for_debugging = index_for_debugging = 0
        self.amplitude_range = amplitude_range = 2

        ##################################################
        # Blocks
        ##################################################
        self.qt_gui_tabs = Qt.QTabWidget()
        self.qt_gui_tabs_widget_0 = Qt.QWidget()
        self.qt_gui_tabs_layout_0 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.qt_gui_tabs_widget_0)
        self.qt_gui_tabs_grid_layout_0 = Qt.QGridLayout()
        self.qt_gui_tabs_layout_0.addLayout(self.qt_gui_tabs_grid_layout_0)
        self.qt_gui_tabs.addTab(self.qt_gui_tabs_widget_0, 'Simple debug to file')
        self.qt_gui_tabs_widget_1 = Qt.QWidget()
        self.qt_gui_tabs_layout_1 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.qt_gui_tabs_widget_1)
        self.qt_gui_tabs_grid_layout_1 = Qt.QGridLayout()
        self.qt_gui_tabs_layout_1.addLayout(self.qt_gui_tabs_grid_layout_1)
        self.qt_gui_tabs.addTab(self.qt_gui_tabs_widget_1, 'GUI- and file-debugging')
        self.qt_gui_tabs_widget_2 = Qt.QWidget()
        self.qt_gui_tabs_layout_2 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.qt_gui_tabs_widget_2)
        self.qt_gui_tabs_grid_layout_2 = Qt.QGridLayout()
        self.qt_gui_tabs_layout_2.addLayout(self.qt_gui_tabs_grid_layout_2)
        self.qt_gui_tabs.addTab(self.qt_gui_tabs_widget_2, 'Last but least')
        self.top_grid_layout.addWidget(self.qt_gui_tabs, 1, 0, 1, 1)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._index_for_debugging_range = Range(0, 1000, 1, 0, 200)
        self._index_for_debugging_win = RangeWidget(self._index_for_debugging_range, self.set_index_for_debugging, 'Index of input', "counter_slider", float)
        self.top_grid_layout.addWidget(self._index_for_debugging_win)
        self._amplitude_range_range = Range(0, 20, 1, 2, 200)
        self._amplitude_range_win = RangeWidget(self._amplitude_range_range, self.set_amplitude_range, 'Amplitude', "counter_slider", int)
        self.top_grid_layout.addWidget(self._amplitude_range_win)
        self.qtgui_time_sink_x_0_0_0_0_1_0_0_1_0_0_0 = qtgui.time_sink_f(
            numPoints, #size
            samp_rate, #samp_rate
            'postpython', #name
            1 #number of inputs
        )
        self.qtgui_time_sink_x_0_0_0_0_1_0_0_1_0_0_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0_0_0_0_1_0_0_1_0_0_0.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_0_0_0_0_1_0_0_1_0_0_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0_0_0_0_1_0_0_1_0_0_0.enable_tags(True)
        self.qtgui_time_sink_x_0_0_0_0_1_0_0_1_0_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0_0_0_0_1_0_0_1_0_0_0.enable_autoscale(True)
        self.qtgui_time_sink_x_0_0_0_0_1_0_0_1_0_0_0.enable_grid(False)
        self.qtgui_time_sink_x_0_0_0_0_1_0_0_1_0_0_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0_0_0_0_1_0_0_1_0_0_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0_0_0_0_1_0_0_1_0_0_0.enable_stem_plot(False)


        labels = ['Original', 'After Operation', 'Signal 3', 'Signal 4', 'Signal 5',
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


        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_0_0_0_0_1_0_0_1_0_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0_0_0_0_1_0_0_1_0_0_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0_0_0_0_1_0_0_1_0_0_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0_0_0_0_1_0_0_1_0_0_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0_0_0_0_1_0_0_1_0_0_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0_0_0_0_1_0_0_1_0_0_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0_0_0_0_1_0_0_1_0_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_0_0_0_1_0_0_1_0_0_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0_0_0_0_1_0_0_1_0_0_0.pyqwidget(), Qt.QWidget)
        self.qt_gui_tabs_layout_2.addWidget(self._qtgui_time_sink_x_0_0_0_0_1_0_0_1_0_0_0_win)
        self.qtgui_time_sink_x_0_0_0_0_1_0_0_0_0_0_0_0 = qtgui.time_sink_f(
            numPoints, #size
            samp_rate, #samp_rate
            'inputPython', #name
            1 #number of inputs
        )
        self.qtgui_time_sink_x_0_0_0_0_1_0_0_0_0_0_0_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0_0_0_0_1_0_0_0_0_0_0_0.set_y_axis(-25, 25)

        self.qtgui_time_sink_x_0_0_0_0_1_0_0_0_0_0_0_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0_0_0_0_1_0_0_0_0_0_0_0.enable_tags(True)
        self.qtgui_time_sink_x_0_0_0_0_1_0_0_0_0_0_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0_0_0_0_1_0_0_0_0_0_0_0.enable_autoscale(True)
        self.qtgui_time_sink_x_0_0_0_0_1_0_0_0_0_0_0_0.enable_grid(False)
        self.qtgui_time_sink_x_0_0_0_0_1_0_0_0_0_0_0_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0_0_0_0_1_0_0_0_0_0_0_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0_0_0_0_1_0_0_0_0_0_0_0.enable_stem_plot(False)


        labels = ['Original', 'After Operation', 'Signal 3', 'Signal 4', 'Signal 5',
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


        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_0_0_0_0_1_0_0_0_0_0_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0_0_0_0_1_0_0_0_0_0_0_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0_0_0_0_1_0_0_0_0_0_0_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0_0_0_0_1_0_0_0_0_0_0_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0_0_0_0_1_0_0_0_0_0_0_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0_0_0_0_1_0_0_0_0_0_0_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0_0_0_0_1_0_0_0_0_0_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_0_0_0_1_0_0_0_0_0_0_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0_0_0_0_1_0_0_0_0_0_0_0.pyqwidget(), Qt.QWidget)
        self.qt_gui_tabs_layout_2.addWidget(self._qtgui_time_sink_x_0_0_0_0_1_0_0_0_0_0_0_0_win)
        self.qtgui_edit_box_msg_0 = qtgui.edit_box_msg(qtgui.STRING, '', 'Passed message demo', False, True, '')
        self._qtgui_edit_box_msg_0_win = sip.wrapinstance(self.qtgui_edit_box_msg_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_edit_box_msg_0_win, 0, 0, 1, 1)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.epy_block_0_0 = epy_block_0_0.blk(input_dim=1, index=index_for_debugging)
        self.blocks_vector_source_x_0 = blocks.vector_source_f((0.1, 0.3, 4,12), True, 1, [])
        self.blocks_throttle_1 = blocks.throttle(gr.sizeof_gr_complex*1, samp_rate,True)
        self.blocks_null_source_0 = blocks.null_source(gr.sizeof_gr_complex*1)
        self.blocks_null_sink_0 = blocks.null_sink(gr.sizeof_gr_complex*1)
        self.analog_sig_source_x_0_0_0_0_0_0_0 = analog.sig_source_f(samp_rate, analog.GR_COS_WAVE, 100, amplitude_range, 0, 0)



        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.epy_block_0_0, 'pmt_msg_out'), (self.qtgui_edit_box_msg_0, 'val'))
        self.connect((self.analog_sig_source_x_0_0_0_0_0_0_0, 0), (self.epy_block_0_0, 0))
        self.connect((self.analog_sig_source_x_0_0_0_0_0_0_0, 0), (self.qtgui_time_sink_x_0_0_0_0_1_0_0_0_0_0_0_0, 0))
        self.connect((self.blocks_null_source_0, 0), (self.blocks_throttle_1, 0))
        self.connect((self.blocks_throttle_1, 0), (self.blocks_null_sink_0, 0))
        self.connect((self.blocks_vector_source_x_0, 0), (self.epy_block_0_0, 1))
        self.connect((self.epy_block_0_0, 0), (self.qtgui_time_sink_x_0_0_0_0_1_0_0_1_0_0_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "MSG_Debugging")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.analog_sig_source_x_0_0_0_0_0_0_0.set_sampling_freq(self.samp_rate)
        self.blocks_throttle_1.set_sample_rate(self.samp_rate)
        self.qtgui_time_sink_x_0_0_0_0_1_0_0_0_0_0_0_0.set_samp_rate(self.samp_rate)
        self.qtgui_time_sink_x_0_0_0_0_1_0_0_1_0_0_0.set_samp_rate(self.samp_rate)

    def get_numPoints(self):
        return self.numPoints

    def set_numPoints(self, numPoints):
        self.numPoints = numPoints

    def get_index_for_debugging(self):
        return self.index_for_debugging

    def set_index_for_debugging(self, index_for_debugging):
        self.index_for_debugging = index_for_debugging
        self.epy_block_0_0.index = self.index_for_debugging

    def get_amplitude_range(self):
        return self.amplitude_range

    def set_amplitude_range(self, amplitude_range):
        self.amplitude_range = amplitude_range
        self.analog_sig_source_x_0_0_0_0_0_0_0.set_amplitude(self.amplitude_range)





def main(top_block_cls=MSG_Debugging, options=None):

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
