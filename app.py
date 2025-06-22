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

fig = go.Figure()

# Extract coordinates for the 2min polygon (assuming Polygon geometry)
polygon_coords = min2polygon["features"][0]["geometry"]["coordinates"][0]
lons, lats = zip(*polygon_coords)
fig.add_trace(
    go.Scattermap(
        lon=lons,
        lat=lats,
        mode='lines',
        fill='toself',
        fillcolor='rgba(0,255,0,0.2)',
        line=dict(width=2, color='green'),
        name='2min Polygon'
    )
)

# Add 3min polygon
polygon_coords_3min = min3polygon["features"][0]["geometry"]["coordinates"][0]
lons_3min, lats_3min = zip(*polygon_coords_3min)
fig.add_trace(
    go.Scattermap(
        lon=lons_3min,
        lat=lats_3min,
        mode='lines',
        fill='toself',
        fillcolor='rgba(255,165,0,0.2)',  # orange
        line=dict(width=2, color='orange'),
        name='3min Polygon'
    )
)

# Add 5min polygon
polygon_coords_5min = min5polygon["features"][0]["geometry"]["coordinates"][0]
lons_5min, lats_5min = zip(*polygon_coords_5min)
fig.add_trace(
    go.Scattermap(
        lon=lons_5min,
        lat=lats_5min,
        mode='lines',
        fill='toself',
        fillcolor='rgba(255,0,0,0.2)',  # red
        line=dict(width=2, color='red'),
        name='5min Polygon'
    )
)

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
    margin={"r":0,"t":0,"l":0,"b":0}
)

# Calculations for the scorecard
total_locations = locations_df.shape[0]
total_revenue = locations_df['properties.REVENUE'].sum()
total_customers = locations_df['properties.CUSTOMERS'].sum()
total_donuts_sold = locations_df['properties.DONUTS_SOLD'].sum()
average_distance =  locations_df['properties.DISTANCE(M)'].mean()
average_drive_time = locations_df['properties.DRIVE_TIME(MINS)'].mean()
average_rating = locations_df['properties.RATING'].mean()
count_chains = locations_df['properties.CHAIN_NAME'].value_counts()

fig1 = px.bar(locations_df, 
               x='properties.NAME', 
               y='properties.REVENUE', 
               title='Coffee Shop Revenue',
               labels={'properties.NAME': 'Coffee Shop', 'properties.REVENUE': 'Revenue ($)'},
               color='properties.RATING',
               color_continuous_scale=px.colors.sequential.Plasma)

fig2 = px.pie(locations_df, names="properties.CHAIN", 
              title="Chain vs Independent Coffee Shops",
                color_discrete_sequence=['#636EFA', '#EF553B'])
              

app.layout = html.Div([
    html.H1(
        "Coffee Shops Close to VertiGIS (2, 3, 5min Drive Time) ",
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
    
        # --- SCORECARD SECTION ---
    html.Div([
        html.Div([
            html.H3("Coffee Shops"),
            html.P(f"{len(locations['features'])}", style={"fontSize": "32px", "fontWeight": "bold"})
        ], style={"padding": "20px", "margin": "10px", "background": "#f9f9f9", "border": "2px solid #333", "borderRadius": "10px", "textAlign": "center", "width": "200px"}),
        html.Div([
            html.H3("Total Revenue"),
            html.P(f"$ {total_revenue}", style={"fontSize": "32px", "fontWeight": "bold"})
        ], style={"padding": "20px", "margin": "10px", "background": "#f9f9f9", "border": "2px solid #333", "borderRadius": "10px", "textAlign": "center", "width": "200px"}),
        html.Div([
            html.H3("Total Customers"),
            html.P(f"{total_customers}", style={"fontSize": "32px", "fontWeight": "bold"})
        ], style={"padding": "20px", "margin": "10px", "background": "#f9f9f9", "border": "2px solid #333", "borderRadius": "10px", "textAlign": "center", "width": "200px"}),
        html.Div([
            html.H3("Donuts Sold"),
            html.P(f"{total_donuts_sold}", style={"fontSize": "32px", "fontWeight": "bold"})
        ], style={"padding": "20px", "margin": "10px", "background": "#f9f9f9", "border": "2px solid #333", "borderRadius": "10px", "textAlign": "center", "width": "200px"}),
        html.Div([
            html.H3("Average Distance (M)"),
            html.P(f"{average_distance:.1f}", style={"fontSize": "32px", "fontWeight": "bold"})
        ], style={"padding": "20px", "margin": "10px", "background": "#f9f9f9", "border": "2px solid #333", "borderRadius": "10px", "textAlign": "center", "width": "200px"}),
        html.Div([
            html.H3("Average Rating"),
            html.P(f"{average_rating:.0f} Stars", style={"fontSize": "32px", "fontWeight": "bold"})
        ], style={"padding": "20px", "margin": "10px", "background": "#f9f9f9", "border": "2px solid #333", "borderRadius": "10px", "textAlign": "center", "width": "200px"}),    
    ], style={"display": "flex", "justifyContent": "center", "marginBottom": "30px"}),
    
    
    # Add the graph to the layout
    dcc.Graph(figure=fig, style={"height": "80vh"}),
    dcc.Graph(figure=fig1) if fig1 else html.P("No data available."),
    dcc.Graph(figure=fig2) if fig2 else html.P("No data available."),
])

if __name__ == "__main__":
    app.run(debug=True)
