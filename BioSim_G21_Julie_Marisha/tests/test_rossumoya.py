# -*- coding: utf-8 -*-

"""
Tests for classes in cell.py using pytest.
"""

__author__ = 'Julie Forrisdal', 'Marisha Gnanaseelan'
__email__ = 'juforris@nmbu.no', 'magn@nmbu.no'

from biosim.rossumoya import Rossumoya
from biosim.rossumoya import MigrationProbabilityCalculator
from biosim.animal import Herbivore, Carnivore
import pytest


class TestMigrationProbabilityCalculator:
    """Tests for class MigrationProbabilityCalculator."""

    @pytest.fixture(autouse=True)
    def create_calculator(self):
        self.loc = (2, 2)
        self.map = Rossumoya.make_geography_coordinates(Rossumoya.default_map)
        Herbivore.set_parameters()
        Carnivore.set_parameters()
        self.species = "Herbivore"
        self.calculator = MigrationProbabilityCalculator(
            self.loc, self.map, self.species
        )

    def test_constructor_callable(self):
        """MigrationProbabilityCalculator is callable. """
        assert isinstance(self.calculator, MigrationProbabilityCalculator)

    def test_propensity_herb(self):
        """propensity_herb() method returns a list."""
        assert isinstance(self.calculator.propensity_herb(), list)

    def test_propensity_carns(self):
        """propensity_carns() method returns a list."""
        assert isinstance(self.calculator.propensity_carns(), list)

    def test_probability(self):
        """probability() method returns a tuple and a list."""
        assert isinstance(self.calculator.probability(), (tuple, list))


class TestRossumoya:
    """Tests for class Rossumoya."""

    @pytest.fixture(autouse=True)
    def create_rossumoya(self):
        self.rossumoya = Rossumoya()

    def test_constructor_default(self):
        """Default constructor callable."""
        assert isinstance(self.rossumoya, Rossumoya)

    def test_island_map(self):
        """Checks if the island_map is a dictionary."""
        assert isinstance(self.rossumoya.island_map, dict)

    def test_geography_coordinates_method(self):
        """make_geography_coordinates can be called."""
        self.rossumoya.make_geography_coordinates(self.rossumoya.default_map)

    def test_add_population_method(self):
        """add_population can be called."""
        self.rossumoya.add_population(self.rossumoya.default_ini_herbs)

    def test_value_error_for_add_population(self):
        """ValueError is raised when animal is put in invalid cell."""
        population = [
            {
                'loc': (1, 9),
                'pop': [{"species": "Carnivore", "age": 2, "weight": 20}]
            }
        ]
        with pytest.raises(ValueError):
            self.rossumoya.add_population(population)

    def test_value_error_check_map_input(self):
        """Test that ValueError is raised for check_map_input"""
        with pytest.raises(ValueError):
            island_map_string = "OOOO\nOAO\nOOOO"
            self.rossumoya.check_map_input(island_map_string)

            island_map_string = "OOOO\nOKJO\nOOOO"
            self.rossumoya.check_map_input(island_map_string)

            island_map_string = "OOOJ\nOJSO\nOOOO"
            self.rossumoya.check_map_input(island_map_string)

    def test_procreation(self):
        """procreation() method is callable. """
        self.rossumoya.add_offspring(Herbivore(), (2, 2))
        self.rossumoya.procreation()
        
    def test_add_offspring(self):
        """add_offspring() method is callable. """
        self.rossumoya.add_offspring(Carnivore(), (4, 6))

    def test_choose_cell(self):
        """choose_cell() method is callable. """
        assert isinstance(
            self.rossumoya.choose_cell((5, 7), "Herbivore"), tuple
                          )

    def test_death_callable(self):
        """death() method is callable. """
        self.rossumoya.death()

    def test_make_geography_coordinates(self):
        """make_geography_coordinates() method returns a dictionary. """
        island_map = "OOO\nOJO\nOOO"
        assert isinstance(
            self.rossumoya.make_geography_coordinates(island_map), dict
        )
