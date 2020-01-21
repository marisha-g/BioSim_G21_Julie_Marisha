# -*- coding: utf-8 -*-

"""
:mod: `biosim.rossumoya provides the user with the annual cycle on Rossumøya.

This file can also be imported as a module and contains the following classes:

    *   MigrationProbabilityCalculator - calculates the probabilities for an
        animal to migrate.
    *   Rossumoya - class where the user creates the island map and initial
        population. This is also where the different methods for the annual
        cycle are run.

.. note::
    *   This script requires that `textwrap` and `numpy` are installed within
        the Python environment you are running this script in.
"""

__author__ = 'Julie Forrisdal', 'Marisha Gnanaseelan'
__email__ = 'juforris@nmbu.no', 'magn@nmbu.no'

import textwrap
import random

from .animal import Herbivore, Carnivore
from .cell import Savannah, Jungle, Desert, Mountain, Ocean


class MigrationProbabilityCalculator:
    """Class used to calculate probabilities for migration."""

    def __init__(self, loc, island_map, species):
        """
        Constructor that initiate MigrationProbabilityCalculator.
        :param loc: Coordinates for the current position of an animal
        :type loc: tuple
        :param island_map: Dictionary with all cells and their locations
        :type island_map: dict
        :param: species: Herbivore or Carnivore
        :type species: str
        """

        x, y = loc
        cell_left = (x, y - 1)
        cell_right = (x, y + 1)
        cell_up = (x - 1, y)
        cell_down = (x + 1, y)

        locations = [cell_left, cell_right, cell_up, cell_down]

        self.locations = locations
        self._island_map = island_map
        self._species = species
        self._propensity_herb = None
        self._propensity_carn = None
        self._probabilities = None

    @property
    def propensity_herb(self):
        """
        Calculates the propensity to migrate from the current location to the
        four neighbouring cells for Herbivores.
        :return: propensities: List with the four neighbouring cells
                 corresponding propensities.
        :rtype: list
        """
        self._propensity_herb = []
        for coordinates in self.locations:
            cell = self._island_map[coordinates]
            self._propensity_herb.append(cell.propensity_migration_herb)
        return self._propensity_herb

    @propensity_herb.setter
    def propensity_herb(self, value):
        """
        Sets the self._propensity_herb to a new value.
        :param value: new value
        :type value: float
        """
        self._propensity_herb = value

    @property
    def propensity_carn(self):
        """
        Calculates the propensity to migrate from the current location to the
        four neighbouring cells for Carnivores.
        :return: propensities: List with the four neighbouring cells
                 corresponding propensities.
        :rtype: list
        """
        self._propensity_carn = []
        for cell in self.locations:
            cell = self._island_map[cell]
            self._propensity_carn.append(cell.propensity_migration_carn)
        return self._propensity_carn

    @propensity_carn.setter
    def propensity_carn(self, value):
        """
        Sets self.propensity_carn to a new value.
        :param value: new value
        :type value: float
        """
        self._propensity_carn = value

    @property
    def probabilities(self):
        """
        Calculates the probabilities for an animal to move from its current
        location to the four neighbouring cells, based on the propensities.
        :return: self._probabilities: current location and the
                 probabilities to move from that location.
        :rtype: list
        """
        if self._species == 'Herbivore':
            propensities = self.propensity_herb
        if self._species == 'Carnivore':
            propensities = self.propensity_carn

        self._probabilities = []
        sum_propensities = sum(propensities)

        for prop in propensities:
            p = prop / sum_propensities
            self._probabilities.append(p)

        return self._probabilities

    @probabilities.setter
    def probabilities(self, prob_list):
        """
        Sets self._probabilities to a new value.
        :param prob_list: new value
        :type prob_list: list
        """
        if sum(prob_list) != 1:
            raise ValueError('Probabilities must sum up to 1')
        self._probabilities = prob_list


class Rossumoya:
    """Class for island in BioSim."""

    default_ini_herbs = [
        {
            "loc": (10, 13),
            "pop": [{"species": "Herbivore", "age": 5, "weight": 20}
                    for _ in range(150)],
        }
    ]
    default_ini_carns = [
        {
            "loc": (10, 13),
            "pop": [
                {"species": "Carnivore", "age": 5, "weight": 20}
                for _ in range(70)
            ],
        }
    ]
    default_map_string = """\
                          OOOOOOOOOOOOOOOOOOOOO
                          OSSSSSJJJJMMJJJJJJJOO
                          OSSSSSJJJJMMJJJJJJJOO
                          OSSSSSJJJJMMJJJJJJJOO
                          OOSSJJJJJJJMMJJJJJJJO
                          OOSSJJJJJJJMMJJJJJJJO
                          OOOOOOOOSMMMMJJJJJJJO
                          OSSSSSJJJJMMJJJJJJJOO
                          OSSSSSSSSSMMJJJJJJOOO
                          OSSSSSDDDDDJJJJJJJOOO
                          OSSSSSDDDDDJJJJJJJOOO
                          OSSSSSDDDDDJJJJJJJOOO
                          OSSSSSDDDDDMMJJJJJOOO
                          OSSSSDDDDDDJJJJOOOOOO
                          OOSSSSDDDDDDJOOOOOOOO
                          OOSSSSDDDDDJJJOOOOOOO
                          OSSSSSDDDDDJJJJJJJOOO
                          OSSSSDDDDDDJJJJOOOOOO
                          OOSSSSDDDDDJJJOOOOOOO
                          OOOSSSSJJJJJJJOOOOOOO
                          OOOSSSSSSOOOOOOOOOOOO
                          OOOOOOOOOOOOOOOOOOOOO"""

    default_map = textwrap.dedent(default_map_string)

    cell_codes = {"S": Savannah,
                  "J": Jungle,
                  "D": Desert,
                  "O": Ocean,
                  "M": Mountain}

    def __init__(self, island_map=None, ini_pop=None):
        """
        Constructor that initiates Rossumoya class instances.
        :param island_map: Multiline string indicating geography of the island.
        :type: str
        :param ini_pop: List of dictionaries indicating
               initial population and location.
        :type: list
        """
        if island_map is None:
            self.island_map_string = Rossumoya.default_map
            self.island_map = self.make_geography_coordinates(
                Rossumoya.default_map
            )

        else:
            if self.check_map_input(island_map):
                self.island_map_string = island_map
                self.island_map = self.make_geography_coordinates(island_map)

        self.map_size = self.map_size()

        if ini_pop is None:
            self.add_population(Rossumoya.default_ini_herbs)
            self.add_population(Rossumoya.default_ini_carns)
        else:
            self.add_population(ini_pop)

        # Set all parameters to default
        # BioSim.set_landscape_parameters and
        # BioSim.set_animal_parameters methods will override if called upon.
        Savannah.set_parameters()
        Jungle.set_parameters()
        Herbivore.set_parameters()
        Carnivore.set_parameters()

    @staticmethod
    def check_map_input(island_map):
        """
        Raises ValueError if input map is not compatible and does not
        follow restrictions for the geography of the island. Returns True
        otherwise.
        :param island_map: Multiline string indicating the geography
               of the island.
        :type island_map: str
        :return: True
        :rtype: bool
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
                if cell not in Rossumoya.cell_codes:
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

    @staticmethod
    def make_geography_coordinates(input_map):
        """
        Makes a dictionary with coordinates as keys and Cell subclass
        instances (Savannah, Jungle, Desert, Mountain, Ocean) as values,
        initiated with default parameters.
        :return: geography_map
        :rtype: dict
        """
        list_island_map = input_map.split('\n')
        geography_map = {}
        for i_index, line in enumerate(list_island_map):
            for j_index, cell in enumerate(line):
                cell_instance = Rossumoya.cell_codes[cell]
                geography_map[(i_index, j_index)] = cell_instance()
        return geography_map

    def add_population(self, population):
        """
        Add population to the island.
        :param population: List of dictionaries specifying
                           population and locations.
        :type population: list
        """
        for cell_dict in population:
            location = cell_dict['loc']
            pop_dict = cell_dict['pop']
            cell = self.island_map[location]
            if cell.animal_can_enter:
                cell.add_population(pop_dict)
            else:
                raise ValueError(f'Cant place animal in {type(cell).__name__}'
                                 f' at coordinates: {location}')

    def procreation(self):
        """
        Checks for animals in the cells and initiate mating season.
        """
        for cell in self.island_map.values():
            if cell.total_herbivores > 1:
                cell.herb_procreation()
            if cell.total_carnivores > 1:
                cell.carn_procreation()

    def migration(self):
        """
        Finds witch animals wants to migrate, and calls _migrate method to
        initiate migration process.
        """
        for loc, cell in self.island_map.items():
            if cell.total_population > 0:
                migrating_animals = cell.find_migrating_animals()
                if len(migrating_animals) > 0:
                    self.migrate(migrating_animals, loc)

    def migrate(self, migrating_animals, old_loc):
        """
        Calls the choose_cell method to get new locations for each migrating
        animal, and moves them there. Then removes all the animals
        from the old location. Also resets indicator for calculating
        propensities.
        :param migrating_animals: List of animals.
        :type migrating_animals: list
        :param old_loc: Coordinates where the animals migrate from.
        :type old_loc: tuple
        """
        for animal in migrating_animals:
            new_loc = self.choose_cell(old_loc, type(animal).__name__)
            self.island_map[new_loc].add_animals([animal])
            self.island_map[old_loc].remove_animals([animal])

            self.island_map[new_loc].propensity_herb_calculated = False
            self.island_map[new_loc].propensity_carn_calculated = False

        self.island_map[old_loc].propensity_herb_calculated = False
        self.island_map[old_loc].propensity_carn_calculated = False

    def choose_cell(self, loc, species):
        """
        Uses :class: MigrationProbabilityCalculator to get the probabilities
        for migrating to each neighbouring cell, and chooses a cell. Returns
        coordinates of chosen cell to migrate to.
        :param: loc: Location coordinates to migrate from.
        :type loc: tuple
        :param: species: Herbivore or Carnivore
        :type species: str
        :return choice: Chosen cell coordinates to migrate to.
        :rtype: tuple
        """
        calculator = MigrationProbabilityCalculator(
            loc, self.island_map, species
        )
        probabilities = calculator.probabilities
        locations = calculator.locations

        choice = random.choices(
            locations, weights=probabilities
        )
        return choice[0]

    def death(self):
        """
        Finds all animals that dies, and removes them from their location.
        Animals die if the prob_death method returns 1.
        """
        for cell in self.island_map.values():
            dead_animals = []
            for animal in cell.animals:
                if animal.prob_death:
                    dead_animals.append(animal)
            cell.remove_animals(dead_animals)

    def single_year(self):
        """
        Simulates one year at Rossumoya.
        """

        # Fodder regrows
        for cell in self.island_map.values():
            cell.regrow_fodder()

        # Herbivores eat, then carnivores prey on herbivores
        for cell in self.island_map.values():
            if cell.total_herbivores > 0:
                cell.herbivores_eat()
                if cell.total_carnivores > 0:
                    cell.carnivores_eat()

        # Some animals mate
        self.procreation()

        # Some animals migrate
        self.migration()

        # Reset migration indicator
        for cell in self.island_map.values():
            cell.reset_migration()

        # All animals age and loose weight
        for cell in self.island_map.values():
            cell.animals_age_and_lose_weight()

        # Some animals die
        self.death()

    def map_size(self):
        """
        Finds the size of the island_map.
        :return: lower right corner coordinates (max values for row and column)
        :rtype: tuple
        """
        coordinates = self.island_map.keys()
        list_coordinates = list(coordinates)
        x, y = list_coordinates[-1]
        size = (x + 1, y + 1)
        return size
