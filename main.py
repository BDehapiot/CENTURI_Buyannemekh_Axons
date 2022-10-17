#%% Imports

import napari
import numpy as np
from skimage import io 
from pathlib import Path
from pystackreg import StackReg

#%% Inputs

stack_name = 'C1-OH99 180521 1001.tif'
# stack_name = 'C1-VBS685 140222 1001.tif'

#%% Make path & open data

stack_path = Path('data', stack_name)
edges_path = Path('data', str(stack_name).replace('.tif', '_edges.tif'))
stack = io.imread(stack_path)

#%% Registration

sr = StackReg(StackReg.RIGID_BODY)
stack_reg = sr.register_transform_stack(stack, reference='previous') 

#%% functions

def ranged_uint8(img, percent_low=1, percent_high=99):

    """ 
    Convert image to uint8 using a percentile range.
    
    Parameters
    ----------
    img : ndarray
        Image to be converted.
        
    percent_low : float
        Percentile to discard low values.
        Between 0 and 100 inclusive.
        
    percent_high : float
        Percentile to discard high values.
        Between 0 and 100 inclusive.
    
    Returns
    -------  
    img : ndarray
        Converted image.
    
    """

    # Get data type 
    data_type = (img.dtype).name
    
    if data_type == 'uint8':
        
        raise ValueError('Input image is already uint8') 
        
    else:
        
        # Get data intensity range
        int_min = np.percentile(img, percent_low)
        int_max = np.percentile(img, percent_high) 
        
        # Rescale data
        img[img<int_min] = int_min
        img[img>int_max] = int_max 
        img = (img - int_min)/(int_max - int_min)
        img = (img*255).astype('uint8')
    
    return img

#%%

from skimage import filters

edges = np.zeros_like(stack_reg)
for i, img in enumerate(stack_reg):
    edges[i,...] = filters.sobel(img)
    
# Display with napari    
viewer = napari.Viewer()
viewer.add_image(stack_reg)
viewer.add_image(edges)

# Save images
io.imsave(edges_path, ranged_uint8(edges, 0.1, 99.9), check_contrast=False)
