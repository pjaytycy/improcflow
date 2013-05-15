import unittest

from django.test import TestCase

from improcflow.logic import *

   
class ControlLogicTests(TestCase):
  def test_control_signal_true_allows_execution(self):
    element_input = InputData(title = "element_input")
    element_input.set_value([[1, 2, 3], [4, 5, 6]])
    element_mean = OpenCVMean(title = "element_mean")
    element_output = OutputData(title = "element_output")
    element_bool = InputData(title = "element_bool")
    element_bool.set_value(True)
    
    flow = Flow()
    flow.add_element(element_input)
    flow.add_element(element_mean)
    flow.add_element(element_bool)
    flow.add_element(element_output)
    flow.connect(element_input.data, element_mean.src, title = "data_connection_1")
    flow.connect(element_mean.mean, element_output.data, title = "data_connection_2")
    flow.connect(element_bool.data, element_mean.flow_control, title = "control_connection")
    flow.run()
    
    self.assertEqual(3.5, element_output.result())
    self.assertEqual(False, element_mean.is_blocked())
  
  
  def test_control_signal_false_blocks_execution(self):
    element_input = InputData(title = "element_input")
    element_input.set_value([[1, 2, 3], [4, 5, 6]])
    element_mean = OpenCVMean(title = "element_mean")
    element_output = OutputData(title = "element_output")
    element_bool = InputData(title = "element_bool")
    element_bool.set_value(False)
    
    flow = Flow()
    flow.add_element(element_input)
    flow.add_element(element_mean)
    flow.add_element(element_bool)
    flow.add_element(element_output)
    flow.connect(element_input.data, element_mean.src, title = "data_connection_1")
    flow.connect(element_mean.mean, element_output.data, title = "data_connection_2")
    flow.connect(element_bool.data, element_mean.flow_control, title = "control_connection")
    flow.run()
    
    self.assertIsNone(element_output.result())
    self.assertEqual(True, element_mean.is_blocked())
  
  
  def test_control_signal_blocked_blocks_execution(self):
    element_input = InputData(title = "element_input")
    element_input.set_value([[1, 2, 3], [4, 5, 6]])
    element_mean = OpenCVMean(title = "element_mean")
    element_output = OutputData(title = "element_output")
    element_bool = InputData(title = "element_bool")
    element_bool.set_value(True)    # assign the value True, which would normally allow to continue
    element_bool.block()            # but mark the element as blocked, which prevents propagation
    
    flow = Flow()
    flow.add_element(element_input)
    flow.add_element(element_mean)
    flow.add_element(element_bool)
    flow.add_element(element_output)
    flow.connect(element_input.data, element_mean.src, title = "data_connection_1")
    flow.connect(element_mean.mean, element_output.data, title = "data_connection_2")
    flow.connect(element_bool.data, element_mean.flow_control, title = "control_connection")
    flow.run()
    
    self.assertIsNone(element_output.result())
    self.assertEqual(True, element_mean.is_blocked())
  
  
  def test_control_signal_invalid_prevents_execution(self):
    element_input = InputData(title = "element_input")
    element_input.set_value([[1, 2, 3], [4, 5, 6]])
    element_mean = OpenCVMean(title = "element_mean")
    element_output = OutputData(title = "element_output")
    element_bool = InputData(title = "element_bool")
    # not assigning any value makes the connector "invalid"
    
    flow = Flow()
    flow.add_element(element_input)
    flow.add_element(element_mean)
    flow.add_element(element_bool)
    flow.add_element(element_output)
    flow.connect(element_input.data, element_mean.src, title = "data_connection_1")
    flow.connect(element_mean.mean, element_output.data, title = "data_connection_2")
    flow.connect(element_bool.data, element_mean.flow_control, title = "control_connection")
    flow.run()
    
    self.assertIsNone(element_output.result())
    
    # element_mean will not be "blocked", because untill the last moment we wait for the possibility for the
    # control flow signal to become valid. When that happens, we will know if we can run or need to block.
    # As this does not happen here, the element will never be ready or blocked.
    self.assertEqual(False, element_mean.is_blocked())
    self.assertEqual(False, element_mean.is_ready())
    self.assertEqual(False, element_mean.is_done())
    self.assertEqual(0, element_mean.get_number_of_executions())
  
  def test_data_signal_blocked_blocks_execution(self):
    element_input = InputData(title = "element_input")
    element_input.set_value([[1, 2, 3], [4, 5, 6]])
    element_mean = OpenCVMean(title = "element_mean")
    element_output = OutputData(title = "element_output")
 
    element_input.block()
    
    flow = Flow()
    flow.add_element(element_input)
    flow.add_element(element_mean)
    flow.add_element(element_output)
    flow.connect(element_input.data, element_mean.src, title = "data_connection_1")
    flow.connect(element_mean.mean, element_output.data, title = "data_connection_2")
    flow.run()
    
    self.assertIsNone(element_output.result())
    self.assertEqual(True, element_mean.is_blocked())
    self.assertEqual(True, element_output.is_blocked())

# tests for these 3 cases:
# invalidate control connection (not disconnect) ==> invalidate mean & result
# disconnect control connection which was False ==> invalidate mean & result, set control signal default (true)
# disconnect control connection which was True ==> no changes in invalidate/control signal

  def test_disconnect_control_connection_which_was_False(self):
    element_input = InputData(title = "element_input")
    element_input.set_value([[1, 2, 3], [4, 5, 6]])
    element_mean = OpenCVMean(title = "element_mean")
    element_output = OutputData(title = "element_output")
    element_bool = InputData(title = "element_bool")
    element_bool.set_value(False)
    
    flow = Flow()
    flow.add_element(element_input)
    flow.add_element(element_mean)
    flow.add_element(element_bool)
    flow.add_element(element_output)
    flow.connect(element_input.data, element_mean.src, title = "data_connection_1")
    flow.connect(element_mean.mean, element_output.data, title = "data_connection_2")
    control_connection = flow.connect(element_bool.data, element_mean.flow_control, title = "control_connection")
    
    flow.run()
    self.assertIsNone(element_output.result())
    self.assertEqual(True, element_mean.is_blocked())

    flow.disconnect(control_connection)
    self.assertEqual(False, element_mean.is_blocked())
    
    flow.run()
    self.assertEqual(False, element_mean.is_blocked())
    self.assertEqual(3.5, element_output.result())

  def test_disconnect_control_connection_which_was_True(self):
    element_input = InputData(title = "element_input")
    element_input.set_value([[1, 2, 3], [4, 5, 6]])
    element_mean = OpenCVMean(title = "element_mean")
    element_output = OutputData(title = "element_output")
    element_bool = InputData(title = "element_bool")
    element_bool.set_value(True)
    
    flow = Flow()
    flow.add_element(element_input)
    flow.add_element(element_mean)
    flow.add_element(element_bool)
    flow.add_element(element_output)
    flow.connect(element_input.data, element_mean.src, title = "data_connection_1")
    flow.connect(element_mean.mean, element_output.data, title = "data_connection_2")
    control_connection = flow.connect(element_bool.data, element_mean.flow_control, title = "control_connection")
    
    flow.run()
    self.assertEqual(False, element_mean.is_blocked())
    self.assertEqual(3.5, element_output.result())

    flow.disconnect(control_connection)
    self.assertEqual(False, element_mean.is_blocked())
    self.assertEqual(3.5, element_output.result())
  
  def test_invalidate_control_connection(self):
    element_input = InputData(title = "element_input")
    element_input.set_value([[1, 2, 3], [4, 5, 6]])
    element_mean = OpenCVMean(title = "element_mean")
    element_output = OutputData(title = "element_output")
    element_bool = InputData(title = "element_bool")
    element_bool.set_value(True)
    
    flow = Flow()
    flow.add_element(element_input)
    flow.add_element(element_mean)
    flow.add_element(element_bool)
    flow.add_element(element_output)
    flow.connect(element_input.data, element_mean.src, title = "data_connection_1")
    flow.connect(element_mean.mean, element_output.data, title = "data_connection_2")
    control_connection = flow.connect(element_bool.data, element_mean.flow_control, title = "control_connection")
    
    flow.run()
    self.assertEqual(False, element_mean.is_blocked())
    self.assertEqual(3.5, element_output.result())

    element_bool.set_value(10)
    self.assertEqual(False, element_mean.is_blocked())
    self.assertEqual(False, element_mean.is_ready())
    self.assertEqual(False, element_mean.is_done())
    self.assertIsNone(element_output.result())
  
  def test_conditional_assignment(self):
    element_input_A = InputData(title = "element_input_A")
    element_input_A.set_value([[1, 3, 5], [7, 9, 11]])
    element_input_B = InputData(title = "element_input_B")
    element_input_B.set_value([[2, 4, 6], [8, 10, 12]])
    element_input_A_enable = InputData(title = "element_input_A_enable")
    element_input_B_enable = InputData(title = "element_input_B_enable")
    element_cond_assign = ConditionalAssignment(title = "element_cond_assign")
    element_mean = OpenCVMean(title = "element_mean")
    element_output = OutputData(title = "element_output")
    
    flow = Flow()
    flow.add_element(element_input_A)
    flow.add_element(element_input_B)
    flow.add_element(element_input_A_enable)
    flow.add_element(element_input_B_enable)
    flow.add_element(element_cond_assign)
    flow.add_element(element_mean)
    flow.add_element(element_output)
    
    flow.connect(element_input_A_enable.data, element_input_A.flow_control)
    flow.connect(element_input_B_enable.data, element_input_B.flow_control)
    flow.connect(element_input_A.data, element_cond_assign.next_input())
    flow.connect(element_input_B.data, element_cond_assign.next_input())
    flow.connect(element_cond_assign.output, element_mean.src)
    flow.connect(element_mean.mean, element_output.data)
    
    # 1) undefined
    flow.run()
    self.assertIsNone(element_output.result())
    
    # 2) choose element A
    element_input_A_enable.set_value(True)
    element_input_B_enable.set_value(False)
    flow.run()
    self.assertEqual(6, element_output.result())
    
    # 3) choose element B
    element_input_A_enable.set_value(False)
    element_input_B_enable.set_value(True)
    flow.run()
    self.assertEqual(7, element_output.result())
    
    # 4) enable both
    element_input_A_enable.set_value(True)
    element_input_B_enable.set_value(True)
    flow.run()
    self.assertIsNone(element_output.result())
    
    # 5) disable both
    element_input_A_enable.set_value(False)
    element_input_B_enable.set_value(False)
    flow.run()
    self.assertIsNone(element_output.result())
    
