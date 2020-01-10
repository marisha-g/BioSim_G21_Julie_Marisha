# -*- coding: utf-8 -*-

"""
"""
from BioSim_G21_Julie_Marisha.src.biosim.animal import Herbivore, Carnivore
from BioSim_G21_Julie_Marisha.src.biosim.cell import Savannah, Jungle, Desert, MountainAndOcean

__author__ = 'Julie Forrisdal', 'Marisha Gnanaseelan'
__email__ = 'juforris@nmbu.no', 'magn@nmbu.no'


import textwrap
import random


class BioSim:
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

    def __init__(
        self,
        island_map=None,
        ini_pop=None,
        seed=None,
        ymax_animals=None,
        cmax_animals=None,
        img_base=None,
        img_fmt="png",
    ):
        """
        :param island_map: Multi-line string specifying island geography
        :param ini_pop: List of dictionaries specifying initial population
        :param seed: Integer used as random number seed
        :param ymax_animals: Number specifying y-axis limit for graph showing animal numbers
        :param cmax_animals: Dict specifying color-code limits for animal densities
        :param img_base: String with beginning of file name for figures, including path
        :param img_fmt: String with file type for figures, e.g. 'png'

        If ymax_animals is None, the y-axis limit should be adjusted automatically.

        If cmax_animals is None, sensible, fixed default values should be used.
        cmax_animals is a dict mapping species names to numbers, e.g.,
           {'Herbivore': 50, 'Carnivore': 20}

        If img_base is None, no figures are written to file.
        Filenames are formed as

            '{}_{:05d}.{}'.format(img_base, img_no, img_fmt)

        where img_no are consecutive image numbers starting from 0.
        img_base should contain a path and beginning of a file name.
        """
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
        for cell in island_map_list[n-1]:
            if cell != "O":
                raise ValueError("Non-ocean boundary.")
        for row in island_map_list:
            num_cells = len(row)
            if row[0] != "O":
                raise ValueError("Non-ocean boundary.")
            if row[num_cells-1] != "O":
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
                geography_map[(i_index+1, j_index+1)] = {
                    "cell type": BioSim.cell_code[cell](),
                    "total pop": 0,
                    "Herbivores": [],
                    "Carnivores": [],

                }

        return geography_map


    @staticmethod
    def set_animal_parameters(species, params):
        """
        Set parameters for animal species.

        :param species: String, name of animal species
        :param params: Dict with valid parameter specification for species
        """
        if species == "Herbivore":
            Herbivore.set_parameters(**params)
        if species == "Carnivore":
            Carnivore.set_parameters(**params)

    @staticmethod
    def set_landscape_parameters(landscape, params):
        """
        Set parameters for landscape type.

        :param landscape: String, code letter for landscape
        :param params: Dict with valid parameter specification for landscape
        """
        if landscape == "S":
            Savannah.set_parameters(**params)
        if landscape == "J":
            Jungle.set_parameters(**params)

    def single_simulation(self):
        """
        Run one single simulation.
        :return:
        """

    def simulate(self, num_years, vis_years=1, img_years=None):
        """
        Run simulation while visualizing the result.

        :param num_years: number of years to simulate
        :param vis_years: years between visualization updates
        :param img_years: years between visualizations saved to files (default: vis_years)

        Image files will be numbered consecutively.
        """

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

    @property
    def year(self):
        """Last year simulated."""

    @property
    def num_animals(self):
        """Total number of animals on island."""

    @property
    def num_animals_per_species(self):
        """Number of animals per species in island, as dictionary."""

    @property
    def animal_distribution(self):
        """Pandas DataFrame with animal count per species for each cell on island."""

    def make_movie(self):
        """Create MPEG4 movie from visualization images saved."""
