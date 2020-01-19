# -*- coding: utf-8 -*-

"""
Advanced tests for BioSim using pytest.
"""

__author__ = 'Julie Forrisdal', 'Marisha Gnanaseelan'
__email__ = 'juforris@nmbu.no', 'magn@nmbu.no'

import pytest
from biosim.animal import Herbivore
from biosim.rossumoya import MigrationProbabilityCalculator
from biosim.simulation import BioSim


class TestAdvanced:
    @pytest.fixture(autouse=True)
    def create_sim(self):
        """
        Setup for tests.
        """
        self.biosim = BioSim()
        self.population = [
            {
                "loc": (2, 2),
                "pop": [{"species": "Herbivore", "age": 5, "weight": 20}
                        for _ in range(150)],
            }
        ]

    def test_all_animals_migrate(self):
        """
        Test that no animals are left in the cell after simulating
        one year when probability to migrate is set to 1.
        """
        island_map = """OOOOO\nOOJOO\nOJJJO\nOOJOO\nOOOOO"""

        sim1 = BioSim(island_map=island_map, ini_pop=self.population)
        Herbivore.prob_migration = 1
        sim1.simulate(num_years=1, vis_years=1)
        cell = sim1.rossumoya.island_map[(2, 2)]
        assert cell.total_population == 0

    def test_all_animals_migrate_right(self):
        """
        Test that all animals migrate to the right neighbour cell
        when simulating one year with probability to migrate set to 1,
        and probability to choose the right hand cell is set to one.
        """
        island_map = """OOOOO\nOOJOO\nOJSJO\nOOJOO\nOOOOO"""
        sim1 = BioSim(island_map=island_map, ini_pop=self.population)
        Herbivore.prob_migration = 1
        MigrationProbabilityCalculator.probabilities = [0, 1, 0, 0]
        sim1.simulate(num_years=1, vis_years=10)

        cell_left = sim1.rossumoya.island_map[(2, 1)]
        cell_up = sim1.rossumoya.island_map[(1, 2)]
        cell_down = sim1.rossumoya.island_map[(3, 2)]

        assert cell_left.total_population == 0
        assert cell_up.total_population == 0
        assert cell_down.total_population == 0

    def test_animals_do_not_migrate_diagonally(self):
        """
        When the probability to migrate is set to one for all animals
        and one year is simulated, no animals stay in the initial cell,
        and no animals migrate to the diagonally displaced cells.
        """
        island_map = """OOOOO\nOJJJO\nOJJJO\nOJJJO\nOOOOO"""
        ini_pop = [{
            "loc": (2, 2),
            "pop": [{"species": "Herbivore", "age": 5, "weight": 20}
                    for _ in range(150)],
        }]
        sim1 = BioSim(island_map=island_map, ini_pop=ini_pop)
        Herbivore.prob_migration = 1
        sim1.simulate(num_years=1, vis_years=10)

        initial_cell = sim1.rossumoya.island_map[(2, 2)]
        diagonal_cell_1 = sim1.rossumoya.island_map[(1, 1)]
        diagonal_cell_2 = sim1.rossumoya.island_map[(1, 3)]
        diagonal_cell_3 = sim1.rossumoya.island_map[(3, 1)]
        diagonal_cell_4 = sim1.rossumoya.island_map[(3, 3)]

        assert initial_cell.total_population == 0
        assert diagonal_cell_1.total_population == 0
        assert diagonal_cell_2.total_population == 0
        assert diagonal_cell_3.total_population == 0
        assert diagonal_cell_4.total_population == 0
