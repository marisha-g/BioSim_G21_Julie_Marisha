# -*- coding: utf-8 -*-

"""
"""

__author__ = 'Julie Forrisdal', 'Marisha Gnanaseelan'
__email__ = 'juforris@nmbu.no', 'magn@nmbu.no'

from src.biosim.landscape import Landscape
import textwrap

class TestLandscape:
    """

    """

    def test_constructor_default(self):
        """Default constructor is callable"""
        b = Landscape()
        assert isinstance(b, Landscape)

    def test_default_parameters(self):
        """Test if default parameters are correct"""
        b = Landscape()
        assert b.f_sav_max == 300.0
        assert b.f_jungle_max == 800.0
        assert b.alpha == 0.3

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
        assert b.geogr == default_map

        assert isinstance(b.geography_map, dict)
