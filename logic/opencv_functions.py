import numpy

from improcflow.logic import Element, register_element_type

class OpenCVMean(Element):
  class_name = "opencv_mean"
  
  def __init__(self, title = None):
    super(OpenCVMean, self).__init__(title = title)
    self.src = self.add_input_connector(title = "src")
    self.mean = self.add_output_connector(title = "mean")
    
  def run(self):
    super(OpenCVMean, self).run()
    self.mean.set_value(numpy.average(self.src.value))
    
register_element_type(OpenCVMean)
