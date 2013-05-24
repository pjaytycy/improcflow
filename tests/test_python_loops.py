import unittest

from django.test import TestCase

from improcflow.logic import *

class PythonLoopTests(TestCase):
  # vision: base all loop / iteration / ... on a combination of:
  #
  # 1) generator expressions / list comprehensions:
  #       general format: list_out = [func_map(list_item) for list_item in list_in if func_filter(list_item)]
  #       example: >>> [x**2 for x in range(10) if (x % 3) == 0]
  #               [0, 9, 36, 81]
  #
  # 2) adjusting one or more non-list variables in each iteration
  #       example: >>> val = 0
  #                >>> for i in range(10): 
  #                ...   val += 2;
  #                >>> val
  #                20
  #
  # 3) support for break / continue statements
  #       example: >>> val = 0
  #                >>> for i in range(10): 
  #                ...   if (i % 2) == 0:
  #                ...     continue
  #                ...   val += 2;
  #                >>> val
  #                10
  #       example: >>> val = 0
  #                >>> for i in range(10): 
  #                ...   if i > 7:
  #                ...     break
  #                ...   val += 2;
  #                >>> val
  #                16
  #
  # I don't need everything from the beginning...
  
  def test_simple_loop_only_map_func(self):
    # [x**2 for x in range(10)] => [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]
    flow = Flow()
    element_input = InputData()
    element_input.set_value(range(10))
    element_param = InputData()
    element_param.set_value(2)
    element_loop_start, element_loop_stop = PythonLoop()
    element_square = PythonExponentiation()
    element_output = OutputData()
    
    flow.add_element(element_input)
    flow.add_element(element_param)
    flow.add_element(element_loop_start)
    flow.add_element(element_square)
    flow.add_element(element_loop_stop)
    flow.add_element(element_output)
    
    flow.connect(element_input.data, element_loop_start.list_in)
    flow.connect(element_loop_start.list_item, element_square.base)
    flow.connect(element_param.data, element_square.exponent)
    flow.connect(element_square.power, element_loop_stop.list_item)
    flow.connect(element_loop_stop.list_out, element_output.data)
    
    flow.run()
    
    self.assertEqual([0, 1, 4, 9, 16, 25, 36, 49, 64, 81], element_output.result())

  def test_simple_loop_only_filter_func(self):
    # [x for x in range(10) if (x % 3) == 0] => [0, 3, 6, 9]
    flow = Flow()
    element_input = InputData()
    element_input.set_value(range(10))
    element_param_1 = InputData()
    element_param_1.set_value(3)
    element_param_2 = InputData()
    element_param_2.set_value(0)
    element_loop_start, element_loop_stop = PythonLoop()
    element_modulo = PythonModulo()
    element_equal = PythonIsEqualTo()
    element_output = OutputData()
    
    flow.add_element(element_input)
    flow.add_element(element_param_1)
    flow.add_element(element_param_2)    
    flow.add_element(element_loop_start)
    flow.add_element(element_modulo)
    flow.add_element(element_equal)
    flow.add_element(element_loop_stop)
    flow.add_element(element_output)
    
    # before the loop
    flow.connect(element_input.data, element_loop_start.list_in)
    flow.connect(element_param_1.data, element_modulo.divisor)
    flow.connect(element_param_2.data, element_equal.right)
    # inside the loop : transform the data
    flow.connect(element_loop_start.list_item, element_loop_stop.list_item)
    # inside the loop : apply the filter
    flow.connect(element_loop_start.list_item, element_modulo.dividend)
    flow.connect(element_modulo.remainder, element_equal.left)
    flow.connect(element_equal.result, element_loop_stop.append)
    # after the loop
    flow.connect(element_loop_stop.list_out, element_output.data)
    
    flow.run()
    
    self.assertEqual([0, 3, 6, 9], element_output.result())

    
  def test_loop_with_map_and_filter_func(self):
    # [x**2 for x in range(10) if (x % 3) == 0] => [0, 9, 36, 81]
    flow = Flow()
    element_input = InputData()
    element_input.set_value(range(10))
    element_const_2 = InputData()
    element_const_2.set_value(2)
    element_const_3 = InputData()
    element_const_3.set_value(3)
    element_const_0 = InputData()
    element_const_0.set_value(0)
    element_loop_start, element_loop_stop = PythonLoop()
    element_square = PythonExponentiation()
    element_modulo = PythonModulo()
    element_equal = PythonIsEqualTo()
    element_output = OutputData()
    
    flow.add_element(element_input)
    flow.add_element(element_const_2)
    flow.add_element(element_const_3)
    flow.add_element(element_const_0)
    flow.add_element(element_loop_start)
    flow.add_element(element_square)
    flow.add_element(element_modulo)
    flow.add_element(element_equal)
    flow.add_element(element_loop_stop)
    flow.add_element(element_output)
    
    # before the loop
    flow.connect(element_input.data, element_loop_start.list_in)
    flow.connect(element_const_2.data, element_square.exponent)
    flow.connect(element_const_3.data, element_modulo.divisor)
    flow.connect(element_const_0.data, element_equal.right)
    # inside the loop : transform the data
    flow.connect(element_loop_start.list_item, element_square.base)
    flow.connect(element_square.power, element_loop_stop.list_item)
    # inside the loop : apply the filter
    flow.connect(element_loop_start.list_item, element_modulo.dividend)
    flow.connect(element_modulo.remainder, element_equal.left)
    flow.connect(element_equal.result, element_loop_stop.append)
    # after the loop
    flow.connect(element_loop_stop.list_out, element_output.data)
    
    flow.run()
    
    self.assertEqual([0, 9, 36, 81], element_output.result())
