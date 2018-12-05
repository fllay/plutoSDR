#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: QPSK
# Author: fa
# Generated: Wed Dec  5 20:09:20 2018
##################################################

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

from gnuradio import blocks
from gnuradio import digital
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio import iio
from gnuradio import wxgui
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from gnuradio.wxgui import forms
from gnuradio.wxgui import scopesink2
from grc_gnuradio import blks2 as grc_blks2
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
import pmt
import wx


class top_block(grc_wxgui.top_block_gui):

    def __init__(self, hdr_format=digital.header_format_default(digital.packet_utils.default_access_code, 0)):
        grc_wxgui.top_block_gui.__init__(self, title="QPSK")

        ##################################################
        # Parameters
        ##################################################
        self.hdr_format = hdr_format

        ##################################################
        # Variables
        ##################################################
        self.sps = sps = 8
        self.excess_bw = excess_bw = 0.35
        self.samp_rate = samp_rate = 32000
        self.rrc_taps = rrc_taps = firdes.root_raised_cosine(1, sps, 1, excess_bw, 45)

        self.qpsk1 = qpsk1 = digital.constellation_qpsk().base()

        self.our_txt = our_txt = 0
        self.code1 = code1 = '010110011011101100010101011111101001001110001011010001101010001'

        ##################################################
        # Blocks
        ##################################################
        self.wxgui_scopesink2_2 = scopesink2.scope_sink_f(
        	self.GetWin(),
        	title='Scope Plot',
        	sample_rate=samp_rate,
        	v_scale=0,
        	v_offset=0,
        	t_scale=0,
        	ac_couple=False,
        	xy_mode=False,
        	num_inputs=1,
        	trig_mode=wxgui.TRIG_MODE_AUTO,
        	y_axis_label='Counts',
        )
        self.Add(self.wxgui_scopesink2_2.win)
        self.wxgui_scopesink2_0_0 = scopesink2.scope_sink_c(
        	self.GetWin(),
        	title='Scope Plot',
        	sample_rate=samp_rate,
        	v_scale=0,
        	v_offset=0,
        	t_scale=0,
        	ac_couple=False,
        	xy_mode=False,
        	num_inputs=1,
        	trig_mode=wxgui.TRIG_MODE_AUTO,
        	y_axis_label='Counts',
        )
        self.Add(self.wxgui_scopesink2_0_0.win)
        self.pluto_source_0 = iio.pluto_source('ip:pluto.local', int(800000000), int(2084000), int(20000000), 0x8000, True, True, True, "manual", 15, '', True)
        self.pluto_sink_2 = iio.pluto_sink('ip:pluto.local', int(800000000), int(2084000), int(20000000), 0x8000, False, 0, '', True)
        self._our_txt_text_box = forms.text_box(
        	parent=self.GetWin(),
        	value=self.our_txt,
        	callback=self.set_our_txt,
        	label='our_txt',
        	converter=forms.str_converter(),
        )
        self.Add(self._our_txt_text_box)
        self.notebook_0 = self.notebook_0 = wx.Notebook(self.GetWin(), style=wx.NB_TOP)
        self.notebook_0.AddPage(grc_wxgui.Panel(self.notebook_0), "tab1")
        self.notebook_0.AddPage(grc_wxgui.Panel(self.notebook_0), "tab2")
        self.notebook_0.AddPage(grc_wxgui.Panel(self.notebook_0), "tab3")
        self.Add(self.notebook_0)
        self.low_pass_filter_2 = filter.fir_filter_ccf(1, firdes.low_pass(
        	1, 2084000, 1000000, 500000, firdes.WIN_HAMMING, 6.76))
        self.digital_pfb_clock_sync_xxx_0 = digital.pfb_clock_sync_ccf(sps, 0.0682, (rrc_taps), 64, 16, 1.5, sps)
        self.digital_map_bb_0 = digital.map_bb(([0,1, 2, 3]))
        self.digital_lms_dd_equalizer_cc_0 = digital.lms_dd_equalizer_cc(21, 0.050, sps, qpsk1)
        self.digital_diff_decoder_bb_1 = digital.diff_decoder_bb(4)
        self.digital_costas_loop_cc_0 = digital.costas_loop_cc(0.0628, 4, True)
        self.digital_constellation_modulator_0 = digital.generic_mod(
          constellation=qpsk1,
          differential=True,
          samples_per_symbol=sps,
          pre_diff_code=True,
          excess_bw=excess_bw,
          verbose=False,
          log=False,
          )
        self.digital_constellation_decoder_cb_0 = digital.constellation_decoder_cb(qpsk1)
        self.blocks_unpack_k_bits_bb_0 = blocks.unpack_k_bits_bb(2)
        self.blocks_file_source_0 = blocks.file_source(gr.sizeof_char*1, '/Users/cake/Desktop/Projects/plutoSDR/2byte.txt', True)
        self.blocks_file_source_0.set_begin_tag(pmt.PMT_NIL)
        self.blocks_file_sink_1 = blocks.file_sink(gr.sizeof_char*1, '/Users/cake/Desktop/Projects/plutoSDR/out.txt', False)
        self.blocks_file_sink_1.set_unbuffered(True)
        self.blocks_char_to_float_1 = blocks.char_to_float(1, 1)
        self.blks2_packet_encoder_0_0 = grc_blks2.packet_mod_b(grc_blks2.packet_encoder(
        		samples_per_symbol=1,
        		bits_per_symbol=1,
        		preamble='',
        		access_code=code1,
        		pad_for_usrp=False,
        	),
        	payload_length=8,
        )
        self.blks2_packet_decoder_0_0 = grc_blks2.packet_demod_b(grc_blks2.packet_decoder(
        		access_code=code1,
        		threshold=-1,
        		callback=lambda ok, payload: self.blks2_packet_decoder_0_0.recv_pkt(ok, payload),
        	),
        )



        ##################################################
        # Connections
        ##################################################
        self.connect((self.blks2_packet_decoder_0_0, 0), (self.blocks_file_sink_1, 0))
        self.connect((self.blks2_packet_encoder_0_0, 0), (self.digital_constellation_modulator_0, 0))
        self.connect((self.blocks_char_to_float_1, 0), (self.wxgui_scopesink2_2, 0))
        self.connect((self.blocks_file_source_0, 0), (self.blks2_packet_encoder_0_0, 0))
        self.connect((self.blocks_unpack_k_bits_bb_0, 0), (self.blks2_packet_decoder_0_0, 0))
        self.connect((self.blocks_unpack_k_bits_bb_0, 0), (self.blocks_char_to_float_1, 0))
        self.connect((self.digital_constellation_decoder_cb_0, 0), (self.digital_map_bb_0, 0))
        self.connect((self.digital_constellation_modulator_0, 0), (self.pluto_sink_2, 0))
        self.connect((self.digital_costas_loop_cc_0, 0), (self.digital_constellation_decoder_cb_0, 0))
        self.connect((self.digital_costas_loop_cc_0, 0), (self.wxgui_scopesink2_0_0, 0))
        self.connect((self.digital_diff_decoder_bb_1, 0), (self.blocks_unpack_k_bits_bb_0, 0))
        self.connect((self.digital_lms_dd_equalizer_cc_0, 0), (self.digital_costas_loop_cc_0, 0))
        self.connect((self.digital_map_bb_0, 0), (self.digital_diff_decoder_bb_1, 0))
        self.connect((self.digital_pfb_clock_sync_xxx_0, 0), (self.digital_lms_dd_equalizer_cc_0, 0))
        self.connect((self.low_pass_filter_2, 0), (self.digital_pfb_clock_sync_xxx_0, 0))
        self.connect((self.pluto_source_0, 0), (self.low_pass_filter_2, 0))

    def get_hdr_format(self):
        return self.hdr_format

    def set_hdr_format(self, hdr_format):
        self.hdr_format = hdr_format

    def get_sps(self):
        return self.sps

    def set_sps(self, sps):
        self.sps = sps
        self.set_rrc_taps(firdes.root_raised_cosine(1, self.sps, 1, self.excess_bw, 45))

    def get_excess_bw(self):
        return self.excess_bw

    def set_excess_bw(self, excess_bw):
        self.excess_bw = excess_bw
        self.set_rrc_taps(firdes.root_raised_cosine(1, self.sps, 1, self.excess_bw, 45))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.wxgui_scopesink2_2.set_sample_rate(self.samp_rate)
        self.wxgui_scopesink2_0_0.set_sample_rate(self.samp_rate)

    def get_rrc_taps(self):
        return self.rrc_taps

    def set_rrc_taps(self, rrc_taps):
        self.rrc_taps = rrc_taps
        self.digital_pfb_clock_sync_xxx_0.update_taps((self.rrc_taps))

    def get_qpsk1(self):
        return self.qpsk1

    def set_qpsk1(self, qpsk1):
        self.qpsk1 = qpsk1

    def get_our_txt(self):
        return self.our_txt

    def set_our_txt(self, our_txt):
        self.our_txt = our_txt
        self._our_txt_text_box.set_value(self.our_txt)

    def get_code1(self):
        return self.code1

    def set_code1(self, code1):
        self.code1 = code1


def argument_parser():
    parser = OptionParser(usage="%prog: [options]", option_class=eng_option)
    return parser


def main(top_block_cls=top_block, options=None):
    if options is None:
        options, _ = argument_parser().parse_args()

    tb = top_block_cls()
    tb.Start(True)
    tb.Wait()


if __name__ == '__main__':
    main()
