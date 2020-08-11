# -*- coding: utf-8 -*-
"""
    @author: Nick Ruggero
    @organization: Covert Lab, Department of Bioengineering, Stanford University
    @date: Created 8/14/2014
    @LastEditors: Hwrn
    @LastEditTime: 2020-08-10 21:52:48
    @FilePath: /WholeCellEcoliRelease/wholecell/utils/units.py
    @Description:
        Defines/registers custom units for Pint
    @TODO:
"""

import scipy.constants
import numpy as np
from unum.units import *
from unum import Unum

count = Unum.unit('count',mol/(scipy.constants.Avogadro))
nt = Unum.unit('nucleotide', count)
aa = Unum.unit('amino_acid', count)

def sort(a, axis=-1, kind='quicksort', order=None):
    """
        @description: 不考虑单位的排序
    """
    assert hasUnit(a), 'Only works on Unum!'
    return getUnit(a) * np.sort(a.asNumber(), axis, kind, order)

def nanmean(a, axis=None, dtype=None, out=None, keepdims=False):
    assert hasUnit(a), 'Only works on Unum!'

    a_unit = getUnit(a)
    a = a.asNumber()
    return a_unit * np.nanmean(a, axis, dtype, out, keepdims)

def sum(array, axis = None, dtype=None, out=None, keepdims=False):
    assert hasUnit(a), 'Only works on Unum!'

    units = getUnit(array)
    return units * np.sum(array.asNumber(), axis, dtype, out, keepdims)

def abs(array):
    assert hasUnit(a), 'Only works on Unum!'

    units = getUnit(array)
    return units * np.abs(array.asNumber())

def dot(a, b, out=None):
    assert hasUnit(a) or hasUnit(b), 'Only works on Unum!'

    if isinstance(a, Unum):
        a = a.asNumber()

    if isinstance(b,Unum):
        b = b.asNumber()

    return getUnit(a) * getUnit(b) * np.dot(a,b,out)

def floor(x):
    assert hasUnit(a), 'Only works on Unum!'
    x_unit = getUnit(x)
    x = x.asNumber()
    return x_unit * np.floor(x)

def transpose(array, axis=None):
    units = getUnit(array)

    return units * np.transpose(array.asNumber(), axis)

def hstack(tup):
    unit = getUnit(tup[0])
    value = []
    for array in tup:
        assert hasUnit(array), 'Only works on Unum!'

        array.normalize()
        value.append(array.matchUnits(unit)[0].asNumber())

    return unit * np.hstack(tuple(value))

def getUnit(value):
    """
        @description:
            if hasUnit(value):
                return its Unit.
            else: return blank unit.
    """
    if hasUnit(value):
        value.normalize()
        value_units = value.copy()
        value_units._value = 1
    else:
        value_units = Unum.unit("")
    return value_units

def hasUnit(value):
    """
        @description:
            if the value has a unit Unum, return True
    """
    return isinstance(value, Unum)

def convertNoUnitToNumber(value):
    """
        @description: two exception: AssertionError, ShouldBeUnitlessError
    """
    assert hasUnit(a), 'Only works on Unum!'

    value.normalize()
    value.checkNoUnit()
    return value.asNumber()
