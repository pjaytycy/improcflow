import unittest

from django.test import TestCase

from improcflow.logic import *
    
  
class DefaultValueTests(TestCase):
  def test_allow_default_None(self):
    class MockElement(Element):
      class_name = "test_allow_default_None_mock"
      
      def __init__(self, title = None, element_model = None):
        super(MockElement, self).__init__(title = title, element_model = element_model)
        self.src = self.add_input_connector(title = "src")
        self.mock = self.add_input_connector(title = "mock", default_value = None)
        self.dst = self.add_output_connector(title = "dst")

      def set_mock_value(self, src):
        self.mock.set_value(src)
        self.flow.invalidate(self.dst)
      
      def run(self, debug = False):
        if self.mock.value is None:
          self.dst.set_value(self.src.value)
        else:
          self.dst.set_value(self.src.value * 4)
                  
    register_element_type(MockElement)

    element_input = InputData(title = "element_input")
    element_input.set_value([[1, 2, 3], [4, 5, 6]])
    element_mean = OpenCVMean(title = "element_mean")
    element_mock = MockElement(title = "element_mock")
    element_output = OutputData(title = "element_output")
    
    flow = Flow()
    flow.add_element(element_input)
    flow.add_element(element_mean)
    flow.add_element(element_mock)
    flow.add_element(element_output)
    flow.connect(element_input.data, element_mean.src, title = "data_connection_1")
    flow.connect(element_mean.mean, element_mock.src, title = "data_connection_2")
    flow.connect(element_mock.dst, element_output.data, title = "data_connection_3")
    
    flow.run()
    self.assertEqual(3.5, element_output.result())
    
    element_mock.set_mock_value("blah")
    
    flow.run()
    self.assertEqual(14.0, element_output.result())

    
  def test_disconnect_input_connector_without_default_value(self):
    element_input = InputData(title = "element_input")
    element_input.set_value([[1, 2, 3], [4, 5, 6]])
    element_mean = OpenCVMean(title = "element_mean")
    element_output = OutputData(title = "element_output")
    
    flow = Flow()
    flow.add_element(element_input)
    flow.add_element(element_mean)
    flow.add_element(element_output)
    connection_data_1 = flow.connect(element_input.data, element_mean.src, title = "data_connection_1")
    connection_data_2 = flow.connect(element_mean.mean, element_output.data, title = "data_connection_2")
    
    flow.run()
    self.assertEqual(3.5, element_output.result())
    
    flow.disconnect(connection_data_1)
    self.assertIsNone(element_output.result())
    self.assertEqual(False, element_mean.is_ready())
  
  
  def test_multiple_connect_disconnect_scenario(self):
    class MockElement(Element):
      class_name = "test_allow_default_None_mock"
      
      def __init__(self, title = None, element_model = None):
        super(MockElement, self).__init__(title = title, element_model = element_model)
        self.src = self.add_input_connector(title = "src")
        self.mock = self.add_input_connector(title = "mock", default_value = None)
        self.dst = self.add_output_connector(title = "dst")

      def set_mock_value(self, src):
        self.mock.set_value(src)
        self.flow.invalidate(self.dst)
      
      def run(self, debug = False):
        if self.mock.value is None:
          self.dst.set_value(self.src.value)
        else:
          self.dst.set_value(self.src.value * 4)
                  
    register_element_type(MockElement)

    element_input = InputData(title = "element_input")
    element_input.set_value([[1, 2, 3], [4, 5, 6]])
    element_input2 = InputData(title = "element_input_2")
    element_input2.set_value("blah")
    element_mean = OpenCVMean(title = "element_mean")
    element_mock = MockElement(title = "element_mock")
    element_output = OutputData(title = "element_output")
    
    flow = Flow()
    flow.add_element(element_input)
    flow.add_element(element_input2)
    flow.add_element(element_mean)
    flow.add_element(element_mock)
    flow.add_element(element_output)
    connection_1 = flow.connect(element_input.data, element_mean.src, title = "data_connection_1")
    connection_2 = flow.connect(element_mean.mean, element_mock.src, title = "data_connection_2")
    connection_3 = flow.connect(element_mock.dst, element_output.data, title = "data_connection_3")
    
    # 1) run with element_mock.mock not connected, ie: default = None
    flow.run()
    self.assertEqual(3.5, element_output.result())

    # 2) connect element_mock.mock to a value != None; this should invalidate everything, then rerun it.
    connection_4 = flow.connect(element_input2.data, element_mock.mock, title = "mock_connection")
    self.assertIsNone(element_output.result())
    
    flow.run()
    self.assertEqual(14, element_output.result())

    # 3) disconnecting should invalidate everything
    flow.disconnect(connection_4)
    self.assertIsNone(element_output.result())
    
    flow.run()
    self.assertEqual(3.5, element_output.result())
    
    # 4) connect element_mock.mock to a value = None; this could leave everything valid or invalidate everything. It is not so important.
    element_input2.set_value(None)
    connection_5 = flow.connect(element_input2.data, element_mock.mock, title = "mock_connection")
    flow.run()
    
    # 5) disconnecting should leave everything valid
    flow.disconnect(connection_5)
    self.assertEqual(3.5, element_output.result())

