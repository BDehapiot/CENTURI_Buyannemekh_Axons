#%% Imports

import napari
import numpy as np
from skimage import io 
from pathlib import Path
from pystackreg import StackReg

#%% Inputs

# stack_name = 'C1-OH99 180521 1001.tif'
stack_name = 'C1-VBS685 140222 1001.tif'

#%% Make path & open data

stack_path = Path('data', stack_name)
stack_reg_path = Path( 

stack = io.imread(stack_path)

#%% Registration

sr = StackReg(StackReg.RIGID_BODY)
stack_reg = sr.register_transform_stack(stack, reference='previous') 

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
io.imsave(stack_path.name, '_reg.tif')
io.imsave(path, range_uint8(crop, int_range=0.99), check_contrast=False)
