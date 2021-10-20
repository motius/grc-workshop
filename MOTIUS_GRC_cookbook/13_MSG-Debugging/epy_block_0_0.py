"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr

import pmt
from datetime import datetime  # needed for some message testing


class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block example - a simple message passer"""

    def __init__(self, input_dim = 1, index= 10 ):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='ePy byte to message-passer-block',   # will show up in GRC
            in_sig  = [ np.single , np.single],#  [ (np.single, input_dim ) ],
            out_sig = [ np.single ]  # no output apart from the message-out
        )
        # Create output port
        self.message_port_register_out(pmt.intern('pmt_msg_out'))  # create a message out port
        self.index = index

    def work(self, input_items, output_items):
        """example: message passing in GRC"""

    #--create msg from string
        str_shape_value = str( len(input_items[0]) )# .shape )
        #prot_var_str_msg = pmt.intern ( str_shape_value )           #This seems to work for all types
        #proto_const_str_msg = pmt.string_to_symbol( '65535 +4 ' )   # This is string specific

    #--Message from real numbers
        integer_value = max(input_items[0]) # get index -> #max (input_items[0]) )
        #proto_long_msg =  pmt.intern( str( integer_value ) )         #for some reason, we can not directly display the info -> typcast to str.  | alternative:  long_msg =  pmt.from_long( integer_value ) #max (input_items[0]) )

        float_value = 1.7
        #proto_float_msg =  pmt.intern( str( float_value) ) #max (input_items[0]) )


    #--interacting with complex numbers in messages
        complex_num = 1j
        # complex_msg = pmt.from_complex(1j) #create a complex pmt  -> type(P2) = pmt.pmt_swig.swig_int_ptr
        # bool_complex = complex_msg.is_complex(P2) # check if message is complex
        #is_comp_messag =  pmt.intern( bool_complex )

    #--other types
        #P_true = pmt.PMT_T
        #P_false = pmt.PMT_F
        #P_nil = pmt.PMT_NIL

    #--Message from arrays (in this case our input )
        array = [42, 23, 23, 23, 223]
        arrayIn = input_items[1]


        filename = "/Applications/GNURadio-comp/projects/debug_test.txt"
        #gr.logger_config(filename, watch_period)  # Configures the logger with conf file filename
        #names = gr.logger_get_names()  # Returns the names of all loggers
        #gr.logger_reset_config()   # Resets logger config by removing all appenders

        #log=gr.logger("nameOfLogger")
        #log.debug("Log a debug message")
        #log.set_level("INFO")


        #for element in range( len(arrayIn) ):
        #    message = pmt.intern( str(element) )
        #    self.message_port_pub(pmt.intern('pmt_msg_out'),  message )


        #array= input_items[0][ 2:5 ]  #real world array

        #type_msg = pmt.intern( str( type(array) )) # conversion to str works  #array_msg = pmt.to_pmt([42, 23, 23, 23, 23]) #sample from the official website -> not working
        #array_msg = pmt.intern (str(array)) # conversion of a real input array

        #max_value = np.max(input_items[0])  index_max_value =  np.argmax(input_items[0]) len_value = len( input_items[0] )   dim= ( input_items[0]).shape

    #--Time stamp testing
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S.%fZ")[:-6]  # warning if you go with higher time resolution than "-3", th programm crashes imidiatly
        time_msg =  pmt.intern(current_time)

    #--Combination of different file type to a pmt-string-message
        #packed_msg= pmt.intern("Val: %s, Shape: %s [TS: %s]" %(str(array), str_shape_value, current_time) ) # + str(integer_value) + str(float_value) ) # str( type(input_items[0][:]) )
        packed_msg= pmt.intern("Shape:%s_TS:%s_%s" %( str(len(array) ) , current_time, str(arrayIn) ) ) # + str(integer_value) + str(float_value) ) # str( type(input_items[0][:]) )



    #--Send cyclic info on the input out via the msg-port
        self.message_port_pub(pmt.intern('pmt_msg_out'),  packed_msg ) # looks like we can only print a pmt-STRING-message

        output_items[0][:] = input_items[0] * 1# create output from inptu

        return len(output_items[0])

    def quitting():
        print("I lived and now i die!!!")
