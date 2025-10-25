from declarative_streamlit.core.build.cstparser import StreamlitComponentParser
from streamlit import button
from test.support import unittest

# Unit test for StreamlitComponentParser

class TestStreamlitComponentParser(unittest.TestCase):
    def setUp(self):
        """
        Set up the test case by creating a StreamlitComponentParser instance.
        """
        self.component = StreamlitComponentParser(button, "test",key="test")
        self.parserconfig = self.component.parserconfig
        self.parserconfig.stateful = True
        self.parserconfig.fatal = False
        self.parserconfig.strict = True

    def test_initialization(self):
        """
        Test the initialization of the StreamlitComponentParser instance.
        """
        self.assertIsInstance(self.component, StreamlitComponentParser)
        self.assertEqual(self.component.component, button)
        self.assertEqual(self.component.args, ["test"])
        self.assertEqual(self.component.kwargs, {"key": "test"})
    

    def test_set_stateful(self):
        """
        Test the set_stateful method.
        """
        self.component.set_stateful(False)
        self.assertFalse(self.component._stateful)
        self.component.set_stateful(True)
        self.assertTrue(self.component._stateful)
    
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
    
    def test_set_errhandler(self):
        """
        Test the set_errhandler method.
        """
        def dummy_errhandler():
            pass
        self.component.set_errhandler(dummy_errhandler)
        self.assertEqual(self.component._errhandler, dummy_errhandler)
    
    def test_add_effects(self):
        """
        Test the add_effects method.
        """
        def dummy_effect():
            pass
        self.component.add_effect(dummy_effect)
        self.assertIn(dummy_effect, self.component._effects)
    
    def test_wrong_stateful(self):
        """
        Test the set_stateful method with invalid input.
        """
        with self.assertRaises(ValueError):
            self.component.set_stateful("invalid")

    def test_wrong_fatal(self):
        """
        Test the set_fatal method with invalid input.
        """
        with self.assertRaises(ValueError):
            self.component.set_fatal("invalid")

    def test_wrong_strict(self):
        """
        Test the set_strict method with invalid input.
        """
        with self.assertRaises(ValueError):
            self.component.set_strict("invalid")

    def test_wrong_errhandler(self):
        """
        Test the set_errhandler method with invalid input.
        """
        with self.assertRaises(ValueError):
            self.component.set_errhandler("invalid")

    def test_wrong_effects(self):
        """
        Test the add_effects method with invalid input.
        """
        with self.assertRaises(ValueError):
            self.component.add_effect("invalid")





if __name__ == "__main__":
    unittest.main()