"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!


This block specifically is based on the grc-"embeded python block"-tutorial founde here:
https://wiki.gnuradio.org/index.php/Embedded_Python_Block


It is used to convert a message from a gui-edit-message-block to a byte string
(that can the be written to a file)  -> see the picture in this folder for details


some more details on the polymorphic Types can be found here :
https://wiki.gnuradio.org/index.php/Polymorphic_Types_(PMTs)
"""

import numpy as np
from gnuradio import gr
import pmt

textboxValue = ""


class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block example - a simple multiply const"""

    """
        reads input from a message port
        outputs text
    """
    def __init__(self, example_param = 2):
        gr.sync_block.__init__(self,
            name = "Embedded Python demo",
            in_sig = None,
            out_sig = [np.byte])

        # register message ports
        self.message_port_register_in(pmt.intern('msg_in'))
        self.message_port_register_out(pmt.intern('clear_input'))
        self.set_msg_handler(pmt.intern('msg_in'), self.handle_msg) # this basically assigns the msg-handler

        # assing input parameters
        self.example_param = example_param


    def handle_msg(self, msg):
        global textboxValue

        textboxValue = pmt.symbol_to_string (msg)
        # print (textboxValue)

        # String to output
        # pmt_test = pmt.string_to_symbol("Test")    # convert string to pmt (polymorphic type)

        # publish pmt-message over a port
        # self.message_port_pub(pmt.intern('clear_input'), pmt_test )
        # self.message_port_pub(pmt.intern('clear_input'), pmt.intern('')) # send '' to the clear_input-port (the output of our system)

        print (textboxValue)


    def work(self, input_items, output_items):
        global textboxValue

        # get length of string
        _len = len(textboxValue)
        if (_len > 0):
            # terminate with LF
            textboxValue += "\n"
            _len += 1
            # store elements in output array
            for x in range(_len):
                output_items[0][x] = ord(textboxValue[x])
                
            textboxValue = ""
            self.message_port_pub(pmt.intern('clear_input'), pmt.intern(''))
            return (_len)
        else:
            return (0)
