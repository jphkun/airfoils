#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
import os
import numpy as np
import numpy.testing as npt
import matplotlib.pyplot as plt
from airfoils import Airfoil, NACADefintionError

class TestNACA4(unittest.TestCase):

    def test_constructor_NACA4(self):
        #Test NACA 4-series constructor

        naca1234 = Airfoil.NACA4('1234')

        wrong_naca_IDs = [
            'very_wrong',
            '12345',
            'NACA1234',
        ]

        for wrong_naca_ID in wrong_naca_IDs:
            with self.assertRaises(NACADefintionError):
                Airfoil.NACA4(wrong_naca_ID)

    def compares_NACA4_with_file(self,name):
        """
        Tests NACA4 airfoil computed with this module and comapres it with data
        points from http://airfoiltools.com/
        """
        foil = Airfoil.NACA4(name)
        filename = 'naca' + name + '.dat'
        path = os.path.join('airfoil_files/',filename)

        precition = 6
        points_from_file = np.loadtxt(path,skiprows=1)
        points_from_file = np.around(points_from_file,precition)
        N = len(points_from_file)

        points = np.empty([N,2])
        upper = True
        error = []
        
        for p in zip(points,points_from_file):
            if upper:
                res = foil.y_upper(p[1][0])
                res_rounded = np.around(res,decimals=precition)
            else:
                res = foil.y_lower(p[1][0])
                res_rounded = np.around(res,decimals=precition)

            # Finds when to switch to lower surface
            if upper and p[1][0] == 0.:
                upper = False

            p[0][0] = p[1][0]
            p[0][1] = res_rounded
            tab = np.array([p[1][0],res_rounded])
            err = res_rounded - p[1][1]
            error.append(err)
                            
        points_reshaped = np.reshape(points,(1,2*N))
        points_from_file_reshaped = np.reshape(points_from_file,(1,2*N))
        
        test = npt.assert_almost_equal(points,
                                       points_from_file,
                                       decimal=2)
        # TODO: There is probably a better way
        if test is None:
            test = True
        else:
            test = False
        
        self.assertTrue(test)
        return error

    def test_NACA4_with_file(self):
        """
        OKTODO: test linear spacing (PASS if not edgecase)
        TODO:   test cosine spacing
        TODO:   get digit precition form the file for error consistancy
        TODO:   implement close trailing edge
        TODO:   Add NACA 4 digits boundaries

        Comment: For classical naca profiles the error is really slim and
        seems acceptable. But regarding edgcases, there definitly is some
        improuvements to make.
        """
        
        # Test parameters
        verbose = False
        plotting = False
        profiles = [
            '0024',
            '1408',
            '1410',
            '1412',
            '2408',
            '2410',
            '2411',
            '2412',
            '2418',
            '2421',
            '2424',
            '2512',
            '2930',
            '4412',
            '4415', 
            '4418',
            '4421', 
            '4424',
            '6409',
            '6412',
            '9930'
        ]
        
        errors = []
        for name in profiles:
            if verbose:
                print(f'Test of profile NACA{name}')
            err = self.compares_NACA4_with_file(name)
            errors.append(err) 
        
        # results processing 
        if plotting:
            plt.figure('Error plot')
            for i in zip(profiles,errors):
                plt.plot(i[1], label='NACA ' + i[0])
            plt.legend()
            plt.title('Error between module and www.airfoiltools.com')
            plt.show()

# TODO: assert that points have been created correctly
