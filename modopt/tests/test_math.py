# -*- coding: utf-8 -*-

"""UNIT TESTS FOR MATH

This module contains unit tests for the modopt.math module.

:Author: Samuel Farrens <samuel.farrens@cea.fr>

"""

from unittest import TestCase
import numpy as np
import numpy.testing as npt
from modopt.math import *


class ConvolveTestCase(TestCase):

    def setUp(self):

        self.data1 = np.arange(18).reshape(2, 3, 3)
        self.data2 = self.data1 + 1

    def tearDown(self):

        self.data1 = None
        self.data2 = None

    def test_convolve_astropy(self):

        npt.assert_allclose(convolve.convolve(self.data1[0], self.data2[0],
                            method='astropy'),
                            np.array([[210., 201., 210.], [129., 120., 129.],
                                     [210., 201., 210.]]),
                            err_msg='Incorrect convolution: astropy')

        npt.assert_raises(ValueError, convolve.convolve, self.data1[0],
                          self.data2)

        npt.assert_raises(ValueError, convolve.convolve, self.data1[0],
                          self.data2[0], method='bla')

    def test_convolve_scipy(self):

        npt.assert_allclose(convolve.convolve(self.data1[0], self.data2[0],
                            method='scipy'),
                            np.array([[14., 35., 38.], [57., 120., 111.],
                                     [110., 197., 158.]]),
                            err_msg='Incorrect convolution: scipy')

    def test_convolve_stack(self):

        npt.assert_allclose(convolve.convolve_stack(self.data1, self.data2),
                            np.array([[[210., 201., 210.],
                                      [129., 120., 129.],
                                      [210., 201., 210.]],
                                     [[1668., 1659., 1668.],
                                      [1587., 1578., 1587.],
                                      [1668., 1659., 1668.]]]),
                            err_msg='Incorrect convolution: stack')

    def test_convolve_stack_rot(self):

        npt.assert_allclose(convolve.convolve_stack(self.data1, self.data2,
                            rot_kernel=True),
                            np.array([[[150., 159., 150.], [231., 240., 231.],
                                      [150., 159., 150.]],
                                     [[1608., 1617., 1608.],
                                      [1689., 1698., 1689.],
                                      [1608., 1617., 1608.]]]),
                            err_msg='Incorrect convolution: stack rot')


class MatrixTestCase(TestCase):

    def setUp(self):

        self.data1 = np.arange(9).reshape(3, 3)
        self.data2 = np.arange(3)
        self.data3 = np.arange(6).reshape(2, 3)
        np.random.seed(1)
        self.pmInstance1 = matrix.PowerMethod(lambda x: x.dot(x.T),
                                              self.data1.shape, verbose=True)
        np.random.seed(1)
        self.pmInstance2 = matrix.PowerMethod(lambda x: x.dot(x.T),
                                              self.data1.shape, auto_run=False,
                                              verbose=True)
        self.pmInstance2.get_spec_rad(max_iter=1)

    def tearDown(self):

        self.data1 = None
        self.data2 = None

    def test_gram_schmidt_orthonormal(self):

        npt.assert_allclose(matrix.gram_schmidt(self.data1),
                            np.array([[0., 0.4472136, 0.89442719],
                                     [0.91287093, 0.36514837, -0.18257419],
                                     [-1., 0., 0.]]),
                            err_msg='Incorrect Gram-Schmidt: orthonormal')

        npt.assert_raises(ValueError, matrix.gram_schmidt, self.data1,
                          return_opt='bla')

    def test_gram_schmidt_orthogonal(self):

        npt.assert_allclose(matrix.gram_schmidt(self.data1,
                            return_opt='orthogonal'),
                            np.array([[0.00000000e+00, 1.00000000e+00,
                                       2.00000000e+00],
                                      [3.00000000e+00, 1.20000000e+00,
                                       -6.00000000e-01],
                                      [-1.77635684e-15, 0.00000000e+00,
                                       0.00000000e+00]]),
                            err_msg='Incorrect Gram-Schmidt: orthogonal')

    def test_gram_schmidt_both(self):

        npt.assert_allclose(matrix.gram_schmidt(self.data1, return_opt='both'),
                            (np.array([[0.00000000e+00, 1.00000000e+00,
                                        2.00000000e+00],
                                       [3.00000000e+00, 1.20000000e+00,
                                        -6.00000000e-01],
                                       [-1.77635684e-15, 0.00000000e+00,
                                       0.00000000e+00]]),
                             np.array([[0., 0.4472136, 0.89442719],
                                      [0.91287093, 0.36514837, -0.18257419],
                                      [-1., 0., 0.]])),
                            err_msg='Incorrect Gram-Schmidt: both')

    def test_nuclear_norm(self):

        npt.assert_almost_equal(matrix.nuclear_norm(self.data1),
                                15.49193338482967,
                                err_msg='Incorrect nuclear norm')

    def test_project(self):

        npt.assert_array_equal(matrix.project(self.data2, self.data2 + 3),
                               np.array([0., 2.8, 5.6]),
                               err_msg='Incorrect projection')

    def test_rot_matrix(self):

        npt.assert_allclose(matrix.rot_matrix(np.pi / 6),
                            np.array([[0.8660254, -0.5],
                                      [0.5, 0.8660254]]),
                            err_msg='Incorrect rotation matrix')

    def test_rotate(self):

        npt.assert_array_equal(matrix.rotate(self.data1, np.pi / 2),
                               np.array([[2, 5, 8], [1, 4, 7], [0, 3, 6]]),
                               err_msg='Incorrect rotation')

        npt.assert_raises(ValueError, matrix.rotate, self.data3, np.pi / 2)

    def test_PowerMethod_converged(self):

        npt.assert_almost_equal(self.pmInstance1.spec_rad,
                                0.90429242629600837,
                                err_msg='Incorrect spectral radius: converged')

        npt.assert_almost_equal(self.pmInstance1.inv_spec_rad,
                                1.1058369736612865,
                                err_msg='Incorrect inverse spectral radius: '
                                        'converged')

    def test_PowerMethod_unconverged(self):

        npt.assert_almost_equal(self.pmInstance2.spec_rad,
                                0.92048833577059219,
                                err_msg='Incorrect spectral radius: '
                                        'unconverged')

        npt.assert_almost_equal(self.pmInstance2.inv_spec_rad,
                                1.0863798715741946,
                                err_msg='Incorrect inverse spectral radius: '
                                        'unconverged')


class StatsTestCase(TestCase):

    def setUp(self):

        self.data1 = np.arange(9).reshape(3, 3)
        self.data2 = np.arange(18).reshape(2, 3, 3)

    def tearDown(self):

        self.data1 = None

    def test_gaussian_kernel_max(self):

        npt.assert_allclose(stats.gaussian_kernel(self.data1.shape, 1),
                            np.array([[0.36787944, 0.60653066, 0.36787944],
                                      [0.60653066, 1., 0.60653066],
                                      [0.36787944, 0.60653066, 0.36787944]]),
                            err_msg='Incorrect gaussian kernel: max norm')

        npt.assert_raises(ValueError, stats.gaussian_kernel, self.data1.shape,
                          1, norm='bla')

    def test_gaussian_kernel_sum(self):

        npt.assert_allclose(stats.gaussian_kernel(self.data1.shape, 1,
                            norm='sum'),
                            np.array([[0.07511361, 0.1238414, 0.07511361],
                                      [0.1238414, 0.20417996, 0.1238414],
                                      [0.07511361, 0.1238414, 0.07511361]]),
                            err_msg='Incorrect gaussian kernel: sum norm')

    def test_gaussian_kernel_none(self):

        npt.assert_allclose(stats.gaussian_kernel(self.data1.shape, 1,
                            norm='none'),
                            np.array([[0.05854983, 0.09653235, 0.05854983],
                                      [0.09653235, 0.15915494, 0.09653235],
                                      [0.05854983, 0.09653235, 0.05854983]]),
                            err_msg='Incorrect gaussian kernel: sum norm')

    def test_mad(self):

        npt.assert_equal(stats.mad(self.data1), 2.0,
                         err_msg='Incorrect median absolute deviation')

    def test_mse(self):

        npt.assert_equal(stats.mse(self.data1, self.data1 + 2), 4.0,
                         err_msg='Incorrect mean squared error')

    def test_psnr_starck(self):

        npt.assert_almost_equal(stats.psnr(self.data1, self.data1 + 2),
                                12.041199826559248,
                                err_msg='Incorrect PSNR: starck')

        npt.assert_raises(ValueError, stats.psnr, self.data1, self.data1,
                          method='bla')

    def test_psnr_wiki(self):

        npt.assert_almost_equal(stats.psnr(self.data1, self.data1 + 2,
                                method='wiki'),
                                42.110203695399477,
                                err_msg='Incorrect PSNR: wiki')

    def test_psnr_stack(self):

        npt.assert_almost_equal(stats.psnr_stack(self.data2, self.data2 + 2),
                                12.041199826559248,
                                err_msg='Incorrect PSNR stack')

        npt.assert_raises(ValueError, stats.psnr_stack, self.data1, self.data1)

    def test_sigma_mad(self):

        npt.assert_almost_equal(stats.sigma_mad(self.data1),
                                2.9651999999999998,
                                err_msg='Incorrect sigma from MAD')
