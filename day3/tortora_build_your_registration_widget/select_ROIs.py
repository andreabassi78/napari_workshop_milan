# -*- coding: utf-8 -*-
"""
Created on Sun Sep 10 18:35:05 2023

@author: GiorgiaT
"""

from magicgui import magicgui
import napari
from napari import Viewer
from napari.layers import Image, Points
import numpy as np
import cv2


def normalize_stack(stack, **kwargs):
    '''
    -normalizes n-dimensional stack it to its maximum and minimum values,
    unless normalization values are provided in kwargs,
    -casts the image to 8 bit for fast processing with cv2
    '''
    img = np.float32(stack)
    if 'vmin' in kwargs:
        vmin = kwargs['vmin']
    else:    
        vmin = np.amin(img)
   
    if 'vmax' in kwargs:
        vmax = kwargs['vmax']
    else:    
        vmax = np.amax(img)
    saturation = 1   
    img = saturation * (img-vmin) / (vmax-vmin)
    img = (img*255).astype('uint8') 
    return img, vmin, vmax
        
def select_rois(first_image, positions, roi_size, zoom):
    
    rois = []
    zoomed_rois = []
    half_size = roi_size//2
    for pos in positions:
        y = int(pos[0])
        x = int(pos[1])
        roi = first_image[y-half_size:y+half_size,
                                x-half_size:x+half_size]
        rois.append(roi)
        zoomed_roi = cv2.resize(roi, [zoom*roi_size,zoom*roi_size])
        zoomed_rois.append(zoomed_roi)
    return rois, zoomed_rois

@magicgui(call_button="Select ROIs")
def select_ROIs(viewer: Viewer,
              image: Image,
              # labels_layer: Labels,
              points_layer: Points,
              zoom: int = 4
              ):
    original_stack = np.asarray(image.data)
    normalized, vmin, vmax = normalize_stack(original_stack)
    points = np.asarray(points_layer.data)
    # labels = np.asarray(labels_layer.data)
    yx_coordinates = points[:,[1,2]]
    rois, zoomed_rois = select_rois (normalized[0,:,:],yx_coordinates,ROI_SIZE, zoom)
    roi_num = len(rois)
    for roi_idx in range(roi_num):
        viewer.add_image(zoomed_rois[roi_idx], name = f'{image.name}_ROI{roi_idx}')

if __name__ == '__main__':
    
    ROI_SIZE = 100
    
    viewer = Viewer()
    # select_ROIs_widget = select_ROIs()
    viewer.window.add_dock_widget(select_ROIs, name = 'Select ROIs',
                                  area='right', add_vertical_stretch=True)
    napari.run() 