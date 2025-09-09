# test_motion_correction.py

import os
import sys
import numpy as np
import pydicom
import SimpleITK as sitk

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(project_root)

from registration.motion_correction import mc_image_pair, mc_sequence

## DICOM_PATH = "<your_dicom_path_here>"

ds = pydicom.dcmread(DICOM_PATH)
arr = ds.pixel_array.astype(np.float32)
fixed = sitk.GetImageFromArray(arr)
moving = sitk.GetImageFromArray(arr) 
seq = np.stack([arr for _ in range(5)], axis=0)


def test_mc_image_pair_basic():

    aligned_np, transform_params = mc_image_pair(
        fixed_image=fixed,
        moving_image=moving,
        transform='affine',          
        resolution=6,                
        metric=None,                 
        n_iteration=None             
    )

    assert isinstance(aligned_np, np.ndarray)
    assert aligned_np.shape == sitk.GetArrayFromImage(fixed).shape
    assert isinstance(transform_params, (list, tuple))
    assert aligned_np is not None
    assert transform_params is not None


def test_mc_sequence_roundtrip():

    aligned_seq = mc_sequence(seq)
    assert isinstance(aligned_seq, np.ndarray)
    assert aligned_seq.shape == seq.shape
    assert aligned_seq is not None

if __name__ == "__main__":

    test_mc_image_pair_basic()
    test_mc_sequence_roundtrip()
    print("All tests completed!")