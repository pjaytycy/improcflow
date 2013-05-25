from improcflow.logic import Element, ElementGroup, register_element_type

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
  
  
  def run(self, debug = False):
    input_ok = None
    for input in self.input_datas:
      if not input.is_blocked():
        if input_ok is None:
          input_ok = input
        else:
          print "2 or more inputs are not blocked!"
    self.output.set_value(input_ok.value)
  
  
register_element_type(ConditionalAssignment)


class PythonLoop(ElementGroup):
  def __init__(self, title = None):
    super(PythonLoop, self).__init__(title = title)
    if title is None:
      start = LoopStart()
      stop = LoopStop()
    else:
      start = LoopStart(title = title + "_start")
      stop = LoopStop(title = title + "_stop")
      
    self.add_element(start)
    self.add_element(stop)
    

class LoopStart(Element):
  class_name = "loop_start"
  
  def __init__(self, title = None, element_model = None):
    super(LoopStart, self).__init__(title = title, element_model = element_model)
    self.list_in = self.add_input_connector(title = "list_in")
    self.list_item = self.add_output_connector(title = "list_item")
    self.i = 0

  def run(self, debug = False):
    self.flow.invalidate_chain(self.list_item)
    value = self.get_next_item(debug = debug)
    self.list_item.set_value(value)
  
  def is_done(self):
    if not(self.i < len(self.list_in.value)):
      return True
    
    return super(LoopStart, self).is_done()
    
  def get_next_item(self, debug = False):
    if debug: 
      print "get_next_item : self.i =", self.i, "=>", 
      
    if not(self.i < len(self.list_in.value)):
      if debug:
        print "END OF LIST"
      raise StopIteration
      
    result = self.list_in.value[self.i]
    self.i += 1
    if debug:
      print result
    return result
    
  
register_element_type(LoopStart)


class LoopStop(Element):
  class_name = "loop_stop"
  
  def __init__(self, title = None, element_model = None):
    super(LoopStop, self).__init__(title = title, element_model = element_model)
    self.list_item = self.add_input_connector(title = "list_item")
    self.append = self.add_input_connector(title = "append", default_value = True)
    self.list_out = self.add_output_connector(title = "list_out")
    self.loop_start = None
    self.tmp_list = []

  def find_loop_start(self):
    if self.loop_start is not None:
      return
      
    result = self.element_group.get_elements_of_type(LoopStart)
    if len(result) != 1:
      print "find_loop_start() failed: len(result) =", len(result)
      return
    
    self.loop_start = result[0]
      
  def is_ready(self):
    if self.append.is_ready():
      if self.append.value == False:
        return True
        
    return super(LoopStop, self).is_ready()
    
  def run(self, debug = False):
    if debug:
      print "append =", self.append.value, "list_item =", self.list_item.value
      
    if self.append.value:
      self.tmp_list.append(self.list_item.value)
    
    try:
      self.find_loop_start()
      self.loop_start.run_or_block(debug = debug)
      
    except StopIteration:
      if debug:
        print "loop finished, set output =", self.tmp_list
        
      self.list_out.set_value(self.tmp_list)
  
  
register_element_type(LoopStop)
