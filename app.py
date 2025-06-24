import pandas as pd
import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import json
import plotly.graph_objects as go


# Load GeoJSON files
with open("data/2min-polygon.geojson") as f:
    min2polygon = json.load(f)
with open("data/3min-polygon.geojson") as f:
    min3polygon = json.load(f)
with open("data/5min-polygon.geojson") as f:
    min5polygon = json.load(f)
with open("data/coffee-locations.geojson") as f:
    locations = json.load(f)
locations_df = pd.json_normalize(locations["features"])
with open("data/vertigis-office.geojson") as f:
    office = json.load(f)

app = dash.Dash(__name__)
server = app.server


def create_map(selected_drive_time):
    fig = go.Figure()
    # Add polygons based on selected_drive_time
    if selected_drive_time == '2':
        polygon_coords = min2polygon["features"][0]["geometry"]["coordinates"][0]
        lons, lats = zip(*polygon_coords)
        fig.add_trace(go.Scattermap(lon=lons, lat=lats, mode='lines', fill='toself', fillcolor='lightblue', line=dict(width=2, color='lightblue'), name='2min Polygon'))
    elif selected_drive_time == '3':
        polygon_coords = min3polygon["features"][0]["geometry"]["coordinates"][0]
        lons, lats = zip(*polygon_coords)
        fig.add_trace(go.Scattermap(lon=lons, lat=lats, mode='lines', fill='toself', fillcolor='orange', line=dict(width=2, color='orange'), name='3min Polygon'))
    elif selected_drive_time == '5':
        polygon_coords = min5polygon["features"][0]["geometry"]["coordinates"][0]
        lons, lats = zip(*polygon_coords)
        fig.add_trace(go.Scattermap(lon=lons, lat=lats, mode='lines', fill='toself', fillcolor='red', line=dict(width=2, color='red'), name='5min Polygon'))
    elif selected_drive_time == 'all':
        for mins, poly, color, legend in [
            ('2', min2polygon, 'blue', '2min Polygon'),
            ('3', min3polygon, 'orange', '3min Polygon'),
            ('5', min5polygon, 'red', '5min Polygon')
        ]:
            polygon_coords = poly["features"][0]["geometry"]["coordinates"][0]
            lons, lats = zip(*polygon_coords)
            fig.add_trace(go.Scattermap(
                lon=lons,
                lat=lats,
                mode='lines',
                fill='toself',
                fillcolor=f'rgba(0,0,0,0)',
                line=dict(width=2, color=color),
                name=legend
            ))

    # Add locations
    # Extract all coffee location points
    lons_loc = []
    lats_loc = []
    for feature in locations["features"]:
        coords = feature["geometry"]["coordinates"]
        lons_loc.append(coords[0])
        lats_loc.append(coords[1])
    fig.add_trace(
        go.Scattermap(
            lon=lons_loc,
            lat=lats_loc,
            mode='markers',
            marker=dict(size=10, color='black'),
            name='Coffee Locations'
        )
    )

    # Add office location
    # Extract all coffee location points
    lons_loc = []
    lats_loc = []
    for feature in office["features"]:
        coords = feature["geometry"]["coordinates"]
        lons_loc.append(coords[0])
        lats_loc.append(coords[1])
    fig.add_trace(
        go.Scattermap(
            lon=lons_loc,
            lat=lats_loc,
            mode='markers',
            marker=dict(size=10, color='green'),
            name='VertiGIS Office'
        )
    )


    fig.update_layout(
        mapbox_style="carto-positron",
        mapbox_center={"lat": 48.42560463541031, "lon": -123.36973664430265},
        mapbox_zoom=18,
        margin={"r":0,"t":0,"l":0,"b":0},
        legend=dict(
            font=dict(size=18)
        ),
)
    return fig


# Calculations for scorecards
# total_locations = filtered_df.shape[0]
# total_revenue = filtered_df['properties.REVENUE'].sum()
# total_customers = filtered_df['properties.CUSTOMERS'].sum()
# total_donuts_sold = filtered_df['properties.DONUTS_SOLD'].sum()
# average_distance =  filtered_df['properties.DISTANCE(M)'].mean()
# average_drive_time = filtered_df['properties.DRIVE_TIME(MINS)'].mean()
# average_rating = filtered_df['properties.RATING'].mean()
# count_chains = filtered_df['properties.CHAIN_NAME'].value_counts()
# grouped_df = (filtered_df.groupby('properties.NAME', as_index=False)['properties.REVENUE'].sum().sort_values(by='properties.REVENUE', ascending=False))
# grouped_df1 = (filtered_df.groupby('properties.CHAIN_NAME', as_index=False)['properties.REVENUE'].sum().sort_values(by='properties.REVENUE', ascending=False))


# fig1 = px.bar(grouped_df, 
#               x='properties.NAME', 
#               y='properties.REVENUE', 
#               title='Coffee Shop Revenue',
#               labels={'properties.NAME': 'Coffee Shops', 'properties.REVENUE': 'Revenue ($)'})

# fig2 = px.pie(filtered_df, names="properties.CHAIN_NAME", 
#              title="Number of Chains vs. Independent Coffee Shops",
#                color_discrete_sequence=['#636EFA', '#EF553B'])

# fig3 = px.pie(grouped_df1, names="properties.CHAIN_NAME", 
#              title="Revenue by Coffee Shops",
#                color_discrete_sequence=['#636EFA', '#EF553B'])              

app.layout = html.Div([
    html.H1(
        "Coffee Shops Close to the VertiGIS NA Office (2, 3, 5 min. Drive Time) ",
        style={
            'textAlign': 'center',
            'marginTop': '20px',
            'marginBottom': '20px',
            'fontSize': '48px',
            'fontFamily': 'Arial, sans-serif',
            'fontWeight': 'bold',
            'color': '#333'
        }
    ),
    html.P("This map shows coffee shops found within 2, 3, and 5 min Drive Times from the VertiGIS office in Victoria, BC."),
    dcc.Dropdown(
        id='drive-time-dropdown',
        options=[
            {'label': 'ALL', 'value': 'all'},
            {'label': '2 min', 'value': '2'},
            {'label': '3 min', 'value': '3'},
            {'label': '5 min', 'value': '5'}
    ],
    value='all',  # default value
    clearable=False,
    style={'width': '200px', 'margin': '0 auto 20px auto', 'fontSize': '18px','fontWeight' : 'bold'}
),

        # --- SCORECARD SECTION ---
    html.Div([
        html.Div([
            html.H3("Coffee Shops", style={"fontsize": "24px", "fontWeight": "bold"}),
            html.P(id="scorecard-shops", style={"fontSize": "42px", "fontWeight": "bold"})
    ], style={"padding": "10px", "margin": "5px", "background": "#f9f9f9", "border": "2px solid #333", "borderRadius": "5px", "textAlign": "center", "width": "200px"}),
    html.Div([
        html.H3("Total Revenue", style={"fontsize": "24px", "fontWeight": "bold"}),
        html.P(id="scorecard-revenue", style={"fontSize": "42px", "fontWeight": "bold"})
    ], style={"padding": "10px", "margin": "5px", "background": "#f9f9f9", "border": "2px solid #333", "borderRadius": "5px", "textAlign": "center", "width": "200px"}),
    html.Div([
        html.H3("Total Customers", style={"fontsize": "24px", "fontWeight": "bold"}),
        html.P(id="scorecard-customers", style={"fontSize": "42px", "fontWeight": "bold"})
    ], style={"padding": "10px", "margin": "5px", "background": "#f9f9f9", "border": "2px solid #333", "borderRadius": "5px", "textAlign": "center", "width": "200px"}),
    html.Div([
        html.H3("Donuts Sold", style={"fontsize": "24px", "fontWeight": "bold"}),
        html.P(id="scorecard-donuts", style={"fontSize": "42px", "fontWeight": "bold"})
    ], style={"padding": "10px", "margin": "5px", "background": "#f9f9f9", "border": "2px solid #333", "borderRadius": "5px", "textAlign": "center", "width": "200px"}),
    html.Div([
        html.H3("Average Distance (M)", style={"fontsize": "24px", "fontWeight": "bold"}),
        html.P(id="scorecard-distance", style={"fontSize": "42px", "fontWeight": "bold"})
    ], style={"padding": "10px", "margin": "5px", "background": "#f9f9f9", "border": "2px solid #333", "borderRadius": "5px", "textAlign": "center", "width": "200px"}),
    html.Div([
        html.H3("Average Rating", style={"fontsize": "24px", "fontWeight": "bold"}),
        html.P(id="scorecard-rating", style={"fontSize": "42px", "fontWeight": "bold"})
    ], style={"padding": "10px", "margin": "5px", "background": "#f9f9f9", "border": "2px solid #333", "borderRadius": "5px", "textAlign": "center", "width": "200px"}),    
], style={"display": "flex", "justifyContent": "center", "marginBottom": "30px"}),   

    # Add the graph to the layout
    dcc.Graph(id='map-graph', style={'height': '80vh'}),
    dcc.Graph(id='bar-graph'),
    html.Div([
        dcc.Graph(id='pie-graph'),
        dcc.Graph(id='pie-graph-2'),
    ], style={"display": "flex", "justifyContent": "center", "alignItems": "stretch", "gap": "20px"}),
    dcc.Graph(id='scatter-graph'),
    html.Div([
    ], style={"display": "flex", "justifyContent": "center", "alignItems": "stretch", "gap": "20px"}),
    dcc.Graph(id='scatter-graph-2')
])

@app.callback(
    [
        Output('map-graph', 'figure'),
        Output('scorecard-shops', 'children'),
        Output('scorecard-revenue', 'children'),
        Output('scorecard-customers', 'children'),
        Output('scorecard-donuts', 'children'),
        Output('scorecard-distance', 'children'),
        Output('scorecard-rating', 'children'),
        Output('bar-graph', 'figure'),
        Output('pie-graph', 'figure'),
        Output('pie-graph-2', 'figure'),
        Output('scatter-graph', 'figure'),
        Output('scatter-graph-2', 'figure')
    ],
    Input('drive-time-dropdown', 'value')
)
def update_dashboard(selected_drive_time):
    if selected_drive_time == 'all':
        filtered_df = locations_df
    else:
        filtered_df = locations_df[locations_df['properties.DRIVE_TIME(MINS)'] == int(selected_drive_time)] 
                                                                                      
    # Scorecard calculations
    total_locations = filtered_df.shape[0]
    total_revenue = filtered_df['properties.REVENUE'].sum()
    total_customers = filtered_df['properties.CUSTOMERS'].sum()
    total_donuts_sold = filtered_df['properties.DONUTS_SOLD'].sum()
    average_distance = filtered_df['properties.DISTANCE(M)'].mean()
    average_rating = filtered_df['properties.RATING'].mean()

    grouped_df = (
        filtered_df.groupby('properties.NAME', as_index=False)['properties.REVENUE']
        .sum().sort_values(by='properties.REVENUE', ascending=False)
        .rename(columns={'properties.NAME': 'Coffee Shop', 'properties.REVENUE': 'Revenue ($)'})
    )
    grouped_df1 = (
        filtered_df.groupby('properties.CHAIN_NAME', as_index=False)['properties.REVENUE']
        .sum().sort_values(by='properties.REVENUE', ascending=False)
    )

    top5_names = (filtered_df.groupby('properties.NAME')['properties.REVENUE']
                  .sum()
                  .sort_values(ascending=False)
                  .head(5)
                  .index
    )
    top5_df = filtered_df[filtered_df['properties.NAME'].isin(top5_names)]


    fig1 = px.bar(grouped_df, x='Coffee Shop', y='Revenue ($)', title='Coffee Shop Revenue')
    fig2 = px.pie(filtered_df, names="properties.CHAIN_NAME", title="Number of Chains vs. Independent Coffee Shops")
    fig3 = px.pie(grouped_df1, names="properties.CHAIN_NAME", values="properties.REVENUE", title="Revenue by Coffee Shops")
    fig4 = px.scatter(filtered_df, x='properties.DISTANCE(M)', y='properties.REVENUE', size='properties.CUSTOMERS', color='properties.NAME', hover_name='properties.NAME', log_x=False, size_max=40,
                      title='Distance vs Revenue by Coffee Shop - Customer Counts',
                      labels={'properties.DISTANCE(M)': 'Distance (M)', 'properties.REVENUE': 'Revenue ($)', 'properties.CUSTOMERS': 'Customers', 'properties.NAME': 'Coffee Shop'})   
    fig5 = px.scatter(top5_df, x='properties.DISTANCE(M)', y='properties.REVENUE', size='properties.DONUTS_SOLD', color='properties.NAME', hover_name='properties.NAME', log_x=False, size_max=40,
                      title='Top 5 Coffee Chains by Revenue - Donuts Sold',
                      labels={'properties.DISTANCE(M)': 'Distance (M)', 'properties.REVENUE': 'Revenue ($)', 'properties.DONUTS_SOLD': 'Donuts Sold', 'properties.NAME': 'Coffee Shop'}) 

    # If you want a third chart, use grouped_df1


    # Map
    fig_map = create_map(selected_drive_time)

    return (
        fig_map, # Map figure
        f"{total_locations}", #scorecard-shops
        f"$ {total_revenue}", #scorecard-shops
        f"{total_customers}", #scorecard-shops
        f"{total_donuts_sold}", #scorecard-shops
        f"{average_distance:.1f}", #scorecard-shops
        f"{average_rating:.0f} Stars", #scorecard-shops
        fig1, #bar-graph all stores
        fig2, #pie-graph chains vs independents
        fig3, #pie-graph-2 revenue by coffee shops
        fig4, #scatter-graph distance vs revenue - customer counts bubble chart
        fig5, #scatter-graph-2 top 5 coffee chains by revenue - donuts sold bubble chart
    )


if __name__ == "__main__":
    app.run(debug=True)
