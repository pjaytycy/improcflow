import unittest

from django.test import TestCase

from improcflow.logic import *

class PythonSubFlowTests(TestCase):
  def test_simple_sub_flow(self):
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
    
    
    element_input_1 = InputData()
    element_input_2 = InputData()
    element_output = OutputData()
    
    flow = Flow(title = "main_flow")
    flow.add_element(element_input_1)
    flow.add_element(element_input_2)
    flow.add_element(sub_flow)
    flow.add_element(element_output)
    flow.connect(element_input_1.data, sub_flow.term1)
    flow.connect(element_input_2.data, sub_flow.term2)
    flow.connect(sub_flow.sum, element_output.data)
    
    element_input_1.set_value(3)
    element_input_2.set_value(5)
    flow.run()
    
    self.assertEqual(8, element_output.result())
