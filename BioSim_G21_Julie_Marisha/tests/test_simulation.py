# -*- coding: utf-8 -*-

"""
Tests for classes in cell.py using pytest.
"""

__author__ = 'Julie Forrisdal', 'Marisha Gnanaseelan'
__email__ = 'juforris@nmbu.no', 'magn@nmbu.no'


from BioSim_G21_Julie_Marisha.src.biosim.simulation import BioSim


class TestBiosim:
    """Tests for class BioSim."""
    def test_year_before_first_simulation(self):
        """Year function return 0 if there has been no simulations. """
        d = BioSim()
        assert d.year == 0

    def test_default_num_animals(self):
        """Test that default number of animals before the first simulation
        is created correctly."""
        d = BioSim()
        assert d.num_animals == 190

    def test_num_animals_per_species(self):
        """Test that num_animals_per_species returns a dictionary."""
        d = BioSim()
        assert isinstance(d.num_animals_per_species, dict)

    def test_default_animal_distribution(self):
        """Default animal distribution in cells are created correctly."""
        sim1 = BioSim()
        data_frame = sim1.animal_distribution
        data_frame.set_index(["Row", "Col"], inplace=True)
        assert data_frame.loc[(10, 10)].Herbivore == 150
        assert data_frame.loc[(10, 10)].Carnivore == 40
