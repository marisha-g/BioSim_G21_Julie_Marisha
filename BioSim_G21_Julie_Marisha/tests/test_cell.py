# -*- coding: utf-8 -*-

"""
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


class TestSavannah:
    """ Tests for Savannah class."""
    def test_constructor(self):
        """Default constructor is callable. """
        s = Savannah()
        assert isinstance(s, Savannah)


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