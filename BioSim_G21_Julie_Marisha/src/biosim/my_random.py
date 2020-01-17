# -*- coding: utf-8 -*-

import numpy


class Random:
    def __init__(self):
        random_num = None

    def draw_random(self, p):
        p = [1-p, p]
        random_num = numpy.random.choice(2, p=p)
        return random_num

    """ Alternativ:
        random_num = numpy.binomial(1, p)
    """