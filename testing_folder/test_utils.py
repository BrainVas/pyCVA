import pydicom
import sys, os

from pycva.AutoTICI import autotici

autoTICI_instance = autotici.autotici()

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.append(project_root)

ds = pydicom.dcmread("input_images\R0160\SN4_Vap_SOP1.3.6.1.4.1.40744.9.96512919107112378459801894939320275800.dcm")
img = ds.pixel_array

def test_normalize():
    result = autoTICI_instance.normalize(img)
    assert result is not None

def test_normalize_0_1():
    result = autoTICI_instance.normalize_0_1(img)
    assert result is not None

def test_remove_text_and_border():
    result = autoTICI_instance.remove_text_and_border(img)
    assert result is not None

def test_minip():
    seq = np.stack([img]*5, axis=0)
    result = autoTICI_instance.minip(seq, axis=0)
    assert result.shape == img.shape

def test_read_sequence():
    seq, spacing = autoTICI_instance.read_sequence(ds.filename)
    assert seq is not None
    assert spacing is not None

def test_get_pixel_spacing_from_header():
    spacing = autoTICI_instance.get_pixel_spacing_from_header(ds)
    assert spacing is not None

def test_resize_to_1024():
    img2d = img
    if img2d.ndim == 3:
        img2d = img2d[0]          
    seq = np.stack([img2d]*3, axis=0)
    resized_seq, new_spacing = autoTICI_instance.resize_to_1024(seq, pixel_spacing=0.5)
    assert resized_seq.shape[1:] == (1024, 1024)
    assert new_spacing is not None

#test_extract_skull_mask(sequence)
def test_extract_skull_mask():
    seq = np.stack([img]*3, axis=0)
    skull_img, background, mask = autoTICI_instance.extract_skull_mask(seq)
    assert skull_img.shape == img.shape
    assert mask.shape == img.shape

def test_binarize_image():
    result = autoTICI_instance.binarize_image(img.astype(np.uint8))
    assert result[1] is not None

def test_truncate():
    truncated = autoTICI_instance.truncate(img.copy(), 30, 200)
    assert np.all(truncated >= 30) and np.all(truncated <= 200)

def test_pad_image():
    img2d = img
    if img2d.ndim == 3:
        img2d = img2d[0]          
    padded = autoTICI_instance.pad_image(img2d, to=1024)
    assert padded.shape == (1024, 1024)

def test_pad_sequence():
    img2d = img
    if img2d.ndim == 3:
        img2d = img2d[0]          
    seq = np.stack([img2d]*3, axis=0)
    padded_seq = autoTICI_instance.pad_sequence(seq, to=1024)
    assert padded_seq.shape[1:] == (1024, 1024)

def test_resize_to_target_spacing():
    img2d = img
    if img2d.ndim == 3:
        img2d = img2d[0]           
    seq = np.stack([img2d]*3, axis=0)
    resized = autoTICI_instance.resize_to_target_spacing(seq, pixel_spacing=0.5, target_spacing=0.25)
    assert resized is not None



