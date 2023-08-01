# -*- coding: utf-8 -*-
"""
Created on Mon Jan 17 23:09:58 2022

@author: andrea
"""
import napari
from qtpy.QtWidgets import QWidget, QPushButton, QSpinBox, QDoubleSpinBox
from qtpy.QtWidgets import QVBoxLayout, QFormLayout
import numpy as np
from numpy.fft import fft2, ifftshift, fftshift, fftfreq

class MyWidget(QWidget):
    
    dr = 0.1
    
    def __init__(self, viewer:napari.Viewer):
        self.viewer = viewer
        super().__init__()
        self.create_ui()
        
    def create_ui(self):
        
        # initialize layout
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        #create spiboxes for NA, n, N_pixel, wavelength

        NAsbox = QDoubleSpinBox()
        NAsbox.setValue(0.5)
        NAsbox.setSingleStep(0.1)
        NALayout = QFormLayout()
        NALayout.addRow('NA', NAsbox)
        layout.addLayout(NALayout)
        self.NAsbox = NAsbox
        
        nsbox = QDoubleSpinBox()
        nsbox.setValue(1.0)
        nsbox.setSingleStep(0.1)
        nLayout = QFormLayout()
        nLayout.addRow('n', nsbox)
        layout.addLayout(nLayout)
        self.nsbox = nsbox
        
        Nsbox = QSpinBox()
        Nsbox.setMaximum(2048)
        Nsbox.setValue(64)
        NLayout = QFormLayout()
        NLayout.addRow('Number of pixels', Nsbox)
        layout.addLayout(NLayout)
        self.Nsbox = Nsbox
        
        lambdasbox = QDoubleSpinBox()
        lambdasbox.setValue(0.633)
        lambdasbox.setSingleStep(0.05)
        lambdaLayout = QFormLayout()
        lambdaLayout.addRow('wavelength', lambdasbox)
        layout.addLayout(lambdaLayout)
        self.lambdasbox = lambdasbox
        
        # add calculate psf button
        calculate_btn = QPushButton('Calculate PSF')
        calculate_btn.clicked.connect(self.calculate_psf)
        layout.addWidget(calculate_btn)
        
    
    def generate_kspace(self):
        
        self.n = self.nsbox.value()
        self.NA = self.NAsbox.value()
        self.wavelength = self.lambdasbox.value()
        self.Nxy = self.Nsbox.value()
        self.k = self.n/self.wavelength # wavenumber
        self.k_cut_off = self.NA/self.wavelength # cut off frequency in the coherent case
        # self.dr = 1/2/self.k_cut_off / 4 # pixel size in 1/4 of the diffraction limit
        kx_lin = fftshift(fftfreq(self.Nxy, self.dr))
        ky_lin = fftshift(fftfreq(self.Nxy, self.dr))
        kx, ky = np.meshgrid(kx_lin,ky_lin)
        # generate k-space in radial coordinates
        with np.errstate(invalid='ignore'):    
            self.k_rho = np.sqrt(kx**2 + ky**2)
            self.k_theta = np.arctan2(ky,kx)  
            self.kz = np.sqrt(self.k**2-self.k_rho**2)
        
    def generate_pupil(self):
        
        pupil = np.ones_like(self.kz)
        cut_idx = (self.k_rho >= self.k_cut_off) 
        pupil[cut_idx] = 0 # exclude k above the cut off frequency
        self.pupil = pupil
        
    def calculate_psf(self):
        
        self.generate_kspace()
        self.generate_pupil()
        ASF = fftshift(fft2(ifftshift(self.pupil))) #* k**2/f**2 # Amplitude Spread Function
        PSF = np.abs(ASF)**2 # Point Spread Function
                
        self.viewer.add_image(PSF,
                          name='PSF',
                          colormap='twilight')
            
    
if __name__ == '__main__':
   
    viewer = napari.Viewer()
    mywidget = MyWidget(viewer)
    viewer.window.add_dock_widget(mywidget, name = 'my psf generation widget')
    napari.run() 