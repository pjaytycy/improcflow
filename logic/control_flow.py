from improcflow.logic import Element, register_element_type

class ConditionalAssignment(Element):
  class_name = "conditional_assignment"
  
  def __init__(self, title = None, element_model = None):
    super(ConditionalAssignment, self).__init__(title = title, element_model = element_model)
    self.input_datas = []
    self.output = self.add_output_connector(title = "output")
    
    
  def next_input(self):
    num_inputs = len(self.input_datas)
    next_title = "input-" + str(num_inputs + 1)
    next_input = self.add_input_connector(title = next_title)
    self.input_datas.append(next_input)
    return next_input
  
  
  def is_blocked(self):
    # We need to overwrite the "is_blocked()" function.
    # Normal elements are considered "blocked" when any of their inputs is blocked
    # a conditional assignment expects all but one of its inputs to be blocked
    if self.flow_control.value == False:
      return True
    
    num_inputs_not_blocked = 0
    for input_connector in self.input_datas:
      if not input_connector.is_blocked():
        num_inputs_not_blocked += 1
    
    return (num_inputs_not_blocked != 1)
  
  
  def run(self):
    input_ok = None
    for input in self.input_datas:
      if not input.is_blocked():
        if input_ok is None:
          input_ok = input
        else:
          print "2 or more inputs are not blocked!"
    self.output.set_value(input_ok.value)
  
  
register_element_type(ConditionalAssignment)
