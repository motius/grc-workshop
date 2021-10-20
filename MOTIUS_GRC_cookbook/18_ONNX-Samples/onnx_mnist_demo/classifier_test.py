#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Classifier Test
# Author: Kevin JOLY
# Description: Test for ONNX inference
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
import sip
from gnuradio import blocks
import pmt
from gnuradio import gr
from gnuradio.filter import firdes
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import video_sdl
import dnn

from gnuradio import qtgui

class classifier_test(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Classifier Test")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Classifier Test")
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

        self.settings = Qt.QSettings("GNU Radio", "classifier_test")

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
        self.output_len = output_len = 10
        self.input_len = input_len = 784

        ##################################################
        # Blocks
        ##################################################
        self.video_sdl_sink_0_0 = video_sdl.sink_uc(0, 28, 28, 0, 28*20, 28*20)
        self.source = blocks.file_source(gr.sizeof_char*1, '/Volumes/JI_MT_exFAT/motius/grc_stuff/01_onnx/onnx_mnist_demo/mnist/test_data_set_0/input_0.pb', True, 0, 0)
        self.source.set_begin_tag(pmt.PMT_NIL)
        self.qtgui_number_sink_0 = qtgui.number_sink(
            gr.sizeof_short,
            0,
            qtgui.NUM_GRAPH_NONE,
            1
        )
        self.qtgui_number_sink_0.set_update_time(-1)
        self.qtgui_number_sink_0.set_title("Classifier")

        labels = ['Number found', '', '', '', '',
            '', '', '', '', '']
        units = ['', '', '', '', '',
            '', '', '', '', '']
        colors = [("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"),
            ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black")]
        factor = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]

        for i in range(1):
            self.qtgui_number_sink_0.set_min(i, -1000)
            self.qtgui_number_sink_0.set_max(i, 1000)
            self.qtgui_number_sink_0.set_color(i, colors[i][0], colors[i][1])
            if len(labels[i]) == 0:
                self.qtgui_number_sink_0.set_label(i, "Data {0}".format(i))
            else:
                self.qtgui_number_sink_0.set_label(i, labels[i])
            self.qtgui_number_sink_0.set_unit(i, units[i])
            self.qtgui_number_sink_0.set_factor(i, factor[i])

        self.qtgui_number_sink_0.enable_autoscale(False)
        self._qtgui_number_sink_0_win = sip.wrapinstance(self.qtgui_number_sink_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_number_sink_0_win)
        self.dnn_dnn_onnx_python_0 = dnn.dnn_onnx_python('/Volumes/JI_MT_exFAT/motius/grc_stuff/01_onnx/onnx_mnist_demo/mnist/model.onnx', False, 1.0)
        self.blocks_uchar_to_float_0 = blocks.uchar_to_float()
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_char*1, 1000000,True)
        self.blocks_tagged_stream_to_pdu_0 = blocks.tagged_stream_to_pdu(blocks.float_t, 'packet_len')
        self.blocks_stream_to_vector_0 = blocks.stream_to_vector(gr.sizeof_float*1, 10)
        self.blocks_stream_to_tagged_stream_0 = blocks.stream_to_tagged_stream(gr.sizeof_float, 1, input_len, "packet_len")
        self.blocks_pdu_to_tagged_stream_0 = blocks.pdu_to_tagged_stream(blocks.float_t, 'output_len')
        self.blocks_null_sink_0 = blocks.null_sink(gr.sizeof_short*1)
        self.blocks_multiply_const_xx_0 = blocks.multiply_const_ff(1.0/255.0, 1)
        self.blocks_argmax_xx_0 = blocks.argmax_fs(10)



        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.blocks_tagged_stream_to_pdu_0, 'pdus'), (self.dnn_dnn_onnx_python_0, 'Input'))
        self.msg_connect((self.dnn_dnn_onnx_python_0, 'Output'), (self.blocks_pdu_to_tagged_stream_0, 'pdus'))
        self.connect((self.blocks_argmax_xx_0, 1), (self.blocks_null_sink_0, 0))
        self.connect((self.blocks_argmax_xx_0, 0), (self.qtgui_number_sink_0, 0))
        self.connect((self.blocks_multiply_const_xx_0, 0), (self.blocks_stream_to_tagged_stream_0, 0))
        self.connect((self.blocks_pdu_to_tagged_stream_0, 0), (self.blocks_stream_to_vector_0, 0))
        self.connect((self.blocks_stream_to_tagged_stream_0, 0), (self.blocks_tagged_stream_to_pdu_0, 0))
        self.connect((self.blocks_stream_to_vector_0, 0), (self.blocks_argmax_xx_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.blocks_uchar_to_float_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.video_sdl_sink_0_0, 0))
        self.connect((self.blocks_uchar_to_float_0, 0), (self.blocks_multiply_const_xx_0, 0))
        self.connect((self.source, 0), (self.blocks_throttle_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "classifier_test")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_output_len(self):
        return self.output_len

    def set_output_len(self, output_len):
        self.output_len = output_len

    def get_input_len(self):
        return self.input_len

    def set_input_len(self, input_len):
        self.input_len = input_len
        self.blocks_stream_to_tagged_stream_0.set_packet_len(self.input_len)
        self.blocks_stream_to_tagged_stream_0.set_packet_len_pmt(self.input_len)





def main(top_block_cls=classifier_test, options=None):

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
