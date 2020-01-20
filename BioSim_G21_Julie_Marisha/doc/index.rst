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
population map for the number of animals per cell and simulation year.


.. toctree::
   :maxdepth: 2
   :caption: Contents:

   modules
   examples
   maths
   references