# -*- coding: utf-8 -*-
"""
Created on Tue Aug 1 11:25:23 2023

@author: Andrea Bassi
"""

from magicgui import magicgui
    
@magicgui(call_button=False,
          result={"enabled":False},
          #auto_call=True
          )
def sum_floats(
    num1: float=5.0,
    num2: float=3.0,
    result: float=8.0):
    sum_floats.result.value = num1+num2
    
sum_floats.show(run=True)

    
