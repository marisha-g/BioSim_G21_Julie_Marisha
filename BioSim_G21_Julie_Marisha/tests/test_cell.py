# -*- coding: utf-8 -*-

"""
Tests for classes in cell.py using pytest.
"""

__author__ = 'Julie Forrisdal', 'Marisha Gnanaseelan'
__email__ = 'juforris@nmbu.no', 'magn@nmbu.no'

from biosim.cell import BaseCell, Savannah, Jungle, Desert, Mountain, Ocean
from biosim.animal import Herbivore, Carnivore
import pytest


class TestCell:
    """Tests for Cell class."""
    @pytest.fixture(autouse=True)
    def create_cell(self):
        self.cell = BaseCell()

    def test_constructor(self):
        """Default constructor is callable."""
        assert isinstance(self.cell, BaseCell)

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

    def test_add_population(self):
        """Test that population is added."""
        pop_list = [{"species": "Herbivore", "age": 5, "weight": 20} for _ in range(150)]
        num_animals_1 = len(self.cell.animals)
        self.cell.add_population(pop_list)
        num_animals_2 = len(self.cell.animals)
        assert num_animals_2 > num_animals_1
        assert num_animals_1 == 0
        assert num_animals_2 == 150

    def test_remove_dead_animal(self):
        """remove_dead_animal method is callable and removes
         the dead animal from the cell."""
        animal = Carnivore()
        self.cell.animals.append(animal)
        self.cell.remove_dead_animals(animal)
        assert self.cell.total_carnivores == 0

    def test_list_of_sorted_herbivores(self):
        """list_of_sorted_herbivores property is callable and sorts the
        herbivores in descending order by fitness.
        """
        pop_list = [{"species": "Herbivore", "age": 5, "weight": 20} for _ in range(150)]
        Herbivore.set_parameters()
        self.cell.add_population(pop_list)
        sorted_list = self.cell.list_of_sorted_herbivores
        assert all(sorted_list[i].fitness >= sorted_list[i+1].fitness for
                   i in range(len(sorted_list)-1))

    def test_list_of_sorted_carnivores(self):
        """list_of_sorted_carnivores property is callable and sorts the
        carnivores in descending order by fitness.
        """
        pop_list = [{"species": "Carnivore", "age": 5, "weight": 20} for _ in range(150)]
        Carnivore.set_parameters()
        self.cell.add_population(pop_list)
        sorted_list = self.cell.list_of_sorted_carnivores
        assert all(sorted_list[i].fitness >= sorted_list[i+1].fitness for
                   i in range(len(sorted_list)-1))


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


class TestMountain:
    """ Tests for Mountain class."""
    @pytest.fixture(autouse=True)
    def create_cell(self):
        self.m = Mountain()

    def test_constructor(self):
        """Default constructor is callable. """
        assert isinstance(self.m, Mountain)

    def test_parameters_mountain_and_ocean(self):
        """Test that parameters for subclass Mountain are correct."""
        assert self.m.fodder_in_cell == 0
        assert self.m.f_max == 0
        assert self.m.animal_can_enter is False


class TestOcean:
    """ Tests for Ocean class."""
    @pytest.fixture(autouse=True)
    def create_cell(self):
        self.o = Ocean()

    def test_constructor(self):
        """Default constructor is callable. """
        assert isinstance(self.o, Ocean)

    def test_parameters_mountain_and_ocean(self):
        """Test that parameters for subclass Ocean are correct."""
        assert self.o.fodder_in_cell == 0
        assert self.o.f_max == 0
        assert self.o.animal_can_enter is False
