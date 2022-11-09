import plotly.express as px
from ipywidgets import interact
import pandas as pd

df2 = px.data.tips()
@interact
def make_fig(x=df2.columns, y=df2.columns, c=df2.columns):    
    return px.scatter(df2, x=x, y=y, color=c, height=600)
     
def scatterplot():
    """
    User can:
    zoom in/out
    pan
    select lasso
    select each continetent
    hover option
    """
    df = px.data.gapminder(year=2007)
    px.scatter(df, x="gdpPercap", y="lifeExp", color="continent", size="pop", template="simple_white",
           hover_name="country", size_max=60, log_x=True, height=600).update_layout(hovermode=False)



def map():
    """
    Earthquake info
    zoom
    hover
    pan
    
    """
    
    df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/earthquakes-23k.csv')

    fig = px.density_mapbox(df, lat='Latitude', lon='Longitude', z='Magnitude', radius=10,
                        center=dict(lat=0, lon=180), zoom=0, hover_name="Date",
                        mapbox_style="stamen-terrain", height=600,
                       color_continuous_scale="magma")
    fig.show() 
    
    
def higher_interact1():

    """
    shows map and list of counties in Texas, changes in one view
    is observable in another view    
    """    

    import holoviews as hv
    from holoviews import opts
    from holoviews.plotting.links import DataLink
    import bokeh.sampledata
    hv.extension('bokeh')
    bokeh.sampledata.download()
    from bokeh.sampledata.us_counties import data as counties
    from bokeh.sampledata.unemployment import data as unemployment
    
    counties = [dict(county, Unemployment=unemployment[cid])
            for cid, county in counties.items()
            if county["state"] == "tx"]

    county_data = [(county['detailed name'], county['Unemployment']) for county in counties]
    
    # create map of texas
    choropleth = hv.Polygons(counties, ['lons', 'lats'], [('detailed name', 'County'), 'Unemployment'], 
                         label='Texas Unemployment')
    
    # create a table of counties and unemployment info
    table = hv.Table(county_data, [('detailed name', 'County'), 'Unemployment'])

    # links the data from two sources as long as they match in length
    #link the data on two views
    DataLink(choropleth, table)

    # tools shows the possible interactions
    (choropleth + table).opts(
        opts.Table(height=428),
        opts.Polygons(width=500, height=500,  tools=['box_select', 'hover', 'tap'], xaxis=None, 
                  yaxis=None, color_index='Unemployment'))
                  
                  
def higher_interact2():   

    import plotly.graph_objects as go
    import ipywidgets as widgets
    import pandas as pd
    import numpy as np

    cars_df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/imports-85.csv')

    # Build parcats dimensions
    categorical_dimensions = ['drive-wheels', 'body-style', 'fuel-type']

    dimensions = [dict(values=cars_df[label], label=label) for label in categorical_dimensions]

    # Build colorscale
    color = np.zeros(len(cars_df), dtype='uint8')
    colorscale = [[0, 'gray'], [0.33, 'gray'],
              [0.33, 'firebrick'], [0.66, 'firebrick'],
              [0.66, 'blue'], [1.0, 'blue']]
    cmin = -0.5
    cmax = 2.5

    # Build figure as FigureWidget
    fig = go.FigureWidget(
        data=[go.Scatter(x=cars_df.horsepower, y=cars_df['highway-mpg'],
                marker={'color': color, 'cmin': cmin, 'cmax': cmax,
                        'colorscale': colorscale, 'showscale': False},
                     mode='markers', text=cars_df['make']),
            go.Parcats(domain={'x': [0, 0.45]}, dimensions=dimensions,
                   line={'colorscale': colorscale, 'cmin': cmin,
                   'cmax': cmax, 'color': color, 'shape': 'hspline'})]
    ).update_layout(height=600, xaxis={'title': 'Horsepower', 'domain': [0.55, 1]},
                  yaxis={'title': 'MPG'},
                  dragmode='lasso', hovermode='closest')

    color_toggle = widgets.ToggleButtons(
        options=['None', 'Red', 'Blue'],
        index=1, description='Brush Color:', disabled=False)

def update_color(trace, points, state):
    new_color = np.array(fig.data[0].marker.color)
    new_color[points.point_inds] = color_toggle.index

    with fig.batch_update():
        fig.data[0].marker.color = new_color
        fig.data[1].line.color = new_color

fig.data[0].on_selection(update_color)
fig.data[1].on_click(update_color)

widgets.VBox([color_toggle, fig])

