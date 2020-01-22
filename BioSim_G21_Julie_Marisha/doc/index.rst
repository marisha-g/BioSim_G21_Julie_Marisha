.. biosim_G21 documentation master file, created by
   sphinx-quickstart on Thu Jan  9 09:47:39 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Modelling the Ecosystem of Rossumøya
======================================
This library provides the computer programs for the simulation of population
dynamics on Rossumøya.

Summary
--------
The long term goal for Rossumøya is to preserve the island as a nature park
for future generations. The ecosystem on Rossumøya is characterized by
different landscape types, such as jungle, savannah, desert, mountain and
ocean. The island's fauna consists of two different species: Herbivores
(plant eaters) and Carnivores (predators). In order to investigate if both
species can survive in the long term we have made a simulation which runs for
a given number of years. After the simulation, one can obtain a status
information which include: number of years that has been simulated,
total number of animals on the island, total number of animals per species
and total number of animals per cell. One is also able to visualize the
simulation results while the simulation runs. The graphics window include:
the island's geography, total number of animals per species as graph,
population map for the number of animals per cell and simulation year. [1]_


Installation
-------------
The BioSim project requires a couple of libraries and other setups in order to run.
Read more about how you can install our BioSim project :doc:`here.<installation/guide>`


.. toctree::
   :maxdepth: 2
   :hidden:
   :caption: Installation

   installation/guide

Modules
-----------

The modules and the source code for this project can be accessed by clicking
on the links below.

*  :doc:`The simulation module <modules/simulation>`

*  :doc:`The Rossumøya module <modules/rossumoya>`

*  :doc:`The cell module <modules/cell>`

*  :doc:`The animal module <modules/animal>`


.. toctree::
   :maxdepth: 2
   :hidden:
   :caption: Modules

   modules/simulation
   modules/rossumoya
   modules/cell
   modules/animal


Examples
------------

*  :doc:`Population generator <examples/population_generator>`
*  :doc:`Checkerboard migration demo <examples/checkerboard_migration_demo>`
*  :doc:`BioSim movie <examples/bio500years>`


.. toctree::
   :maxdepth: 2
   :hidden:
   :caption: Examples

   examples/population_generator
   examples/checkerboard_migration_demo
   examples/bio500years

References
----------
.. [1] Moe, Y. M. (2019). *Modelling the Ecosystem of Rossumøya*.






