# -*- coding: utf-8 -*-
"""
Created on Wed Jan 19 16:10:49 2022

@author: andrea
"""
import napari
import numpy as np
from napari.qt.threading import thread_worker
from magicgui import magicgui
import warnings
 
def update_layer(image):
     sy,sx = image.shape    
     name = f'image_with_{sy}X{sx}_pixels'
     try:
         viewer.layers[name].data = image    
     except:    
         viewer.add_image(image,
                      contrast_limits=(0., 1.),
                      name=name)

@thread_worker(connect={'yielded': update_layer})
def create_image_point_by_point(N):
    warnings.filterwarnings('ignore')
    image = np.zeros((N, N))
    for y in range(N):
        for x in range(N):
            image[y,x] = np.random.random(1)
            if x==0 and y%10==0:
                yield(image)

@magicgui(call_button="create image", pixel_num={'max':2048})
def create_image(pixel_num:int = 512):
    create_image_point_by_point(pixel_num)
    

viewer = napari.Viewer()

viewer.window.add_dock_widget(create_image)

napari.run()

