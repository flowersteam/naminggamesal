from __future__ import absolute_import, division, print_function
import unittest
import random
import numpy as np

import dotdot
import lib
from lib.ngvoc import Vocabulary


random.seed(0)

class TestAdd(unittest.TestCase):

    def _voc_equal(self, v1, v2):
        np.testing.assert_array_equal(v1.get_content(), v2.get_content())

    def _nonzero_equal(self, v, nonzeros):
        """Verify that non-zeros in vocabulary `v` are the same as in `nonzeros`"""
        nz = np.nonzero(np.array(v.get_content()))
        nz_set = set()
        for i, j in zip(*nz):
                nz_set.add((i, j))
        self.assertEqual(nz_set, set([tuple(e) for e in nonzeros]))

    def test_add(self):
        """Test that add works ok"""
        M, W = 5, 10
        voc = Vocabulary(voc_type='matrix', M=M, W=W)
        np.testing.assert_array_equal(voc.get_content(), np.zeros((M, W)))
        voc.add(3, 4, 1)
        self._nonzero_equal(voc, [(3, 4)])
        voc.add(2, 3, 1)
        self._nonzero_equal(voc, [(3, 4), (2, 3)])
        voc.add(3, 3, 1)
        self._nonzero_equal(voc, [(3, 4), (2, 3), (3, 3)])

        # testing random additions
        voc = Vocabulary(voc_type='matrix', M=M, W=W)
        nonzeros = set()
        for _ in range(100):
            i, j = random.randint(0, M-1), random.randint(0, W-1)
            voc.add(i, j, 1)
            nonzeros.add((i, j))
            i, j = random.randint(0, M-1), random.randint(0, W-1)
            voc.add(i, j, 0)
            nonzeros.discard((i, j))
            self._nonzero_equal(voc, nonzeros)

    def test_add_coherent(self):
        """Test that all implementations are coherent"""
        M, W = 5, 10
        vocs = []
        for classname in lib.ngvoc.voc_class:
            vocs.append(Vocabulary(voc_type=classname, M=M, W=W))
        for v in vocs:
            self._voc_equal(vocs[0], v)
        for v in vocs:
            v.add(3, 4, 1)

if __name__ == '__main__':
    unittest.main()
