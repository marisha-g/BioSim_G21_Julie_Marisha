Guide
===================

Required packages
-------------------
The BioSim project supports Python 3.6+. You also need to install the following
packages: numba, matplotlib, scipy, pandas, numpy, os, textwrap and subprocess.
Some of these packages should come pre-installed on any Anaconda installation,
otherwise they can be installed using ``pip``::
    pip install numba
    pip install matplotlib
    pip install scipy
    pip install pandas
    pip install numpy
    pip install os
    pip install textwrap
    pip install subprocess

The module also requires the program ``ffmpeg`` which is available from
`<https://ffmpeg.org>`_.

Installing BioSim
--------------------
To install biosim via ``pip``, simply run the command::

    pip install BioSim_G21_Julie_Marisha

Alternatively, you can manually pull this repository and run the
``setup.py`` file::

    git clone https://github.com/marisha-g/BioSim_G21_Julie_Marisha.git
    cd BioSim_G21_Julie_Marisha
    python setup.py

References
----------
*   Moe, Y.M. (2019). *Group-Lasso*. `<https://group-lasso.readthedocs.io/en/latest/installation.html>`_.