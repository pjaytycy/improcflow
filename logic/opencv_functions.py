from improcflow.logic import Element, register_element_type

import numpy
import cv2

class OpenCVMean(Element):
  class_name = "opencv_mean"
  
  def __init__(self, title = None, element_model = None):
    super(OpenCVMean, self).__init__(title = title, element_model = element_model)
    self.src = self.add_input_connector(title = "src", data_types = [numpy.ndarray])
    self.mean = self.add_output_connector(title = "mean")
    
  def run(self, debug = False):
    avg_list = cv2.mean(self.src.value)
    self.mean.set_value(avg_list[0])
    
register_element_type(OpenCVMean)


class OpenCVDilate(Element):
  class_name = "opencv_dilate"
  
  def __init__(self, title = None, element_model = None):
    super(OpenCVDilate, self).__init__(title = title, element_model = element_model)
    self.src = self.add_input_connector(title = "src", data_types = [numpy.ndarray])
    self.kernel = self.add_input_connector(title = "kernel", data_types = [numpy.ndarray], default_value = [[1, 1, 1], [1, 1, 1], [1, 1, 1]])
    self.anchor = self.add_input_connector(title = "anchor", default_value = (-1, -1)) # notation = (x, y); which is opposite the NumPy convention
    self.iterations = self.add_input_connector(title = "iterations", default_value = 1)
    self.border_type = self.add_input_connector(title = "border_type", default_value = cv2.BORDER_CONSTANT)
    self.border_value = self.add_input_connector(title = "border_value", default_value = float('-inf'))
    
    self.dst = self.add_output_connector(title = "dst")
  
  def run(self, debug = False):
    result = cv2.dilate(src = self.src.value, kernel = self.kernel.value, anchor = self.anchor.value,
                        iterations = self.iterations.value, borderType = self.border_type.value, 
                        borderValue = self.border_value.value)
    self.dst.set_value(result)

register_element_type(OpenCVDilate)
