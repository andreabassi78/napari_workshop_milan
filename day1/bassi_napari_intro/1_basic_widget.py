
import numpy as np
from napari.layers import Image, Labels
from magicgui import magicgui
import napari

@magicgui(call_button="Apply threshold",
          thresold = {'max':256})
def thresold_image(image_layer :Image, 
             thresold: int = 120):
    
    data = image_layer.data
    result = data > thresold

    try:
        viewer.layers['result_label'].data = result
    except: 
        result_label = viewer.add_labels(result, name = 'result_label' )


viewer = napari.Viewer()

viewer.window.add_dock_widget(thresold_image,
                              name = 'Threshold widged')
napari.run()