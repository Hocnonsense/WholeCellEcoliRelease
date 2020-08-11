#!/usr/bin/env python

"""
UnitStructArray

Wraps Numpy struct arrays using Pint units. Will assure that correct units are
being used while loading constants.

@author: Nick Ruggero
@organization: Covert Lab, Department of Bioengineering, Stanford University
@date: Created 4/31/2014
"""

import numpy as np
import unum

# avoid var-name conflict
from wholecell.utils import units as units_pkg

# TODO: Write test!
class UnitStructArray:
    """UnitStructArray"""

    def __init__(self, struct_array, units):
        self._validate(struct_array, units)

        self.struct_array = struct_array
        self.units = units

    def _validate(self, struct_array, units):
        assert isinstance(struct_array, np.ndarray), 'UnitStructArray must be initialized with a numpy array!\n'
        assert isinstance(units, dict), 'UnitStructArray must be initialized with a dict storing units!\n'
        assert set([x[0] for x in struct_array.dtype.descr]) == set(units.keys()), 'Struct array fields do not match unit fields!\n'

    def _field(self, fieldname):
        if units_pkg.hasUnit(self.units[fieldname]):
            return self.units[fieldname] * self.struct_array[fieldname]
        if self.units[fieldname]:
            raise TypeError(
                'Field has incorrect units or unitless designation!\n')
        return self.struct_array[fieldname]

    def fullArray(self):
        return self.struct_array

    def fullUnits(self):
        return self.units

    def __getitem__(self, key):
        if type(key) == slice:
            return UnitStructArray(self.struct_array[key], self.units)
        elif type(key) == np.ndarray or type(key) == list:
            return UnitStructArray(self.struct_array[key], self.units)
        elif type(key) == int:
            return self.struct_array[key]
        else:
            return self._field(key)

    def __setitem__(self, key, value):
        if units_pkg.hasUnit(value):
            try:
                self.units[key].matchUnits(value)
            except unum.IncompatibleUnitsError:
                raise TypeError('Units do not match!\n')

            self.struct_array[key] = value.asNumber()
            self.units[key] = units_pkg.getUnit(value)

        elif type(value) == list or type(value) == np.ndarray:
            # so unly unit * array is avaible but not vice versa
            if units_pkg.hasUnit(self.units[key]):
                raise TypeError(
                    'Units do not match! Quantity has units your input does not!\n')
            self.struct_array[key] = value
            self.units[key] = None

        else:
            raise TypeError(
                'Cant assign data-type other than unum datatype or list/numpy array!\n')

    def __len__(self):
        return len(self.struct_array)

    def __repr__(self):
        return 'STRUCTURED ARRAY:\n{}\nUNITS:\n{}'.format(self.struct_array.__repr__(), self.units)

    def __eq__(self, other):
        return type(other) == type(self) and \
            self.struct_array.dtype == other.struct_array.dtype and \
            all(self.struct_array == other.struct_array) and \
            self.units == other.units

    def __ne__(self, other):
        return not self.__eq__(other)
