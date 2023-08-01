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
        closing_size_sbox = QSpinBox()
        closing_size_sbox.setMinimum(1)
        closing_size_sbox.setMaximum(2048)
        closing_size_sbox.setValue(4)
        NLayout = QFormLayout()
        NLayout.addRow('closing size', closing_size_sbox)
        layout.addLayout(NLayout)
        self.closing_size_sbox = closing_size_sbox

        #create spinbox for setting the size of the minimum objects 
        min_size_sbox = QSpinBox()
        min_size_sbox.setMinimum(1)
        min_size_sbox.setMaximum(2048)
        min_size_sbox.setValue(20)
        NLayout = QFormLayout()
        NLayout.addRow('remove smaller than', min_size_sbox)
        layout.addLayout(NLayout)
        self.min_size_sbox = min_size_sbox
        
        #create button
        segment_btn = QPushButton('Segment')
        segment_btn.clicked.connect(self.segment)
        layout.addWidget(segment_btn)

    def segment(self):
        image_layer = list(self.viewer.layers.selection)[0] # returns the selected layer (the first one if many)
        closing_size = self.closing_size_sbox.value()
        remove_smaller_than = self.min_size_sbox.value()
        data = np.array(image_layer.data)
        thresh = threshold_otsu(data)
        bw = closing(data > thresh, square(closing_size))
        cleared = remove_small_objects(clear_border(bw), remove_smaller_than)
        label_image = label(cleared)
        self.viewer.add_labels(label_image)
            
if __name__ == '__main__':
   
    viewer = napari.Viewer()
    mywidget = MyWidget(viewer)
    viewer.window.add_dock_widget(mywidget, name = 'my first QT widget')
    napari.run() 