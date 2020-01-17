# -*- coding: utf-8 -*-

"""
Tests for classes in rossumoya.py using pytest.
"""

__author__ = 'Julie Forrisdal', 'Marisha Gnanaseelan'
__email__ = 'juforris@nmbu.no', 'magn@nmbu.no'

import pytest

from biosim.rossumoya import Rossumoya
from biosim.rossumoya import MigrationProbabilityCalculator
from biosim.animal import Herbivore, Carnivore


class TestMigrationProbabilityCalculator:
    """Tests for class MigrationProbabilityCalculator."""

    @pytest.fixture(autouse=True)
    def create_calculator(self):
        self.loc = (2, 2)
        self.map = Rossumoya.make_geography_coordinates(Rossumoya.default_map)
        Herbivore.set_parameters()
        Carnivore.set_parameters()
        self.calculator_herb = MigrationProbabilityCalculator(
            self.loc, self.map, "Herbivore"
        )
        self.calculator_carn = MigrationProbabilityCalculator(
            self.loc, self.map, "Carnivore"
        )

    def test_constructor_callable(self):
        """MigrationProbabilityCalculator is callable. """
        assert isinstance(self.calculator_herb, MigrationProbabilityCalculator)
        assert isinstance(self.calculator_carn, MigrationProbabilityCalculator)

    def test_propensity_herb(self):
        """propensity_herb() method returns a list."""
        assert isinstance(self.calculator_herb.propensity_herb, list)

    def test_propensity_herb_setter(self):
        """Propensity for Herbivore can be set."""
        self.calculator_herb.propensity_herb = 4
        assert self.calculator_herb._propensity_herb == 4

    def test_propensity_carn(self):
        """propensity_carns() method returns a list."""
        assert isinstance(self.calculator_carn.propensity_carn, list)

    def test_propensity_carn_setter(self):
        """Propensity for Carnivore can be set."""
        self.calculator_carn.propensity_carn = 8
        assert self.calculator_carn._propensity_carn == 8

    def test_probabilities(self):
        """Property probabilities() returns a tuple and a list."""
        assert isinstance(self.calculator_herb.probabilities, (tuple, list))
        assert isinstance(self.calculator_carn.probabilities, (tuple, list))

    def test_probabilities_setter(self):
        """Probabilities can be set."""
        self.calculator_herb.probabilities = 0.2
        assert self.calculator_herb._probabilities == 0.2

        self.calculator_carn.probabilities = 1
        assert self.calculator_carn._probabilities == 1

    def test_probabilities_return_coordinates(self):
        """Property probabilities() returns correct coordinates for
        neighbouring cell of (2, 2)."""
        coordinates, probabilities = self.calculator_herb.probabilities
        assert coordinates == [(2, 1), (2, 3), (1, 2), (3, 2)]

        coordinates, probabilities = self.calculator_carn.probabilities
        assert coordinates == [(2, 1), (2, 3), (1, 2), (3, 2)]

    def test_probabilities_return_probabilities(self):
        """Property probabilities() returns correct probabilities for three
         identical Savannah cells and one Ocean cell as neighbouring cells."""
        coordinates, probabilities = self.calculator_herb.probabilities
        sum_probabilities = sum(probabilities)
        assert sum_probabilities == 1
        assert probabilities[0] == pytest.approx(0.333, rel=1e-2)
        assert probabilities[1] == pytest.approx(0.333, rel=1e-2)
        assert probabilities[2] == 0.0
        assert probabilities[3] == pytest.approx(0.333, rel=1e-2)

        coordinates, probabilities = self.calculator_carn.probabilities
        sum_probabilities = sum(probabilities)
        assert sum_probabilities == 1
        assert probabilities[0] == pytest.approx(0.333, rel=1e-2)
        assert probabilities[1] == pytest.approx(0.333, rel=1e-2)
        assert probabilities[2] == 0.0
        assert probabilities[3] == pytest.approx(0.333, rel=1e-2)

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

    def test_value_error_check_map_input(self):
        """Test that ValueError is raised for check_map_input"""
        with pytest.raises(ValueError):
            island_map_string = "OOOO\nOAO\nOOOO"
            self.rossumoya.check_map_input(island_map_string)
        with pytest.raises(ValueError):
            island_map_string = "OOOO\nOKJO\nOOOO"
            self.rossumoya.check_map_input(island_map_string)
        with pytest.raises(ValueError):
            island_map_string = "OOOJ\nOJSO\nOOOO"
            self.rossumoya.check_map_input(island_map_string)

    def test_geography_coordinates_method(self):
        """make_geography_coordinates can be called."""
        self.rossumoya.make_geography_coordinates(self.rossumoya.default_map)

    def test_make_geography_coordinates(self):
        """make_geography_coordinates() method returns a dictionary. """
        island_map = "OOO\nOJO\nOOO"
        assert isinstance(
            self.rossumoya.make_geography_coordinates(island_map), dict
        )

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

    def test_procreation(self):
        """procreation() method is callable."""
        self.rossumoya.add_offspring(Herbivore(), (2, 2))
        self.rossumoya.procreation()

    def test_add_offspring(self):
        """add_offspring() method is callable."""
        self.rossumoya.add_offspring(Carnivore(), (4, 6))

    def test_choose_cell(self):
        """choose_cell() method is callable."""
        assert isinstance(
            self.rossumoya.choose_cell((5, 7), "Herbivore"), tuple
                          )

    def test_migration_callable(self):
        """Migration method is callable"""
        self.rossumoya.migration()

    def test_death_callable(self):
        """death() method is callable. """
        self.rossumoya.death()

    def test_single_year_callable(self):
        """single_year() method is callable. """
        self.rossumoya.single_year()

    def test_map_axis(self):
        axis = self.rossumoya.map_axis()
        assert axis == (20, 12)
