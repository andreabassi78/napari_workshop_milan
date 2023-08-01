
import numpy as np
from napari.layers import Image, Labels
from magicgui import magicgui
import napari

@magicgui(call_button="Apply threshold")
def sum_images(image_layer :Image, 
               thresold: int = 120)->Labels:
    
    data = image_layer.data
    result = data > thresold
    return Labels(result)

viewer = napari.Viewer()

viewer.window.add_dock_widget(sum_images,
                              name = 'Threshold widged')
napari.run()