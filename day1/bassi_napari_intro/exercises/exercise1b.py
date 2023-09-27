# -*- coding: utf-8 -*-
"""
Created on Tue Aug 1 11:25:23 2023

@author: Andrea Bassi
"""

from magicgui import magicgui

@magicgui(call_button=False,
          result={"enabled":False},
          )
def sum_floats(
    num1: float=5.0,
    num2: float=3.0,
    result: float=0.0):
    pass

#@sum_floats.num2.changed.connect
@sum_floats.num1.changed.connect
def on_num_changed():
    sum_floats.result.value = sum_floats.num1.value + sum_floats.num2.value


sum_floats.show(run=True)

    
