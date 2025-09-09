import numpy
import scipy
import cv2          
import pydicom
import SimpleITK      
import ants
import ast
from tqdm import tqdm
from skimage.segmentation import watershed
from scipy.ndimage import binary_opening, uniform_filter
from scipy.ndimage import binary_fill_holes 
from scipy.stats import mode
from skimage.morphology import (
    binary_dilation,
    disk,
    remove_small_objects,
    binary_closing,
    remove_small_holes,
)
from skimage.transform import resize
from skimage.filters import frangi
from pathlib import Path

print("Everything is running fine")