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
    
    
    
    