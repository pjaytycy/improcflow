from improcflow.models import ElementModel, ConnectionModel
from improcflow.logic import convert_data

DEBUG = False

# a dictionary to keep string => class mapping
element_model_to_class = {}
def register_element_type(cls):
  element_model_to_class[cls.class_name] = cls
  
  
def get_class_for_element_type(class_name):
  return element_model_to_class[class_name]
  
  
class Connector(object):
  def __init__(self, element, title = None, data_types = None, default_value = None):
    self.value = default_value
    if default_value is None:
      self.valid = False
    else:
      self.valid = True
    self.blocked = False
    self.element = element
    self.title = title
    self.data_types = data_types
  
  def debug_string(self):
    return self.title + " : value = " + str(self.value) + ", valid = " + str(self.valid) + ", blocked = " + str(self.blocked)
    
  def set_value(self, value):
    if DEBUG:
      print "%s %s %s set_value" % (self.__class__.__name__, self.element.title, self.title)
    self.value = convert_data(value, self.data_types)
    self.valid = True
  
  def invalidate(self):
    # This function only invalidates this single connector. If you 
    # want to invalidate the full chain behind a connector, use:
    #    flow.invalidate(connector)
    
    if DEBUG:
      print "%s %s invalidate" % (self.element.title, self.title)
      
    self.valid = False
  
  def is_ready(self):
    if DEBUG:
      print "%s %s is_ready: %s" % (self.element.title, self.title, self.valid)
      
    return self.valid

  def is_blocked(self):
    return self.blocked
  
  def block(self):
    self.blocked = True
    self.valid = True

    
class Element(object):
  class_name = "element"
  
  def __init__(self, title = None, element_model = None):
    self.input_connectors = []
    self.output_connectors = []
    self.flow_control = Connector(element = self, title = "flow_control", default_value = True)
    self.flow = None
    self.number_of_runs = 0
    if element_model is None:
      self.create_new(title)
    else:
      self.load_from_database(element_model = element_model)
      
  def create_new(self, title = None):
    self.title = title
    if title is None:
      self.element_model = ElementModel(class_name = self.class_name)
    else:
      self.element_model = ElementModel(class_name = self.class_name, title = title)

  def set_flow(self, flow):
    self.flow = flow
    self.element_model.flow = flow.flow_model
    self.element_model.save()
    
  def load_from_database(self, element_model = None):
    self.element_model = element_model
    self.title = self.element_model.title
  
  def delete(self):
    self.element_model.delete()

  def debug_state(self):
    print "  -- Element : %s : %s --" % (self.__class__.__name__, self.title)
    print "  number_of_runs =", self.number_of_runs
    print "  is_ready ?", self.is_ready()
    print "  is_blocked ?", self.is_blocked()
    print "  is_done ?", self.is_done()
    print "  flow_control :", self.flow_control.debug_string()
    for input_connector in self.input_connectors:
      print "  input_connector :", input_connector.debug_string()
    for output_connector in self.output_connectors:
      print "  output_connector :", output_connector.debug_string()
    print "  -- --"
    
  @classmethod
  def get_all_saved_elements(cls):
    return ElementModel.objects.all()
    
  def add_input_connector(self, title = None, data_types = None):
    input_connector = Connector(element = self, title = title, data_types = data_types)
    self.input_connectors.append(input_connector)
    return input_connector
  
  def add_output_connector(self, title = None):
    output_connector = Connector(element = self, title = title)
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
  
  def get_connector(self, connector_title):
    for connector in self.input_connectors:
      if connector.title == connector_title:
        return connector
    
    for connector in self.output_connectors:
      if connector.title == connector_title:
        return connector
    
    return None
  
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
  
  
  def run_or_block(self):
    if self.is_blocked():
      self.block()
    else:
      self.number_of_runs += 1
      if DEBUG:
        print "%s %s run (# %d)" % (self.__class__.__name__, self.title, self.number_of_runs)
      self.run()
  
  
  def block(self):
    for output_connector in self.output_connectors:
      output_connector.block()
      
    
  def is_ready(self):
    if not(self.flow_control.is_ready()):
      return False
      
    for input_connector in self.input_connectors:
      if not(input_connector.is_ready()):
        return False
    return True
  
  
  def is_done(self):
    for output_connector in self.output_connectors:
      if not(output_connector.is_ready()):
        return False
    return True
  
  
  def is_blocked(self):
    if self.flow_control.is_blocked():
      return True
    
    if self.flow_control.value == False:
      return True
    
    for input_connector in self.input_connectors:
      if input_connector.is_blocked():
        return True
    
    return False
  
  def get_number_of_executions(self):
    return self.number_of_runs
    
register_element_type(Element)


class Connection(Element):
  class_name = "connection"
  
  def __init__(self, title = None, element_model = None):
    super(Connection, self).__init__(title = title, element_model = element_model)
    self.src = self.add_input_connector()
    self.dst = self.add_output_connector()
    if element_model is None:
      self.connection_model = None
    else:
      self.connection_model = element_model.connectionmodel
  
  @classmethod
  def get_all_saved_connections(cls):
    return ConnectionModel.objects.all()
  
  def set_flow(self, flow):
    super(Connection, self).set_flow(flow)
    # this is the place where the element_model gets saved, so I can create the connection model
    if self.connection_model is None:
      self.connection_model = ConnectionModel(element = self.element_model)

  
  def set_src_dst(self, src, dst):
    self.src = self.replace_input_connector(self.src, src)
    self.dst = self.replace_output_connector(self.dst, dst)
    
    self.connection_model.src_element = src.element.element_model
    self.connection_model.src_connector = src.title
    self.connection_model.dst_element = dst.element.element_model
    self.connection_model.dst_connector = dst.title
    self.connection_model.save()
    
    if self.flow:
      self.flow.invalidate(self.dst)
    else:
      self.dst.invalidate()
    
        
  def run(self):
    if DEBUG:
      print "  Connection %s from %s to %s" % (self.title, self.src.title, self.dst.title)
    self.dst.set_value(self.src.value)

  
  def block(self):
    # exceptional case for a connection: even if src is "blocked", we still want to copy
    # the data from src to dst, because we don't want a connection with different data on
    # both ends of the line.
    self.dst.set_value(self.src.value)
    super(Connection, self).block()
    
register_element_type(Connection)
