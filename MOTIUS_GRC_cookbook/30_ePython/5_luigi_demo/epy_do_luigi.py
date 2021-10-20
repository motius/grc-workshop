"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr




"""All aspects related to supporting streaming luigi tasks.
"""
from abc import abstractmethod
from luigi.task import flatten
from luigi.util import requires
import luigi



class StreamMixin:
    """Mixin for Luigi (d6tflow) tasks to support stream processing rather than batch."""

    def run(self):
        """Handles routing of input and output for batch processing"""
        output = self._run(self.inputLoad())
        self.save(output)

    @abstractmethod
    def _run(self, input_data):
        pass


def stream(task, stream_inputs):
    """Calls Luigi task in stream format.

    Parameters
    ---
    task : luigi.task
        Root task to run
    stream_inputs : dict
        Dictionary of inputs meant to be used in place of entry points outputs. One key per entry
        point, with key matching task class name.

    Example
    ---
    > task = TaskProcess("blah")
    > d6tflow.preview(task)
     ===== Luigi Execution Preview =====


    └─--[TaskProcess-{'mode': 'blah'} (PENDING)]
       |--[TaskLoadData- (PENDING)]
       └─--[TaskReshape- (PENDING)]
          └─--[TaskLoadData2- (PENDING)]

     ===== Luigi Execution Preview =====
    > stream(task, {"TaskLoadData": np.ones(...), "TaskLoadData2": np.zeros(...)})
    """
    deps = flatten(task.requires())
    if deps:
        if not isinstance(task, StreamMixin):
            raise TypeError(
                f"Tasks {task} has dependencies, to use in streaming,"
                "it is expected to include StreamMixin."
            )

        # Step 1: recurse and call all dependencies
        inputs = []
        for dep_task in deps:
            inputs.append(stream(dep_task, stream_inputs))

        # Handle single inputs
        if len(inputs) == 1:
            inputs = inputs[0]

        return task._run(inputs)
    return stream_inputs[task.task_family]



'''Pipeline nodes
'''

'''
        TaskInput
            |
      TaskAddToData
            |
        multData
'''
class TaskInput(StreamMixin, luigi.Task):
    """Reshapes data"""

    def _run(self, input_data):
        # split per frame
        return input_data


@requires(TaskInput)                 #defines the requirements for this specific node
class TaskAddToData(StreamMixin, luigi.Task):
    """Add value to data"""
    add_val = luigi.parameter.FloatParameter()

    def _run(self, input_data):
        # split per frame
        return input_data + self.add_val


@requires(TaskAddToData)
class multData(StreamMixin, luigi.Task):
    """ Multiply val """
    multiply_val = luigi.parameter.FloatParameter()

    def _run(self, input_data):
        # split per frame
        return input_data * self.multiply_val




#Todo: create a "Y"-node
'''
TaskInput
    |
TaskAddToData   TaskInput
    |          |
     add_inputs
'''


@requires(TaskAddToData, TaskInput)
class add_inputs(StreamMixin, luigi.Task):
    """ Multiply val """

    def _run(self, input_data):
        # split per frame
        return input_data[0]+input_data [1]





"""All aspects related to GNURADIO
"""

class luigi_blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block for Luigi-pipelines"""

    def __init__(self, mult_var=1.0, add_var=1.0, luigi_model_path= '' ):  # only default arguments here
        """ Arguments to this function show up as parameters in GRC """
        gr.sync_block.__init__(
            self,
            name='Embedded Python Block',   # will show up in GRC
            in_sig=[np.single],
            out_sig=[np.single]
        )

        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        self.mult_var = mult_var
        self.add_var = add_var


    def work(self, input_items, output_items):
        """ Example: multiply with constant """

        output_items[0][:] = self.apply_luigi(input_items[0] )

        return len(output_items[0])




    def apply_luigi(self, input_items):
        """ This reprents the first test fo applying a luigi pipeline in GRC """
        #task = TaskAddToData( add_val=self.example_param )   #Calling a different node in the graph is also possible
        task=  multData( multiply_val= self.mult_var, add_val=self.add_var )

        output = stream(task, {"TaskInput": input_items})
        return (output)
