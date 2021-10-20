"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr
import pmt  # needed for message controlling


class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block example - basic messag creation"""

    def __init__(self, example_param=1.0, fileLocation= ''):  # only default arguments here
        """
        arguments to this function show up as parameters in GRC
        """
        gr.sync_block.__init__(
            self,
            name='ePy message-based debuging',   # will show up in GRC
            in_sig=[np.byte],
            out_sig=[np.single, np.byte] )# , np.complex64])   #np.float is NOT working np.float32 is!

        # if an attribute with the same name as a parameter is found, a callback is registered (properties work, too).
        self.example_param = example_param
        self.fileLocation= fileLocation

        # register message_output -> https://wiki.gnuradio.org/index.php/Embedded_Python_Block for a outclearing block-graph and
        # for a general overview look here: https://wiki.gnuradio.org/index.php/Message_Passing

        #self.message_port_register_out(pmt.intern('output'))  # generate output info

        #self.message_port_register_in(pmt.intern('input'))   # proto messag-in handling
        #self.set_msg_handler(pmt.intern("input"), self.handle_msg)


    #def handle_msg(self, msg):
    #   """ This is a mock message handler """
    #   print (msg)



    def work(self, input_items, output_items):
        """This method represents data interaction and message creationg
            right now, multiply by factor"""

        # get mat file from harddrive & the according vector

        # multiply the value using matrix multiplication scemes

        #self.message_port_pub(pmt.intern("output") , pmt.intern('message received!') ) #print info: port, message

        output_items[0][:] = input_items[0] * self.example_param
        return len(output_items[0])
