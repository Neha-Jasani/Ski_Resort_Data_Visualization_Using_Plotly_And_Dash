from dash import dcc, html,Dash

from dash.dependencies import Output, Input
from dash.exceptions import PreventUpdate

import plotly.express as px
import pandas as pd

ski_resorts = (pd.read_csv("resorts.csv", encoding = "ISO-8859-1").query("Country in ['United States', 'Canada']"))

app = Dash(__name__)

app.layout = html.Div([
    html.H2(id="title"),
    dcc.Slider(
        id="price-selector",
        min=0,
        max=150,
        step=10,
        value=150
#         marks={i: f'{i}' for i in range(0, 150, 10)}
),
    dcc.RadioItems(
        id="Feature Radio",
        options=[
            {"label": "Has Night Skiing", "value": "Yes"},
            {"label": "No Night Skiing", "value": "No"}
        ],
        value="No"
    ),
    dcc.Graph(id="resort-map"),
])

@app.callback(
    Output("title", "children"),
    Output("resort-map", "figure"),
    Input("price-selector", "value"),
    Input("Feature Radio", "value"),
)

def plot_lift_number(price, feature):
    if not price and feature:
        raise PreventUpdate
        
    title = f"Areas with a ticket price less than ${price}."
        
    
    if feature == 'Yes':
        df = ski_resorts[(ski_resorts['Price'] < price) & (ski_resorts['Nightskiing'] == 'Yes')]
    else:
        df = ski_resorts[(ski_resorts['Price'] < price) & (ski_resorts['Nightskiing'] != 'Yes')]
        
        
    
    fig = px.density_mapbox(
        df,
        lat="Latitude",
        lon="Longitude",
        z="Total slopes",
        hover_name="Resort",
        center={"lat": 45, "lon": -100},
        zoom=3,
        mapbox_style="open-street-map",
        color_continuous_scale="blues",
#         width=1000,
#         height=800
    )

    return title, fig 
    
if __name__ == "__main__":
    app.run(debug=True)