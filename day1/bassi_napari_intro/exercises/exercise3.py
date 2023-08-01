# -*- coding: utf-8 -*-
"""
Created on Mon Jan 17 23:09:58 2022

@author: Andrea Bassi
"""
import napari
from qtpy.QtWidgets import QWidget, QPushButton, QSpinBox
from qtpy.QtWidgets import QVBoxLayout, QFormLayout
import numpy as np
from skimage.filters import threshold_otsu
from skimage.segmentation import clear_border
from skimage.measure import label
from skimage.morphology import closing, square, remove_small_objects
from magicgui.widgets import SpinBox, PushButton, Container
from magicgui import magicgui
from napari.layers import Image

class MyWidget(QWidget):
    
    def __init__(self, viewer:napari.Viewer):
        self.viewer = viewer
        super().__init__()
        self.create_ui()
        
    def create_ui(self):
        
        # initialize layout
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # create closing size spinbox
        closing_size_sbox = SpinBox(value = 4, label = "closing size")
        self.closing_size_sbox = closing_size_sbox
        
        #create spinbox for setting the size of the minimum objects 
        min_size_sbox = SpinBox(value = 20, label = "remove smaller than")
        self.min_size_sbox = min_size_sbox
        
        #create button
        segment_btn = PushButton(text ='Segment')
        segment_btn.clicked.connect(self.segment)

        @magicgui(call_button=False)
        def select_layer(self, image_layer:Image):
            pass

        select_layer.image_layer.label = ''
        self.select_layer = select_layer

        widgets_container = Container(widgets=[closing_size_sbox,
                                              min_size_sbox,
                                              select_layer,
                                              segment_btn])
        
        layout.addWidget(widgets_container.native) # NOTE that we need to use the native attribute with magicgui objects
        self.viewer.layers.events.inserted.connect(widgets_container.reset_choices)
        self.viewer.layers.events.removed.connect(widgets_container.reset_choices)

    def segment(self):
        image_layer = self.select_layer.image_layer.value
        closing_size = self.closing_size_sbox.value 
        remove_smaller_than = self.min_size_sbox.value
        data = np.array(image_layer.data)
        thresh = threshold_otsu(data)
        bw = closing(data > thresh, square(closing_size))
        cleared = remove_small_objects(clear_border(bw), remove_smaller_than)
        label_image = label(cleared)
        self.viewer.add_labels(label_image)
            
if __name__ == '__main__':
   
    viewer = napari.Viewer()
    mywidget = MyWidget(viewer)
    viewer.window.add_dock_widget(mywidget, name = 'my QT widget with magicgui widgets and image selection combo box')
    napari.run() 