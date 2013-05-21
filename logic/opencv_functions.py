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
