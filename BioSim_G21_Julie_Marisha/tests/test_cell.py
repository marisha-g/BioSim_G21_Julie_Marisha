# -*- coding: utf-8 -*-

"""
Tests for classes in cell.py using pytest.
"""

__author__ = 'Julie Forrisdal', 'Marisha Gnanaseelan'
__email__ = 'juforris@nmbu.no', 'magn@nmbu.no'

from src.biosim.cell import Cell, Savannah, Jungle, Desert, MountainAndOcean
from BioSim_G21_Julie_Marisha.src.biosim.animal import Herbivore, Carnivore

import pytest


class TestCell:
    """Tests for Cell class."""
    @pytest.fixture(autouse=True)
    def create_cell(self):
        self.cell = Cell()

    def test_constructor(self):
        """Default constructor is callable."""
        assert isinstance(self.cell, Cell)

    def test_default_parameters(self):
        """Default parameters are set correctly."""
        assert self.cell.fodder_in_cell == 0
        assert self.cell.animal_can_enter is True
        assert self.cell.animals == []

    def test_fodder_first_year(self):
        """ Tests that fodder_first_year method is callable and
         changes fodder_in_cell attribute."""
        assert self.cell.fodder_in_cell == 0
        self.cell.fodder_first_year(10)
        assert self.cell.fodder_in_cell == 10

    def test_regrow_fodder(self):
        """ Test regrow_fodder method is callable and regrows fodder
        according to f_max."""
        self.cell.f_max = 10
        self.cell.regrow_fodder()
        assert self.cell.fodder_in_cell == 10

    def test_abundance_of_fodder_herbivores(self):
        """Abundance of fodder is equal to 0 when there is no fodder in cell."""
        Herbivore.set_parameters()
        self.cell.fodder_in_cell = 0
        assert self.cell.abundance_of_fodder_herbivores == 0

    def test_abundance_of_fodder_carnivores(self):
        """Abundance of fodder is equal to 0 when there is no Herbivore
        in cell. """
        Carnivore.set_parameters()
        assert self.cell.abundance_of_fodder_carnivores == 0


    def test_list_of_sorted_herbivores(self):
        pass




class TestSavannah:
    """ Tests for Savannah class."""

    @pytest.fixture(autouse=True)
    def create_cell(self):
        self.s = Savannah()

    def test_constructor(self):
        """Default constructor is callable. """
        assert isinstance(self.s, Savannah)

    def test_classmethod_set_parameters(self):
        """Classmethod set_parameters is callable,
         and default parameters are set."""
        self.s.set_parameters()
        assert Savannah.f_max == 300.0
        assert Savannah.alpha == 0.3

    def test_value_error(self):
        """Negative parameters raises ValueError."""
        with pytest.raises(ValueError):
            Savannah.set_parameters(f_max=-100)
            Savannah.set_parameters(alpha=-0.3)


class TestJungle:
    """ Tests for Jungle class."""
    @pytest.fixture(autouse=True)
    def create_cell(self):
        self.j = Jungle()

    def test_constructor(self):
        """Default constructor is callable. """
        assert isinstance(self.j, Jungle)

    def test_default_parameters(self):
        assert self.j.f_max == 800.0
        assert self.j.animal_can_enter is True
        assert self.j.animals == []
        assert self.j.fodder_in_cell == self.j.f_max

    def test_classmethod_set_parameters(self):
        """Classmethod set_parameters is callable,
         and default parameters are set."""
        assert Jungle.f_max == 800.0

    def test_value_error(self):
        """Negative parameters raises ValueError."""
        with pytest.raises(ValueError):
            Jungle.set_parameters(f_max=-100)


class TestDesert:
    """ Tests for Desert class."""
    @pytest.fixture(autouse=True)
    def create_cell(self):
        self.d = Desert()

    def test_constructor(self):
        """Default constructor is callable. """
        assert isinstance(self.d, Desert)

    def test_parameters_desert(self):
        """Test that parameters for subclass Desert are correct."""
        assert self.d.fodder_in_cell == 0
        assert self.d.f_max == 0
        assert self.d.animal_can_enter is True


class TestMountainAndOcean:
    """ Tests for MountainAndOcean class."""
    @pytest.fixture(autouse=True)
    def create_cell(self):
        self.mo = MountainAndOcean()

    def test_constructor(self):
        """Default constructor is callable. """
        assert isinstance(self.mo, MountainAndOcean)

    def test_parameters_mountain_and_ocean(self):
        """Test that parameters for subclass MountainAndOcean are correct."""
        assert self.mo.fodder_in_cell == 0
        assert self.mo.f_max == 0
        assert self.mo.animal_can_enter is False
