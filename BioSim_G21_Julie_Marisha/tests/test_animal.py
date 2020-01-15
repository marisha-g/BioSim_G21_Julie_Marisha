# -*- coding: utf-8 -*-

"""
Tests for classes in animal.py using pytest.
"""

__author__ = 'Julie Forrisdal', 'Marisha Gnanaseelan'
__email__ = 'juforris@nmbu.no', 'magn@nmbu.no'

from biosim.animal import BaseAnimal, Herbivore, Carnivore
import pytest


class TestAnimal:
    """Tests for class Animal."""
    def test_value_error_for_negative_values(self):
        """Negative values raises ValueError."""
        with pytest.raises(ValueError):
            BaseAnimal.set_parameters(
                -8.0, -1.5, -0.9,  -0.05, -40.0, -0.2, -10.0, -0.1,
                -0.25, -1.0, -0.2, -3.5, -1.2, -0.4, -10.0
            )

    def test_draw_birth_weight(self):
        """ Test that birth_weight method returns positive number."""
        herb = Herbivore()
        carn = Carnivore()

        Herbivore.set_parameters()
        Carnivore.set_parameters()

        assert herb.draw_birth_weight() >= 0
        assert carn.draw_birth_weight() >= 0

    def test_value_error_for_age_and_weight(self):
        """Check if ValueError is raised for negative inputs. """
        with pytest.raises(ValueError):
            Herbivore(age=-4, weight=-5)
            Carnivore(age=-60, weight=-2.2)

    def test_aging(self):
        """Test if aging method increments an animal's age by 1."""
        herb = Herbivore()
        carn = Carnivore()
        herb.age = 0
        carn.age = 0
        herb.aging()
        carn.aging()

        assert herb.age == 1
        assert carn.age == 1

    def test_weight_gain(self):
        """Weight increases when weight gain method is called. """
        herb = Herbivore()
        carn = Carnivore()

        Herbivore.set_parameters()
        Carnivore.set_parameters()

        herb_weight_1 = herb.weight
        carn_weight_1 = carn.weight

        herb.weight_gain(5)
        carn.weight_gain(5)

        assert herb_weight_1 < herb.weight
        assert carn_weight_1 < carn.weight

    def test_weight_loss(self):
        """Weight decreases when weight loss method is called."""
        herb = Herbivore()
        carn = Carnivore()

        Herbivore.set_parameters()
        Carnivore.set_parameters()

        herb_weight_1 = herb.weight
        carn_weight_1 = carn.weight

        herb.weight_loss()
        carn.weight_loss()

        assert herb_weight_1 > herb.weight
        assert carn_weight_1 > carn.weight

    def test_prob_procreation(self):
        """Probability for procreation is 0 when weight is 0."""
        herb = Herbivore()
        carn = Carnivore()

        Herbivore.set_parameters()
        Carnivore.set_parameters()

        herb.weight = 0
        carn.weight = 0

        assert herb.prob_procreation(10) == 0
        assert carn.prob_procreation(13) == 0

    def test_fitness(self):
        """Tests if the formula for evaluating fitness works."""
        a = Herbivore()
        a.set_parameters()
        a.weight = 10
        a.age = 2
        assert a.fitness == pytest.approx(0.49975)

    def test_prob_death_is_callable(self):
        """Property prob_death is callable."""
        Herbivore.set_parameters()
        Carnivore.set_parameters()

        Herbivore.prob_death
        Carnivore.prob_death


class TestHerbivore:
    """Tests for subclass Herbivore."""
    def test_constructor_default(self):
        """Default constructor callable."""
        a = Herbivore()
        assert isinstance(a, Herbivore)

    def test_default_parameters(self):
        """Test if default parameters are given."""
        a = Herbivore()
        assert a.age == 0
        assert a.weight == 10
        assert a._fitness is None

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
        assert a.F == 10.0

    def test_zero_weight_gives_zero_fitness(self):
        """Fitness is zero if weight is zero. """
        a = Herbivore(weight=0)
        assert a.fitness == 0.0


class TestCarnivore:
    """Tests for subclass Carnivore"""
    def test_constructor_default(self):
        """Default constructor callable."""
        a = Carnivore()
        assert isinstance(a, Carnivore)

    def test_default_parameters(self):
        """Tests if default parameters are given."""
        a = Carnivore()
        assert a.age == 0
        assert a.weight == 10

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
        assert a.F == 50.0
        assert a.DeltaPhiMax == 10.0

    def test_delta_phi_max_value_error(self):
        """Test that delta phi max must be strictly positive."""
        with pytest.raises(ValueError):
            a = Carnivore()
            a.set_parameters(DeltaPhiMax=0)
            a.set_parameters(DeltaPhiMax=-2)

    def test_value_error_for_mu(self):
        """Test that mu can not be greater than 1."""
        with pytest.raises(ValueError):
            a = Carnivore()
            a.set_parameters(mu=2)
