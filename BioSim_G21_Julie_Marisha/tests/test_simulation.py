# -*- coding: utf-8 -*-

"""
Tests for classes in cell.py using pytest.
"""

__author__ = 'Julie Forrisdal', 'Marisha Gnanaseelan'
__email__ = 'juforris@nmbu.no', 'magn@nmbu.no'


from biosim.simulation import BioSim
import pytest


class TestBiosim:
    """Tests for class BioSim."""
    @pytest.fixture(autouse=True)
    def create_sim(self):
        self.biosim = BioSim()

    def test_year_before_first_simulation(self):
        """Year property return 0 if there has been no simulations. """
        assert self.biosim.year == 0

    def test_default_num_animals(self):
        """Test that default number of animals before the first simulation
        is created correctly."""
        assert self.biosim.num_animals == 190

    def test_num_animals_per_species(self):
        """Test that num_animals_per_species returns a dictionary."""
        assert isinstance(self.biosim.num_animals_per_species, dict)

    def test_default_animal_distribution(self):
        """Default animal distribution in cells are created correctly."""
        data_frame = self.biosim.animal_distribution
        data_frame.set_index(["Row", "Col"], inplace=True)
        assert data_frame.loc[(10, 10)].Herbivore == 150
        assert data_frame.loc[(10, 10)].Carnivore == 40
