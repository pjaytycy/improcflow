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
    element_not_equal = PythonIsNotEqualTo()
    element_output = OutputData()
    
    flow = Flow()
    flow.add_element(element_input_1)
    flow.add_element(element_input_2)
    flow.add_element(element_not_equal)
    flow.add_element(element_output)
    flow.connect(element_input_1.data, element_not_equal.left)
    flow.connect(element_input_2.data, element_not_equal.right)
    flow.connect(element_not_equal.result, element_output.data)
    
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
    
  def test_greater_with_integers(self):
    element_input_1 = InputData()
    element_input_2 = InputData()
    element_greater = PythonIsGreaterThan()
    element_output = OutputData()
    
    flow = Flow()
    flow.add_element(element_input_1)
    flow.add_element(element_input_2)
    flow.add_element(element_greater)
    flow.add_element(element_output)
    flow.connect(element_input_1.data, element_greater.left)
    flow.connect(element_input_2.data, element_greater.right)
    flow.connect(element_greater.result, element_output.data)
    
    element_input_1.set_value(3)
    element_input_2.set_value(5)
    flow.run()
    self.assertFalse(element_output.result())
    
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
    self.assertFalse(element_output.result())
    
    element_input_1.set_value(0)
    element_input_2.set_value(0)
    flow.run()
    self.assertFalse(element_output.result())

  def test_less_with_integers(self):
    element_input_1 = InputData()
    element_input_2 = InputData()
    element_less = PythonIsLessThan()
    element_output = OutputData()
    
    flow = Flow()
    flow.add_element(element_input_1)
    flow.add_element(element_input_2)
    flow.add_element(element_less)
    flow.add_element(element_output)
    flow.connect(element_input_1.data, element_less.left)
    flow.connect(element_input_2.data, element_less.right)
    flow.connect(element_less.result, element_output.data)
    
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
    self.assertFalse(element_output.result())

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

  def test_not_less_than_with_integers(self):
    element_input_1 = InputData()
    element_input_2 = InputData()
    element_not_less = PythonIsNotLessThan()
    element_output = OutputData()
    
    flow = Flow()
    flow.add_element(element_input_1)
    flow.add_element(element_input_2)
    flow.add_element(element_not_less)
    flow.add_element(element_output)
    flow.connect(element_input_1.data, element_not_less.left)
    flow.connect(element_input_2.data, element_not_less.right)
    flow.connect(element_not_less.result, element_output.data)
    
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
    self.assertTrue(element_output.result())

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
    