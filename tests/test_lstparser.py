from declarative_streamlit.core.build.lstparser import StreamlitLayoutParser
from declarative_streamlit.core.build.cstparser import StreamlitComponentParser
from declarative_streamlit.core.handlers.layer import Layer
from declarative_streamlit.core.handlers.schema import Schema
from streamlit import container,button
from test.support import unittest


# Unit test for StreamlitLayoutParser

class TestStreamlitLayoutParser(unittest.TestCase):
    def setUp(self):
        """
        Set up the test case by creating a StreamlitLayoutParser instance.
        """
        self.component = StreamlitLayoutParser(container)
        self.parserconfig = self.component.parserconfig
        self.parserconfig.stateful = True
        self.parserconfig.fatal = False
        self.parserconfig.strict = True

    def test_initialization(self):
        """
        Test the initialization of the StreamlitLayoutParser instance.
        """
        self.assertIsInstance(self.component, StreamlitLayoutParser)
        self.assertEqual(self.component.component, container)
    
    def test_body(self):
        """
        Test the body attribute of the StreamlitLayoutParser instance.
        """
        self.assertIsInstance(self.component.body, Layer)
    
    def test_schema(self):
        """
        Test the schema attribute of the StreamlitLayoutParser instance.
        """
        self.assertIsInstance(self.component.schema, Schema)
    
    
    def test_set_fatal(self):
        """
        Test the set_fatal method.
        """
        self.component.set_fatal(True)
        self.assertTrue(self.component._fatal)
        self.component.set_fatal(False)
        self.assertFalse(self.component._fatal)
    
    def test_set_strict(self):
        """
        Test the set_strict method.
        """
        self.component.set_strict(True)
        self.assertTrue(self.component._strict)
        self.component.set_strict(False)
        self.assertFalse(self.component._strict)
    
    def test_set_column_based(self):
        """
        Test the set_column_based method.
        """
        self.component.set_column_based(True)
        self.assertTrue(self.component._colum_based)
        self.component.set_column_based(False)
        self.assertFalse(self.component._colum_based)
    
    def test_set_errhandler(self):
        """
        Test the set_errhandler method.
        """
        def dummy_errhandler():
            pass
        
        self.component.set_errhandler(dummy_errhandler)
        self.assertEqual(self.component._errhandler, dummy_errhandler)


    def test_wrong_fatal(self):
        """
        Test the set_fatal method with wrong value.
        """
        with self.assertRaises(ValueError):
            self.component.set_fatal("wrong_value")
    
    def test_wrong_strict(self):
        """
        Test the set_strict method with wrong value.
        """
        with self.assertRaises(ValueError):
            self.component.set_strict("wrong_value")
    
    def test_wrong_column_based(self):
        """
        Test the set_column_based method with wrong value.
        """
        with self.assertRaises(ValueError):
            self.component.set_column_based("wrong_value")
    
    def test_wrong_errhandler(self):
        """
        Test the set_errhandler method with wrong value.
        """
        with self.assertRaises(ValueError):
            self.component.set_errhandler("wrong_value")
    
    def test_add_component(self):
        """
        Test the add_component method.
        """
        add = self.component.add_component(button, "test", key="test")
        self.assertIsInstance(add, StreamlitComponentParser)
        self.assertIsInstance(self.component.body[-1], StreamlitComponentParser)
    
    def test_add_container(self):
        """
        Test the add_container method.
        """
        add = self.component.add_container(container)
        self.assertIsInstance(add, StreamlitLayoutParser)
        self.assertIsInstance(self.component.body[-1], StreamlitLayoutParser)