# -*- coding: utf-8 -*-

"""
Tests for classes in cell.py using pytest.
"""

__author__ = 'Julie Forrisdal', 'Marisha Gnanaseelan'
__email__ = 'juforris@nmbu.no', 'magn@nmbu.no'

from src.biosim.cell import Cell, Savannah, Jungle, Desert, MountainAndOcean

import pytest


class TestCell:
    """Tests for Cell class."""
    def test_constructor(self):
        """Default constructor is callable."""
        c = Cell()
        assert isinstance(c, Cell)

    def test_fodder_first_year(self):
        """ Tests that fodder_first_year method
         changes fodder_in_cell attribute"""
        c = Cell()
        assert c.fodder_in_cell is None
        c.fodder_first_year(10)
        assert c.fodder_in_cell == 10


class TestSavannah:
    """ Tests for Savannah class."""
    def test_constructor(self):
        """Default constructor is callable. """
        s = Savannah()
        assert isinstance(s, Savannah)

    def test_default_values(self):
        s1 = Savannah()
        assert s1.f_max is None




class TestJungle:
    """ Tests for Jungle class."""
    def test_constructor(self):
        """Default constructor is callable. """
        j = Jungle()
        assert isinstance(j, Jungle)


class TestDesert:
    """ Tests for Desert class."""
    def test_constructor(self):
        """Default constructor is callable. """
        d = Desert()
        assert isinstance(d, Desert)


class TestMountainAndOcean:
    """ Tests for MountainAndOcean class."""
    def test_constructor(self):
        """Default constructor is callable. """
        p = MountainAndOcean()
        assert isinstance(p, MountainAndOcean)