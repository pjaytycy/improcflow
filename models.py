import numpy

from django.db import models


DEBUG = False

# some defines for valid_id:
VALID_ID_START   = 1    # first value for the flow
VALID_ID_NO_DATA = -1   # no data for this connector, so it can never be valid
VALID_ID_UNKNOWN = -2   # we have data, but don't know the valid_id to assign to it => always valid

# a helper function to compare valid_id's:
def is_valid(actual_valid_id, expected_valid_id):
  if (actual_valid_id == VALID_ID_NO_DATA):
    return False
  if (actual_valid_id == VALID_ID_UNKNOWN):
    return True
  return (actual_valid_id == expected_valid_id)

# a helper function to combine 2 parts of a title
def combine_title(part1, part2):
  if part1 is None:
    return None
  if part2 is None:
    return None
  return str(part1) + "." + str(part2)


class Connector(object):
  def __init__(self, title = None):
    self.value = None
    self.valid_id = VALID_ID_NO_DATA
    self.title = title
    
  def set_value(self, value, valid_id):
    self.value = value
    self.valid_id = valid_id
  
  def is_ready(self, valid_id):
    return is_valid(self.valid_id, valid_id)

    
class Element(object):
  def __init__(self, title = None):
    self.title = title
    self.input_connectors = []
    self.output_connectors = []
    
  def add_input_connector(self, title = None):
    input_connector = Connector(title = combine_title(self.title, title))
    self.input_connectors.append(input_connector)
    return input_connector
  
  def add_output_connector(self, title = None):
    output_connector = Connector(title = combine_title(self.title, title))
    self.output_connectors.append(output_connector)
    return output_connector
  
  def replace_input_connector(self, old_input_connector, new_input_connector):
    self.input_connectors.remove(old_input_connector)
    self.input_connectors.append(new_input_connector)
    return new_input_connector
  
  def replace_output_connector(self, old_output_connector, new_output_connector):
    self.output_connectors.remove(old_output_connector)
    self.output_connectors.append(new_output_connector)
    return new_output_connector
    
  def run(self):
    if DEBUG:
      print "%s %s run" % (self.__class__.__name__, self.title)
  
  def is_ready(self, valid_id):
    for input_connector in self.input_connectors:
      if not(input_connector.is_ready(valid_id)):
        return False
    return True
  
  def get_next_valid_id(self):
    if self.flow is None:
      new_valid_id = VALID_ID_UNKNOWN
    else:
      new_valid_id = self.flow.get_next_valid_id()
    return new_valid_id
  
  def get_current_valid_id(self):
    if self.flow is None:
      current_valid_id = VALID_ID_UNKNOWN
    else:
      current_valid_id = self.flow.get_current_valid_id()
    return current_valid_id
  
  
class Connection(Element):
  def __init__(self, title = None):
    super(Connection, self).__init__(title = title)
    self.src = self.add_input_connector()
    self.dst = self.add_output_connector()
  
  def set_src_dst(self, src, dst):
    self.src = self.replace_input_connector(self.src, src)
    self.dst = self.replace_output_connector(self.dst, dst)
        
  def run(self):
    super(Connection, self).run()
    if DEBUG:
      print "  Connection %s from %s to %s" % (self.title, self.src.title, self.dst.title)
    self.dst.set_value(self.src.value, self.src.valid_id)

    
class InputImage(Element):
  def __init__(self, title = None):
    super(InputImage, self).__init__(title = title)
    self.dummy = self.add_input_connector(title = "")
    self.image = self.add_output_connector(title = "image")
    self.flow = None

  def set_value(self, src):
    new_valid_id = self.get_next_valid_id()
    self.dummy.set_value(True, new_valid_id)
    self.image.set_value(src, new_valid_id)
    
    
class OpenCVMean(Element):
  def __init__(self, title = None):
    super(OpenCVMean, self).__init__(title = title)
    self.src = self.add_input_connector(title = "src")
    self.mean = self.add_output_connector(title = "mean")
    
  def run(self):
    super(OpenCVMean, self).run()
    self.mean.set_value(numpy.average(self.src.value), self.src.valid_id)
    
  
class OutputNumber(Element):
  def __init__(self, title = None):
    super(OutputNumber, self).__init__(title = title)
    self.number = self.add_input_connector(title = "number")
      
  def result(self):
    current_valid_id = self.get_current_valid_id()
    if self.is_ready(current_valid_id):
      return self.number.value
    return None
    
  
class Flow(object):
  def __init__(self):
    self.elements = []
    self.valid_id = VALID_ID_START
  
  def add_element(self, element):
    element.flow = self
    self.elements.append(element)
  
  def connect(self, src, dst, title = None):
    connection = Connection(title = title)
    connection.set_src_dst(src, dst)
    self.elements.append(connection)
  
  def run(self, elements_to_do = None):
    if elements_to_do is None:
      elements_to_do = self.elements[:]
    
    elements_left = []
    elements_done = 0
    for element in elements_to_do:
      if element.is_ready(self.get_current_valid_id()):
        element.run()
        elements_done += 1
      else:
        elements_left.append(element)
    
    if elements_done == 0:
      return True
    
    return self.run(elements_left)
  
  def get_next_valid_id(self):
    self.valid_id += 1
    return self.valid_id
  
  def get_current_valid_id(self):
    return self.valid_id