from improcflow.logic import Element, register_element_type

class InputImage(Element):
  class_name = "input_image"
  
  def __init__(self, title = None, element_model = None):
    super(InputImage, self).__init__(title = title, element_model = element_model)
    self.dummy = self.add_input_connector(title = "dummy")
    self.image = self.add_output_connector(title = "image")

  def set_value(self, src):
    self.dummy.set_value(src)
    if self.flow:
      self.flow.invalidate(self.image)
    else:
      self.image.invalidate()
  
  def run(self):
    super(InputImage, self).run()
    self.image.set_value(self.dummy.value)
    
register_element_type(InputImage)


class InputBoolean(Element):
  class_name = "input_boolean"
  
  def __init__(self, title = None, element_model = None):
    super(InputBoolean, self).__init__(title = title, element_model = element_model)
    self.dummy = self.add_input_connector(title = "dummy")
    self.boolean = self.add_output_connector(title = "boolean")
  
  def set_value(self, src):
    self.dummy.set_value(src)
    if self.flow:
      self.flow.invalidate(self.boolean)
    else:
      self.boolean.invalidate()
  
  def run(self):
    super(InputBoolean, self).run()
    self.boolean.set_value(self.dummy.value)

register_element_type(InputBoolean)

class OutputNumber(Element):
  class_name = "output_number"
  
  def __init__(self, title = None, element_model = None):
    super(OutputNumber, self).__init__(title = title, element_model = element_model)
    self.number = self.add_input_connector(title = "number")
      
  def result(self):
    if self.is_ready():
      return self.number.value
    return None
    
register_element_type(OutputNumber)
