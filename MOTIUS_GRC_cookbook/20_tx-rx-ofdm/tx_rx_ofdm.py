#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: OFDM TxRx
# Description: Example of an OFDM Transmitter
# GNU Radio version: v3.8.2.0-53-gc42a162b

from gnuradio import analog
from gnuradio import blocks
import numpy
from gnuradio import digital
from gnuradio import fft
from gnuradio.fft import window
from gnuradio import gr
from gnuradio.filter import firdes
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio.digital.utils import tagged_streams


class tx_rx_ofdm(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "OFDM TxRx")

        ##################################################
        # Variables
        ##################################################
        self.pilot_symbols_rx = pilot_symbols_rx = ((1, 1, 1, -1,),)
        self.pilot_carriers_rx = pilot_carriers_rx = ((-21, -7, 7, 21,),)
        self.payload_mod_tx = payload_mod_tx = digital.constellation_qpsk()
        self.payload_mod_rx = payload_mod_rx = digital.constellation_qpsk()
        self.packet_length_tag_key_rx = packet_length_tag_key_rx = "packet_len_rx"
        self.occupied_carriers_tx = occupied_carriers_tx = (list(range(-26, -21)) + list(range(-20, -7)) + list(range(-6, 0)) + list(range(1, 7)) + list(range(8, 21)) + list(range(22, 27)),)
        self.occupied_carriers_rx = occupied_carriers_rx = (list(range(-26, -21)) + list(range(-20, -7)) + list(range(-6, 0)) + list(range(1, 7)) + list(range(8, 21)) + list(range(22, 27)),)
        self.length_tag_key_tx = length_tag_key_tx = "packet_len_tx"
        self.length_tag_key_rx = length_tag_key_rx = "frame_len_rx"
        self.header_mod_tx = header_mod_tx = digital.constellation_bpsk()
        self.header_mod_rx = header_mod_rx = digital.constellation_bpsk()
        self.fft_len_rx = fft_len_rx = 64
        self.sync_word2_tx = sync_word2_tx = [0, 0, 0, 0, 0, 0, -1, -1, -1, -1, 1, 1, -1, -1, -1, 1, -1, 1, 1, 1, 1, 1, -1, -1, -1, -1, -1, 1, -1, -1, 1, -1, 0, 1, -1, 1, 1, 1, -1, 1, 1, 1, -1, 1, 1, 1, 1, -1, 1, -1, -1, -1, 1, -1, 1, -1, -1, -1, -1, 0, 0, 0, 0, 0]
        self.sync_word2_rx = sync_word2_rx = [0j, 0j, 0j, 0j, 0j, 0j, (-1+0j), (-1+0j), (-1+0j), (-1+0j), (1+0j), (1+0j), (-1+0j), (-1+0j), (-1+0j), (1+0j), (-1+0j), (1+0j), (1+0j), (1 +0j), (1+0j), (1+0j), (-1+0j), (-1+0j), (-1+0j), (-1+0j), (-1+0j), (1+0j), (-1+0j), (-1+0j), (1+0j), (-1+0j), 0j, (1+0j), (-1+0j), (1+0j), (1+0j), (1+0j), (-1+0j), (1+0j), (1+0j), (1+0j), (-1+0j), (1+0j), (1+0j), (1+0j), (1+0j), (-1+0j), (1+0j), (-1+0j), (-1+0j), (-1+0j), (1+0j), (-1+0j), (1+0j), (-1+0j), (-1+0j), (-1+0j), (-1+0j), 0j, 0j, 0j, 0j, 0j]
        self.sync_word1_tx = sync_word1_tx = [0., 0., 0., 0., 0., 0., 0., 1.41421356, 0., -1.41421356, 0., 1.41421356, 0., -1.41421356, 0., -1.41421356, 0., -1.41421356, 0., 1.41421356, 0., -1.41421356, 0., 1.41421356, 0., -1.41421356, 0., -1.41421356, 0., -1.41421356, 0., -1.41421356, 0., 1.41421356, 0., -1.41421356, 0., 1.41421356, 0., 1.41421356, 0., 1.41421356, 0., -1.41421356, 0., 1.41421356, 0., 1.41421356, 0., 1.41421356, 0., -1.41421356, 0., 1.41421356, 0., 1.41421356, 0., 1.41421356, 0., 0., 0., 0., 0., 0.]
        self.sync_word1_rx = sync_word1_rx = [0., 0., 0., 0., 0., 0., 0., 1.41421356, 0., -1.41421356, 0., 1.41421356, 0., -1.41421356, 0., -1.41421356, 0., -1.41421356, 0., 1.41421356, 0., -1.41421356, 0., 1.41421356, 0., -1.41421356, 0., -1.41421356, 0., -1.41421356, 0., -1.41421356, 0., 1.41421356, 0., -1.41421356, 0., 1.41421356, 0., 1.41421356, 0., 1.41421356, 0., -1.41421356, 0., 1.41421356, 0., 1.41421356, 0., 1.41421356, 0., -1.41421356, 0., 1.41421356, 0., 1.41421356, 0., 1.41421356, 0., 0., 0., 0., 0., 0.]
        self.samp_rate_tx = samp_rate_tx = 50000
        self.samp_rate_rx = samp_rate_rx = 10000
        self.rolloff = rolloff = 0
        self.pilot_symbols_tx = pilot_symbols_tx = ((1, 1, 1, -1,),)
        self.pilot_carriers_tx = pilot_carriers_tx = ((-21, -7, 7, 21,),)
        self.payload_equalizer_rx = payload_equalizer_rx = digital.ofdm_equalizer_simpledfe(fft_len_rx, payload_mod_rx.base(), occupied_carriers_rx, pilot_carriers_rx, pilot_symbols_rx, 1)
        self.packet_len_tx = packet_len_tx = 96
        self.packet_len_rx = packet_len_rx = 96
        self.header_formatter_tx = header_formatter_tx = digital.packet_header_ofdm(occupied_carriers_tx, n_syms=1, len_tag_key=length_tag_key_tx, frame_len_tag_key=length_tag_key_tx, bits_per_header_sym=header_mod_tx.bits_per_symbol(), bits_per_payload_sym=payload_mod_tx.bits_per_symbol(), scramble_header=False)
        self.header_formatter_rx = header_formatter_rx = digital.packet_header_ofdm(occupied_carriers_rx, n_syms=1, len_tag_key=packet_length_tag_key_rx, frame_len_tag_key=length_tag_key_rx, bits_per_header_sym=header_mod_rx.bits_per_symbol(), bits_per_payload_sym=payload_mod_rx.bits_per_symbol(), scramble_header=False)
        self.header_equalizer_rx = header_equalizer_rx = digital.ofdm_equalizer_simpledfe(fft_len_rx, header_mod_rx.base(), occupied_carriers_rx, pilot_carriers_rx, pilot_symbols_rx)
        self.fft_len_tx = fft_len_tx = 64

        ##################################################
        # Blocks
        ##################################################
        self.fft_vxx_1 = fft.fft_vcc(fft_len_rx, True, (), True, 1)
        self.fft_vxx_0_0 = fft.fft_vcc(fft_len_rx, True, (), True, 1)
        self.fft_vxx_0 = fft.fft_vcc(fft_len_tx, False, (), True, 1)
        self.digital_packet_headerparser_b_0 = digital.packet_headerparser_b(header_formatter_rx.base())
        self.digital_packet_headergenerator_bb_0 = digital.packet_headergenerator_bb(header_formatter_tx.base(), length_tag_key_tx)
        self.digital_ofdm_sync_sc_cfb_0_0 = digital.ofdm_sync_sc_cfb(fft_len_rx, fft_len_rx//4, False, 0.9)
        self.digital_ofdm_serializer_vcc_payload = digital.ofdm_serializer_vcc(fft_len_rx, occupied_carriers_rx, length_tag_key_rx, packet_length_tag_key_rx, 1, '', True)
        self.digital_ofdm_serializer_vcc_header = digital.ofdm_serializer_vcc(fft_len_rx, occupied_carriers_rx, length_tag_key_rx, '', 0, '', True)
        self.digital_ofdm_frame_equalizer_vcvc_1 = digital.ofdm_frame_equalizer_vcvc(payload_equalizer_rx.base(), fft_len_rx//4, length_tag_key_rx, True, 0)
        self.digital_ofdm_frame_equalizer_vcvc_0 = digital.ofdm_frame_equalizer_vcvc(header_equalizer_rx.base(), fft_len_rx//4, length_tag_key_rx, True, 1)
        self.digital_ofdm_cyclic_prefixer_0 = digital.ofdm_cyclic_prefixer(fft_len_tx, fft_len_tx + fft_len_tx//4, rolloff, length_tag_key_tx)
        self.digital_ofdm_chanest_vcvc_0 = digital.ofdm_chanest_vcvc(sync_word1_rx, sync_word2_rx, 1, 0, 3, False)
        self.digital_ofdm_carrier_allocator_cvc_0 = digital.ofdm_carrier_allocator_cvc( fft_len_tx, occupied_carriers_tx, pilot_carriers_tx, pilot_symbols_tx, (sync_word1_tx, sync_word2_tx), length_tag_key_tx, True)
        self.digital_header_payload_demux_0_0 = digital.header_payload_demux(
            3,
            fft_len_rx,
            fft_len_rx//4,
            length_tag_key_rx,
            "",
            True,
            gr.sizeof_gr_complex,
            "rx_time",
            samp_rate_rx,
            (),
            0)
        self.digital_crc32_bb_0_0 = digital.crc32_bb(True, packet_length_tag_key_rx, True)
        self.digital_crc32_bb_0 = digital.crc32_bb(False, length_tag_key_tx, True)
        self.digital_constellation_decoder_cb_1 = digital.constellation_decoder_cb(payload_mod_rx.base())
        self.digital_constellation_decoder_cb_0 = digital.constellation_decoder_cb(header_mod_rx.base())
        self.digital_chunks_to_symbols_xx_0_0 = digital.chunks_to_symbols_bc(payload_mod_tx.points(), 1)
        self.digital_chunks_to_symbols_xx_0 = digital.chunks_to_symbols_bc(header_mod_tx.points(), 1)
        self.blocks_throttle_0_0_0 = blocks.throttle(gr.sizeof_gr_complex*1, samp_rate_rx,True)
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_gr_complex*1, samp_rate_tx,True)
        self.blocks_tagged_stream_mux_0 = blocks.tagged_stream_mux(gr.sizeof_gr_complex*1, length_tag_key_tx, 0)
        self.blocks_tag_gate_0 = blocks.tag_gate(gr.sizeof_gr_complex * 1, False)
        self.blocks_tag_gate_0.set_single_key("")
        self.blocks_tag_debug_1 = blocks.tag_debug(gr.sizeof_char*1, 'Rx Bytes', "")
        self.blocks_tag_debug_1.set_display(True)
        self.blocks_stream_to_tagged_stream_0 = blocks.stream_to_tagged_stream(gr.sizeof_char, 1, packet_len_tx, length_tag_key_tx)
        self.blocks_repack_bits_bb_0_0 = blocks.repack_bits_bb(payload_mod_rx.bits_per_symbol(), 8, packet_length_tag_key_rx, True, gr.GR_LSB_FIRST)
        self.blocks_repack_bits_bb_0 = blocks.repack_bits_bb(8, payload_mod_tx.bits_per_symbol(), length_tag_key_tx, False, gr.GR_LSB_FIRST)
        self.blocks_null_sink_0 = blocks.null_sink(gr.sizeof_char*1)
        self.blocks_multiply_xx_0_0 = blocks.multiply_vcc(1)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_cc(0.05)
        self.blocks_delay_0_0 = blocks.delay(gr.sizeof_gr_complex*1, fft_len_rx+fft_len_rx//4)
        self.analog_random_source_x_0 = blocks.vector_source_b(list(map(int, numpy.random.randint(0, 255, 1000))), True)
        self.analog_frequency_modulator_fc_0_0 = analog.frequency_modulator_fc(-2.0/fft_len_rx)



        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.digital_packet_headerparser_b_0, 'header_data'), (self.digital_header_payload_demux_0_0, 'header_data'))
        self.connect((self.analog_frequency_modulator_fc_0_0, 0), (self.blocks_multiply_xx_0_0, 0))
        self.connect((self.analog_random_source_x_0, 0), (self.blocks_stream_to_tagged_stream_0, 0))
        self.connect((self.blocks_delay_0_0, 0), (self.blocks_multiply_xx_0_0, 1))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_tag_gate_0, 0))
        self.connect((self.blocks_multiply_xx_0_0, 0), (self.digital_header_payload_demux_0_0, 0))
        self.connect((self.blocks_repack_bits_bb_0, 0), (self.digital_chunks_to_symbols_xx_0_0, 0))
        self.connect((self.blocks_repack_bits_bb_0_0, 0), (self.digital_crc32_bb_0_0, 0))
        self.connect((self.blocks_stream_to_tagged_stream_0, 0), (self.digital_crc32_bb_0, 0))
        self.connect((self.blocks_tag_gate_0, 0), (self.blocks_throttle_0, 0))
        self.connect((self.blocks_tagged_stream_mux_0, 0), (self.digital_ofdm_carrier_allocator_cvc_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.blocks_throttle_0_0_0, 0))
        self.connect((self.blocks_throttle_0_0_0, 0), (self.blocks_delay_0_0, 0))
        self.connect((self.blocks_throttle_0_0_0, 0), (self.digital_ofdm_sync_sc_cfb_0_0, 0))
        self.connect((self.digital_chunks_to_symbols_xx_0, 0), (self.blocks_tagged_stream_mux_0, 0))
        self.connect((self.digital_chunks_to_symbols_xx_0_0, 0), (self.blocks_tagged_stream_mux_0, 1))
        self.connect((self.digital_constellation_decoder_cb_0, 0), (self.digital_packet_headerparser_b_0, 0))
        self.connect((self.digital_constellation_decoder_cb_1, 0), (self.blocks_repack_bits_bb_0_0, 0))
        self.connect((self.digital_crc32_bb_0, 0), (self.blocks_repack_bits_bb_0, 0))
        self.connect((self.digital_crc32_bb_0, 0), (self.digital_packet_headergenerator_bb_0, 0))
        self.connect((self.digital_crc32_bb_0_0, 0), (self.blocks_null_sink_0, 0))
        self.connect((self.digital_crc32_bb_0_0, 0), (self.blocks_tag_debug_1, 0))
        self.connect((self.digital_header_payload_demux_0_0, 0), (self.fft_vxx_0_0, 0))
        self.connect((self.digital_header_payload_demux_0_0, 1), (self.fft_vxx_1, 0))
        self.connect((self.digital_ofdm_carrier_allocator_cvc_0, 0), (self.fft_vxx_0, 0))
        self.connect((self.digital_ofdm_chanest_vcvc_0, 0), (self.digital_ofdm_frame_equalizer_vcvc_0, 0))
        self.connect((self.digital_ofdm_cyclic_prefixer_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.digital_ofdm_frame_equalizer_vcvc_0, 0), (self.digital_ofdm_serializer_vcc_header, 0))
        self.connect((self.digital_ofdm_frame_equalizer_vcvc_1, 0), (self.digital_ofdm_serializer_vcc_payload, 0))
        self.connect((self.digital_ofdm_serializer_vcc_header, 0), (self.digital_constellation_decoder_cb_0, 0))
        self.connect((self.digital_ofdm_serializer_vcc_payload, 0), (self.digital_constellation_decoder_cb_1, 0))
        self.connect((self.digital_ofdm_sync_sc_cfb_0_0, 0), (self.analog_frequency_modulator_fc_0_0, 0))
        self.connect((self.digital_ofdm_sync_sc_cfb_0_0, 1), (self.digital_header_payload_demux_0_0, 1))
        self.connect((self.digital_packet_headergenerator_bb_0, 0), (self.digital_chunks_to_symbols_xx_0, 0))
        self.connect((self.fft_vxx_0, 0), (self.digital_ofdm_cyclic_prefixer_0, 0))
        self.connect((self.fft_vxx_0_0, 0), (self.digital_ofdm_chanest_vcvc_0, 0))
        self.connect((self.fft_vxx_1, 0), (self.digital_ofdm_frame_equalizer_vcvc_1, 0))


    def get_pilot_symbols_rx(self):
        return self.pilot_symbols_rx

    def set_pilot_symbols_rx(self, pilot_symbols_rx):
        self.pilot_symbols_rx = pilot_symbols_rx
        self.set_header_equalizer_rx(digital.ofdm_equalizer_simpledfe(self.fft_len_rx, header_mod_rx.base(), self.occupied_carriers_rx, self.pilot_carriers_rx, self.pilot_symbols_rx))
        self.set_payload_equalizer_rx(digital.ofdm_equalizer_simpledfe(self.fft_len_rx, payload_mod_rx.base(), self.occupied_carriers_rx, self.pilot_carriers_rx, self.pilot_symbols_rx, 1))

    def get_pilot_carriers_rx(self):
        return self.pilot_carriers_rx

    def set_pilot_carriers_rx(self, pilot_carriers_rx):
        self.pilot_carriers_rx = pilot_carriers_rx
        self.set_header_equalizer_rx(digital.ofdm_equalizer_simpledfe(self.fft_len_rx, header_mod_rx.base(), self.occupied_carriers_rx, self.pilot_carriers_rx, self.pilot_symbols_rx))
        self.set_payload_equalizer_rx(digital.ofdm_equalizer_simpledfe(self.fft_len_rx, payload_mod_rx.base(), self.occupied_carriers_rx, self.pilot_carriers_rx, self.pilot_symbols_rx, 1))

    def get_payload_mod_tx(self):
        return self.payload_mod_tx

    def set_payload_mod_tx(self, payload_mod_tx):
        self.payload_mod_tx = payload_mod_tx

    def get_payload_mod_rx(self):
        return self.payload_mod_rx

    def set_payload_mod_rx(self, payload_mod_rx):
        self.payload_mod_rx = payload_mod_rx

    def get_packet_length_tag_key_rx(self):
        return self.packet_length_tag_key_rx

    def set_packet_length_tag_key_rx(self, packet_length_tag_key_rx):
        self.packet_length_tag_key_rx = packet_length_tag_key_rx
        self.set_header_formatter_rx(digital.packet_header_ofdm(self.occupied_carriers_rx, n_syms=1, len_tag_key=self.packet_length_tag_key_rx, frame_len_tag_key=self.length_tag_key_rx, bits_per_header_sym=header_mod_rx.bits_per_symbol(), bits_per_payload_sym=payload_mod_rx.bits_per_symbol(), scramble_header=False))

    def get_occupied_carriers_tx(self):
        return self.occupied_carriers_tx

    def set_occupied_carriers_tx(self, occupied_carriers_tx):
        self.occupied_carriers_tx = occupied_carriers_tx
        self.set_header_formatter_tx(digital.packet_header_ofdm(self.occupied_carriers_tx, n_syms=1, len_tag_key=self.length_tag_key_tx, frame_len_tag_key=self.length_tag_key_tx, bits_per_header_sym=header_mod_tx.bits_per_symbol(), bits_per_payload_sym=payload_mod_tx.bits_per_symbol(), scramble_header=False))

    def get_occupied_carriers_rx(self):
        return self.occupied_carriers_rx

    def set_occupied_carriers_rx(self, occupied_carriers_rx):
        self.occupied_carriers_rx = occupied_carriers_rx
        self.set_header_equalizer_rx(digital.ofdm_equalizer_simpledfe(self.fft_len_rx, header_mod_rx.base(), self.occupied_carriers_rx, self.pilot_carriers_rx, self.pilot_symbols_rx))
        self.set_header_formatter_rx(digital.packet_header_ofdm(self.occupied_carriers_rx, n_syms=1, len_tag_key=self.packet_length_tag_key_rx, frame_len_tag_key=self.length_tag_key_rx, bits_per_header_sym=header_mod_rx.bits_per_symbol(), bits_per_payload_sym=payload_mod_rx.bits_per_symbol(), scramble_header=False))
        self.set_payload_equalizer_rx(digital.ofdm_equalizer_simpledfe(self.fft_len_rx, payload_mod_rx.base(), self.occupied_carriers_rx, self.pilot_carriers_rx, self.pilot_symbols_rx, 1))

    def get_length_tag_key_tx(self):
        return self.length_tag_key_tx

    def set_length_tag_key_tx(self, length_tag_key_tx):
        self.length_tag_key_tx = length_tag_key_tx
        self.set_header_formatter_tx(digital.packet_header_ofdm(self.occupied_carriers_tx, n_syms=1, len_tag_key=self.length_tag_key_tx, frame_len_tag_key=self.length_tag_key_tx, bits_per_header_sym=header_mod_tx.bits_per_symbol(), bits_per_payload_sym=payload_mod_tx.bits_per_symbol(), scramble_header=False))

    def get_length_tag_key_rx(self):
        return self.length_tag_key_rx

    def set_length_tag_key_rx(self, length_tag_key_rx):
        self.length_tag_key_rx = length_tag_key_rx
        self.set_header_formatter_rx(digital.packet_header_ofdm(self.occupied_carriers_rx, n_syms=1, len_tag_key=self.packet_length_tag_key_rx, frame_len_tag_key=self.length_tag_key_rx, bits_per_header_sym=header_mod_rx.bits_per_symbol(), bits_per_payload_sym=payload_mod_rx.bits_per_symbol(), scramble_header=False))

    def get_header_mod_tx(self):
        return self.header_mod_tx

    def set_header_mod_tx(self, header_mod_tx):
        self.header_mod_tx = header_mod_tx

    def get_header_mod_rx(self):
        return self.header_mod_rx

    def set_header_mod_rx(self, header_mod_rx):
        self.header_mod_rx = header_mod_rx

    def get_fft_len_rx(self):
        return self.fft_len_rx

    def set_fft_len_rx(self, fft_len_rx):
        self.fft_len_rx = fft_len_rx
        self.set_header_equalizer_rx(digital.ofdm_equalizer_simpledfe(self.fft_len_rx, header_mod_rx.base(), self.occupied_carriers_rx, self.pilot_carriers_rx, self.pilot_symbols_rx))
        self.set_payload_equalizer_rx(digital.ofdm_equalizer_simpledfe(self.fft_len_rx, payload_mod_rx.base(), self.occupied_carriers_rx, self.pilot_carriers_rx, self.pilot_symbols_rx, 1))
        self.analog_frequency_modulator_fc_0_0.set_sensitivity(-2.0/self.fft_len_rx)
        self.blocks_delay_0_0.set_dly(self.fft_len_rx+self.fft_len_rx//4)

    def get_sync_word2_tx(self):
        return self.sync_word2_tx

    def set_sync_word2_tx(self, sync_word2_tx):
        self.sync_word2_tx = sync_word2_tx

    def get_sync_word2_rx(self):
        return self.sync_word2_rx

    def set_sync_word2_rx(self, sync_word2_rx):
        self.sync_word2_rx = sync_word2_rx

    def get_sync_word1_tx(self):
        return self.sync_word1_tx

    def set_sync_word1_tx(self, sync_word1_tx):
        self.sync_word1_tx = sync_word1_tx

    def get_sync_word1_rx(self):
        return self.sync_word1_rx

    def set_sync_word1_rx(self, sync_word1_rx):
        self.sync_word1_rx = sync_word1_rx

    def get_samp_rate_tx(self):
        return self.samp_rate_tx

    def set_samp_rate_tx(self, samp_rate_tx):
        self.samp_rate_tx = samp_rate_tx
        self.blocks_throttle_0.set_sample_rate(self.samp_rate_tx)

    def get_samp_rate_rx(self):
        return self.samp_rate_rx

    def set_samp_rate_rx(self, samp_rate_rx):
        self.samp_rate_rx = samp_rate_rx
        self.blocks_throttle_0_0_0.set_sample_rate(self.samp_rate_rx)

    def get_rolloff(self):
        return self.rolloff

    def set_rolloff(self, rolloff):
        self.rolloff = rolloff

    def get_pilot_symbols_tx(self):
        return self.pilot_symbols_tx

    def set_pilot_symbols_tx(self, pilot_symbols_tx):
        self.pilot_symbols_tx = pilot_symbols_tx

    def get_pilot_carriers_tx(self):
        return self.pilot_carriers_tx

    def set_pilot_carriers_tx(self, pilot_carriers_tx):
        self.pilot_carriers_tx = pilot_carriers_tx

    def get_payload_equalizer_rx(self):
        return self.payload_equalizer_rx

    def set_payload_equalizer_rx(self, payload_equalizer_rx):
        self.payload_equalizer_rx = payload_equalizer_rx

    def get_packet_len_tx(self):
        return self.packet_len_tx

    def set_packet_len_tx(self, packet_len_tx):
        self.packet_len_tx = packet_len_tx
        self.blocks_stream_to_tagged_stream_0.set_packet_len(self.packet_len_tx)
        self.blocks_stream_to_tagged_stream_0.set_packet_len_pmt(self.packet_len_tx)

    def get_packet_len_rx(self):
        return self.packet_len_rx

    def set_packet_len_rx(self, packet_len_rx):
        self.packet_len_rx = packet_len_rx

    def get_header_formatter_tx(self):
        return self.header_formatter_tx

    def set_header_formatter_tx(self, header_formatter_tx):
        self.header_formatter_tx = header_formatter_tx

    def get_header_formatter_rx(self):
        return self.header_formatter_rx

    def set_header_formatter_rx(self, header_formatter_rx):
        self.header_formatter_rx = header_formatter_rx

    def get_header_equalizer_rx(self):
        return self.header_equalizer_rx

    def set_header_equalizer_rx(self, header_equalizer_rx):
        self.header_equalizer_rx = header_equalizer_rx

    def get_fft_len_tx(self):
        return self.fft_len_tx

    def set_fft_len_tx(self, fft_len_tx):
        self.fft_len_tx = fft_len_tx





def main(top_block_cls=tx_rx_ofdm, options=None):
    tb = top_block_cls()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        sys.exit(0)

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    tb.start()

    try:
        input('Press Enter to quit: ')
    except EOFError:
        pass
    tb.stop()
    tb.wait()


if __name__ == '__main__':
    main()
