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
  
  def test_simple_loop(self):
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

