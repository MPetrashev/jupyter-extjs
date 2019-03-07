import unittest
import numpy.polynomial.chebyshev as cheb
from chebyshev.Chebyshev import Chebyshev
import numpy as np

from chebyshev.blacksholes import call_price


class ChebyshevTest(unittest.TestCase):

    def testBlackScholes(self):
        price = call_price(23.75, 15., 0.01, 0.35, 0.5)
        # See: https://www.mystockoptions.com/black-scholes.cfm?s=23.75&x=15&t=0.5&r=1%25&v=35%25&calculate=Calculate
        self.assertAlmostEqual(8.879159263714124, price, delta=0.001)

    def test1D_BlackScholes(self):
        x_r_sigma_t = [15., 0.01, 0.35,  0.5]
        obj = cheb.Chebyshev.interpolate(np.vectorize(call_price), 25, [0, 100], x_r_sigma_t)
        price = call_price(23.75, *x_r_sigma_t)
        self.assertAlmostEqual(price, obj(23.75), delta=0.001)

    def test2D_BlackScholes(self):
        f = lambda s, sigma: call_price(s, 15., 0.01, sigma, 0.5)
        obj = Chebyshev.interpolate(np.vectorize(f), 25, [[10, 100], [0.1, 1.]])
        price = obj(23.75, 0.35)
        self.assertAlmostEqual(8.879159263714124, price, delta=0.001)
