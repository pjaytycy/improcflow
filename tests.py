from django.test import TestCase

from improcflow.models import *

class FlowModelTests(TestCase):
  def test_mean_1(self):
    element_input = InputImage([[1, 2, 3], [4, 5, 6]])
    element_mean = OpenCVMean()
    element_output = OutputNumber()
    
    flow = Flow()
    flow.addElement(element_input)
    flow.addElement(element_mean)
    flow.addElement(element_output)
    flow.connect(element_input.image, element_mean.src)
    flow.connect(element_mean.mean, element_output.number)
    flow.run()
    
    expected = 3.5
    actual = element_output.number
    self.assertEqual(expected, actual)
  
  def test_mean_2(self):
    element_input = InputImage([[4, 5, 6], [7, 8, 9]])
    element_mean = OpenCVMean()
    element_output = OutputNumber()
    
    flow = Flow()
    flow.addElement(element_input)
    flow.addElement(element_mean)
    flow.addElement(element_output)
    flow.connect(element_input.image, element_mean.src)
    flow.connect(element_mean.mean, element_output.number)
    flow.run()
    
    expected = 6.5
    actual = element_output.number
    self.assertEqual(expected, actual)