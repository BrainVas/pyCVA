# test_register_basic.py

import sys
import numpy as np
import pydicom
import pytest
import SimpleITK as sitk
import ants


import registration.prepost_registration as pr
import utils.utils as utils

# make sure we can import your code
import os
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(project_root)

from registration.prepost_registration import register, register_to_postEVT, parse_args

## DICOM_PATH = "<your_dicom_path_here>"

ds = pydicom.dcmread(DICOM_PATH)
arr = ds.pixel_array.astype(np.float32)
fixed = np.ndarray((64, 64), dtype=np.uint8)
moving = np.ndarray((64, 64), dtype=np.uint8)
seq = np.ndarray((5, 64, 64), dtype=np.uint8)
seq2 = np.ndarray((4, 64, 64), dtype=np.uint8)

def test_register():

    out = register(fixed, moving)
    assert isinstance(out, tuple) and len(out) == 2

    metric_value, transform_map = out
    assert isinstance(metric_value, float)
    assert transform_map is not None

def read_sequence(fp):
    ds, pixel_spacing = utils.read_sequence(fp)  
    return ds, pixel_spacing

def test_register_to_postEVT(monkeypatch):
    seq1, sp1 = read_sequence(DICOM_PATH)
    seq2, sp2 = read_sequence(DICOM_PATH)

    seq_fixed  = np.tile(seq1,  (5, 1, 1))
    seq_moving = np.tile(seq2,  (5, 1, 1))

    class DummyMetric:
        def __init__(self, *args, **kwargs): pass
        def get_value(self):        return 0.0

    monkeypatch.setattr(ants, "create_ants_metric",
                        lambda fixed, mov, metric_type: DummyMetric())

    
    pre_aligned, post = pr.register_to_postEVT(seq_fixed, seq_moving)


    assert isinstance(pre_aligned, np.ndarray)
    assert isinstance(post, np.ndarray)
    assert pre_aligned.shape == seq_fixed.shape
    assert post.shape       == seq_moving.shape

def test_parse_args(monkeypatch):
    monkeypatch.setattr(sys, "argv", ["prog", "fixed.npy", "moving.npy"])
    args = parse_args()
    assert args.fixed == "fixed.npy"
    assert args.moving == "moving.npy"
    


if __name__ == "__main__":
    test_register()
    test_parse_args()
    test_register_to_postEVT()
    print("All tests completed!")