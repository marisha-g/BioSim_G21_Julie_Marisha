# -*- coding: utf-8 -*-

"""
"""
import numpy as np

from BioSim_G21_Julie_Marisha.src.biosim.animal import Herbivore, Carnivore
from BioSim_G21_Julie_Marisha.src.biosim.cell import Savannah, Jungle, Desert, MountainAndOcean

__author__ = 'Julie Forrisdal', 'Marisha Gnanaseelan'
__email__ = 'juforris@nmbu.no', 'magn@nmbu.no'

import textwrap


class Rossumoya:
    """
    Island in Biosim.
    """
    default_ini_herbs = [
        {
            "loc": (10, 10),
            "pop": [{"species": "Herbivore", "age": 5, "weight": 20}
                    for _ in range(150)],
        }
    ]
    default_ini_carns = [
        {
            "loc": (10, 10),
            "pop": [
                {"species": "Carnivore", "age": 5, "weight": 20}
                for _ in range(40)
            ],
        }
    ]
    default_map = """\
                          OOOOOOOOOOOOOOOOOOOOO
                          OOOOOOOOSMMMMJJJJJJJO
                          OSSSSSJJJJMMJJJJJJJOO
                          OSSSSSSSSSMMJJJJJJOOO
                          OSSSSSJJJJJJJJJJJJOOO
                          OSSSSSJJJDDJJJSJJJOOO
                          OSSJJJJJDDDJJJSSSSOOO
                          OOSSSSJJJDDJJJSOOOOOO
                          OSSSJJJJJDDJJJJJJJOOO
                          OSSSSJJJJDDJJJJOOOOOO
                          OOSSSSJJJJJJJJOOOOOOO
                          OOOSSSSJJJJJJJOOOOOOO
                          OOOOOOOOOOOOOOOOOOOOO"""

    default_map = textwrap.dedent(default_map)

    cell_code = {"S": Savannah, "J": Jungle, "D": Desert, "O": MountainAndOcean, "M": MountainAndOcean}

    def __init__(self, island_map=None, ini_pop=None):
        if island_map is None:
            island_map = Rossumoya.default_map
            self.island_map = self.make_geography_coordinates(island_map)

        else:
            if self.check_map_input(island_map):
                self.island_map = self.make_geography_coordinates(island_map)

        if ini_pop is None:
            self.add_population(Rossumoya.default_ini_herbs)
            self.add_population(Rossumoya.default_ini_carns)
        else:
            self.add_population(ini_pop)

        # Set all parameters to default
        # BioSim.set_landscape_parameters and
        # Biosim.set_animal_parameters methods will override if called upon.
        Savannah.set_parameters()
        Jungle.set_parameters()
        Herbivore.set_parameters()
        Carnivore.set_parameters()

    @staticmethod
    def check_map_input(island_map):
        """
        Checks if the input map is compatible.
        :param island_map: str
        :return: bool
        """
        island_map_list = island_map.split("\n")
        length_row = len(island_map_list[0])
        n = len(island_map_list)

        for row in island_map_list:
            if len(row) != length_row:
                raise ValueError("Inconsistent line length.")

        for row in island_map_list:
            for cell in row:
                if cell not in Rossumoya.cell_code:
                    raise ValueError("Invalid landscape type.")

        for cell in island_map_list[0]:
            if cell != "O":
                raise ValueError("Non-ocean boundary.")
        for cell in island_map_list[n - 1]:
            if cell != "O":
                raise ValueError("Non-ocean boundary.")
        for row in island_map_list:
            num_cells = len(row)
            if row[0] != "O":
                raise ValueError("Non-ocean boundary.")
            if row[num_cells - 1] != "O":
                raise ValueError("Non-ocean boundary.")
        return True

    @staticmethod
    def make_geography_coordinates(input_map):
        """
        Making a dictionary with coordinates as keys and lists with cell
        types "O, M, S, J, D" and fodder in cell as values.

        :return: dict
        """
        list_island_map = input_map.split('\n')
        geography_map = {}
        for i_index, line in enumerate(list_island_map):
            for j_index, cell in enumerate(line):
                geography_map[(i_index, j_index)] = Rossumoya.cell_code[cell]()
        return geography_map

    def procreation(self):
        for loc, cell in self.island_map.items():
            if cell.animal_can_enter:
                herb_pop = len(cell.herbivores)
                carn_pop = len(cell.carnivores)

                if herb_pop > 1:
                    for herbivore in cell.herbivores:
                        p = herbivore.prob_procreation()
                        if np.random.choice(2, p=[1-p, p]):
                            weight = herbivore.draw_birth_weight()
                            self.add_population([{'loc': loc,
                                                  'pop': {'species': Herbivore,
                                                          'age': 0,
                                                          'weight': weight}}])

                if carn_pop > 1:
                    for carnivore in cell.carnivores:
                        p = carnivore.prob_procreation()
                        if np.random.choice(2, p=[1-p, p]):
                            weight = carnivore.draw_birth_weight()
                            self.add_population([{'loc': loc,
                                                  'pop': {'species': Carnivore,
                                                          'age': 0,
                                                          'weight': weight}}])

    def migration_herbs(self):
        for loc, cell in self.island_map.items():
            if cell.animal_can_enter:
                for herbivore in cell.herbivores:
                    if herbivore.prob_migration:
                        new_loc = self.choose_cell(loc, 'herbivore')
                        self.island_map[new_loc].herbivores.append(herbivore)
                        self.island_map[loc].herbivores.remove(herbivore)

    def migration_carnivores(self):
        if cell.animal_can_enter:
            for loc, cell in self.island_map.items():
                for carnivore in cell.carnivores:
                    if carnivore.prob_migration:
                        new_loc = self.choose_cell(loc, 'carnivore')
                        self.island_map[new_loc].herbivores.append(carnivore)
                        self.island_map[loc].carnivores.remove(carnivore)

    def choose_cell(self, loc, species):
        pass

    def add_population(self, population):
        """
        Add a population to the island

        :param population: List of dictionaries specifying population
        """
        for cell_dict in population:
            location = cell_dict['loc']

            for pop_dict in cell_dict['pop']:
                species = pop_dict['species']
                age = pop_dict['age']
                weight = pop_dict['weight']
                if species == 'Herbivore':
                    self.island_map[location].carnivores.append(Herbivore(age, weight))
                if species == 'Carnivore':
                    self.island_map[location].carnivores.append(Carnivore(age, weight))
