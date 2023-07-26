import pathlib
from magicgui import magicgui


@magicgui(folder={'mode': 'd'}, call_button='Run')
def widget(folder =  pathlib.Path.home()):
    print(folder)


widget.show(run=True)