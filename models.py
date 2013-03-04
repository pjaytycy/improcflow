import numpy


DEBUG = False


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
    self.valid = False
    self.title = title
    
  def set_value(self, value):
    if DEBUG:
      print "%s %s set_value" % (self.__class__.__name__, self.title)
    self.value = value
    self.valid = True
  
  def invalidate(self):
    # This function only invalidates this single connectors. If you 
    # want to invalidate the full chain behind a connector, use:
    #    flow.invalidate(connector)
    
    if DEBUG:
      print "%s invalidate" % (self.title)
      
    self.valid = False
  
  def is_ready(self):
    if DEBUG:
      print "%s is_ready: %s" % (self.title, self.valid)
      
    return self.valid

    
class Element(object):
  def __init__(self, title = None):
    self.title = title
    self.input_connectors = []
    self.output_connectors = []
    self.flow = None
    self.number_of_runs = 0
    
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
  
  def invalidate(self, invalid_connector):
    # This function only invalidates output connectors of this element. If you 
    # want to invalidate the full chain behind a connector, use:
    #    self.flow.invalidate(connector)
    #
    # invalidate all output connectors if one input connector changes
    # only report output connectors that were valid previously!
    if DEBUG:
      print "%s %s invalidate" % (self.__class__.__name__, self.title)
    
    result = []
    if not(invalid_connector in self.input_connectors):
      return result
    
    for output_connector in self.output_connectors:
      if output_connector.is_ready():
        output_connector.invalidate()
        result.append(output_connector)
        
    return result
    
    
  def run(self):
    self.number_of_runs += 1
    if DEBUG:
      print "%s %s run (# %d)" % (self.__class__.__name__, self.title, self.number_of_runs)
    
  
  def is_ready(self):
    for input_connector in self.input_connectors:
      if not(input_connector.is_ready()):
        return False
    return True
  
  
  def is_done(self):
    for output_connector in self.output_connectors:
      if not(output_connector.is_ready()):
        return False
    return True
    
  
  def get_number_of_executions(self):
    return self.number_of_runs
    
  
class Connection(Element):
  def __init__(self, title = None):
    super(Connection, self).__init__(title = title)
    self.src = self.add_input_connector()
    self.dst = self.add_output_connector()
  
  def set_src_dst(self, src, dst):
    self.src = self.replace_input_connector(self.src, src)
    self.dst = self.replace_output_connector(self.dst, dst)
    if self.flow:
      self.flow.invalidate(self.dst)
    else:
      self.dst.invalidate()
        
  def run(self):
    super(Connection, self).run()
    if DEBUG:
      print "  Connection %s from %s to %s" % (self.title, self.src.title, self.dst.title)
    self.dst.set_value(self.src.value)

    
class InputImage(Element):
  def __init__(self, title = None):
    super(InputImage, self).__init__(title = title)
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
    
    
class OpenCVMean(Element):
  def __init__(self, title = None):
    super(OpenCVMean, self).__init__(title = title)
    self.src = self.add_input_connector(title = "src")
    self.mean = self.add_output_connector(title = "mean")
    
  def run(self):
    super(OpenCVMean, self).run()
    self.mean.set_value(numpy.average(self.src.value))
    
  
class OutputNumber(Element):
  def __init__(self, title = None):
    super(OutputNumber, self).__init__(title = title)
    self.number = self.add_input_connector(title = "number")
      
  def result(self):
    if self.is_ready():
      return self.number.value
    return None
    
  
class Flow(object):
  def __init__(self):
    self.elements = []
  
  def add_element(self, element):
    element.flow = self
    self.elements.append(element)
  
  def connect(self, src, dst, title = None):
    for element in self.elements:
      if type(element) != Connection:
        continue
      if (element.dst != dst):
        continue
      self.disconnect(element)
      break
      
    connection = Connection(title = title)
    connection.set_src_dst(src, dst)
    self.elements.append(connection)
  
  def disconnect(self, connection):
    self.elements.remove(connection)
    self.invalidate(connection.dst)
  
  
  def invalidate(self, invalid_connector):
    invalid_connector.invalidate()
    for element in self.elements:
      if invalid_connector in element.input_connectors:
        # only return connectors which were still valid and are now made invalid
        new_invalid_connectors = element.invalidate(invalid_connector)
        for new_invalid_connector in new_invalid_connectors:
          self.invalidate(new_invalid_connector)
          
  
  def run(self, elements_to_do = None):
    if elements_to_do is None:
      elements_to_do = self.elements[:]
    
    elements_left = []
    elements_done = 0
    for element in elements_to_do:
      if element.is_ready() and not element.is_done():
        element.run()
        elements_done += 1
      else:
        elements_left.append(element)
    
    if elements_done == 0:
      return True
    
    return self.run(elements_left)
  
