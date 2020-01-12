# -*- coding: utf-8 -*-

"""
"""
from BioSim_G21_Julie_Marisha.src.biosim.animal import Herbivore, Carnivore
from BioSim_G21_Julie_Marisha.src.biosim.cell import Savannah, Jungle, Desert, MountainAndOcean
from BioSim_G21_Julie_Marisha.src.biosim.rossumoya import Rossumoya
import pandas as pd


__author__ = 'Julie Forrisdal', 'Marisha Gnanaseelan'
__email__ = 'juforris@nmbu.no', 'magn@nmbu.no'


class BioSim:

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
        self.rossumoya = Rossumoya(island_map, ini_pop)
        if seed is None:
            seed = 1
        self.seed = seed
        self._year = 0

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
        self._year += 1

    def simulate(self, num_years, vis_years=1, img_years=None):
        """
        Run simulation while visualizing the result.

        :param num_years: number of years to simulate
        :param vis_years: years between visualization updates
        :param img_years: years between visualizations saved to files (default: vis_years)

        Image files will be numbered consecutively.
        """

        for year in range(num_years):
            self.single_simulation()

    def add_population(self, population):
        """
        Add a population to the island

        :param population: List of dictionaries specifying population
        """
        self.rossumoya.add_population(population)

    @property
    def year(self):
        """Last year simulated."""
        return self._year

    @property
    def num_animals(self):
        """Total number of animals on island."""
        num_animals = 0
        for cell in self.rossumoya.island_map.values():
            num_animals += cell.total_population
        return num_animals

    @property
    def num_animals_per_species(self):
        """Number of animals per species in island, as dictionary."""
        num_herb = 0
        num_carn = 0

        for cell in self.rossumoya.island_map.values():
            num_herb += cell.total_herbivores
            num_carn += cell.total_carnivores

        num_animals_per_species = {'Herbivore': num_herb,
                                   'Carnivore': num_carn}

        return num_animals_per_species

    @property
    def animal_distribution(self):
        """Pandas DataFrame with animal count per species
         for each cell on island."""
        data_dict = {}
        for cell in self.rossumoya.island_map.values():
            data_dict[loc] = [cell.total_herbivores, cell.total_carnivores]

        data_frame = pd.DataFrame.from_dict(data_dict, orient='index')
        data_frame.columns = ['total_herbivores',
                              'total_carnivores']
        data_frame.index.name = 'Coordinates'

        return data_frame

    def make_movie(self):
        """Create MPEG4 movie from visualization images saved."""
