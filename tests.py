from django.test import TestCase

from improcflow.logic import *

class FlowLogicTests(TestCase):
  def test_mean_with_ndarray_1_to_6(self):
    element_input = InputImage(title = "element_input")
    element_input.set_value([[1, 2, 3], [4, 5, 6]])
    element_mean = OpenCVMean(title = "element_mean")
    element_output = OutputNumber(title = "element_output")
    
    flow = Flow()
    flow.add_element(element_input)
    flow.add_element(element_mean)
    flow.add_element(element_output)
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
    flow.add_element(element_input)
    flow.add_element(element_mean)
    flow.add_element(element_output)
    flow.connect(element_input.image, element_mean.src)
    flow.connect(element_mean.mean, element_output.number)
    flow.run()
    
    expected = 6.5
    actual = element_output.result()
    self.assertEqual(expected, actual)
    
  def test_mean_with_two_calls_to_run(self):
    element_input = InputImage(title = "element_input")
    element_mean = OpenCVMean(title = "element_mean")
    element_output = OutputNumber(title = "element_output")
    
    flow = Flow()
    flow.add_element(element_input)
    flow.add_element(element_mean)
    flow.add_element(element_output)
    flow.connect(element_input.image, element_mean.src, title = "conn_1")
    flow.connect(element_mean.mean, element_output.number, title = "conn_2")

    element_input.set_value([[1, 2, 3], [4, 5, 6]])
    flow.run()
    
    expected = 3.5
    actual = element_output.result()
    self.assertEqual(expected, actual)
    
    element_input.set_value([[7, 8, 9], [4, 5, 6]])
    flow.run()
    
    expected = 6.5
    actual = element_output.result()
    self.assertEqual(expected, actual)
  
  def test_mean_with_multiple_set_value_calls_before_calling_run(self):
    element_input = InputImage()
    element_mean = OpenCVMean()
    element_output = OutputNumber()
    
    flow = Flow()
    flow.add_element(element_input)
    flow.add_element(element_mean)
    flow.add_element(element_output)
    flow.connect(element_input.image, element_mean.src)
    flow.connect(element_mean.mean, element_output.number)
    
    element_input.set_value([[1, 1], [3, 3]])
    element_input.set_value([[2, 2], [4, 4]])
    element_input.set_value([[3, 3], [5, 5]])
    flow.run()
    
    expected = 4
    actual = element_output.result()
    self.assertEqual(expected, actual)
    
    element_input.set_value([[1, 2, 3], [4, 5, 6]])
    
    actual = element_output.result()
    self.assertIsNone(actual)
  
  def test_change_flow_structure_between_two_calls_to_run(self):
    element_input_1 = InputImage(title = "element_input_1")
    element_input_1.set_value([[1, 2, 3], [4, 5, 6]])
    element_input_2 = InputImage(title = "element_input_2")
    element_input_2.set_value([[4, 5], [7, 8]])
    element_mean = OpenCVMean(title = "element_mean")
    element_output = OutputNumber(title = "element_output")
    
    flow = Flow()
    flow.add_element(element_input_1)
    flow.add_element(element_input_2)
    flow.add_element(element_mean)
    flow.add_element(element_output)
    flow.connect(element_input_1.image, element_mean.src, title = "conn_1a")
    flow.connect(element_mean.mean, element_output.number, title = "conn_2")
    
    flow.run()
    
    expected = 3.5
    actual = element_output.result()
    self.assertEqual(expected, actual)
    
    flow.connect(element_input_2.image, element_mean.src, title = "conn_1b")
    
    flow.run()
    
    expected = 6
    actual = element_output.result()
    self.assertEqual(expected, actual)
    
    # also test for unnecessary executions
    self.assertEqual(1, element_input_1.get_number_of_executions())
    self.assertEqual(1, element_input_2.get_number_of_executions())
    self.assertEqual(2, element_mean.get_number_of_executions())
  
  def test_save_and_load_an_empty_flow(self):
    flow = Flow(title = "test_flow")
    flow_id = flow.get_id()
    flow2 = Flow(flow_id = flow_id)
    
    expected = "test_flow"
    actual = flow2.title
    self.assertEqual(expected, actual)
    expected = flow_id
    actual = flow2.get_id()
    self.assertEqual(expected, actual)
    
    