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
                for animal in cell.animals:
                    species = type(animal).__name__
                    if species == 'Herbivore':
                        p = animal.prob_procreation(cell.total_herbivores)
                    if species == 'Carnivore':
                        p = animal.prob_procreation(cell.total_carnivores)

                    if np.random.choice(2, p=[1-p, p]):
                        weight = animal.draw_birth_weight()
                        self.add_population([{'loc': loc,
                                              'pop': {
                                                     'species': species,
                                                     'age': 0,
                                                     'weight': weight}}])

    def migration(self):
        for loc, cell in self.island_map.items():
            if cell.animal_can_enter:
                for animal in cell.animals:
                    animal_list = []
                    if animal.prob_migration:
                        new_loc = self.choose_cell(loc, type(animal).__name__)
                        self.island_map[new_loc].animals.append(animal)
                        animal_list.append(animal)
                    cell.animals.remove(animal_list)

    def choose_cell(self, loc, species):
        """ Returns cooridnates of chosen cell to migrate to.
        :return: choice
        """
        x, y = loc
        cell_left = (x, y-1)
        cell_right = (x, y+1)
        cell_up = (x-1, y)
        cell_down = (x+1, y)
        locations = [cell_left, cell_right, cell_up, cell_down]

        if species == 'Herbivore':
            calculate_propensities_herb = self.propensity_calculator('Herbivore')
            propensities = calculate_propensities_herb(locations)

        if species == 'Carnivore':
            calculate_propensities_carn = self.propensity_calculator('Carnivore')
            propensities = calculate_propensities_carn(locations)

        sum_propensities = sum(propensities)
        pl = propensities[0] / sum_propensities * propensities[0]
        pr = propensities[1] / sum_propensities * propensities[1]
        pu = propensities[2] / sum_propensities * propensities[2]
        pd = propensities[3] / sum_propensities * propensities[3]

        choice = np.random.choice(locations, p=[pl, pr, pu, pd])
        return choice

    def propensity_calculator(self, species):
        propensities = []
        if species == 'Herbivore':
            def calculator(locations):
                for cell in locations:
                    propensities.append(self.island_map[cell].propensity_migration_herb)
                return propensities
            return calculator

        if species == 'Carnivore':
            def calculator(locations):
                for cell in locations:
                    propensities.append(self.island_map[cell].propensity_migration_carn)
                return propensities
            return calculator

    def probability_migrate(self):
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
                    self.island_map[location].animals.append(Herbivore(age, weight))
                if species == 'Carnivore':
                    self.island_map[location].animals.append(Carnivore(age, weight))
