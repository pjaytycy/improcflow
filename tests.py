from django.test import TestCase

from improcflow.models import *

class FlowModelTests(TestCase):
  def test_mean_with_ndarray_1_to_6(self):
    element_input = InputImage(title = "element_input")
    element_input.set_value([[1, 2, 3], [4, 5, 6]])
    element_mean = OpenCVMean(title = "element_mean")
    element_output = OutputNumber(title = "element_output")
    
    flow = Flow()
    flow.addElement(element_input)
    flow.addElement(element_mean)
    flow.addElement(element_output)
    flow.connect(element_input.image, element_mean.src, title = "conn_1")
    flow.connect(element_mean.mean, element_output.number, title = "conn_2")
    flow.run()
    
    expected = 3.5
    actual = element_output.result()
    self.assertEqual(expected, actual)
  
  def test_mean_with_ndarray_4_to_9(self):
    element_input = InputImage()
    element_input.set_value([[4, 5, 6], [7, 8, 9]])
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
    actual = element_output.result()
    self.assertEqual(expected, actual)
    