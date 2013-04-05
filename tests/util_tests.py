import unittest
from sforce.util import Struct
from sforce import (COMMONS as c, container)

class CommonTest(unittest.TestCase):
    def setUp(self):
        self.c = c
        
    def test_common_sandbox(self):
        self.c['sandbox'] = True
        self.assertTrue("test.salesforce.com" in container(self.c, '/'))

    def test_common_production(self):
        self.c['sandbox'] = False
        self.assertTrue("login.salesforce.com" in container(self.c, '/'))

class UtilTest(unittest.TestCase):
    def test_struct_create(self):
        s = Struct({'aTestAttribute':'Test!'})
        self.assertTrue(hasattr(s, 'aTestAttribute'))
        setattr(s, 'aTestAttribute', 'edited')
        self.assertEqual(s.aTestAttribute, 'edited')
        setattr(s, 'aNewAttribute', 'edited')
        self.assertTrue(hasattr(s, 'aNewAttribute'))
