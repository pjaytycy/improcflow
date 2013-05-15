from improcflow.logic import Element, register_element_type


class PythonComparisonBase(Element):
  def __init__(self, title = None, element_model = None):
    super(PythonComparisonBase, self).__init__(title = title, element_model = element_model)
    self.left = self.add_input_connector(title = "left")
    self.right = self.add_input_connector(title = "right")
    self.result = self.add_output_connector(title = "result")
  

class PythonIsEqualTo(PythonComparisonBase):
  class_name = "python_is_equal_to"
  
  def run(self):
    self.result.set_value(self.left.value == self.right.value)
    
register_element_type(PythonIsEqualTo)


class PythonIsNotEqualTo(PythonComparisonBase):
  class_name = "python_is_not_equal_to"
  
  def run(self):
    self.result.set_value(self.left.value != self.right.value)
    
register_element_type(PythonIsNotEqualTo)


class PythonIsGreaterThan(PythonComparisonBase):
  class_name = "python_is_greater_than"
  
  def run(self):
    self.result.set_value(self.left.value > self.right.value)
    
register_element_type(PythonIsGreaterThan)


class PythonIsLowerThan(PythonComparisonBase):
  class_name = "python_is_lower_than"
  
  def run(self):
    self.result.set_value(self.left.value < self.right.value)
    
register_element_type(PythonIsLowerThan)


class PythonIsNotLessThan(PythonComparisonBase):
  class_name = "python_is_not_less_than"
  
  def run(self):
    self.result.set_value(self.left.value >= self.right.value)
    
register_element_type(PythonIsNotLessThan)
