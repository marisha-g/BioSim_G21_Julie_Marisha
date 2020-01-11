# -*- coding: utf-8 -*-

"""
Tests for classes in cell.py using pytest.
"""

__author__ = 'Julie Forrisdal', 'Marisha Gnanaseelan'
__email__ = 'juforris@nmbu.no', 'magn@nmbu.no'


from BioSim_G21_Julie_Marisha.src.biosim.simulation import BioSim

class TestBiosim:
    def test_default_animal_distribution(self):
        sim1 = BioSim()
        data_frame = sim1.animal_distribution
        print(data_frame['total_herbivores'][[(10, 10)]])
