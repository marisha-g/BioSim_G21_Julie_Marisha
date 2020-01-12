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

    def test_classmethod_set_parameters(self):
        """Classmethod set_parameters is callable,
         and default parameters are set."""
        Savannah.set_parameters()
        assert Savannah.f_max == 300.0
        assert Savannah.alpha == 0.3

    def test_value_error(self):
        """Negative parameters raises ValueError."""
        with pytest.raises(ValueError):
            Savannah.set_parameters(f_max=-100)
            Savannah.set_parameters(alpha=-0.3)


class TestJungle:
    """ Tests for Jungle class."""
    def test_constructor(self):
        """Default constructor is callable. """
        j = Jungle()
        assert isinstance(j, Jungle)

    def test_classmethod_set_parameters(self):
        """Classmethod set_parameters is callable,
         and default parameters are set."""
        Jungle.set_parameters()
        assert Jungle.f_max == 800.0

    def test_value_error(self):
        """Negative parameters raises ValueError."""
        with pytest.raises(ValueError):
            Jungle.set_parameters(f_max=-100)


class TestDesert:
    """ Tests for Desert class."""
    def test_constructor(self):
        """Default constructor is callable. """
        d = Desert()
        assert isinstance(d, Desert)

    def test_parameters_desert(self):
        """Test that parameters for subclass Desert are correct."""
        d = Desert()
        assert d.fodder_in_cell == 0
        assert d.f_max == 0


class TestMountainAndOcean:
    """ Tests for MountainAndOcean class."""
    def test_constructor(self):
        """Default constructor is callable. """
        p = MountainAndOcean()
        assert isinstance(p, MountainAndOcean)

    def test_parameters_mountain_and_ocean(self):
        """Test that parameters for subclass MountainAndOcean are correct."""
        mo = MountainAndOcean()
        assert mo.fodder_in_cell == 0
        assert mo.f_max == 0
        assert mo.animal_can_enter is False