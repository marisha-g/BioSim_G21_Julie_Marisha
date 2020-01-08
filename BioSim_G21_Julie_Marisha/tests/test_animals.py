# -*- coding: utf-8 -*-

"""
"""

__author__ = 'Julie Forrisdal', 'Marisha Gnanaseelan'
__email__ = 'juforris@nmbu.no', 'magn@nmbu.no'

from src.biosim.animals import Animals, Herbivore, Carnivore
import pytest


class TestAnimals:
    def default(self):
        pass

    def test_aging(self):
        """ """
        a = Animals()
        a.aging()
        assert a.age == 1


class TestHerbivore:
    """
    Tests for Animals class
    """
    def test_default_parameters(self):
        a = Herbivore()
        assert a.age == 0
        assert a.weight is None

        a.set_parameters()
        assert a.w_birth == 8.0
        assert a.sigma_birth == 1.5
        assert a.beta == 0.9
        assert a.eta == 0.05
        assert a.a_half == 40.0
        assert a.phi_age == 0.2
        assert a.w_half == 10.0
        assert a.phi_weight == 0.1
        assert a.mu == 0.25
        assert a.lambda_ == 1.0
        assert a.gamma == 0.2
        assert a.zeta == 3.5
        assert a.xi == 1.2
        assert a.omega == 0.4
        assert a.f == 10.0

    def test_birth_weight(self):
        """ Test that birth_weight method returns positive number."""
        a = Herbivore()
        assert a.birth_weight() >= 0


    def test_condition(self):
        a = Herbivore()
        a.set_parameters()
        a.weight = 10
        a.age = 2
        a.evaluate_fitness()
        assert a.fitness == pytest.approx(0.49975)


class TestCarnivore:
    def test_default_parameters(self):
        a = Carnivore()
        assert a.age == 0
        assert a.weight is None

        a.set_parameters()
        assert a.w_birth == 6.0
        assert a.sigma_birth == 1.0
        assert a.beta == 0.75
        assert a.eta == 0.125
        assert a.a_half == 60.0
        assert a.phi_age == 0.4
        assert a.w_half == 4.0
        assert a.phi_weight == 0.4
        assert a.mu == 0.4
        assert a.lambda_ == 1.0
        assert a.gamma == 0.8
        assert a.zeta == 3.5
        assert a.xi == 1.1
        assert a.omega == 0.9
        assert a.f == 50.0
