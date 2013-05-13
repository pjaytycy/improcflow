from improcflow.logic import Element, register_element_type

class InputData(Element):
  class_name = "input_data"
  
  def __init__(self, title = None, element_model = None):
    super(InputData, self).__init__(title = title, element_model = element_model)
    self.dummy = self.add_input_connector(title = "dummy")
    self.data = self.add_output_connector(title = "data")

  def set_value(self, src):
    self.dummy.set_value(src)
    if self.flow:
      self.flow.invalidate(self.data)
    else:
      self.data.invalidate()
  
  def run(self):
    self.data.set_value(self.dummy.value)
    
register_element_type(InputData)



class OutputData(Element):
  class_name = "output_data"
  
  def __init__(self, title = None, element_model = None):
    super(OutputData, self).__init__(title = title, element_model = element_model)
    self.data = self.add_input_connector(title = "data")
      
  def result(self):
    if self.is_ready() and not self.is_blocked():
      return self.data.value
    return None
    
register_element_type(OutputData)
