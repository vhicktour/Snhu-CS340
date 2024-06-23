from jupyter_dash import JupyterDash
import dash_leaflet as dl
from dash import dcc, html, dash_table
import plotly.express as px
from dash.dependencies import Input, Output
import base64

import pandas as pd
import re  # needed for the regex pattern matching

from modules.animal_shelter import AnimalShelter

###########################
# Data Manipulation / Model
###########################
username = "victoroudeh"
password = "naijaboy007"

# Connect to database via CRUD Module
shelter = AnimalShelter(username, password)

# Load a sample of records to improve initial load time
df = pd.DataFrame.from_records(shelter.read({}, limit=100))

# MongoDB v5+ is going to return the '_id' column and that is going to have an 
# invalid object type of 'ObjectID' - which will cause the data_table to crash - so we remove
# it in the dataframe here. The df.drop command allows us to drop the column. If we do not set
# inplace=True - it will return a new dataframe that does not contain the dropped column(s)
df.drop(columns=['_id'], inplace=True)

#########################
# Dashboard Layout / View
#########################
app = JupyterDash(__name__)

# Add in Grazioso Salvare’s logo
image_filename = 'assets/grazioso-logo.png'
encoded_image = base64.b64encode(open(image_filename, 'rb').read())

app.layout = html.Div([
    html.A([
        html.Center(html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()), height=250, width=251))
    ], href='https://www.snhu.edu', target="_blank"),
    html.Center(html.B(html.H1("Victor Udeh's SNHU CS-340 Dashboard"))),
    html.Hr(),
    dcc.RadioItems(
        id='filter-type',
        options=[
            {'label': 'All', 'value': 'All'},
            {'label': 'Water Rescue', 'value': 'Water'},
            {'label': 'Mountain or Wilderness Rescue', 'value': 'Mountain'},
            {'label': 'Disaster Rescue or Individual Tracking', 'value': 'Disaster'},
        ],
        value='All'
    ),
    html.Hr(),
    dash_table.DataTable(id='datatable-id',
                         columns=[{"name": i, "id": i, "deletable": False, "selectable": True} for i in df.columns],
                         data=df.to_dict('records'),
                         editable=True,
                         row_selectable="single",
                         selected_rows=[],
                         filter_action="native",
                         sort_action="native",
                         page_action="native",
                         page_current=0,
                         page_size=10,
                        ),
    html.Br(),
    html.Hr(),
    html.Div(className='row',
             style={'display': 'flex'},
             children=[
                 html.Div(id='graph-id', className='col s12 m6'),
                 html.Div(id='map-id', className='col s12 m6')
             ])
])

#############################################
# Interaction Between Components / Controller
#############################################

@app.callback(
    Output('datatable-id', 'data'),
    [Input('filter-type', 'value')]
)
def update_dashboard(filter_type):
    query = {}
    if filter_type == 'Water':
        labRegex = re.compile(".*lab.*", re.IGNORECASE)
        chesaRegex = re.compile(".*chesa.*", re.IGNORECASE)
        newRegex = re.compile(".*newf.*", re.IGNORECASE)
        query = {
            '$or': [
                {"breed": {'$regex': newRegex}},
                {"breed": {'$regex': chesaRegex}},
                {"breed": {'$regex': labRegex}},
            ],
            "sex_upon_outcome": "Intact Female",
            "age_upon_outcome_in_weeks": {"$gte": 26.0, "$lte": 156.0}
        }
    elif filter_type == 'Mountain':
        germanRegex = re.compile(".*german.*", re.IGNORECASE)
        alaskanRegex = re.compile(".*mala.*", re.IGNORECASE)
        oldRegex = re.compile(".*old english.*", re.IGNORECASE)
        huskyRegex = re.compile(".*husk.*", re.IGNORECASE)
        rottRegex = re.compile(".*rott.*", re.IGNORECASE)
        query = {
            '$or': [
                {"breed": {'$regex': germanRegex}},
                {"breed": {'$regex': alaskanRegex}},
                {"breed": {'$regex': oldRegex}},
                {"breed": {'$regex': huskyRegex}},
                {"breed": {'$regex': rottRegex}},
            ],
            "sex_upon_outcome": "Intact Male",
            "age_upon_outcome_in_weeks": {"$gte": 26.0, "$lte": 156.0}
        }
    elif filter_type == 'Disaster':
        germanRegex = re.compile(".*german.*", re.IGNORECASE)
        goldenRegex = re.compile(".*golden.*", re.IGNORECASE)
        bloodRegex = re.compile(".*blood.*", re.IGNORECASE)
        doberRegex = re.compile(".*dober.*", re.IGNORECASE)
        rottRegex = re.compile(".*rott.*", re.IGNORECASE)
        query = {
            '$or': [
                {"breed": {'$regex': germanRegex}},
                {"breed": {'$regex': goldenRegex}},
                {"breed": {'$regex': bloodRegex}},
                {"breed": {'$regex': doberRegex}},
                {"breed": {'$regex': rottRegex}},
            ],
            "sex_upon_outcome": "Intact Male",
            "age_upon_outcome_in_weeks": {"$gte": 20.0, "$lte": 300.0}
        }
    df_filtered = pd.DataFrame.from_records(shelter.read(query, limit=100))
    df_filtered.drop(columns=['_id'], inplace=True)
    return df_filtered.to_dict('records')

@app.callback(
    Output('datatable-id', 'style_data_conditional'),
    [Input('datatable-id', 'selected_columns')]
)
def update_styles(selected_columns):
    return [{
        'if': {'column_id': i},
        'background_color': '#D2F3FF'
    } for i in selected_columns]

@app.callback(
    Output('graph-id', "children"),
    [Input('datatable-id', "derived_virtual_data")]
)
def update_graphs(viewData):
    dffPie = pd.DataFrame.from_dict(viewData)
    return [
        dcc.Graph(            
            figure=px.pie(dffPie, names='breed', title='Preferred Animals')
        )    
    ]

@app.callback(
    Output('map-id', "children"),    
    [Input('datatable-id', "derived_virtual_data"), Input('datatable-id', "derived_virtual_selected_rows")]
)
def update_map(viewData, index):
    if viewData is None or index is None:
        return
    dff = pd.DataFrame.from_dict(viewData)
    row = index[0] if index else 0

    return [
        dl.Map(style={'width': '1000px', 'height': '500px'}, center=[30.75, -97.48], zoom=10, children=[
            dl.TileLayer(id="base-layer-id"),
            dl.Marker(position=[dff.iloc[row, 13], dff.iloc[row, 14]], children=[
                dl.Tooltip(dff.iloc[row, 4]),
                dl.Popup([
                    html.H1("Animal Name"),
                    html.P(dff.iloc[row, 9])
                ])
            ])
        ])
    ]

if __name__ == '__main__':
    app.run_server(debug=True)
