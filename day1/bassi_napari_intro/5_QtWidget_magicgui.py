# -*- coding: utf-8 -*-
"""
Created on Mon Jan 17 23:09:58 2022

@author: andrea
"""
import napari
import numpy as np
from numpy.fft import fft2, ifftshift, fftshift, fftfreq
from magicgui import magicgui

class MyClass():
    
    dr = 0.1
    
    def __init__(self, viewer:napari.Viewer):
        self.viewer = viewer
        super().__init__()
        self.generate_kspace()
     
    def generate_kspace(self, 
                        n:float=1.,
                        NA:float=0.6,
                        wavelength:float = 0.56,
                        N:int = 64):
        
        self.k_cut_off = NA/wavelength # cut off frequency in the coherent case
        kx_lin = fftshift(fftfreq(N, self.dr))
        ky_lin = fftshift(fftfreq(N, self.dr))
        kx, ky = np.meshgrid(kx_lin, ky_lin)
        # generate k-space in radial coordinates
        self.k_rho = np.sqrt(kx**2 + ky**2)
        self.k_theta = np.arctan2(ky, kx)
        
    def generate_pupil(self):
        
        pupil = np.ones_like(self.k_rho)
        cut_idx = (self.k_rho >= self.k_cut_off) 
        pupil[cut_idx] = 0 # exclude k above the cut off frequency
        self.pupil = pupil
        
    def calculate_psf(self):
        
        self.generate_pupil()
        ASF = fftshift(fft2(ifftshift(self.pupil))) #* k**2/f**2 # Amplitude Spread Function
        PSF = np.abs(ASF)**2 # Point Spread Function
        
        self.viewer.add_image(PSF,
                             name='PSF',
                             colormap='twilight')
            
    
if __name__ == '__main__':
   
    viewer = napari.Viewer()
    
    myclass = MyClass(viewer)
    
    generate = magicgui(myclass.generate_kspace,auto_call=True)
    
    calculate = magicgui(myclass.calculate_psf, call_button='Calculate PSF')
    
    viewer.window.add_dock_widget((generate, calculate),
                                  name = 'my second app',
                                  add_vertical_stretch = True)
    napari.run() 