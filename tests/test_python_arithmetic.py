import unittest

from django.test import TestCase

from improcflow.logic import *

class PythonArithmeticTests(TestCase):
  def test_adding_integers(self):
    element_input_1 = InputData()
    element_input_2 = InputData()
    element_add = PythonAddition()
    element_output = OutputData()
    
    flow = Flow()
    flow.add_element(element_input_1)
    flow.add_element(element_input_2)
    flow.add_element(element_add)
    flow.add_element(element_output)
    flow.connect(element_input_1.data, element_add.term1)
    flow.connect(element_input_2.data, element_add.term2)
    flow.connect(element_add.sum, element_output.data)
    
    element_input_1.set_value(3)
    element_input_2.set_value(5)
    flow.run()
    self.assertEqual(8, element_output.result())
    
    element_input_1.set_value(-3)
    flow.run()
    self.assertEqual(2, element_output.result())
    
    element_input_2.set_value(0)
    flow.run()
    self.assertEqual(-3, element_output.result())
    
  def test_subtracting_integers(self):
    element_input_1 = InputData()
    element_input_2 = InputData()
    element_sub = PythonSubtraction()
    element_output = OutputData()
    
    flow = Flow()
    flow.add_element(element_input_1)
    flow.add_element(element_input_2)
    flow.add_element(element_sub)
    flow.add_element(element_output)
    flow.connect(element_input_1.data, element_sub.term1)
    flow.connect(element_input_2.data, element_sub.term2)
    flow.connect(element_sub.difference, element_output.data)
    
    element_input_1.set_value(3)
    element_input_2.set_value(5)
    flow.run()
    self.assertEqual(-2, element_output.result())
    
    element_input_1.set_value(-3)
    flow.run()
    self.assertEqual(-8, element_output.result())
    
    element_input_2.set_value(0)
    flow.run()
    self.assertEqual(-3, element_output.result())
    
  def test_multiplying_integers(self):
    element_input_1 = InputData()
    element_input_2 = InputData()
    element_mul = PythonMultiplication()
    element_output = OutputData()
    
    flow = Flow()
    flow.add_element(element_input_1)
    flow.add_element(element_input_2)
    flow.add_element(element_mul)
    flow.add_element(element_output)
    flow.connect(element_input_1.data, element_mul.factor1)
    flow.connect(element_input_2.data, element_mul.factor2)
    flow.connect(element_mul.product, element_output.data)
    
    element_input_1.set_value(3)
    element_input_2.set_value(5)
    flow.run()
    self.assertEqual(15, element_output.result())
    
    element_input_1.set_value(-3)
    flow.run()
    self.assertEqual(-15, element_output.result())
    
    element_input_2.set_value(0)
    flow.run()
    self.assertEqual(0, element_output.result())
    
  def test_dividing_integers_with_true_division(self):
    element_input_1 = InputData()
    element_input_2 = InputData()
    element_div = PythonTrueDivision()
    element_output = OutputData()
    
    flow = Flow()
    flow.add_element(element_input_1)
    flow.add_element(element_input_2)
    flow.add_element(element_div)
    flow.add_element(element_output)
    flow.connect(element_input_1.data, element_div.dividend)
    flow.connect(element_input_2.data, element_div.divisor)
    flow.connect(element_div.quotient, element_output.data)
    
    element_input_1.set_value(3)
    element_input_2.set_value(5)
    flow.run()
    self.assertEqual(0.6, element_output.result())
    
    element_input_1.set_value(-3)
    flow.run()
    self.assertEqual(-0.6, element_output.result())
    
    element_input_2.set_value(-0.1)
    flow.run()
    self.assertEqual(30, element_output.result())
  
  def test_modulo_operation_with_integers(self):
    element_input_1 = InputData()
    element_input_2 = InputData()
    element_mod = PythonModulo()
    element_output = OutputData()
    
    flow = Flow()
    flow.add_element(element_input_1)
    flow.add_element(element_input_2)
    flow.add_element(element_mod)
    flow.add_element(element_output)
    flow.connect(element_input_1.data, element_mod.dividend)
    flow.connect(element_input_2.data, element_mod.divisor)
    flow.connect(element_mod.remainder, element_output.data)
    
    element_input_1.set_value(3)
    element_input_2.set_value(5)
    flow.run()
    self.assertEqual(3, element_output.result())
    
    element_input_1.set_value(-3)
    flow.run()
    self.assertEqual(2, element_output.result())
    
    element_input_2.set_value(-0.1)
    flow.run()
    # due to rounding -3 / -0.1 returns 29.9999999999999999
    # for floor division this means: 29
    # for modulo this means: -0.1 * 29 + M = -3.0 <=> M = -0.1
    # however on machines without the rounding problem, the 
    # division result might be 30.0, which would result in
    # a modulo of 0.0

    self.assertIn(round(element_output.result(), 7), (-0.1, 0.0))
  
  def test_exponentiation_with_integers(self):
    element_input_1 = InputData()
    element_input_2 = InputData()
    element_pow = PythonExponentiation()
    element_output = OutputData()
    
    flow = Flow()
    flow.add_element(element_input_1)
    flow.add_element(element_input_2)
    flow.add_element(element_pow)
    flow.add_element(element_output)
    flow.connect(element_input_1.data, element_pow.base)
    flow.connect(element_input_2.data, element_pow.exponent)
    flow.connect(element_pow.power, element_output.data)
    
    element_input_1.set_value(3)
    element_input_2.set_value(5)
    flow.run()
    self.assertEqual(243, element_output.result())
    
    element_input_1.set_value(-3)
    flow.run()
    self.assertEqual(-243, element_output.result())
    
    element_input_2.set_value(-2)
    flow.run()
    self.assertEqual(1.0/9, element_output.result())

  def test_dividing_integers_with_floor_division(self):
    element_input_1 = InputData()
    element_input_2 = InputData()
    element_div = PythonFloorDivision()
    element_output = OutputData()
    
    flow = Flow()
    flow.add_element(element_input_1)
    flow.add_element(element_input_2)
    flow.add_element(element_div)
    flow.add_element(element_output)
    flow.connect(element_input_1.data, element_div.dividend)
    flow.connect(element_input_2.data, element_div.divisor)
    flow.connect(element_div.quotient, element_output.data)
    
    element_input_1.set_value(3)
    element_input_2.set_value(5)
    flow.run()
    self.assertEqual(0, element_output.result())
    
    element_input_1.set_value(-3)
    flow.run()
    self.assertEqual(-1, element_output.result())
    
    element_input_2.set_value(-0.1)
    flow.run()
    # due to rounding -3 / -0.1 returns 29.9999999999999999
    # for floor division this means: 29
    # however on machines without the rounding problem, the result might be 30.0
    self.assertIn(element_output.result(), (29, 30))
  
