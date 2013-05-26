import unittest

import numpy
from django.test import TestCase

from improcflow.logic import *

class OpenCVDilateTests(TestCase):
  def setUp(self):
    self.element_src = InputData(title = "element_src")
    self.element_kernel = InputData(title = "element_kernel")
    self.element_anchor = InputData(title = "element_anchor")
    self.element_iterations = InputData(title = "element_iterations")
    self.element_border_type = InputData(title = "element_border_type")
    self.element_border_value = InputData(title = "element_border_value")
    self.element_dilate = OpenCVDilate(title = "element_dilate")
    self.element_output = OutputData(title = "element_output")

    self.flow = Flow()
    self.flow.add_element(self.element_src)
    self.flow.add_element(self.element_kernel)
    self.flow.add_element(self.element_anchor)
    self.flow.add_element(self.element_iterations)
    self.flow.add_element(self.element_border_type)
    self.flow.add_element(self.element_border_value)
    self.flow.add_element(self.element_dilate)
    self.flow.add_element(self.element_output)
    self.flow.connect(self.element_src.data, self.element_dilate.src)
    self.flow.connect(self.element_dilate.dst, self.element_output.data)
    
  def test_default_dilate_full_white(self):
    np_full_white = numpy.ones([5,5], dtype = numpy.uint8)
    self.element_src.set_value(np_full_white)
    self.flow.run()
    
    numpy.testing.assert_equal(np_full_white, self.element_output.result())

  def test_default_dilate_full_black(self):
    np_full_black = numpy.zeros([5,5], dtype = numpy.uint8)
    self.element_src.set_value(np_full_black)
    self.flow.run()
    
    numpy.testing.assert_equal(np_full_black, self.element_output.result())
    
