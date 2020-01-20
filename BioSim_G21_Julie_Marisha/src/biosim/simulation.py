# -*- coding: utf-8 -*-

"""
:mod: `biosim.simulation` provides the user the interface to the package.

The simulation will run for a given number of years. The user will also be 
able to visualize the simulation results while the simulation is in progress. 
The visualization is given in one graphics window with the following elements:

    *   Geography of the island is shown with color codes for the different 
        landscape types. 
    *   Line graph that shows the total number of animals in the island by 
        species.
    *   Population map with color bars that shows how many animals per species 
        there are in each cell. 

This file can be imported as a module and contains the following
class:

    *   BioSim - 

.. note::
    *   This script requires that `math` is installed within the Python
        environment you are running this script in.

"""

__author__ = 'Julie Forrisdal', 'Marisha Gnanaseelan'
__email__ = 'juforris@nmbu.no', 'magn@nmbu.no'

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import subprocess

from src.biosim.animal import Herbivore, Carnivore
from src.biosim.cell import Savannah, Jungle
from src.biosim.rossumoya import Rossumoya, MigrationProbabilityCalculator

# update these variables to point to your ffmpeg and convert binaries
FFMPEG = r'C:\Users\be15069901\Documents\NMBU Data 2019-2020\INF200\biosim_project\BioSim_G21_Julie_Marisha\BioSim_G21_Julie_Marisha\ffmpeg\bin\ffmpeg.exe'
_CONVERT_BINARY = 'magick'

# update this to the directory and file-name beginning
# for the graphics files
_DEFAULT_GRAPHICS_DIR = os.path.join('..', 'figs')
_DEFAULT_IMAGE_NAME = 'bio'
_DEFAULT_IMAGE_FORMAT = "png"
_DEFAULT_MOVIE_FORMAT = 'mp4'
DEFAULT_IMAGE_BASE = r'C:\Users\be15069901\Documents\NMBU Data 2019-2020\INF200\biosim_project\BioSim_G21_Julie_Marisha\BioSim_G21_Julie_Marisha\src\figs\bio'


class BioSim:
    """
    Simulation
    """

    def __init__(
            self,
            island_map=None,
            ini_pop=None,
            seed=1,
            ymax_animals=None,
            cmax_animals=None,
            img_base=None,
            img_fmt=None,
    ):
        """
        :param island_map: Multi-line string specifying island geography
        :type island_map: str
        :param ini_pop: List of dictionaries specifying initial population
        :type ini_pop: list
        :param seed: Random number seed
        :type seed: int
        :param ymax_animals: y-axis limit for graph showing animal numbers
        :type ymax_animals: int
        :param cmax_animals: Color-code limits for animal densities,
                             e.g. {'Herbivore': 100, 'Carnivore': 50}
        :type cmax_animals: dict
        :param img_base: Beginning of file name for figures,
                         including path
        :type img_base: str
        :param img_fmt: File type for figures, e.g. 'png'
        :type img_fmt: str

        If img_base is None, no figures are written to file.
        img_base should contain a path and beginning of a file name.
        """
        np.random.seed(seed)
        self.rossumoya = Rossumoya(island_map, ini_pop)
        self._year = 0
        self._final_year = None
        self._image_counter = 0

        if img_base is not None:
            self._image_base = img_base
        else:
            self._image_base = None

        if img_fmt is None:
            img_fmt = _DEFAULT_IMAGE_FORMAT
        self._image_format = img_fmt

        self._image_counter = 0

        if ymax_animals is None:
            ymax_animals = 15000
        self._ymax = ymax_animals

        if cmax_animals is None:
            cmax_herbs = 150
            cmax_carns = 150
        else:
            cmax_herbs = cmax_animals['Herbivore']
            cmax_carns = cmax_animals['Carnivore']

        self._cmax_herbs = cmax_herbs
        self._cmax_carns = cmax_carns

        # the following will be initialized by _setup_graphics
        self.vis_years = None
        self._nested_list = None
        self._fig = None
        self._map_ax = None
        self._map_axis = None
        self._map_code_ax = None
        self._map_code_axis = None
        self._graph_ax = None
        self._herb_line = None
        self._carn_line = None
        self._heat_map_carn_ax = None
        self._heat_map_carn_axis = None
        self._heat_map_herb_ax = None
        self._heat_map_herb_axis = None

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

    def simulate(self, num_years, vis_years=1, img_years=None):
        """
        Run simulation while visualizing the result.

        :param num_years: number of years to simulate
        :param vis_years: years between visualization updates
        :param img_years: years between visualizations saved to files
         (default: vis_years)

        .. note:: Image files will be numbered consecutively.

        """

        if img_years is None:
            img_years = vis_years

        self.vis_years = vis_years

        self._final_year = self._year + num_years
        self._setup_graphics()

        while self._year < self._final_year:

            if self._year % vis_years == 0:
                self._update_graphics()

            """if self._year % img_years == 0:
                self._save_file()"""

            self.rossumoya.single_year()
            self._year += 1
        self._update_graphics()

    def add_population(self, population):
        """
        Add a population to the island

        :param population: List of dictionaries specifying population
        """
        self.rossumoya.add_population(population)

    def _make_map_with_rgb_colours(self):
        """ Makes map from nested_coordinates_list with rgb colour codes for visualization."""
        colour_map = self.nested_coordinates_list
        map_list = self.rossumoya.island_map_string.split('\n')

        for x, cell_row in enumerate(map_list):
            for y, cell_code in enumerate(cell_row):
                if cell_code == 'S':
                    colour_map[x][y] = (200, 200, 50)

                if cell_code == 'J':
                    colour_map[x][y] = (40, 150, 30)

                if cell_code == 'O':
                    colour_map[x][y] = (51, 102, 153)

                if cell_code == 'D':
                    colour_map[x][y] = (175, 104, 22)

                if cell_code == 'M':
                    colour_map[x][y] = (210, 200, 220)
        return colour_map

    def _make_population_heat_maps(self):
        data_frame = self.animal_distribution
        data_frame.set_index(["Row", "Col"], inplace=True)

        carn_pop_list = self.nested_coordinates_list

        for x, list_ in enumerate(carn_pop_list):
            for y, _ in enumerate(list_):
                carn_pop = (
                    data_frame.loc[(x, y)].Carnivore
                )
                carn_pop_list[x][y] = carn_pop

        herb_pop_list = self.nested_coordinates_list

        for x, list_ in enumerate(herb_pop_list):
            for y, _ in enumerate(list_):
                herb_pop = (
                    data_frame.loc[(x, y)].Herbivore
                )
                herb_pop_list[x][y] = herb_pop

        return carn_pop_list, herb_pop_list

    @property
    def nested_coordinates_list(self):
        """
        Make a nested list with None as values, with indexing corresponding
        to the coordinates of the island map.
        :return: self._nested_list
        :type: list
        """
        self._nested_list = []
        map_size = self.rossumoya.map_size
        x, y = map_size
        for x_index in range(x):
            self._nested_list.append([])
            for _ in range(y):
                self._nested_list[x_index].append(None)
        return self._nested_list

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
        data_dict = {'Row': [], 'Col': [], 'Herbivore': [], 'Carnivore': []}
        for loc, cell in self.rossumoya.island_map.items():
            x, y = loc
            data_dict['Row'].append(x)
            data_dict['Col'].append(y)
            data_dict['Herbivore'].append(cell.total_herbivores)
            data_dict['Carnivore'].append(cell.total_carnivores)

        data_frame = pd.DataFrame.from_dict(data_dict)

        return data_frame

    def _update_heat_map(self):
        """ Update the 2D-view of the map.
        """
        data_map = self._make_population_heat_maps()
        data_map_carn, data_map_herb = data_map

        if self._heat_map_carn_axis is None:
            self._heat_map_carn_axis = self._heat_map_carn_ax.imshow(
                data_map_carn,
                interpolation='nearest',
                vmin=0,
                vmax=self._cmax_carns
            )
            plt.colorbar(self._heat_map_carn_axis,
                         ax=self._heat_map_carn_ax,
                         orientation='vertical')
        else:
            self._heat_map_carn_axis.set_data(data_map_carn)

        if self._heat_map_herb_axis is None:
            self._heat_map_herb_axis = self._heat_map_herb_ax.imshow(
                data_map_herb,
                interpolation='nearest',
                vmin=0,
                vmax=self._cmax_herbs
            )
            plt.colorbar(self._heat_map_herb_axis,
                         ax=self._heat_map_herb_ax,
                         orientation='vertical')
        else:
            self._heat_map_herb_axis.set_data(data_map_herb)

    def _update_graphics(self):
        """Updates graph and heat map in figure window."""
        self._fig.suptitle(f'Year: {self.year}', fontsize=20)
        self._update_graph()
        self._update_heat_map()
        plt.pause(1e-2)

    def _update_graph(self):
        """Updates population graph."""
        data_dict = self.num_animals_per_species
        total_carns = data_dict['Carnivore']
        total_herbs = data_dict['Herbivore']

        herb_data = self._herb_line.get_ydata()
        herb_data[self._year] = total_herbs
        if self.vis_years != 1:
            herb_data = self._interpolate_gaps(herb_data)

        carn_data = self._carn_line.get_ydata()
        carn_data[self._year] = total_carns
        if self.vis_years != 1:
            carn_data = self._interpolate_gaps(carn_data)

        self._carn_line.set_ydata(carn_data)
        self._herb_line.set_ydata(herb_data)

    def _interpolate_gaps(self, values):
        """
        Fill gaps using linear interpolation, optionally only fill gaps up to a
        size of `limit`.

        Code originates from:
        https://stackoverflow.com/questions/36455083/working-with-nan-values-in-matplotlib
        """
        limit = self.vis_years
        values = np.asarray(values)
        i = np.arange(values.size)
        valid = np.isfinite(values)
        filled = np.interp(i, i[valid], values[valid])

        if limit is not None:
            invalid = ~valid
            for n in range(1, limit + 1):
                invalid[:-n] &= invalid[n:]
            filled[invalid] = np.nan

        return filled

    def _setup_graphics(self):
        """Creates subplots."""
        self._nested_list = self.nested_coordinates_list

        # create new figure window
        if self._fig is None:
            self._fig = plt.figure(constrained_layout=True, figsize=(8, 6))
            gs = self._fig.add_gridspec(4, 12)

        # Add subplot for map
        if self._map_ax is None:
            self._map_ax = self._fig.add_subplot(gs[:2, 0:5])
            self._map_ax.set_title('Rossumøya')

        if self._map_axis is None:
            map_ = self._make_map_with_rgb_colours()
            self._map_axis = self._map_ax.imshow(map_)
            self._map_ax.get_xaxis().set_visible(False)
            self._map_ax.get_yaxis().set_visible(False)

        # Add subplot for map codes
        if self._map_code_ax is None:
            self._map_code_ax = self._fig.add_subplot(gs[:2, 5:7])
            cell_codes_bar = [[(200, 200, 50)],
                              [(40, 150, 30)],
                              [(175, 104, 22)],
                              [(210, 200, 220)],
                              [(51, 102, 153)]]

            self._map_code_axis = self._map_code_ax.imshow(cell_codes_bar)
            codes = ['', 'Savannah', 'Jungle', 'Desert', 'Mountain', 'Ocean']
            self._map_code_ax.set_yticklabels(codes)
            self._map_code_ax.get_xaxis().set_visible(False)

        # Add subplot for graph
        if self._graph_ax is None:
            self._graph_ax = self._fig.add_subplot(gs[:2, 7:])
            self._graph_ax.set_ylim(0, self._ymax)
            self._graph_ax.set_xlim(0, self._final_year + 1)
        else:
            self._graph_ax.set_ylim(0, self._ymax)
            self._graph_ax.set_xlim(0, self._final_year + 1)

        # Initiate total Herbivores graph
        if self._herb_line is None:
            herb_graph = self._graph_ax.plot(
                np.arange(0, self._final_year + 1),
                np.full(self._final_year + 1, np.nan))
            self._herb_line = herb_graph[0]
        else:
            x_data, y_data = self._herb_line.get_data()
            x_new = np.arange(x_data[-1] + 1, self._final_year + 1)
            if len(x_new) > 0:
                y_new = np.full(x_new.shape, np.nan)
                self._herb_line.set_data(np.hstack((x_data, x_new)),
                                         np.hstack((y_data, y_new)))

        # Initiate total Carnivores graph
        if self._carn_line is None:
            carn_plot = self._graph_ax.plot(
                np.arange(0, self._final_year + 1),
                np.full(self._final_year + 1, np.nan))
            self._carn_line = carn_plot[0]
        else:
            x_data, y_data = self._carn_line.get_data()
            x_new = np.arange(x_data[-1] + 1, self._final_year + 1)
            if len(x_new) > 0:
                y_new = np.full(x_new.shape, np.nan)
                self._carn_line.set_data(np.hstack((x_data, x_new)),
                                         np.hstack((y_data, y_new)))

        # Add legend to graph
        self._graph_ax.legend((self._herb_line, self._carn_line),
                              ('Herbivores', 'Carnivores'),
                              loc='upper left')

        # Add subplots for heat map
        if self._heat_map_carn_ax is None:
            self._heat_map_carn_ax = self._fig.add_subplot(gs[2:, :6])
            self._heat_map_carn_ax.get_xaxis().set_visible(False)
            self._heat_map_carn_ax.get_yaxis().set_visible(False)
            self._heat_map_carn_ax.set_title('Carnivores locations')

        if self._heat_map_herb_ax is None:
            self._heat_map_herb_ax = self._fig.add_subplot(gs[2:, 6:])
            self._heat_map_herb_ax.get_xaxis().set_visible(False)
            self._heat_map_herb_ax.get_yaxis().set_visible(False)
            self._heat_map_herb_ax.set_title('Herbivores locations')

    def _save_file(self):
        """Saves graphics to file if file name given.
        Author: Hans Ekkehard Plesser
        """

        if self._image_base is None:
            return

        plt.savefig('{base}_{num:05d}.{type}'.format(base=self._image_base,
                                                     num=self._image_counter,
                                                     type=self._image_format))
        self._image_counter += 1

    def make_movie(self, movie_fmt=_DEFAULT_MOVIE_FORMAT):
        """
        Creates MPEG4 movie from visualization images saved.

        .. :note:
            Requires ffmpeg

        The movie is stored as img_base + movie_fmt
        Author: Hans Ekkehard Plesser
        """

        if self._image_base is None:
            raise RuntimeError("No filename defined.")

        movie_fmt = 'mp4'
        try:
            subprocess.check_call(f'{FFMPEG} -y -r 2 -i '
                                  f'{self._image_base}%05d.{self._image_format}'
                                  f' -c:v libx264 -vf fps=25 -pix_fmt '
                                  f'yuv420p '
                                  f'{self._image_base}.{movie_fmt}')

        except subprocess.CalledProcessError as err:
            raise RuntimeError('ERROR: ffmpeg failed with: {}'.format(err))


if __name__ == '__main__':
    sim1 = BioSim()
    sim1.simulate(num_years=30, vis_years=2, img_years=5)
    plt.show()
