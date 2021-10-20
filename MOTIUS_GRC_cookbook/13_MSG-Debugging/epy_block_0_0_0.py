"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!


This python block represents pmt-message creation from different data-Types
by using pmt-to-string and string-to-pmt casts

That for it mainly plays with the PMT-data type on which more can be found here :
https://wiki.gnuradio.org/index.php/Polymorphic_Types_(PMTs)


"""

import numpy as np
from gnuradio import gr
import pmt

textboxValue = ""


class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block example - pmt forwardning """

    """
        reads input from a message port
        outputs text (cast from pmt to string)
                and a message (cast back to pmt)
    """
    def __init__(self, example_param = 2):
        gr.sync_block.__init__(self,
            name = "message conversion demo",
            in_sig = None, # [np.single], #byte, single or complex64
            out_sig = [np.byte])

        # register message ports
        self.message_port_register_in(pmt.intern('msg_in'))
        self.message_port_register_out(pmt.intern('clear_input'))  # this port only sends '' when a message is recieved, interacting with the text box block
        self.message_port_register_out(pmt.intern('pmt_msg_out'))  # this represents our message out-port (format is pmt)

        # this basically assigns the msg-handler for the 'msg_in'-port
        self.set_msg_handler(pmt.intern('msg_in'), self.handle_msg)

        # assing input parameters
        self.example_param = example_param


    def handle_msg(self, msg):
        global textboxValue

        textboxValue = pmt.symbol_to_string (msg)
        print (textboxValue)
        print_out_str = 'message: '+ textboxValue
        print  ( print_out_str, '( original message:',  msg, ' -> converted to str:', textboxValue, ')' )
        # String to output
        #pmt_test = pmt.string_to_symbol("Test")                     # convert string to pmt (polymorphic type)
        #self.message_port_pub(pmt.intern('pmt_msg_out'), pmt_test ) # publish pmt-message over a port

        self.message_port_pub(pmt.intern('pmt_msg_out'),  msg )# pmt.intern(print_out_str) )# pmt.intern( 'message received! ')   )
        #check if pmt concatinating is possible via +



        # publish pmt-message over a port
        # self.message_port_pub(pmt.intern('clear_input'), pmt_test )
        # self.message_port_pub(pmt.intern('clear_input'), pmt.intern('')) # send '' to the clear_input-port (the output of our system)



        # Basic PMT info can be found here: https://wiki.gnuradio.org/index.php/Guided_Tutorial_Programming_Topics
        #P_tuple = pmt.to_pmt((1, 2, 3, 'spam', 'eggs'))
        #P_dict = pmt.to_pmt({'spam': 42, 'eggs': 23})



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
            # print
            textboxValue = ""
            self.message_port_pub(pmt.intern('clear_input'), pmt.intern(''))
            return (_len)
        else:
            return (0)
