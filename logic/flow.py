from improcflow.models import FlowModel
from improcflow.logic import Element, Connection


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
      element = Element.load_from_database(element_model = element_model)
      element.set_flow(self)
      self.elements.append(element)
    
  def get_id(self):
    return self.flow_model.id
  
  def add_element(self, element):
    element.set_flow(self)
    self.elements.append(element)
  
  def get_element(self, title = None):
    for element in self.elements:
      if element.title == title:
        return element
    return None
  
  def get_num_elements(self):
    return len(self.elements)
  
  def connect(self, src, dst, title = None):
    for element in self.elements:
      if not(isinstance(element, Connection)):
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
  
