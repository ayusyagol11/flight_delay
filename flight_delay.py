import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

# Load airline data
airline_data = pd.read_csv('Flight_Delay-Data.csv', 
                            encoding='ISO-8859-1',
                            dtype={'Div1Airport': str, 'Div1TailNum': str, 
                                   'Div2Airport': str, 'Div2TailNum': str})

# Airline abbreviations and full names
airline_dict = {
    "9E": "Endeavor Air", "AA": "American Airlines", "B6": "JetBlue Airways", "CO": "Continental Airlines",
    "DL": "Delta Airlines", "EV": "ExpressJet Airlines", "F9": "Frontier Airlines", "FL": "AirTran Airways",
    "MQ": "Envoy Air", "OH": "PSA Airlines", "OO": "SkyWest Airlines", "UA": "United Airlines",
    "US": "US Airways", "WN": "Southwest Airlines", "XE": "ExpressJet Airlines", "YV": "Mesa Airlines",
    "AS": "Alaska Airlines", "HA": "Hawaiian Airlines"
}

# Initialize Dash app
app = dash.Dash(__name__)

# Define app layout
app.layout = html.Div([
    html.H1('Flight Delay Time Statistics', style={'textAlign': 'center', 'color': '#503D36', 'font-size': '36px'}),
    html.Div(["Input Year: ", 
              dcc.Input(id='input-year', value='2010', type='number', 
                        style={'height': '35px', 'font-size': '24px'})], 
              style={'font-size': '24px', 'textAlign': 'center'}),
    html.Br(),
    
    # Charts layout
    html.Div([
        html.Div(dcc.Graph(id='carrier-plot'), style={'width': '48%', 'display': 'inline-block'}),
        html.Div(dcc.Graph(id='weather-plot'), style={'width': '48%', 'display': 'inline-block'})
    ], style={'textAlign': 'center'}),
    
    html.Div([
        html.Div(dcc.Graph(id='nas-plot'), style={'width': '48%', 'display': 'inline-block'}),
        html.Div(dcc.Graph(id='security-plot'), style={'width': '48%', 'display': 'inline-block'})
    ], style={'textAlign': 'center'}),
    
    html.Div(dcc.Graph(id='late-plot'), style={'width': '65%', 'margin': 'auto'}),
    html.Br(),
    
    # Airlines List
    html.H3('Airline Abbreviations:', style={'textAlign': 'center', 'marginTop': '20px'}),
    html.Ul([html.Li(f"{abbr} - {name}") for abbr, name in airline_dict.items()],
            style={'textAlign': 'center', 'listStyleType': 'none', 'fontSize': '18px'}),
    
    # Footer
    html.Hr(),
    html.P('Dashboard created by Aayush Yagol, 2025', style={'textAlign': 'center', 'fontSize': '16px', 'fontStyle': 'italic'})
])

# Compute averages function
def compute_info(airline_data, entered_year):
    df = airline_data[airline_data['Year'] == int(entered_year)]
    avg_car = df.groupby(['Month', 'Reporting_Airline'])['CarrierDelay'].mean().reset_index()
    avg_weather = df.groupby(['Month', 'Reporting_Airline'])['WeatherDelay'].mean().reset_index()
    avg_NAS = df.groupby(['Month', 'Reporting_Airline'])['NASDelay'].mean().reset_index()
    avg_sec = df.groupby(['Month', 'Reporting_Airline'])['SecurityDelay'].mean().reset_index()
    avg_late = df.groupby(['Month', 'Reporting_Airline'])['LateAircraftDelay'].mean().reset_index()
    return avg_car, avg_weather, avg_NAS, avg_sec, avg_late

# Callback function
@app.callback([
    Output('carrier-plot', 'figure'),
    Output('weather-plot', 'figure'),
    Output('nas-plot', 'figure'),
    Output('security-plot', 'figure'),
    Output('late-plot', 'figure')
],
Input('input-year', 'value'))
def get_graph(entered_year):
    avg_car, avg_weather, avg_NAS, avg_sec, avg_late = compute_info(airline_data, entered_year)
    
    carrier_fig = px.line(avg_car, x='Month', y='CarrierDelay', color='Reporting_Airline', title='Average Carrier Delay')
    weather_fig = px.line(avg_weather, x='Month', y='WeatherDelay', color='Reporting_Airline', title='Average Weather Delay')
    nas_fig = px.line(avg_NAS, x='Month', y='NASDelay', color='Reporting_Airline', title='Average NAS Delay')
    sec_fig = px.line(avg_sec, x='Month', y='SecurityDelay', color='Reporting_Airline', title='Average Security Delay')
    late_fig = px.line(avg_late, x='Month', y='LateAircraftDelay', color='Reporting_Airline', title='Average Late Aircraft Delay')
    
    for fig in [carrier_fig, weather_fig, nas_fig, sec_fig, late_fig]:
        fig.update_layout(title={'x': 0.5, 'xanchor': 'center', 'font': {'size': 18, 'family': 'Arial', 'weight': 'bold'}})
    
    return [carrier_fig, weather_fig, nas_fig, sec_fig, late_fig]

# Run server
if __name__ == '__main__':
    app.run_server(debug=True)
