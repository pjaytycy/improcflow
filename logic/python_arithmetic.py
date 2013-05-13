from improcflow.logic import Element, register_element_type

class PythonAddition(Element):
  class_name = "python_addition"
  
  def __init__(self, title = None, element_model = None):
    super(PythonAddition, self).__init__(title = title, element_model = element_model)
    self.term1 = self.add_input_connector(title = "term1")
    self.term2 = self.add_input_connector(title = "term2")
    self.sum = self.add_output_connector(title = "sum")
  
  def run(self):
    self.sum.set_value(self.term1.value + self.term2.value)
    
register_element_type(PythonAddition)


class PythonSubtraction(Element):
  class_name = "python_subtraction"
  
  def __init__(self, title = None, element_model = None):
    super(PythonSubtraction, self).__init__(title = title, element_model = element_model)
    self.term1 = self.add_input_connector(title = "term1")
    self.term2 = self.add_input_connector(title = "term2")
    self.difference = self.add_output_connector(title = "difference")
  
  def run(self):
    self.difference.set_value(self.term1.value - self.term2.value)
    
register_element_type(PythonSubtraction)


class PythonMultiplication(Element):
  class_name = "python_multiplication"
  
  def __init__(self, title = None, element_model = None):
    super(PythonMultiplication, self).__init__(title = title, element_model = element_model)
    self.factor1 = self.add_input_connector(title = "factor1")
    self.factor2 = self.add_input_connector(title = "factor2")
    self.product = self.add_output_connector(title = "product")
  
  def run(self):
    self.product.set_value(self.factor1.value * self.factor2.value)
    
register_element_type(PythonMultiplication)
