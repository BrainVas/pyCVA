#test_transform_sequence(img_seq, transform_parameter_map)
#already tested in 
#test_transform_image(img, transform_parameter_map)
#not used anywhere??

#test_warp_sequence(img, transformation_matrix)

import numpy as np
import pytest
from numpy.testing import assert_array_equal
import registration.transformation as tr  

def test_warp_sequence_translation():
    seq = np.zeros((3, 10, 10), dtype=np.uint8)
    seq[0, 2, 3] = 255

    M = np.float32([[1, 0, 2],
                    [0, 1, 1]])

    out = tr.warp_sequence(seq.copy(), M)

    expected = np.zeros_like(seq)
    expected[0, 2+1, 3+2] = 255

    assert_array_equal(out, expected)
