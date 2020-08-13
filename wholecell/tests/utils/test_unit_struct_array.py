#!/usr/bin/env python

"""
Test unit_struct_array.py

@author: Nick Ruggero
@organization: Covert Lab, Department of Chemical Engineering, Stanford University
@date: Created 8/14/2014
"""
from wholecell.utils.unit_struct_array import UnitStructArray
from wholecell.utils.units import g, mol, fg
import numpy as np

import nose.plugins.attrib as noseAttrib
import nose.tools as noseTools
import unittest

class Test_unit_struct_array(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        """
            @example:
                 >>> us_array
                STRUCTURED ARRAY:
                array([(b'', 0.), (b'', 0.), (b'', 0.)],
                      dtype=[('id', "U10"), ('mass', '<f8')])
                UNITS:
                {'id': None, 'mass': 1 [g]}
        """
        self.struct_array = np.zeros(3, dtype = [('id','a10'),('mass',np.float64)])
        self.units = {'id' : None, 'mass' : g}
        self.us_array = UnitStructArray(self.struct_array, self.units)

    def tearDown(self):
        pass


    @noseAttrib.attr('smalltest','unitstructarray')
    def test_init(self):
        """
            @description:
                check if can recognize param errors
        """
        with self.assertRaises(AssertionError) as context:
            UnitStructArray(1., {'hello' : 'goodbye'})
        self.assertEqual(str(context.exception), 'UnitStructArray must be initialized with a numpy array!\n')

        with self.assertRaises(AssertionError) as context:
            UnitStructArray(self.struct_array, 'foo')
        self.assertEqual(str(context.exception), 'UnitStructArray must be initialized with a dict storing units!\n')

        with self.assertRaises(AssertionError) as context:
            self.units['hi'] = 'bye'
            UnitStructArray(self.struct_array, self.units)
        self.assertEqual(str(context.exception), 'Struct array fields do not match unit fields!\n')

    @noseAttrib.attr('smalltest','unitstructarray')
    def test_field(self):
        """
            @description:
                array message and units

        """
        # array([b'', b'', b''], dtype='|S10')
        self.assertTrue(
            (self.us_array['id'] == self.struct_array['id']).all()
        )

        # [0. 0. 0.] [g]
        self.assertTrue(
            (self.us_array['mass'] == g * self.struct_array['mass']).all()
        )

    @noseAttrib.attr('smalltest','unitstructarray')
    def test_fullArray(self):
        self.assertTrue(
            (self.us_array.fullArray() == self.struct_array).all()
        )

    @noseAttrib.attr('smalltest','unitstructarray')
    def test_fullUnits(self):
        self.assertEqual(
            self.us_array.fullUnits(),
            self.units
        )

    @noseAttrib.attr('smalltest','unitstructarray')
    def test_getItem_slice(self):
        """
            @description: 切片的分配律
        """
        self.assertEqual(
            self.us_array[:1],
            UnitStructArray(self.struct_array[:1], self.units)
            )

    @noseAttrib.attr('smalltest','unitstructarray')
    def test_getItem_indicies(self):
        """
            @description: 指针的分配律
        """
        index = [0,2]

        self.assertEqual(
            self.us_array[index],
            UnitStructArray(self.struct_array[index], self.units)
            )

        index = [True, False, True]

        self.assertEqual(
            self.us_array[index],
            UnitStructArray(self.struct_array[index], self.units)
            )

    @noseAttrib.attr('smalltest','unitstructarray')
    def test_getItem_singleindex(self):
        self.assertEqual(
            self.us_array[0],
            self.struct_array[0]
            )

    @noseAttrib.attr('smalltest','unitstructarray')
    def test_setItem_quantity_with_units(self):
        # np.array([1.,2.,3.]) * g is unavaible
        self.us_array['mass'] = g * np.array([1.,2.,3.])
        self.assertTrue(
            (self.us_array['mass'] == g * np.array([1.,2.,3.])).all()
        )

        with self.assertRaises(Exception) as context:
            self.us_array['mass'] = mol*np.array([1.,2.,3.])
        self.assertEqual(str(context.exception), 'Units do not match!\n')


    @noseAttrib.attr('smalltest','unitstructarray')
    def test_setItem_quantity_no_units(self):
        self.us_array['id'] = ['nick', 'derek', 'john']

        self.assertTrue(
            (self.us_array['id'] == np.array(['nick', 'derek', 'john'], dtype='|S10')).all()
        )

        with self.assertRaises(Exception) as context:
            self.us_array['mass'] = [1,2,3]
        self.assertEqual(str(context.exception), 'Units do not match! Quantity has units your input does not!\n')
