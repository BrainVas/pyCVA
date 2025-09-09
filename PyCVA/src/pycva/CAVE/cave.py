# Add all the methods the user can use with a cave_dsa object
from . import cave_wrapper
from . import prepare_data
import sys
import os

class cave():
        
    def __init__(self):
        """
        Initializes the Cave wrapper.
        """
        self._cave_wrapper = None


            
    @property
    def cave_wrapper(self):
        """
        This method ONLY runs when someone accesses self.cave_wrapper
        """
        if self._cave_wrapper is None:
            self._cave_wrapper = cave_wrapper.cave_wrapper()
        return self._cave_wrapper

        

    def run_cave(self, *args, **kwargs):
        """
        Runs the tool using Docker or Singularity, based on what is installed.

        Args:
            input_dicom_dir (str): Directory containing input DICOM files.
            output_masks_dir (str): Directory to store output masks.
            checkpoints_dir (str): Directory containing model checkpoints (minip_av_sigmoid_image512_charmed-cosmos-1086.pt,minip_av_sigmoid_image1024_valiant-resonance-1199.pt, minip_vessel_sigmoid_image512_polished-lake-1078.pt, 
                                    minip_vessel_sigmoid_image1024_solar-resonance-1172.pt, sequence_av_sigmoid_image512_ConvGRU_logical-star-1097.pt, sequence_vessel_sigmoid_image512_ConvGRU_devoted-pine-1024.pt ).
            input_file (str): Input DICOM filename.
            output_file (str): Output mask filename.
            model_file (str): Model file name.
            input_type (str): Input type for the model
            label_type (str): Label type for training.
            img_size (int): Image resolution.
            rnn (str): RNN type (e.g., 'ConvGRU').
            rnn_kernel (int): Kernel size for the RNN.
            rnn_layers (int): Number of RNN layers.
            amp (bool): Whether to use automatic mixed precision.
        Returns:
            Returns a/multiple images depending on chosen model that depicts the input DCM's veins or arteries.

        Raises:
            RuntimeError: If neither Docker nor Singularity is installed.
            RuntimeError: non-zero exit status 127. (Start up Docker)
        """
        return self.cave_wrapper.run(*args, **kwargs)

    
    def cut_seq(self, seq, max_len):
        """
        Recursively trims a sequence to a maximum length by removing frames with lower contrast.

        If the sequence length exceeds `max_len`, the function compares the sum of pixel values
        of the first and last frames and removes the frame with the smaller sum (assumed to have
        less contrast). This process repeats recursively until the sequence length is at most `max_len`.

        Args:
            seq (numpy.ndarray): Input sequence of shape (frames, ...), e.g. (N, height, width).
            max_len (int): Maximum allowed length for the sequence.

        Returns:
            numpy.ndarray: Trimmed sequence with length less than or equal to `max_len`.
        """
        return prepare_data.cut_seq(seq, max_len)