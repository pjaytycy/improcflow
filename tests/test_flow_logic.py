import unittest

from django.test import TestCase

from improcflow.logic import *
from improcflow.models import ElementModel, ConnectionModel

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
    
  def test_save_and_load_a_flow_with_one_element(self):
    flow1 = Flow(title = "test_flow_with_one_element")
    flow1.add_element(InputImage("test_element"))
    flow_id = flow1.get_id()
    
    flow2 = Flow(flow_id = flow_id)
    
    expected = 1
    actual = flow2.get_num_elements()
    self.assertEqual(expected, actual)
    
    element = flow2.get_element("test_element")
    
    expected = "test_element"
    actual = element.title
    self.assertEqual(expected, actual)
    
    expected = InputImage
    actual = type(element)
    self.assertEqual(expected, actual)
    
  def test_save_and_load_a_flow_with_multiple_elements(self):
    flow1 = Flow()
    flow1.add_element(InputImage("test_input_image_1"))
    flow1.add_element(InputImage("test_input_image_2"))
    flow1.add_element(OpenCVMean("test_opencv_mean"))
    flow1.add_element(OutputNumber("test_output_number"))
    
    flow_id = flow1.get_id()
    
    flow2 = Flow(flow_id = flow_id)
    self.assertEqual(4, flow2.get_num_elements())
    
    element = flow2.get_element("test_input_image_1")
    self.assertEqual("test_input_image_1", element.title)
    self.assertEqual(InputImage, type(element))
    
    element = flow2.get_element("test_input_image_2")
    self.assertEqual("test_input_image_2", element.title)
    self.assertEqual(InputImage, type(element))
    
    element = flow2.get_element("test_opencv_mean")
    self.assertEqual("test_opencv_mean", element.title)
    self.assertEqual(OpenCVMean, type(element))
    
    element = flow2.get_element("test_output_number")
    self.assertEqual("test_output_number", element.title)
    self.assertEqual(OutputNumber, type(element))
    
  def test_save_and_load_a_flow_with_connections(self):
    element_input = InputImage("test_input")
    element_mean = OpenCVMean()
    element_output = OutputNumber("test_output")
    
    flow = Flow()
    flow.add_element(element_input)
    flow.add_element(element_mean)
    flow.add_element(element_output)
    flow.connect(element_input.image, element_mean.src)
    flow.connect(element_mean.mean, element_output.number)
    
    flow_id = flow.get_id()
    
    flow2 = Flow(flow_id = flow_id)
    element_input2 = flow2.get_element("test_input")
    element_output2 = flow2.get_element("test_output")
    element_input2.set_value([[1, 1], [3, 3]])
    
    flow2.run()
    self.assertEqual(2, element_output2.result())

  def test_change_structure_after_save_and_load_database(self):
    element_input = InputImage("test_input1")
    element_mean = OpenCVMean("test_mean")
    element_output = OutputNumber("test_output")
    
    flow = Flow()
    flow.add_element(element_input)
    flow.add_element(element_mean)
    flow.add_element(element_output)
    flow.connect(element_input.image, element_mean.src, title = "connection1")
    flow.connect(element_mean.mean, element_output.number, title = "connection2")
    
    element_input.set_value([[3, 4], [6, 7]])
    flow.run()
    self.assertEqual(5, element_output.result())
    
    flow_id = flow.get_id()
    
    flow2 = Flow(flow_id = flow_id)
    # try to get the original connection; it should be present
    connection1 = flow2.get_element("connection1")
    self.assertIsNotNone(connection1)
    
    element_input2 = InputImage("test_input2")
    flow2.add_element(element_input2)
    element_mean2 = flow2.get_element("test_mean")
    flow2.connect(element_input2.image, element_mean2.src, title = "connection3")
    
    element_input2.set_value([[1, 2], [4, 5]])
    flow2.run()
    element_output2 = flow2.get_element("test_output")
    self.assertEqual(3, element_output2.result())
    
    # try to get the new connection; it should be present
    connection3 = flow2.get_element("connection3")
    self.assertIsNotNone(connection3)
    
    # try to get the original connection; it should NOT be present
    with self.assertRaises(ElementNotFoundError):
      connection1 = flow2.get_element("connection1")
    
    # make sure the connection is really not in the database!
    self.assertEqual(2, len(ConnectionModel.objects.all()))
  
  
  def test_remove_element_from_flow(self):
   element_input = InputImage("test_input")
   element_mean = OpenCVMean("test_mean")
   element_output = OutputNumber("test_output")
   
   flow = Flow()
   flow.add_element(element_input)
   flow.add_element(element_mean)
   flow.add_element(element_output)
   flow.connect(element_input.image, element_mean.src, title = "connection1")
   flow.connect(element_mean.mean, element_output.number, title = "connection2")
   
   element_input.set_value([[1, 2, 3, 4, 5], [6, 7, 8, 9, 10], [11, 12, 13, 14, 15]])
   flow.run()
   self.assertEqual(8, element_output.result())
   
   # make sure 3 elements + 2 connections are present in the flow object
   self.assertEqual(5, flow.get_num_elements())
   # make sure 2 connections are present in the DB
   self.assertEqual(2, len(ConnectionModel.objects.all()))

   flow.remove_element(element_mean)
   
   # make sure 2 elements + 0 connections are present in the flow object
   self.assertEqual(2, flow.get_num_elements())
   # make sure all connections are gone in the DB
   self.assertEqual(0, len(ConnectionModel.objects.all()))
   
   # make sure the end result is invalid
   self.assertEqual(None, element_output.result())
   
   
   
   
