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

    self.full_white = numpy.ones([5, 5], dtype = numpy.uint8) * 255
    self.full_black = numpy.zeros([5, 5], dtype = numpy.uint8)
    
  def test_default_dilate_full_white(self):
    self.element_src.set_value(self.full_white)
    self.flow.run()
    
    numpy.testing.assert_equal(self.full_white, self.element_output.result())

  def test_default_dilate_full_black(self):
    self.element_src.set_value(self.full_black)
    self.flow.run()
    
    numpy.testing.assert_equal(self.full_black, self.element_output.result())
    
  def test_default_dilate_black_cross_on_white(self):
    black_on_white = self.full_white.copy()
    black_on_white[1:4, 2] = 0
    black_on_white[2, 1:4] = 0
    
    self.element_src.set_value(black_on_white)
    self.flow.run()
    
    numpy.testing.assert_equal(self.full_white, self.element_output.result())
  
  def test_default_dilate_white_cross_on_black(self):
    white_on_black = self.full_black.copy()
    white_on_black[1:4, 2] = 255
    white_on_black[2, 1:4] = 255
    
    self.element_src.set_value(white_on_black)
    self.flow.run()
        
    fat_white_on_black = self.full_white.copy()
    fat_white_on_black[(0, 0, 4, 4), (0, 4, 0, 4)] = 0
    
    numpy.testing.assert_equal(fat_white_on_black, self.element_output.result())
    
  def test_default_dilate_fat_black_cross_on_white(self):
    fat_black_on_white = self.full_black.copy()
    fat_black_on_white[(0, 0, 4, 4), (0, 4, 0, 4)] = 255
    
    self.element_src.set_value(fat_black_on_white)
    self.flow.run()
    
    black_on_white = self.full_white.copy()
    black_on_white[:, 2] = 0
    black_on_white[2, :] = 0
    
    numpy.testing.assert_equal(black_on_white, self.element_output.result())

  def test_default_dilate_fat_white_cross_on_black(self):
    fat_white_on_black = self.full_white.copy()
    fat_white_on_black[(0, 0, 4, 4), (0, 4, 0, 4)] = 0
    
    self.element_src.set_value(fat_white_on_black)
    self.flow.run()
    
    numpy.testing.assert_equal(self.full_white, self.element_output.result())

  def test_default_dilate_1_white_pixel_on_each_border(self):
    white_on_black = self.full_black.copy()
    white_on_black[(0, 2, 2, 4), (2, 0, 4, 2)] = 255
    
    self.element_src.set_value(white_on_black)
    self.flow.run()
    
    black_on_white = self.full_white.copy()
    black_on_white[(0, 0, 2, 4, 4), (0, 4, 2, 0, 4)] = 0
    
    numpy.testing.assert_equal(black_on_white, self.element_output.result())
    
  def test_dilate_custom_kernel(self):
    white_on_black = self.full_black.copy()
    white_on_black[1:4, 2] = 255
    white_on_black[2, 1:4] = 255
    
    self.element_src.set_value(white_on_black)
    
    self.flow.connect(self.element_kernel.data, self.element_dilate.kernel)
    kernel = numpy.array([[0, 0, 0], [0, 0, 0], [1, 0, 0]], dtype = numpy.uint8)
    self.element_kernel.set_value(kernel)
    
    self.flow.run()
    
    white_on_black_shift = self.full_black.copy()
    white_on_black_shift[0:3, 3] = 255
    white_on_black_shift[1, 2:5] = 255
    
    numpy.testing.assert_equal(white_on_black_shift, self.element_output.result())
    
  def test_dilate_custom_anchor(self):
    white_on_black = self.full_black.copy()
    white_on_black[1:4, 2] = 255
    white_on_black[2, 1:4] = 255
    
    self.element_src.set_value(white_on_black)
    
    self.flow.connect(self.element_anchor.data, self.element_dilate.anchor)
    self.element_anchor.set_value((0, 2))
    
    self.flow.run()
    
    fat_white_on_black_shift = self.full_white.copy()
    fat_white_on_black_shift[0, :] = 0
    fat_white_on_black_shift[:, 4] = 0
    fat_white_on_black_shift[1, 3] = 0
    
    numpy.testing.assert_equal(fat_white_on_black_shift, self.element_output.result())
    
