from improcflow.logic import Element, register_element_type

class InputData(Element):
  class_name = "input_data"
  
  def __init__(self, title = None, element_model = None):
    super(InputData, self).__init__(title = title, element_model = element_model)
    self.data_in = self.add_input_connector(title = "data_in")
    self.data = self.add_output_connector(title = "data")

  def set_value(self, src):
    self.data_in.set_value(src)
    if self.flow:
      self.flow.invalidate(self.data)
    else:
      self.data.invalidate()
  
  def run(self, debug = False):
    self.data.set_value(self.data_in.value)
    
register_element_type(InputData)



class OutputData(Element):
  class_name = "output_data"
  
  def __init__(self, title = None, element_model = None):
    super(OutputData, self).__init__(title = title, element_model = element_model)
    self.data = self.add_input_connector(title = "data")
    self.data_out = self.add_output_connector(title = "data_out")
      
  def result(self):
    if self.is_ready() and not self.is_blocked():
      return self.data.value
    return None

  def run(self, debug = False):
    self.data_out.set_value(self.data.value)
    
register_element_type(OutputData)
