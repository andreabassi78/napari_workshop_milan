
import numpy as np
from napari.layers import Image,Labels
from skimage.filters import threshold_otsu
from skimage.segmentation import clear_border
from skimage.measure import label
from skimage.morphology import closing, square, remove_small_objects

from magicgui import magicgui
import napari

@magicgui(call_button="run segmentation")
def segment(image_layer:Image, 
            closing_size:int=4,
            remove_smaller_than:int=20)->Labels:
    
    data = np.array(image_layer.data)
    thresh = threshold_otsu(data)
    bw = closing(data > thresh, square(closing_size))
    cleared = remove_small_objects(clear_border(bw), remove_smaller_than)
    label_image = label(cleared)
    
    return Labels(label_image)


viewer = napari.Viewer()

viewer.window.add_dock_widget(segment,
                              name = 'Segmentation tool')
napari.run()