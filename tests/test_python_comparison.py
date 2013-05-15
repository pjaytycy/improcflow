import unittest

from django.test import TestCase

from improcflow.logic import *

class PythonComparisonTests(TestCase):
  def test_equal_integers(self):
    element_input_1 = InputData()
    element_input_2 = InputData()
    element_equal = PythonIsEqualTo()
    element_output = OutputData()
    
    flow = Flow()
    flow.add_element(element_input_1)
    flow.add_element(element_input_2)
    flow.add_element(element_equal)
    flow.add_element(element_output)
    flow.connect(element_input_1.data, element_equal.left)
    flow.connect(element_input_2.data, element_equal.right)
    flow.connect(element_equal.result, element_output.data)
    
    element_input_1.set_value(3)
    element_input_2.set_value(5)
    flow.run()
    self.assertFalse(element_output.result())
    
    element_input_1.set_value(3)
    element_input_2.set_value(3)
    flow.run()
    self.assertTrue(element_output.result())

    element_input_1.set_value(3)
    element_input_2.set_value(-5)
    flow.run()
    self.assertFalse(element_output.result())

    element_input_1.set_value(-5)
    element_input_2.set_value(-5)
    flow.run()
    self.assertTrue(element_output.result())
    
    element_input_1.set_value(-8)
    element_input_2.set_value(-5)
    flow.run()
    self.assertFalse(element_output.result())
    
    element_input_1.set_value(0)
    element_input_2.set_value(0)
    flow.run()
    self.assertTrue(element_output.result())

  def test_inequal_integers(self):
    element_input_1 = InputData()
    element_input_2 = InputData()
    element_notequal = PythonIsNotEqualTo()
    element_output = OutputData()
    
    flow = Flow()
    flow.add_element(element_input_1)
    flow.add_element(element_input_2)
    flow.add_element(element_notequal)
    flow.add_element(element_output)
    flow.connect(element_input_1.data, element_notequal.left)
    flow.connect(element_input_2.data, element_notequal.right)
    flow.connect(element_notequal.result, element_output.data)
    
    element_input_1.set_value(3)
    element_input_2.set_value(5)
    flow.run()
    self.assertTrue(element_output.result())
    
    element_input_1.set_value(3)
    element_input_2.set_value(3)
    flow.run()
    self.assertFalse(element_output.result())

    element_input_1.set_value(3)
    element_input_2.set_value(-5)
    flow.run()
    self.assertTrue(element_output.result())

    element_input_1.set_value(-5)
    element_input_2.set_value(-5)
    flow.run()
    self.assertFalse(element_output.result())
    
    element_input_1.set_value(-8)
    element_input_2.set_value(-5)
    flow.run()
    self.assertTrue(element_output.result())
    
    element_input_1.set_value(0)
    element_input_2.set_value(0)
    flow.run()
    self.assertFalse(element_output.result())
    