"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr


class iterator_blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """ Embedded Python Block - a simple iterator with a definable stepsize """

    def __init__(self, starting_index = 0, max_index = 200, stepsize = 1.0):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='Embedded Python Block',   # will show up in GRC
            in_sig=[],                      # as this is a simple "function-generator", we do not need any input
            out_sig=[np.single]             # the output should be
        )

        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        self.min_index = starting_index
        self.max_index = max_index
        self.iterator  = starting_index
        self.stepsize  = stepsize


    def work(self, input_items, output_items):
        """example: iterate through a variable -> start at "starting_index" and end at "max_index" """

        if self.iterator< self.max_index :
            self.iterator = self.iterator + self.stepsize
        else:
            self.iterator = self.min_index


        output_items[0][:] =  self.iterator
        return len(output_items[0])
