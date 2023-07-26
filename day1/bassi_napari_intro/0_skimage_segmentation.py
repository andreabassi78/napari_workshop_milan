# -*- coding: utf-8 -*-
"""
Created on Sun Jan 16 14:07:53 2022

@author: andrea
"""

import napari
from skimage import data
from skimage.filters import threshold_otsu
from skimage.segmentation import clear_border
from skimage.measure import label
from skimage.morphology import closing, square, remove_small_objects

coins = data.coins()

# apply threshold
thresh = threshold_otsu(coins)
bw = closing(coins > thresh, square(4))

# remove artifacts connected to image border
cleared = remove_small_objects(clear_border(bw), 20)

# label image regions
label_image = label(cleared)


#%% create the viewer 
viewer = napari.Viewer()

# add the coins image
image_layer = viewer.add_image(coins, name='coins')

# add the labels
labels_layer = viewer.add_labels(label_image, name='segmentation')

napari.run()