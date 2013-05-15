from improcflow.logic import Element, register_element_type

class PythonIsEqualTo(Element):
  class_name = "python_is_equal_to"
  
  def __init__(self, title = None, element_model = None):
    super(PythonIsEqualTo, self).__init__(title = title, element_model = element_model)
    self.left = self.add_input_connector(title = "left")
    self.right = self.add_input_connector(title = "right")
    self.result = self.add_output_connector(title = "result")
  
  def run(self):
    self.result.set_value(self.left.value == self.right.value)
    
register_element_type(PythonIsEqualTo)
