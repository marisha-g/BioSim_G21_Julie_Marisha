# -*- coding: utf-8 -*-

"""
Tests for classes in cell.py using pytest.
"""

__author__ = 'Julie Forrisdal', 'Marisha Gnanaseelan'
__email__ = 'juforris@nmbu.no', 'magn@nmbu.no'

from src.biosim.rossumoya import Rossumoya
from BioSim_G21_Julie_Marisha.src.biosim.rossumoya import MigrationProbabilityCalculator
from BioSim_G21_Julie_Marisha.src.biosim.animal import Herbivore, Carnivore
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

    def test_propensity_herb(self):
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


