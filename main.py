#%% Imports

import napari
import numpy as np
from skimage import io 
from pathlib import Path
from pystackreg import StackReg

#%% Inputs

stack_name = 'C1-OH99 180521 1001.tif'

#%% Open data

stack = io.imread(Path('data', stack_name))

#%% Registration

sr = StackReg(StackReg.RIGID_BODY)
stack_reg = sr.register_transform_stack(stack, reference='previous') 

#%%



#%% Display

viewer = napari.Viewer()
viewer.add_image(stack_reg)