import unittest

from django.test import TestCase

from improcflow.logic import *

class PythonSubFlowTests(TestCase):
  def setUp(self):
    sub_flow_input_1 = InputData(title = "term1")
    sub_flow_input_2 = InputData(title = "term2")
    sub_flow_sum = PythonAddition()
    sub_flow_output = OutputData(title = "sum")
    
    sub_flow = Flow(title = "wrap_add")
    sub_flow.add_element(sub_flow_input_1)
    sub_flow.add_element(sub_flow_input_2)
    sub_flow.add_element(sub_flow_sum)
    sub_flow.add_element(sub_flow_output)
    sub_flow.connect(sub_flow_input_1.data, sub_flow_sum.term1)
    sub_flow.connect(sub_flow_input_2.data, sub_flow_sum.term2)
    sub_flow.connect(sub_flow_sum.sum, sub_flow_output.data)
    
    self.sub_flow = sub_flow
    
    self.element_input_1 = InputData()
    self.element_input_2 = InputData()
    self.element_output = OutputData()
    
    self.flow = Flow(title = "main_flow")
    self.flow.add_element(self.element_input_1)
    self.flow.add_element(self.element_input_2)
    self.flow.add_element(self.sub_flow)
    self.flow.add_element(self.element_output)
    self.flow.connect(self.element_input_1.data, self.sub_flow.term1)
    self.flow.connect(self.element_input_2.data, self.sub_flow.term2)
    self.flow.connect(self.sub_flow.sum, self.element_output.data)

    self.element_input_1.set_value(3)
    self.element_input_2.set_value(5)
    
  
  def test_simple_sub_flow(self):
    self.flow.run()
    
    self.assertEqual(8, self.element_output.result())

  def test_control_signal_true_allows_execution(self):
    element_bool = InputData()
    element_bool.set_value(True)
    self.flow.add_element(element_bool)
    self.flow.connect(element_bool.data, self.sub_flow.flow_control)
    self.flow.run()
    
    self.assertEqual(8, self.element_output.result())
    
  def test_control_signal_false_blocks_execution(self):
    element_bool = InputData()
    element_bool.set_value(False)
    self.flow.add_element(element_bool)
    self.flow.connect(element_bool.data, self.sub_flow.flow_control)
    self.flow.run()
    
    self.assertIsNone(self.element_output.result())
    
  def test_control_signal_blocked_blocks_execution(self):
    element_bool = InputData()
    element_bool.set_value(True)    # assign the value True, which would normally allow to continue
    element_bool.block()            # but mark the element as blocked, which prevents propagation
    self.flow.add_element(element_bool)
    self.flow.connect(element_bool.data, self.sub_flow.flow_control)
    self.flow.run()
    
    self.assertIsNone(self.element_output.result())
  
  def test_control_signal_invalid_blocks_execution(self):
    element_bool = InputData()
    # not assigning any value makes the connector "invalid"
    self.flow.add_element(element_bool)
    self.flow.connect(element_bool.data, self.sub_flow.flow_control)
    self.flow.run()
    
    self.assertIsNone(self.element_output.result())

  def test_data_signal_blocked_blocks_execution(self):
    self.element_input_1.block()
    self.flow.run()
    
    self.assertIsNone(self.element_output.result())

# tests for these 3 cases:
# invalidate control connection (not disconnect) ==> invalidate mean & result
# disconnect control connection which was False ==> invalidate mean & result, set control signal default (true)
# disconnect control connection which was True ==> no changes in invalidate/control signal

  def test_disconnect_control_connection_which_was_false(self):
    element_bool = InputData()
    element_bool.set_value(False)
    self.flow.add_element(element_bool)
    control_connection = self.flow.connect(element_bool.data, self.sub_flow.flow_control)
    self.flow.run()
    self.assertIsNone(self.element_output.result())
    self.flow.disconnect(control_connection)
    self.flow.run()
    self.assertEqual(8, self.element_output.result())
  
  def test_disconnect_control_connection_which_was_true(self):
    element_bool = InputData()
    element_bool.set_value(True)
    self.flow.add_element(element_bool)
    control_connection = self.flow.connect(element_bool.data, self.sub_flow.flow_control)
    self.flow.run()
    self.assertEqual(8, self.element_output.result())
    self.flow.disconnect(control_connection)
    self.assertEqual(8, self.element_output.result())
    
  def test_invalidate_control_connection(self):
    element_bool = InputData()
    element_bool.set_value(True)
    self.flow.add_element(element_bool)
    control_connection = self.flow.connect(element_bool.data, self.sub_flow.flow_control)
    self.flow.run()
    self.assertEqual(8, self.element_output.result())
    element_bool.set_value(10)
    self.assertIsNone(self.element_output.result())
   
  def test_two_calls_to_run(self):
    self.flow.run()
    self.assertEqual(8, self.element_output.result())
    
    self.element_input_1.set_value(9)
    self.element_input_2.set_value(-3)
    self.flow.run()
    self.assertEqual(6, self.element_output.result())
    
  def test_multiple_set_value_calls(self):
    self.element_input_1.set_value(9)
    self.element_input_2.set_value(-3)
    self.element_input_2.set_value(0)
    self.element_input_2.set_value(2)
    self.flow.run()
    self.assertEqual(11, self.element_output.result())
    self.element_input_2.set_value(5)
    self.assertIsNone(self.element_output.result())
  
  def test_change_flow_structure_between_two_calls_to_run(self):
    self.flow.run()
    self.assertEqual(8, self.element_output.result())
    self.flow.connect(self.element_input_1.data, self.sub_flow.term2)
    self.flow.run()
    self.assertEqual(6, self.element_output.result())
    
    