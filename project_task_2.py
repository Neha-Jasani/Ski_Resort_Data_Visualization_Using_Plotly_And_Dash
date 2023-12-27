from dash import dcc, html, Dash
from dash.dependencies import Output, Input
from dash.exceptions import PreventUpdate

import plotly.express as px
import pandas as pd

resorts = (
    pd.read_csv("resorts.csv", encoding = "ISO-8859-1")
    .query("Country in ['United States', 'Canada']")
)

app = Dash(__name__)

app.layout = html.Div([
    html.H1(id='title'),
    dcc.Checklist(
    id = 'country-checklist',
    options = ['Canada', 'United States'],
    value = ['Canada', 'United States']
    ),
    dcc.Dropdown(
    id = 'column-picker',
    options = resorts.select_dtypes('number').columns[3:],
    value = False
    ),
    dcc.RadioItems(
    id = 'ascending-selector',
    options = [
        {'label': 'Ascending', 'value': True},
        {'label': 'Descending', 'value': False}],
    value=False,
    ),
    dcc.Graph(id='metric-bar')
])

@app.callback(Output(component_id='title', component_property='children'),
              Output(component_id='metric-bar', component_property='figure'),
              Input(component_id='country-checklist', component_property='value'),
              Input(component_id='column-picker', component_property='value'),
              Input(component_id='ascending-selector', component_property='value')
             )

def plot_hist(country, column, ascending):

    title = f'Top 10 resorts by {column}'
    
    df = resorts.query('Country in @country')
    
    fig = px.bar(
        df.sort_values(column, ascending=ascending).iloc[:10],
        x='Resort',
        y=column,
        color="Country",
        width=1000,
        height=800
    )
    
    return title, fig

if __name__ == '__main__':
    app.run_server()
