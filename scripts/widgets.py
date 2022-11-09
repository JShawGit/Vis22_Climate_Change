import ipywidgets as widgets
from ipywidgets import interact

"""https://ipywidgets.readthedocs.io/en/latest/examples/Widget%20List.html"""

def select():
    sel = widgets.Select(options=['Linux', 'Windows', 'macOS'],
        value='macOS',
        # rows=10,
        description='OS:',
        disabled=False
    )
    display(sel)



def check_box():

    data = ["data1", "data2", "data3", "data4"]
    checkboxes = [widgets.Checkbox(value=False, description=label) for label in data]
    output = widgets.VBox(children=checkboxes)
    display(output)
  

def radio_buttons(options, description):
    rb = widgets.RadioButtons(
        options=['pepperoni', 'pineapple', 'anchovies'],
        #    value='pineapple', # Defaults to 'pineapple'
        #    layout={'width': 'max-content'}, # If the items' names are long
        description='Pizza topping:',
        disabled=False
    )
    display(rb)




def drop_down(options, value, description):

    dd = widgets.Dropdown(
        options=['Addition', 'Multiplication', 'Subtraction', 'Division'],
        value='Addition',
        description='Task:',
    )
    display(dd)
    
def combo(placeholder, value, options, description):
    comb = widgets.Combobox(
    # value='John',
    placeholder='Choose Someone',
    options=['Paul', 'John', 'George', 'Ringo'],
    description='Combobox:',
    ensure_option=True,
    disabled=False
    )
    display(comb)
    
def button():

    button = widgets.Button(
    description='Click me',
    disabled=False,
    button_style='', # 'success', 'info', 'warning', 'danger' or ''
    tooltip='Click me',
    icon='check' # (FontAwesome names without the `fa-` prefix)
    )
    display(button)

def slider():
    slide = widgets.FloatSlider(
    value=7.5,
    min=0,
    max=10.0,
    step=0.1,
    description='Test:',
    disabled=False,
    continuous_update=False,
    orientation='horizontal',
    readout=True,
    readout_format='.1f',
    )
    display(slide)



def play_slider():
    play = widgets.Play(
    value=50,
    min=0,
    max=100,
    step=1,
    interval=500,
    description="Press play",
    disabled=False
    )
    slider = widgets.IntSlider()
    widgets.jslink((play, 'value'), (slider, 'value'))
    widgets.HBox([play, slider])
    