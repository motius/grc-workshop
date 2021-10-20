#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Top Block
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
from PyQt5.QtCore import QObject, pyqtSlot
from gnuradio import eng_notation
from gnuradio import analog
from gnuradio import audio
from gnuradio import blocks
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import gr
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio.qtgui import Range, RangeWidget
import iio

from gnuradio import qtgui

class top_block(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Top Block")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Top Block")
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

        self.settings = Qt.QSettings("GNU Radio", "top_block")

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
        self.working_samp_rate = working_samp_rate = 400e3
        self.volume = volume = 20
        self.transition_width = transition_width = 10e3
        self.source_selector_var = source_selector_var = 0
        self.samp_rate = samp_rate = 2e6
        self.rfBandwidth = rfBandwidth = 20e6
        self.freq_tx = freq_tx = 2398e6
        self.freq_rx = freq_rx = 98e6
        self.filePath = filePath = "/home/funki/git/gnu-radio/00_sample_code/00_GRC_COOK-BOOK/14_PlutoSDR_DEMO/sample.wav"
        self.channel_width = channel_width = 150e3
        self.center_freq = center_freq = 2400e6
        self.audio_transition = audio_transition = 2e3
        self.audio_samp_rate = audio_samp_rate = 48000
        self.audio_cutoff = audio_cutoff = 20e3

        ##################################################
        # Blocks
        ##################################################
        # Create the options list
        self._source_selector_var_options = (0, 1, )
        # Create the labels list
        self._source_selector_var_labels = ('wav-file', 'Mic/Line-in', )
        # Create the combo box
        self._source_selector_var_tool_bar = Qt.QToolBar(self)
        self._source_selector_var_tool_bar.addWidget(Qt.QLabel('Audio source' + ": "))
        self._source_selector_var_combo_box = Qt.QComboBox()
        self._source_selector_var_tool_bar.addWidget(self._source_selector_var_combo_box)
        for _label in self._source_selector_var_labels: self._source_selector_var_combo_box.addItem(_label)
        self._source_selector_var_callback = lambda i: Qt.QMetaObject.invokeMethod(self._source_selector_var_combo_box, "setCurrentIndex", Qt.Q_ARG("int", self._source_selector_var_options.index(i)))
        self._source_selector_var_callback(self.source_selector_var)
        self._source_selector_var_combo_box.currentIndexChanged.connect(
            lambda i: self.set_source_selector_var(self._source_selector_var_options[i]))
        # Create the radio buttons
        self.top_grid_layout.addWidget(self._source_selector_var_tool_bar)
        self._freq_tx_tool_bar = Qt.QToolBar(self)
        self._freq_tx_tool_bar.addWidget(Qt.QLabel('freq_tx' + ": "))
        self._freq_tx_line_edit = Qt.QLineEdit(str(self.freq_tx))
        self._freq_tx_tool_bar.addWidget(self._freq_tx_line_edit)
        self._freq_tx_line_edit.returnPressed.connect(
            lambda: self.set_freq_tx(eng_notation.str_to_num(str(self._freq_tx_line_edit.text()))))
        self.top_grid_layout.addWidget(self._freq_tx_tool_bar)
        self._volume_range = Range(0, 100, 10, 20, 200)
        self._volume_win = RangeWidget(self._volume_range, self.set_volume, 'volume', "counter_slider", float)
        self.top_grid_layout.addWidget(self._volume_win)
        self.rational_resampler_xxx_0_0 = filter.rational_resampler_fff(
                interpolation=int(working_samp_rate/audio_samp_rate),
                decimation=1,
                taps=firdes.low_pass(1,working_samp_rate,audio_cutoff,audio_transition),
                fractional_bw=None)
        self.rational_resampler_xxx_0 = filter.rational_resampler_ccc(
                interpolation=int(samp_rate/working_samp_rate),
                decimation=1,
                taps=firdes.low_pass(1,samp_rate,channel_width/2,transition_width),
                fractional_bw=None)
        self.iio_pluto_sink_0 = iio.pluto_sink('pluto.local', int(center_freq), int(samp_rate), int(rfBandwidth), 32768, False, 0.0, '', True)
        self._freq_rx_tool_bar = Qt.QToolBar(self)
        self._freq_rx_tool_bar.addWidget(Qt.QLabel('freq_rx' + ": "))
        self._freq_rx_line_edit = Qt.QLineEdit(str(self.freq_rx))
        self._freq_rx_tool_bar.addWidget(self._freq_rx_line_edit)
        self._freq_rx_line_edit.returnPressed.connect(
            lambda: self.set_freq_rx(eng_notation.str_to_num(str(self._freq_rx_line_edit.text()))))
        self.top_grid_layout.addWidget(self._freq_rx_tool_bar)
        self.blocks_wavfile_source_0 = blocks.wavfile_source(filePath, True)
        self.blocks_selector_0 = blocks.selector(gr.sizeof_float*1,source_selector_var,0)
        self.blocks_selector_0.set_enabled(True)
        self.blocks_multiply_xx_0 = blocks.multiply_vcc(1)
        self.audio_source_0 = audio.source(audio_samp_rate, '', True)
        self.analog_wfm_tx_0 = analog.wfm_tx(
        	audio_rate=int(working_samp_rate),
        	quad_rate=int(working_samp_rate),
        	tau=75e-6,
        	max_dev=75e3,
        	fh=-1.0,
        )
        self.analog_sig_source_x_0 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, freq_tx-center_freq, 1, 0, 0)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_multiply_xx_0, 1))
        self.connect((self.analog_wfm_tx_0, 0), (self.rational_resampler_xxx_0, 0))
        self.connect((self.audio_source_0, 0), (self.blocks_selector_0, 1))
        self.connect((self.blocks_multiply_xx_0, 0), (self.iio_pluto_sink_0, 0))
        self.connect((self.blocks_selector_0, 0), (self.rational_resampler_xxx_0_0, 0))
        self.connect((self.blocks_wavfile_source_0, 0), (self.blocks_selector_0, 0))
        self.connect((self.rational_resampler_xxx_0, 0), (self.blocks_multiply_xx_0, 0))
        self.connect((self.rational_resampler_xxx_0_0, 0), (self.analog_wfm_tx_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "top_block")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_working_samp_rate(self):
        return self.working_samp_rate

    def set_working_samp_rate(self, working_samp_rate):
        self.working_samp_rate = working_samp_rate
        self.rational_resampler_xxx_0_0.set_taps(firdes.low_pass(1,self.working_samp_rate,self.audio_cutoff,self.audio_transition))

    def get_volume(self):
        return self.volume

    def set_volume(self, volume):
        self.volume = volume

    def get_transition_width(self):
        return self.transition_width

    def set_transition_width(self, transition_width):
        self.transition_width = transition_width
        self.rational_resampler_xxx_0.set_taps(firdes.low_pass(1,self.samp_rate,self.channel_width/2,self.transition_width))

    def get_source_selector_var(self):
        return self.source_selector_var

    def set_source_selector_var(self, source_selector_var):
        self.source_selector_var = source_selector_var
        self._source_selector_var_callback(self.source_selector_var)
        self.blocks_selector_0.set_input_index(self.source_selector_var)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate)
        self.iio_pluto_sink_0.set_params(int(self.center_freq), int(self.samp_rate), int(self.rfBandwidth), 0.0, '', True)
        self.rational_resampler_xxx_0.set_taps(firdes.low_pass(1,self.samp_rate,self.channel_width/2,self.transition_width))

    def get_rfBandwidth(self):
        return self.rfBandwidth

    def set_rfBandwidth(self, rfBandwidth):
        self.rfBandwidth = rfBandwidth
        self.iio_pluto_sink_0.set_params(int(self.center_freq), int(self.samp_rate), int(self.rfBandwidth), 0.0, '', True)

    def get_freq_tx(self):
        return self.freq_tx

    def set_freq_tx(self, freq_tx):
        self.freq_tx = freq_tx
        Qt.QMetaObject.invokeMethod(self._freq_tx_line_edit, "setText", Qt.Q_ARG("QString", eng_notation.num_to_str(self.freq_tx)))
        self.analog_sig_source_x_0.set_frequency(self.freq_tx-self.center_freq)

    def get_freq_rx(self):
        return self.freq_rx

    def set_freq_rx(self, freq_rx):
        self.freq_rx = freq_rx
        Qt.QMetaObject.invokeMethod(self._freq_rx_line_edit, "setText", Qt.Q_ARG("QString", eng_notation.num_to_str(self.freq_rx)))

    def get_filePath(self):
        return self.filePath

    def set_filePath(self, filePath):
        self.filePath = filePath

    def get_channel_width(self):
        return self.channel_width

    def set_channel_width(self, channel_width):
        self.channel_width = channel_width
        self.rational_resampler_xxx_0.set_taps(firdes.low_pass(1,self.samp_rate,self.channel_width/2,self.transition_width))

    def get_center_freq(self):
        return self.center_freq

    def set_center_freq(self, center_freq):
        self.center_freq = center_freq
        self.analog_sig_source_x_0.set_frequency(self.freq_tx-self.center_freq)
        self.iio_pluto_sink_0.set_params(int(self.center_freq), int(self.samp_rate), int(self.rfBandwidth), 0.0, '', True)

    def get_audio_transition(self):
        return self.audio_transition

    def set_audio_transition(self, audio_transition):
        self.audio_transition = audio_transition
        self.rational_resampler_xxx_0_0.set_taps(firdes.low_pass(1,self.working_samp_rate,self.audio_cutoff,self.audio_transition))

    def get_audio_samp_rate(self):
        return self.audio_samp_rate

    def set_audio_samp_rate(self, audio_samp_rate):
        self.audio_samp_rate = audio_samp_rate

    def get_audio_cutoff(self):
        return self.audio_cutoff

    def set_audio_cutoff(self, audio_cutoff):
        self.audio_cutoff = audio_cutoff
        self.rational_resampler_xxx_0_0.set_taps(firdes.low_pass(1,self.working_samp_rate,self.audio_cutoff,self.audio_transition))





def main(top_block_cls=top_block, options=None):

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
