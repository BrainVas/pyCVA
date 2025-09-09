# Add all the methods the user can use with an autoTICI object

from . import autotici_wrapper
from . import phase_predict_wrapper

from .utils import utils
import sys
import os



  
class autotici():
    """
    This class provides an interface for processing medical images with functionality from AutoTICI,
    and utility functions for analysing cerebral angiographic sequences.
    """

    def __init__(self):
        """
        Initializes the AutoTICI as none to allow lazy loading later on.
        """
        self._autotici_wrapper = None  
        self._phase_predict_wrapper = None

    @property
    def autotici_wrapper(self):
        """
        This method ONLY runs when someone accesses self.autotici_wrapper
        """
        if self._autotici_wrapper is None:
            self._autotici_wrapper = autotici_wrapper.autotici_wrapper()
        return self._autotici_wrapper

    @property  
    def phase_predict_wrapper(self):
        """
        This method ONLY runs when someone accesses self.phase_predict_wrapper
        """
        if self._phase_predict_wrapper is None:
            self._phase_predict_wrapper = phase_predict_wrapper.phase_predict_wrapper()
        return self._phase_predict_wrapper


# Containerised functionality
    def run_autoTICI(self, *args, **kwargs):
        """
        Runs the tool using Docker or Singularity, based on what is installed. 

        Args:
            pre_image (str): Path to the PreEVT DICOM file.
            post_image (str): Path to the PostEVT DICOM file.
            occ (str): Occlusion site label (e.g. M1, ICA or M2).
            output_dir (str): Path to the output directory.
            model_dir (str, optional): Path to the directory containing model files. Defaults to None.
            motion_correction (bool, optional): Enable motion correction. Defaults to False.
            preregistration (bool, optional): Enable preregistration. Defaults to False.
            view (str, optional): Specific angiographic view to use. Defaults to None.

        Returns:
            Creates an img called ``pipeline.png`` in the chosen directory (output_dir).

        Raises:
            RuntimeError: If neither Docker nor Singularity is installed
            RuntimeError: non-zero exit status 127. (Start up Docker)
        
        """
        return self.autotici_wrapper.run(*args, **kwargs)


    def run_phase_predict(self, *args, **kwargs):
        """
        Runs the tool using Docker or Singularity, based on what is installed. 

        Args:
            dicom_path (str): Path to the input DICOM file.
            output_dir (str): Output directory for prediction results.
            model_dir (str, optional): Directory containing the model.
        Returns:
            Returns a JSON file representing the predicted brain phases in the chosen output directory (output_dir)

        Raises:
            RuntimeError: If neither Docker nor Singularity is installed.
            RuntimeError: non-zero exit status 127. (Start up Docker)
        """
        return self.phase_predict_wrapper.run(*args, **kwargs)


   # Utils.py
    def normalize(self, img):
         """
         Normalise image values to range [0, 255] using OpenCV normalization.

         Args:
            img (numpy.ndarray): Input image or sequence.

         Returns:
            numpy.ndarray: Normalized image with values in range [0, 255] as uint8.
         """
         return utils.normalize(img)


    def normalize_0_1(self, img):
         """
         Normalize image values to the range [0, 1] using OpenCV normalization.

         Args:
            img (numpy.ndarray): Input image or sequence.

         Returns:
            numpy.ndarray: Image normalized to [0, 1] range as float32.
         """
         return utils.normalize_0_1(img)


    def remove_text_and_border(self, in_img):
         """
         Args:
            in_img (numpy.ndarray): Input image (2D) or sequence (3D).

         Returns:
            numpy.ndarray: Processed image with text and borders removed.

         Note:
            Can add any quirks for the method in here
         """
         return utils.remove_text_and_border(in_img)


    def minip(self, img_seq, axis=0):
         """
         Compute minimum intensity projection along specified axis.

         Creates a 2D projection by taking the minimum intensity value
         along the specified axis of a 3D image sequence.

         Args:
            img_seq (numpy.ndarray): Image sequence.
            axis (int, optional): Axis along which to compute projection. Defaults to 0.

         Returns:
            numpy.ndarray: Minimum intensity projection image.
         """
         return utils.minip(img_seq, axis)


    def read_sequence(self, fp):
         """
         Read DICOM image sequence from file path.

         Reads a DICOM file and extracts both the pixel array and pixel spacing
         information. Handles both 2D and 3D sequences, expanding 2D to 3D if needed.

         Args:
            fp (str): File path to DICOM sequence.

         Returns:
            tuple (numpy.ndarray, float): Tuple of (image_sequence, pixel_spacing).
         """
         return utils.read_sequence(fp)


    def get_pixel_spacing_from_header(self, ds):
         """
         Extract pixel spacing information from DICOM header.

         Attempts to extract pixel spacing using multiple fallback methods:
         1. Direct PixelSpacing tag
         2. Calculated from DistanceSourceToDetector, DistanceSourceToPatient, and ImagerPixelSpacing
         3. Returns NaN if unavailable

         Args:
            ds (pydicom.Dataset): DICOM dataset object.

         Returns:
            float: Pixel spacing value (first element if array) or NaN if unavailable.
         """
         return utils.get_pixel_spacing_from_header(ds)


    def resize_to_1024(self, seq, pixel_spacing):
         """
         Resize sequence to 1024x1024 maintaining aspect ratio and updating pixel spacing.

         First pads the sequence to square dimensions, then resizes to 1024x1024.
         Updates pixel spacing proportionally based on the resize factor.

         Args:
            seq (numpy.ndarray): Input sequence.
            pixel_spacing (float): Current pixel spacing value.

         Returns:
            tuple (numpy.ndarray, float): Tuple of (resized_sequence, updated_pixel_spacing).
         """
         return utils.resize_to_1024(seq, pixel_spacing)


    def extract_skull_mask(self, sequence):
         """
         Extract skull mask from image sequence using temporal analysis.

         Creates a minimum intensity projection and identifies background regions
         by analyzing pixel value consistency across frames. Returns skull-masked
         image with background regions set to 0.

         Args:
            sequence (numpy.ndarray): Input image sequence.

         Returns:
            tuple (numpy.ndarray, float, numpy.ndarray): Tuple of (skull_masked_minip, background_intensity, background_mask).
         """
         return utils.extract_skull_mask(sequence)


    def binarize_image(self, img, thresh=0):
         """
         Convert image to binary using threshold or Otsu's method.

         If thresh=0, uses Otsu's automatic thresholding. Otherwise uses
         the specified threshold value. Input image must be uint8.

         Args:
            img (numpy.ndarray): Input image (must be uint8).
            thresh (float, optional): Threshold value for binarization (0 for Otsu's method). Defaults to 0.

         Returns:
            tuple (float, numpy.ndarray): Tuple of (threshold_value, binary_image).
         """
         return utils.binarize_image(img, thresh)


    def truncate(self, img, img_min=0, img_max=255):
         """
         Clip image values to specified range in-place.

         Modifies the input image directly by setting values below img_min to img_min
         and values above img_max to img_max.

         Args:
            img (numpy.ndarray): Input image (modified in-place).
            img_min (float, optional): Minimum value for clipping. Defaults to 0.
            img_max (float, optional): Maximum value for clipping. Defaults to 255.

         Returns:
            numpy.ndarray: Clipped image (same as input, modified in-place).
         """
         return utils.truncate(img, img_min, img_max)


    def pad_image(self, img, to=1024, cval=None):
         """
         Pad image to specified size using constant value padding.

         Centers the image in the target size by adding equal padding on opposite sides.
         If cval is None, uses the mode (most frequent value) of the image.

         Args:
            img (numpy.ndarray): Input image.
            to (int, optional): Target size for padding. Defaults to 1024.
            cval (float, optional): Constant value for padding (None for image mode). Defaults to None.

         Returns:
            numpy.ndarray: Padded image.
         """
         return utils.pad_image(img, to, cval)


    def pad_sequence(self, seq, to=1024):
         """
         Pad image sequence to specified size.

         Args:
            seq (numpy.ndarray): Input 3D image sequence.
            to (int, optional): Target size for padding. Defaults to 1024.

         Returns:
            numpy.ndarray: Padded image sequence.
         """
         return utils.pad_sequence(seq, to)


    def resize_to_target_spacing(self, seq, pixel_spacing, target_spacing=None):
      """
      Resize image sequence to achieve a target pixel spacing with cropping or padding.

      Resizes the image sequence so that the pixel spacing matches the desired target spacing.
      If the resized image is smaller than 1024x1024, it is padded to 1024.
      If larger, it is center-cropped to 1024.
      If `target_spacing` is None or equal to `pixel_spacing`, no resizing is performed.

      Args:
         seq (numpy.ndarray): Input image sequence.
         pixel_spacing (float): Current pixel spacing value.
         target_spacing (float, optional): Desired pixel spacing. Defaults to None.

      Returns:
         tuple (numpy.ndarray, float): Tuple of (resized_sequence, updated_pixel_spacing).

      """
      return utils.resize_to_target_spacing(seq, pixel_spacing, target_spacing)