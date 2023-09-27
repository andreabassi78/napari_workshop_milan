# if you are using jupyter notebook:
# %gui qt 

from magicgui import magicgui

@magicgui()
def sum_numbers(number1:int = 5, number2:int = 2):

    result = number1+number2

    print(result)

    return(result)


#sum_numbers.show(run=True)

