# app.py

# Import necessary libraries
from dash import Dash, dcc, html, dash_table  # Dash libraries for creating the web application
from dash.dependencies import Input, Output  # Dash dependencies for callback functions
import dash_leaflet as dl  # Dash-Leaflet for map rendering
import pandas as pd  # Pandas for data manipulation

# Import the AnimalShelter class from the CRUD module
from crud import AnimalShelter  # Assuming your CRUD module is named `crud.py`

# Initialize the AnimalShelter class with MongoDB connection details
username = "victoroudeh"
password = "dpa2Vmz631UCUNYF"
shelter = AnimalShelter()  # Instantiate the AnimalShelter class

# Retrieve data from MongoDB using the read method
data = shelter.read({})

# Convert the retrieved data to a DataFrame
df = pd.DataFrame.from_records(data)

# Remove the '_id' column if it exists, as it is not needed for the dashboard
if '_id' in df.columns:
    df.drop(columns=['_id'], inplace=True)

# Debugging: Print the number of records and the columns of the DataFrame
print(len(df.to_dict(orient='records')))
print(df.columns)

# Initialize the Dash app
app = Dash(__name__)

# Define the layout of the dashboard
app.layout = html.Div([
    html.Div(id='hidden-div', style={'display': 'none'}),  # Hidden div for potential future use
    html.Center(html.B(html.H1('VUDEH SNHU CS-340 Dashboard'))),  # Dashboard title
    html.Hr(),  # Horizontal line for separation
    dash_table.DataTable(
        id='datatable-id',  # Unique ID for the data table
        columns=[{"name": i, "id": i, "deletable": False, "selectable": True} for i in df.columns],  # Define columns
        data=df.to_dict('records'),  # Data for the table
        style_table={'height': '400px', 'overflowY': 'auto'},  # Styling for the table
        style_cell={'textAlign': 'left'},  # Cell styling
        row_selectable='single',  # Allow single row selection
        selected_rows=[0],  # Initially select the first row
        page_size=10  # Number of rows per page
    ),
    html.Br(),  # Line break
    html.Hr(),  # Horizontal line for separation
    html.Div(
        id='map-id',  # Unique ID for the map
        className='col s12 m6'  # Styling classes
    )
])

#############################################
# Interaction Between Components / Controller
#############################################

# Callback to highlight a row on the data table when the user selects it
@app.callback(
    Output('datatable-id', 'style_data_conditional'),  # Output: style changes for the data table
    [Input('datatable-id', 'selected_columns')]  # Input: selected columns in the data table
)
def update_styles(selected_columns):
    # Ensure selected_columns is not None before processing
    if selected_columns is None:
        return []
    # Highlight the selected columns
    return [{
        'if': {'column_id': i},
        'background_color': '#D2F3FF'
    } for i in selected_columns]

# Callback to update the geo-location chart for the selected data entry
@app.callback(
    Output('map-id', "children"),  # Output: children elements of the map div
    [Input('datatable-id', "derived_virtual_data"),  # Input: data from the data table
     Input('datatable-id', "derived_virtual_selected_rows")]  # Input: selected rows from the data table
)
def update_map(viewData, index):
    # Check if viewData is valid
    if not viewData or not isinstance(viewData, list) or len(viewData) == 0:
        return []

    # Convert the viewData to a DataFrame
    dff = pd.DataFrame.from_dict(viewData)
    # Get the selected row index
    row = index[0] if index else 0

    # Check if the DataFrame is empty or if the row index is out of bounds
    if dff.empty or row >= len(dff):
        return []

    # Return the map with a marker for the selected row
    return [
        dl.Map(style={'width': '1000px', 'height': '500px'},
               center=[30.75, -97.48], zoom=10, children=[
            dl.TileLayer(id="base-layer-id"),
            dl.Marker(position=[dff.iloc[row, 13], dff.iloc[row, 14]],
                      children=[
                          dl.Tooltip(dff.iloc[row, 4]),
                          dl.Popup([
                              html.H1("Animal Name"),
                              html.P(dff.iloc[row, 9])
                          ])
                      ])
        ])
    ]

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)
