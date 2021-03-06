from improcflow.models import FlowModel, ElementModel
from improcflow.logic import get_class_for_element_type, register_element_type
from improcflow.logic import Element, Connection
from improcflow.logic import InputData, OutputData

class ElementNotFoundError(Exception):
  pass

class Flow(Element):
  class_name = "flow"
  
  def __init__(self, title = None, flow_id = None, element_model = None):
    self.elements = []
    self.element_groups = []
    if (flow_id is None) and (element_model is None):
      # creating a new object : first create the Element(), then create a new flow
      super(Flow, self).__init__(title = title)
      self.create_new_flow()
    else:
      # loading an existing object : first get the element_model, then load the element from DB, then load the flow from DB
      if (element_model is None):
        # assume flow_id is not None
        # get flow_model and element_model from flow_id
        flow_model = FlowModel.objects.get(pk = flow_id)
        element_model = flow_model.element
      else:
        # we got element_model, get flow_model from it
        flow_model = element_model.flowmodel
        
      super(Flow, self).__init__(title = title, element_model = element_model)
        
      self.load_flow_from_database(flow_model)
        
  def create_new_flow(self):
    # don't repeat the actions from create_new_element() !
    if self.title is None:
      self.flow_model = FlowModel(element = self.element_model)
    else:
      self.flow_model = FlowModel(element = self.element_model, title = self.title)
    self.flow_model.save()
    
  def load_flow_from_database(self, flow_model = None):
    self.flow_model = flow_model
    self.title = self.flow_model.title
    for element_model in self.flow_model.elementmodel_set.all():
      specific_class = get_class_for_element_type(element_model.class_name)
      element = specific_class(element_model = element_model)
      self.add_element(element)
      element.find_and_set_group_update_grouplist(self.element_groups)
    
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
    return self.element_model.id
  
  def add_element(self, element):
    element.set_flow(self)
    self.elements.append(element)
    
    if (type(element) == InputData) and not(element.title is None):
      self.input_connectors.append(element.data_in)
      setattr(self, element.title, element.data_in)
    
    if (type(element) == OutputData) and not(element.title is None):
      self.output_connectors.append(element.data_out)
      setattr(self, element.title, element.data_out)
  
  def get_element(self, title = None, element_id = None):
    if element_id is not None:
      for element in self.elements:
        if element.element_model.id == element_id:
          return element
        if isinstance(element, Flow):
          try:
            return element.get_element(element_id = element_id)
          except ElementNotFoundError:
            pass
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
      self.invalidate_chain(invalid_connector)
    
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
    return connection
  
  def disconnect(self, connection):
    self.elements.remove(connection)
    needs_invalidate = connection.dst.default_needs_invalidate()
    if needs_invalidate:
      self.invalidate_chain(connection.dst)
    connection.dst.default()  # need to set default *after* invalidate()
    connection.delete()
  
  def invalidate_chain(self, invalid_connector):
    invalid_connector.invalidate_connector()
    for element in self.elements:
      if invalid_connector in element.input_connectors:
        # only return connectors which were still valid and are now made invalid
        new_invalid_connectors = element.invalidate_element(invalid_connector)
        for new_invalid_connector in new_invalid_connectors:
          self.invalidate_chain(new_invalid_connector)
  
  # extend element.invalidate_element() in case of element == Flow()
  # we need to also invalidate the internal flow, not just the output connectors
  # at the end, we need to return the result of element.invalidate_element() 
  # which is the list of output connectors that were invalidated
  def invalidate_element(self, invalid_connector):
    result = super(Flow, self).invalidate_element(invalid_connector)
    self.invalidate_chain(invalid_connector)
    return result
  
  def run(self, iteration = 0, debug = False):
    if debug:
      print
      print self.title, ":: run() :: iteration", iteration
      print
    
    elements_done = 0
    for element in self.elements:
      if element.is_ready() and not element.is_done():
        if debug:
          print self.title, "  execute element :", element
        element.run_or_block(debug = debug)
        elements_done += 1

    if debug:
      print
      print self.title, "  elements_done =", elements_done
      print
    
    if elements_done == 0:
      return True
    
    return self.run(iteration + 1, debug = debug)
  

  def debug_state(self):
    print "==== FLOW : %s ====" % self.title
    super(Flow, self).debug_state()
    for element in self.elements:
      element.debug_state()
    print "==== ===="

register_element_type(Flow)
