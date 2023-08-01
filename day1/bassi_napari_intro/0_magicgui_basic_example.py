# -*- coding: utf-8 -*-
"""
Created on Fri Jan 14 15:35:26 2022

@author: Andrea Bassi
"""

from magicgui import magicgui
    
@magicgui()
def sum_numbers(number1:int = 5, number2:int = 2):
    result = number1 + number2
    print(result)
    return(result)
    
sum_numbers.show(run=True)