# -*- coding: utf-8 -*-

"""
"""
import numpy as np

from BioSim_G21_Julie_Marisha.src.biosim.animal import Herbivore, Carnivore
from BioSim_G21_Julie_Marisha.src.biosim.cell import Savannah, \
    Jungle, Desert, MountainAndOcean

__author__ = 'Julie Forrisdal', 'Marisha Gnanaseelan'
__email__ = 'juforris@nmbu.no', 'magn@nmbu.no'

import textwrap


class PropensityCalculator:
    def __init__(self, locations, island_map):
        """
        Constructor initiate PropensityCalculator
        :param locations: List of the four neighbouring cells,
         in this exact order: [Left, Right, Up, Down].
        :type: list
        :param island_map: Dictionary with all cells and their locations
        :type: dict
        """
        self.locations = locations
        self.island_map = island_map

    def herbs(self):
        """
        Calculate the propensities of the four cells for herbivores.
        :return: propensities: List with the four neighbouring cells
         corresponding propensities.
        :type: list
        """
        propensities = []
        for cell in self.locations:
            cell = self.island_map[cell]
            propensities.append(cell.propensity_migration_herb)
        return propensities

    def carns(self):
        """
        Calculate the propensities of the four cells for carnivores.

        :return: propensities: List with the four neighbouring cells
         corresponding propensities.
        :type: list
        """
        propensities = []
        for cell in self.locations:
            cell = self.island_map[cell]
            propensities.append(cell.propensity_migration_carn)
        return propensities


class Rossumoya:
    """
    Island class in simulation BioSim.
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

    cell_code = {"S": Savannah,
                 "J": Jungle,
                 "D": Desert,
                 "O": MountainAndOcean,
                 "M": MountainAndOcean}

    def __init__(self, island_map=None, ini_pop=None):
        """
        Constructor initiate Rossumoya class instance.
        :param island_map: Multiline string indicating geography of the island.
        :type: str
        :param ini_pop: List of dictionaries indicating
         initial population and location.
        :type: list
        """
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
        Raises ValueError if input map is not compatible and does not
        follows restrictions for the geography of the island. Returns True
        otherwise.
        :param island_map: Multiline string indicating the geography
         of the island.
        :type: str
        :return: True
        :type: bool
        """
        # All lines must be of same length
        island_map_list = island_map.split("\n")
        length_first_row = len(island_map_list[0])
        for row in island_map_list:
            if len(row) != length_first_row:
                raise ValueError("Inconsistent line length.")

        # All cells must be of valid landscape type
        for row in island_map_list:
            for cell in row:
                if cell not in Rossumoya.cell_code:
                    raise ValueError("Invalid landscape type.")

        # All outer cells must be of type Ocean
        for cell in island_map_list[0]:
            if cell != "O":
                raise ValueError("Non-ocean boundary.")
        for cell in island_map_list[-1]:
            if cell != "O":
                raise ValueError("Non-ocean boundary.")
        for row in island_map_list:
            if row[0] != "O":
                raise ValueError("Non-ocean boundary.")
            if row[-1] != "O":
                raise ValueError("Non-ocean boundary.")
        return True

    def add_population(self, population):
        """
        Add population to the island.
        :param population: List of dictionaries specifying
         population and locations.
        :type: list
        """
        for cell_dict in population:
            location = cell_dict['loc']

            for pop_dict in cell_dict['pop']:
                species = pop_dict['species']
                age = pop_dict['age']
                weight = pop_dict['weight']
                if species == 'Herbivore':
                    self.island_map[location].animals.append(
                        Herbivore(age, weight)
                    )
                if species == 'Carnivore':
                    self.island_map[location].animals.append(
                        Carnivore(age, weight)
                    )

    def procreation(self):
        """
        If an animal gives birth, a new animal of the same species with
        age zero and weight drawn from draw_birth_weight is added to the same
        cell.
        """
        for loc, cell in self.island_map.items():
            if cell.animal_can_enter:
                for animal in cell.animals:
                    species = type(animal).__name__

                    if species == 'Herbivore':
                        animal_gives_birth = animal.prob_procreation(
                            cell.total_herbivores
                        )
                    if species == 'Carnivore':
                        animal__gives_birth = animal.prob_procreation(
                            cell.total_carnivores
                        )

                    if animal_gives_birth:
                        self.animal_give_birth(animal, loc)

    def animal_give_birth(self, animal, loc):
        weight = animal.draw_birth_weight()
        baby = [{'loc': loc,
                'pop': {
                    'species': type(animal).__name__,
                    'age': 0,
                    'weight': weight}}]
        self.add_population(baby)

    def migration(self):
        """
        Moves animal from current cell to one of the possible
        neighbouring cells, if prob_migrate returns 1.
        """
        for loc, cell in self.island_map.items():
            if cell.animal_can_enter:
                for animal in cell.animals:
                    migrating_animals = []
                    if animal.prob_migration:
                        new_loc = self.choose_cell(loc, type(animal).__name__)
                        self.island_map[new_loc].animals.append(animal)
                        migrating_animals.append(animal)
                    for gone_animal in migrating_animals:
                        cell.animals.remove(gone_animal)

    def choose_cell(self, loc, species):
        """
        Calculate propensities and returns
        coordinates of chosen cell to migrate to.
        :param: loc: Location coordinates before migration.
        :type: tuple
        :param: species: Herbivore or Carnivore
        :type: str
        :return: choice: Chosen cell coordinates to migrate to.
        :type: tuple
        """
        x, y = loc
        cell_left = (x, y-1)
        cell_right = (x, y+1)
        cell_up = (x-1, y)
        cell_down = (x+1, y)
        locations = [cell_left, cell_right, cell_up, cell_down]

        if species == 'Herbivore':
            calculator = PropensityCalculator(locations, self.island_map)
            propensities = calculator.herbs()

        if species == 'Carnivore':
            calculate_prop_carn = self.propensity_calculator('Carnivore')
            propensities = calculate_prop_carn(locations)

        sum_propensities = sum(propensities)
        pl = propensities[0] / sum_propensities * propensities[0]
        pr = propensities[1] / sum_propensities * propensities[1]
        pu = propensities[2] / sum_propensities * propensities[2]
        pd = propensities[3] / sum_propensities * propensities[3]

        choice = np.random.choice(locations, p=[pl, pr, pu, pd])
        return choice

    def death(self):
        """
        Animals are removed if prob_death returns 1.
        """
        for cell in self.island_map.values():
            dead_animals = []
            for animal in cell.animals:
                if animal.prob_death:
                    dead_animals.append(animal)
            for dead_animal in dead_animals:
                cell.animals.remove(dead_animal)

    @staticmethod
    def make_geography_coordinates(input_map):
        """
        Makes a dictionary with coordinates as keys and Cell subclass
        instances (Savannah, Jungle, Desert, MountainAndOcean) as values,
        initiated with default parameters.
        :return: geography_map
        :type: dict
        """
        list_island_map = input_map.split('\n')
        geography_map = {}
        for i_index, line in enumerate(list_island_map):
            for j_index, cell in enumerate(line):
                cell_instance = Rossumoya.cell_code[cell]
                geography_map[(i_index, j_index)] = cell_instance()
        return geography_map
