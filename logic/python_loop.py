from improcflow.logic import Element, ElementGroup, register_element_type


class PythonLoop(ElementGroup):
  def __init__(self, title = None):
    super(PythonLoop, self).__init__(title = title)
    if title is None:
      start = PythonLoopStart()
      stop = PythonLoopStop()
    else:
      start = PythonLoopStart(title = title + "_start")
      stop = PythonLoopStop(title = title + "_stop")
      
    self.add_element(start)
    self.add_element(stop)
    

class PythonLoopStart(Element):
  class_name = "python_loop_start"
  
  def __init__(self, title = None, element_model = None):
    super(PythonLoopStart, self).__init__(title = title, element_model = element_model)
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
    
    return super(PythonLoopStart, self).is_done()
    
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
    
  
register_element_type(PythonLoopStart)


class PythonLoopStop(Element):
  class_name = "python_loop_stop"
  
  def __init__(self, title = None, element_model = None):
    super(PythonLoopStop, self).__init__(title = title, element_model = element_model)
    self.list_item = self.add_input_connector(title = "list_item")
    self.append = self.add_input_connector(title = "append", default_value = True)
    self.list_out = self.add_output_connector(title = "list_out")
    self.loop_start = None
    self.tmp_list = []

  def find_loop_start(self):
    if self.loop_start is not None:
      return
      
    result = self.element_group.get_elements_of_type(PythonLoopStart)
    if len(result) != 1:
      print "find_loop_start() failed: len(result) =", len(result)
      return
    
    self.loop_start = result[0]
      
  def is_ready(self):
    if self.append.is_ready():
      if self.append.value == False:
        return True
        
    return super(PythonLoopStop, self).is_ready()
    
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
  
  
register_element_type(PythonLoopStop)
