# -*- coding: utf-8 -*-

"""
Tests for classes in cell.py using pytest.
"""

__author__ = 'Julie Forrisdal', 'Marisha Gnanaseelan'
__email__ = 'juforris@nmbu.no', 'magn@nmbu.no'

from src.biosim.rossumoya import Rossumoya
import textwrap
import pytest



class TestRossumoya:
    """Tests for class Rossumoya."""

    def test_constructor_default(self):
        """Default constructor callable."""
        c = Rossumoya()
        assert isinstance(c, Rossumoya)

    def test_island_map(self):
        """Checks if the island_map is a dictionary."""
        c = Rossumoya()
        assert isinstance(c.island_map, dict)

    def test_geography_coordinates_method(self):
        """make_geography_coordinates can be called."""
        c = Rossumoya()
        c.make_geography_coordinates(Rossumoya.default_map)

    def test_add_population_method(self):
        """add_population can be called."""
        c = Rossumoya()
        c.add_population(Rossumoya.default_ini_herbs)
