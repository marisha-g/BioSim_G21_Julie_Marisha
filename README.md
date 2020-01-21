
BioSim project
===============

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
The BioSim project supports python 3.6+. It also requires a couple of libraries 
and other setups in order to run. Packages you need to install are:
    *   numba
    *   matplotlib
    *   scipy
    *   pandas
    *   numpy
    *   os
    *   textwrap
    *   subprocess
   
 To install biosim via ``pip``, simply run the command::

    pip install BioSim_G21_Julie_Marisha

Alternatively, you can manually pull this repository and run the
``setup.py`` file::

    git clone https://github.com/marisha-g/BioSim_G21_Julie_Marisha.git
    cd BioSim_G21_Julie_Marisha
    python setup.py

Documentation
--------------
You can read the full documentation on `readthedocs <https://group-lasso.readthedocs.io/en/latest/maths.html>`_.


References
----------
.. [1] Moe, Y. M. (2019). *Modelling the Ecosystem of Rossumøya*.
