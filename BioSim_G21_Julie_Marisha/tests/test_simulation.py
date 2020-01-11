# -*- coding: utf-8 -*-

"""
Tests for classes in cell.py using pytest.
"""

__author__ = 'Julie Forrisdal', 'Marisha Gnanaseelan'
__email__ = 'juforris@nmbu.no', 'magn@nmbu.no'


from BioSim_G21_Julie_Marisha.src.biosim.simulation import BioSim
import pandas as pd


class TestBiosim:
    def test_default_animal_distribution(self):
        """Default animal distribution in cells are created correctly"""
        sim1 = BioSim()
        data_frame = sim1.animal_distribution
        num_herbivore_list = data_frame['total_herbivores'][[(10, 10)]]
        assert num_herbivore_list.to_list() == [150]

        num_carnivore_list = data_frame['total_carnivores'][[(10, 10)]]
        assert num_carnivore_list.to_list() == [40]


