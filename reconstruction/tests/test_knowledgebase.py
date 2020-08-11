"""
Test KnowledgeBase.py

@author: Derek Macklin
@organization: Covert Lab, Department of Bioengineering, Stanford University
@date: Created 3/22/2013
"""



import unittest
import warnings

import pickle
import os

import wholecell.utils.constants

import nose.plugins.attrib as noseAttrib

class Test_KnowledgeBase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self.kb = kb = pickle.load(
            open(os.path.join(
                wholecell.utils.constants.SERIALIZED_KB_DIR,
                wholecell.utils.constants.SERIALIZED_KB_FIT_FILENAME
                ), "rb")
            )

    def tearDown(self):
        pass
