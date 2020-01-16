# -*- coding: utf-8 -*-

"""
creds to Hans Ekkehard Plesser for visualization

"""

__author__ = 'Julie Forrisdal', 'Marisha Gnanaseelan'
__email__ = 'juforris@nmbu.no', 'magn@nmbu.no'

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import subprocess


from biosim.animal import Herbivore, Carnivore
from biosim.cell import Savannah, Jungle
from biosim.rossumoya import Rossumoya

# update these variables to point to your ffmpeg and convert binaries
_FFMPEG_BINARY = 'ffmpeg'
_CONVERT_BINARY = 'magick'

# update this to the directory and file-name beginning
# for the graphics files
_DEFAULT_GRAPHICS_DIR = os.path.join('..', 'figs')
_DEFAULT_IMAGE_BASE = 'bio'
_DEFAULT_IMAGE_FORMAT = "png"
_DEFAULT_MOVIE_FORMAT = 'mp4'


class BioSim:

    def __init__(
            self,
            island_map=None,
            ini_pop=None,
            seed=1,
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
        np.random.seed(seed)
        self.rossumoya = Rossumoya(island_map, ini_pop)
        self._year = 0
        self._final_year = None
        self._image_counter = 0

        if img_base is None:
            img_base = _DEFAULT_IMAGE_BASE
        self._image_base = img_base

        if img_fmt is None:
            img_fmt = _DEFAULT_IMAGE_FORMAT
        self._image_format = img_fmt

        self._image_counter = 0

        if ymax_animals is None:
            ymax_animals = 1000
        self._ymax = ymax_animals
        self._cmax = cmax_animals

        # the following will be initialized by _setup_graphics
        self._fig = None
        self._map_ax = None
        self._map_axis = None
        self._map_code_ax = None
        self._map_code_axis = None
        self._graph_ax = None
        self._graph_axis = None
        self._heat_map_ax = None
        self._heat_map_axis = None


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
        :param img_years: years between visualizations saved to files (default: vis_years)

        Image files will be numbered consecutively.
        Author: Hans Ekkehard Plesser
        """

        if img_years is None:
            img_years = vis_years

        self._final_year = self.year + num_years
        self._setup_graphics()

        while self.year < self._final_year:

            if self.year % vis_years == 0:
                self._update_graphics()

            if self.year % img_years == 0:
                self._save_file()

            self.rossumoya.single_year()
            self._year += 1

    def add_population(self, population):
        """
        Add a population to the island

        :param population: List of dictionaries specifying population
        """
        self.rossumoya.add_population(population)

    def _make_map_with_rgb_colours(self):
        colour_map = []
        map_list = self.rossumoya.island_map_string.split('\n')
        print(map_list)

        for x, cell_row in enumerate(map_list):
            colour_map.append([])
            for cell_code in cell_row:
                if cell_code == 'S':
                    colour_map[x].append((200, 200, 50))

                if cell_code == 'J':
                    colour_map[x].append((40, 150, 30))

                if cell_code == 'O':
                    colour_map[x].append((0, 130, 300))

                if cell_code == 'D':
                    colour_map[x].append((220, 180, 140))

                if cell_code == 'M':
                    colour_map[x].append((210, 200, 220))
        return colour_map

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

    def _update_heat_map(self, sys_map):
        """ Update the 2D-view of the map.
        Author: Hans Ekkehard Plesser
        """
        if self._heat_map_axis is not None:
            self._heat_map_axis.set_data(sys_map)
        else:
            self._heat_map_axis = self._map_ax.imshow(sys_map,
                                                      interpolation='nearest',
                                                      vmin=0, vmax=1)
            plt.colorbar(self._heat_map_axis, ax=self._map_ax,
                         orientation='horizontal')

    def _update_graphics(self):
        self._update_heat_map()
        self._update_graph()
        plt.pause(1e-6)

    def _update_graph(self):
        pass

    def _setup_graphics(self):
        """Creates subplots."""
        # create new figure window
        if self._fig is None:
            self._fig = plt.figure(constrained_layout=True)
            gs = self._fig.add_gridspec(2, 4)

        # Add subplot for map
        if self._map_ax is None:
            self._map_ax = self._fig.add_subplot(gs[1, :])

        if self._map_axis is None:
            map = self._make_map_with_rgb_colours()
            self._map_axis = self._map_ax.imshow(map)
        """
        # Add subplot for map codes
        if self._map_code_ax is None:
           self._map_code_ax = self._fig.add_subplot(gs[0, 4:6])

        # Add subplot for graph
        if self._graph_ax is None:
            self._graph_ax = self._fig.add_subplot(gs[0, 6:])
            self._graph_ax.set_ylim(0, self._ymax)
            self._graph_ax.set_xlim(0, self._final_year + 1)

        # Add subplot for heat map
        if self._heat_map_ax is None:
            self._heat_map_ax = self._fig.add_subplot(2, 3, 1)
            self._heat_map_axis = None

        # Initiate graph
        if self._graph_axis is None:
            graph_plot = self._graph_ax.plot(np.arange(0, self._final_year),
                                             np.full(self._final_year, np.nan))
            self._graph_axis_ = graph_plot[0]
        else:
            xdata, ydata = self._graph_axis.get_data()
            xnew = np.arange(xdata[-1] + 1, self._final_year)
            if len(xnew) > 0:
                ynew = np.full(xnew.shape, np.nan)
                self._graph_axis.set_data(np.hstack((xdata, xnew)),
                                          np.hstack((ydata, ynew)))
        """
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

        if movie_fmt == 'mp4':
            try:
                # Parameters chosen according to http://trac.ffmpeg.org/wiki/Encode/H.264,
                # section "Compatibility"
                subprocess.check_call([_FFMPEG_BINARY,
                                       '-i', '{}_%05d.png'.format(self._image_base),
                                       '-y',
                                       '-profile:v', 'baseline',
                                       '-level', '3.0',
                                       '-pix_fmt', 'yuv420p',
                                       '{}.{}'.format(self._image_base,
                                                      movie_fmt)])
            except subprocess.CalledProcessError as err:
                raise RuntimeError('ERROR: ffmpeg failed with: {}'.format(err))
        elif movie_fmt == 'gif':
            try:
                subprocess.check_call([_CONVERT_BINARY,
                                       '-delay', '1',
                                       '-loop', '0',
                                       '{}_*.png'.format(self._image_base),
                                       '{}.{}'.format(self._image_base,
                                                      movie_fmt)])
            except subprocess.CalledProcessError as err:
                raise RuntimeError('ERROR: convert failed with: {}'.format(err))
        else:
            raise ValueError('Unknown movie format: ' + movie_fmt)

if __name__ == '__main__':
    sim1 = BioSim()
    sim1._final_year = 2
    sim1._setup_graphics()
    plt.show()