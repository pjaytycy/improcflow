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
    # notation = (x, y); which is opposite the NumPy convention (row, col)
    self.anchor = self.add_input_connector(title = "anchor", default_value = (-1, -1))
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


class OpenCVGaussianBlur(Element):
  class_name = "opencv_gaussian_blur"
  
  def __init__(self, title = None, element_model = None):
    super(OpenCVGaussianBlur, self).__init__(title = title, element_model = element_model)
    self.src = self.add_input_connector(title = "src", data_types = [numpy.ndarray])
    # notation = (width, height); which is opposite the NumPy convention (rows, cols)
    self.kernel_size = self.add_input_connector(title = "kernel_size", default_value = (5, 5))
    self.sigma_x = self.add_input_connector(title = "sigma_x", default_value = 0)
    self.sigma_y = self.add_input_connector(title = "sigma_y", default_value = 0)
    self.border_type = self.add_input_connector(title = "border_type", default_value = cv2.BORDER_REFLECT_101)
    
    self.dst = self.add_output_connector(title = "dst")

  def run(self, debug = False):
    result = cv2.GaussianBlur(src = self.src.value, ksize = self.kernel_size.value, 
                              sigma1 = self.sigma_x.value, sigma2 = self.sigma_y.value, 
                              borderType = self.border_type.value)
    self.dst.set_value(result)
