# -*- coding: utf-8 -*-
"""
Created on Wed Jan 19 16:10:49 2022

@author: Andrea Bassi
"""
import napari
import numpy as np
from magicgui import magicgui
 

def create_image_point_by_point(N):
    image = np.zeros((N, N))
    for y in range(N):
        for x in range(N):
            image[y,x] = np.random.random(1)       
    return(image)

@magicgui(call_button="create image",
          pixel_num={'max':4096})
def create_image(pixel_num:int = 1024):
    image = create_image_point_by_point(pixel_num)
    sy,sx = image.shape    
    name = f'image_with_{sy}X{sx}_pixels'
    viewer.add_image(image,
                    contrast_limits=(0., 1.),
                    name=name)
    

viewer = napari.Viewer()
viewer.window.add_dock_widget(create_image)
napari.run()

