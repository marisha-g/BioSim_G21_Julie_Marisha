# -*- coding: utf-8 -*-

"""
Tests for classes in cell.py using pytest.
"""

__author__ = 'Julie Forrisdal', 'Marisha Gnanaseelan'
__email__ = 'juforris@nmbu.no', 'magn@nmbu.no'


from biosim.simulation import BioSim
from biosim.animal import Herbivore, Carnivore
import pytest


class TestBiosim:
    """Tests for class BioSim."""
    @pytest.fixture(autouse=True)
    def create_sim(self):
        self.biosim = BioSim()
        self.population = population = [
        {
            "loc": (10, 10),
            "pop": [{"species": "Herbivore", "age": 5, "weight": 20}
                    for _ in range(150)],
        }
    ]

    def test_year_before_first_simulation(self):
        """Year property returns 0 before simulation. """
        assert self.biosim.year == 0

    def test_default_num_animals(self):
        """num_animals property returns
        default value before simulation."""
        assert self.biosim.num_animals == 190

    def test_num_animals_per_species(self):
        """num_animals_per_species returns a dictionary."""
        assert isinstance(self.biosim.num_animals_per_species, dict)

    def test_default_animals_per_species(self):
        """animal_per_species property returns default values
        before simulation."""
        num_animals_per_species = {'Herbivore': 150,
                                   'Carnivore': 40}
        assert self.biosim.num_animals_per_species == num_animals_per_species

    def test_default_animal_distribution(self):
        """Default animal distribution in cells are created correctly."""
        data_frame = self.biosim.animal_distribution
        data_frame.set_index(["Row", "Col"], inplace=True)
        assert data_frame.loc[(10, 10)].Herbivore == 150
        assert data_frame.loc[(10, 10)].Carnivore == 40

    def test_set_animal_parameters_callabe(self):
        """set_animal_parameters method can be called."""
        params = {}
        self.biosim.set_animal_parameters('Herbivore', params)

    def test_set_animal_parameters(self):
        """set_animal_parameters method changes parameters of animal class
        correctly."""
        params1 = {'gamma': 0.5}
        params2 = {'xi': 0.4}
        self.biosim.set_animal_parameters('Herbivore', params1)
        self.biosim.set_animal_parameters('Carnivore', params2)
        assert Herbivore.gamma == 0.5
        assert Carnivore.xi == 0.4

    def test_add_population(self):
        """ add_population method can be called."""
        self.biosim.add_population(self.population)