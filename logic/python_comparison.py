from improcflow.logic import Element, register_element_type


class PythonComparisonBase(Element):
  def __init__(self, title = None, element_model = None):
    super(PythonComparisonBase, self).__init__(title = title, element_model = element_model)
    self.left = self.add_input_connector(title = "left")
    self.right = self.add_input_connector(title = "right")
    self.result = self.add_output_connector(title = "result")
  

class PythonIsEqualTo(PythonComparisonBase):
  class_name = "python_is_equal_to"
  
  def run(self, debug = False):
    self.result.set_value(self.left.value == self.right.value)
    
register_element_type(PythonIsEqualTo)


class PythonIsNotEqualTo(PythonComparisonBase):
  class_name = "python_is_not_equal_to"
  
  def run(self, debug = False):
    self.result.set_value(self.left.value != self.right.value)
    
register_element_type(PythonIsNotEqualTo)


class PythonIsGreaterThan(PythonComparisonBase):
  class_name = "python_is_greater_than"
  
  def run(self, debug = False):
    self.result.set_value(self.left.value > self.right.value)
    
register_element_type(PythonIsGreaterThan)


class PythonIsLessThan(PythonComparisonBase):
  class_name = "python_is_less_than"
  
  def run(self, debug = False):
    self.result.set_value(self.left.value < self.right.value)
    
register_element_type(PythonIsLessThan)


class PythonIsNotLessThan(PythonComparisonBase):
  class_name = "python_is_not_less_than"
  
  def run(self, debug = False):
    self.result.set_value(self.left.value >= self.right.value)
    
register_element_type(PythonIsNotLessThan)


class PythonIsNotGreaterThan(PythonComparisonBase):
  class_name = "python_is_not_greater_than"
  
  def run(self, debug = False):
    self.result.set_value(self.left.value <= self.right.value)
    
register_element_type(PythonIsNotGreaterThan)


class PythonAnd(PythonComparisonBase):
  class_name = "python_and"
  
  def run(self, debug = False):
    self.result.set_value(self.left.value and self.right.value)
    
register_element_type(PythonAnd)


class PythonOr(PythonComparisonBase):
  class_name = "python_or"
  
  def run(self, debug = False):
    self.result.set_value(self.left.value or self.right.value)
    
register_element_type(PythonOr)


class PythonNot(Element):
  class_name = "python_not"
  
  def __init__(self, title = None, element_model = None):
    super(PythonNot, self).__init__(title = title, element_model = element_model)
    self.input = self.add_input_connector(title = "input")
    self.result = self.add_output_connector(title = "result")
  
  def run(self, debug = False):
    self.result.set_value(not(self.input.value))
    
register_element_type(PythonNot)
    