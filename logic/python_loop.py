from improcflow.logic import Element, register_element_type


class PythonLoop(object):
  def __init__(self):
    self.start = PythonLoopStart()
    self.stop = PythonLoopStop()
    self.stop.loop_start = self.start
    
  def __iter__(self):
    yield self.start
    yield self.stop


class PythonLoopStart(Element):
  class_name = "python_loop_start"
  
  def __init__(self, title = None, element_model = None):
    super(PythonLoopStart, self).__init__(title = title, element_model = element_model)
    self.list_in = self.add_input_connector(title = "list_in")
    self.list_item = self.add_output_connector(title = "list_item")
    self.i = 0

  def run(self, debug = False):
    value = self.get_next_item(debug = debug)
    self.set_next_item(value, debug = debug)
  
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
    
  def set_next_item(self, value, debug = False):
    self.flow.invalidate_chain(self.list_item)
    self.list_item.set_value(value)
  
register_element_type(PythonLoopStart)


class PythonLoopStop(Element):
  class_name = "python_loop_stop"
  
  def __init__(self, title = None, element_model = None):
    super(PythonLoopStop, self).__init__(title = title, element_model = element_model)
    self.list_item = self.add_input_connector(title = "list_item")
    self.list_out = self.add_output_connector(title = "list_out")
    self.loop_start = None
    self.tmp_list = []

  def run(self, debug = False):
    if debug:
      print "append", self.list_item.value
      
    self.tmp_list.append(self.list_item.value)
    
    try:
      self.loop_start.run_or_block(debug = debug)
      
    except StopIteration:
      if debug:
        print "loop finished, set output =", self.tmp_list
        
      self.list_out.set_value(self.tmp_list)
  
  
register_element_type(PythonLoopStop)
