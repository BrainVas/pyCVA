import pydicom
import sys, os
import numpy
import natsort
import pandas as pd
from collections import namedtuple

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(project_root)

from prepare_data import *
import input_paths

## ds = pydicom.dcmread("<your_dicom_path_here>")
img = ds.pixel_array

def test_normalize():
    result = normalize(img)
    assert isinstance(result, np.ndarray)
    assert result.dtype == np.uint8
    assert result.min() >=   0 and result.max() <= 255

def test_cut_seq():
    seq = np.stack([img]*25, axis=0)
    maxLength = 20
    result = cut_seq(seq, maxLength)
    assert isinstance(result, np.ndarray) 
    assert result.shape[0] == maxLength

#def test_prepare_sequence_and_minip_reads_real_file():

   
    #df_info = pd.read_csv(input_paths.patient_info_csv)
    #df_train = df_info[df_info['patient_id'].isin(train_patients)]

    #for idx, row in enumerate(df_train.itertuples()):
    #    prepare_sequence_and_minip(row, mode='train')
    #    prepare_masks(row, mode='train')

    #raw_len = prepare_sequence_and_minip(row, mode="test")
    #assert raw_len is not None

#def test_prepare_masks():
    
#Last two perspective tests are on functionality that is seemingly not complete or used within the main fucntionality of the tool. 
