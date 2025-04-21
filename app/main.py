import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
from data_processing.etl_pipeline import load_clean_data
from data_processing.geospatial import generate_geojson
from models.arima_model import predict_drought
from models.regression import predict_yield

# Inizializza l'app Dash
app = dash.Dash(__name__)
server = app.server

# Carica e pulisci i dati
df = load_clean_data()
geodata = generate_geojson("data/fields.shp")

# Layout dell'interfaccia
app.layout = html.Div([
    html.H1("Dashboard Agricoltura 4.0", className="header"),
    dcc.Dropdown(
        id='crop-dropdown',
        options=[{'label': i, 'value': i} for i in df['coltura'].unique()],
        value='Mais'
    ),
    dcc.Graph(id='yield-map'),
    dcc.Graph(id='weather-forecast')
])

# Callback per aggiornare le mappe
@app.callback(
    [Output('yield-map', 'figure'),
     Output('weather-forecast', 'figure')],
    [Input('crop-dropdown', 'value')]
)
def update_graphs(selected_crop):
    filtered_df = df[df['coltura'] == selected_crop]
    yield_map = px.choropleth_mapbox(
        filtered_df,
        geojson=geodata,
        locations='id_campo',
        color='resa_kg_ettaro',
        mapbox_style="carto-positron"
    )
    
    weather_fig = px.line(
        filtered_df,
        x='data',
        y='precipitazioni_mm',
        title='Andamento Precipitazioni'
    )
    
    return yield_map, weather_fig

if __name__ == '__main__':
    app.run_server(debug=True)
