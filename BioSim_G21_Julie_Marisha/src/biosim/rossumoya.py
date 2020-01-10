# -*- coding: utf-8 -*-

"""
"""

__author__ = 'Julie Forrisdal', 'Marisha Gnanaseelan'
__email__ = 'juforris@nmbu.no', 'magn@nmbu.no'

import textwrap


class Rossumoya:
    """
    Island in Biosim.
    """
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

    def __init__(self, island_map, ini_pop):
        if island_map is None:
            self.island_map = BioSim.default_map
        if self.check_map_input(island_map):
            self.island_map = island_map
            self.island_map = self.make_geography_coordinates(self.island_map)

        if ini_pop is None:
            self.add_population(BioSim.default_ini_pop)
        else:
            self.add_population(ini_pop)

    @staticmethod
    def check_map_input(island_map):
        island_map_list = island_map.split("\n")
        length_row = len(island_map_list[0])
        n = len(island_map_list)

        for row in island_map_list:
            if len(row) != length_row:
                raise ValueError("Inconsistent line length.")

        for row in island_map_list:
            for cell in row:
                if cell not in BioSim.cell_code:
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

    def make_geography_coordinates(self, input_map):
        """
        Making a dictionary with coordinates as keys and lists with cell
        types "O, M, S, J, D" and fodder in cell as values.

        :return: dict
        """
        list_island_map = self.default_map.split('\n')
        geography_map = {}
        for i_index, line in enumerate(list_island_map):
            for j_index, cell in enumerate(line):
                geography_map[(i_index + 1, j_index + 1)] = {
                    "cell type": BioSim.cell_code[cell](),
                    "total pop": 0,
                    "Herbivores": [],
                    "Carnivores": [],
                }
        return geography_map

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
                    self.island_map[location]['Herbivores'].append(Herbivore(age, weight))
                if species == 'Carnivore':
                    self.island_map[location]['Carnivores'].append(Carnivore(age, weight))
