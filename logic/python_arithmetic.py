from improcflow.logic import Element, register_element_type

class PythonAddition(Element):
  class_name = "python_addition"
  
  def __init__(self, title = None, element_model = None):
    super(PythonAddition, self).__init__(title = title, element_model = element_model)
    self.term1 = self.add_input_connector(title = "term1")
    self.term2 = self.add_input_connector(title = "term2")
    self.sum = self.add_output_connector(title = "sum")
  
  def run(self, debug = False):
    self.sum.set_value(self.term1.value + self.term2.value)
    
register_element_type(PythonAddition)


class PythonSubtraction(Element):
  class_name = "python_subtraction"
  
  def __init__(self, title = None, element_model = None):
    super(PythonSubtraction, self).__init__(title = title, element_model = element_model)
    self.term1 = self.add_input_connector(title = "term1")
    self.term2 = self.add_input_connector(title = "term2")
    self.difference = self.add_output_connector(title = "difference")
  
  def run(self, debug = False):
    self.difference.set_value(self.term1.value - self.term2.value)
    
register_element_type(PythonSubtraction)


class PythonMultiplication(Element):
  class_name = "python_multiplication"
  
  def __init__(self, title = None, element_model = None):
    super(PythonMultiplication, self).__init__(title = title, element_model = element_model)
    self.factor1 = self.add_input_connector(title = "factor1")
    self.factor2 = self.add_input_connector(title = "factor2")
    self.product = self.add_output_connector(title = "product")
  
  def run(self, debug = False):
    self.product.set_value(self.factor1.value * self.factor2.value)
    
register_element_type(PythonMultiplication)


class PythonTrueDivision(Element):
  class_name = "python_true_division"
  
  def __init__(self, title = None, element_model = None):
    super(PythonTrueDivision, self).__init__(title = title, element_model = element_model)
    self.dividend = self.add_input_connector(title = "dividend")
    self.divisor = self.add_input_connector(title = "divisor")
    self.quotient = self.add_output_connector(title = "quotient")
  
  def run(self, debug = False):
    # We don't use 'from __future__ import division', because that will change division operators
    # in the whole Python instance running at the moment. Also float(x)/y does not work in case
    # x is a complex number or a NumPy-array. The x*1.0/y method seems most convenient and robust.
    # It is also the proposed temporary solution in http://www.python.org/dev/peps/pep-0238/
    self.quotient.set_value(self.dividend.value * 1.0 / self.divisor.value)
    
register_element_type(PythonTrueDivision)


class PythonModulo(Element):
  class_name = "python_modulo"
  
  def __init__(self, title = None, element_model = None):
    super(PythonModulo, self).__init__(title = title, element_model = element_model)
    self.dividend = self.add_input_connector(title = "dividend")
    self.divisor = self.add_input_connector(title = "divisor")
    self.remainder = self.add_output_connector(title = "remainder")
  
  def run(self, debug = False):
    self.remainder.set_value(self.dividend.value % self.divisor.value)
    
register_element_type(PythonModulo)


class PythonExponentiation(Element):
  class_name = "python_exponentiation"
  
  def __init__(self, title = None, element_model = None):
    super(PythonExponentiation, self).__init__(title = title, element_model = element_model)
    self.base = self.add_input_connector(title = "base")
    self.exponent = self.add_input_connector(title = "exponent")
    self.power = self.add_output_connector(title = "power")
  
  def run(self, debug = False):
    self.power.set_value(self.base.value ** self.exponent.value)
    
register_element_type(PythonExponentiation)


class PythonFloorDivision(Element):
  class_name = "python_floor_division"
  
  def __init__(self, title = None, element_model = None):
    super(PythonFloorDivision, self).__init__(title = title, element_model = element_model)
    self.dividend = self.add_input_connector(title = "dividend")
    self.divisor = self.add_input_connector(title = "divisor")
    self.quotient = self.add_output_connector(title = "quotient")
  
  def run(self, debug = False):
    self.quotient.set_value(self.dividend.value // self.divisor.value)
    
register_element_type(PythonFloorDivision)
