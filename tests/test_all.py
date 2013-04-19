from django.test import TestCase

from improcflow.logic import *

import numpy
import cv2
from cv2 import cv

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
    
    
#-------- ideas for further tests------------
# 0) refactor tests into a separate module instead of this 1 long file
# 1) store values and & valid attribute of connectors
# 2) test if an automatic disconnect() does not leave the old connection in the DB


class AutomaticConversionTests(TestCase):
  src_list  = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
  src_array = numpy.array(src_list)
  src_mat   = cv.fromarray(src_array)
  src_ipl   = cv.GetImage(src_mat)
  
  def test_list_to_None(self):
    dst = convert_data(self.src_list, None)
    self.assertEqual(type(dst), list)
    
  def test_list_to_list(self):
    dst = convert_data(self.src_list, [list])
    self.assertEqual(type(dst), list)
    
  def test_list_to_array(self):
    dst = convert_data(self.src_list, [numpy.ndarray])
    self.assertEqual(type(dst), numpy.ndarray)
  
  def test_list_to_cvmat(self):
    dst = convert_data(self.src_list, [cv.cvmat])
    self.assertEqual(type(dst), cv.cvmat)
  
  def test_list_to_iplimage(self):
    dst = convert_data(self.src_list, [cv.iplimage])
    self.assertEqual(type(dst), cv.iplimage)
  
  def test_list_to_cvmat_or_iplimage(self):
    dst = convert_data(self.src_list, [cv.cvmat, cv.iplimage])
    self.assertEqual(type(dst), cv.cvmat)
    
  def test_list_to_iplimage_or_cvmat(self):
    dst = convert_data(self.src_list, [cv.iplimage, cv.cvmat])
    self.assertEqual(type(dst), cv.cvmat)
  
  def test_array_to_None(self):
    dst = convert_data(self.src_array, None)
    self.assertEqual(type(dst), numpy.ndarray)
    
  def test_array_to_list(self):
    dst = convert_data(self.src_array, [list])
    self.assertEqual(type(dst), list)
    
  def test_array_to_array(self):
    dst = convert_data(self.src_array, [numpy.ndarray])
    self.assertEqual(type(dst), numpy.ndarray)
  
  def test_array_to_cvmat(self):
    dst = convert_data(self.src_array, [cv.cvmat])
    self.assertEqual(type(dst), cv.cvmat)
  
  def test_array_to_iplimage(self):
    dst = convert_data(self.src_array, [cv.iplimage])
    self.assertEqual(type(dst), cv.iplimage)
  
  def test_array_to_cvmat_or_iplimage(self):
    dst = convert_data(self.src_array, [cv.cvmat, cv.iplimage])
    self.assertEqual(type(dst), cv.cvmat)
    
  def test_array_to_iplimage_or_cvmat(self):
    dst = convert_data(self.src_array, [cv.iplimage, cv.cvmat])
    self.assertEqual(type(dst), cv.cvmat)
  
  def test_cvmat_to_None(self):
    dst = convert_data(self.src_mat, None)
    self.assertEqual(type(dst), cv.cvmat)
    
  def test_cvmat_to_list(self):
    dst = convert_data(self.src_mat, [list])
    self.assertEqual(type(dst), list)
    
  def test_cvmat_to_array(self):
    dst = convert_data(self.src_mat, [numpy.ndarray])
    self.assertEqual(type(dst), numpy.ndarray)
  
  def test_cvmat_to_cvmat(self):
    dst = convert_data(self.src_mat, [cv.cvmat])
    self.assertEqual(type(dst), cv.cvmat)
  
  def test_cvmat_to_iplimage(self):
    dst = convert_data(self.src_mat, [cv.iplimage])
    self.assertEqual(type(dst), cv.iplimage)
  
  def test_cvmat_to_cvmat_or_iplimage(self):
    dst = convert_data(self.src_mat, [cv.cvmat, cv.iplimage])
    self.assertEqual(type(dst), cv.cvmat)
    
  def test_cvmat_to_iplimage_or_cvmat(self):
    dst = convert_data(self.src_mat, [cv.iplimage, cv.cvmat])
    self.assertEqual(type(dst), cv.cvmat)
  
  def test_iplimage_to_None(self):
    dst = convert_data(self.src_ipl, None)
    self.assertEqual(type(dst), cv.iplimage)
    
  def test_iplimage_to_list(self):
    dst = convert_data(self.src_ipl, [list])
    self.assertEqual(type(dst), list)
    
  def test_iplimage_to_array(self):
    dst = convert_data(self.src_ipl, [numpy.ndarray])
    self.assertEqual(type(dst), numpy.ndarray)
  
  def test_iplimage_to_cvmat(self):
    dst = convert_data(self.src_ipl, [cv.cvmat])
    self.assertEqual(type(dst), cv.cvmat)
  
  def test_iplimage_to_iplimage(self):
    dst = convert_data(self.src_ipl, [cv.iplimage])
    self.assertEqual(type(dst), cv.iplimage)
  
  def test_iplimage_to_cvmat_or_iplimage(self):
    dst = convert_data(self.src_ipl, [cv.cvmat, cv.iplimage])
    self.assertEqual(type(dst), cv.iplimage)
    
  def test_iplimage_to_iplimage_or_cvmat(self):
    dst = convert_data(self.src_ipl, [cv.iplimage, cv.cvmat])
    self.assertEqual(type(dst), cv.iplimage)