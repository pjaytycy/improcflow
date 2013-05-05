from improcflow.models import FlowModel
from improcflow.logic import get_class_for_element_type
from improcflow.logic import Element, Connection

class ElementNotFoundError(Exception):
  pass

class Flow(object):
  def __init__(self, title = None, flow_id = None):
    if flow_id is None:
      self.create_new(title)
    else:
      self.load_from_database(flow_id)
        
  def create_new(self, title = None):
    self.elements = []
    self.title = title
    if title is None:
      self.flow_model = FlowModel()
    else:
      self.flow_model = FlowModel(title = title)
    self.flow_model.save()
    
  def load_from_database(self, flow_id):
    self.flow_model = FlowModel.objects.get(pk = flow_id)
    self.title = self.flow_model.title
    self.elements = []
    for element_model in self.flow_model.elementmodel_set.all():
      specific_class = get_class_for_element_type(element_model.class_name)
      element = specific_class(element_model = element_model)
      element.set_flow(self)
      self.elements.append(element)
    
    for element in self.elements:
      if not(isinstance(element, Connection)):
        continue
      
      src_element_id = element.connection_model.src_element.id
      dst_element_id = element.connection_model.dst_element.id
      src_element = self.get_element(element_id = src_element_id)
      dst_element = self.get_element(element_id = dst_element_id)
      src = src_element.get_connector(element.connection_model.src_connector)
      dst = dst_element.get_connector(element.connection_model.dst_connector)
      element.set_src_dst(src, dst)
    
  @classmethod
  def get_all_saved_flows(cls):
    return FlowModel.objects.all()
    
  def get_id(self):
    return self.flow_model.id
  
  def add_element(self, element):
    element.set_flow(self)
    self.elements.append(element)
  
  def get_element(self, title = None, element_id = None):
    if element_id is not None:
      for element in self.elements:
        if element.element_model.id == element_id:
          return element
      raise ElementNotFoundError("Could not find element with id == %d" % (element_id))
          
    if title is not None:
      for element in self.elements:
        if element.title == title:
          return element
      raise ElementNotFoundError("Could not find element with title == %s" % (title))
  
    raise ValueError("Atleast title or element_id should be provided")
  
  def get_num_elements(self):
    return len(self.elements)
  
  def remove_element(self, element):
    # invalidate all the output connectors of this element + everything in this flow that depends on them
    for invalid_connector in element.output_connectors:
      self.invalidate(invalid_connector)
    
    # Remove the element from this flow object
    self.elements.remove(element)
    
    # Remove the linked connections from this flow object
    # We need to iterate over a copy of self.elements[], because items will be removed from it
    for connection in self.elements[:]:
      if not(isinstance(connection, Connection)):
        continue
      if connection.dst in element.input_connectors:
        self.disconnect(connection)
        continue
      if connection.src in element.output_connectors:
        self.disconnect(connection)
        continue
      
    # Remove the element from the database
    # The database will automatically be updated to also remove the connections linked to this element
    element.delete()
    
  def connect(self, src, dst, title = None):
    for element in self.elements:
      if not(isinstance(element, Connection)):
        continue
      if (element.dst != dst):
        continue
      self.disconnect(element)
      break
      
    connection = Connection(title = title)
    connection.set_flow(self)
    connection.set_src_dst(src, dst)
    self.elements.append(connection)
  
  def disconnect(self, connection):
    self.elements.remove(connection)
    self.invalidate(connection.dst)
    connection.delete()
  
  
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
        element.run_or_block()
        elements_done += 1
      else:
        elements_left.append(element)
    
    if elements_done == 0:
      return True
    
    return self.run(elements_left)
  

  def debug_state(self):
    print "==== FLOW : %s ====" % self.title
    for element in self.elements:
      element.debug_state()
    print "==== ===="