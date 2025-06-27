# coffee-demo

https://coffee-demo.onrender.com/


## 1. Data Import & Preparation<br>
Loading GeoJSON and other data files (coffee locations, polygons, office).<br> 
Flattening GeoJSON with pd.json_normalize.<br>
Converting columns to numeric for calculations and plotting.<br>

## 2. Coordinate Extraction<br>
Extracting coordinates from GeoJSON features for both polygons (drive time areas) and point locations (coffee shops, office).<br>
Used for plotting polygons and markers on the map.<br>

## 3. Map Definition<br>
Defining the map figure using Plotly Graph Objects (go.Figure).<br>
Adding polygons for drive time areas with different colors and opacities.<br>
Adding coffee shop and office markers with custom hover text.<br>

## 4. App Layout
Dash layout with html.Div, dcc.Dropdown for filtering, scorecard section, and multiple dcc.Graph components for map and charts.
Scorecard section for key metrics (shops, revenue, customers, etc.).

9. Scorecard Calculations
Calculating totals and averages (number of shops, revenue, customers, donuts sold, average distance, average rating) from the filtered DataFrame.

10. Figure Creation
Creating charts (bar, pie, scatter) using Plotly Express, based on filtered data.
Customizing chart labels, titles, and bubble sizes (e.g., using revenue for scatter size).

12. Dash Callback
Callback function to update all figures and scorecards when the dropdown filter changes.
Filtering data based on dropdown selection.
Returning figures and scorecard values in the correct order to match the layout.

14. Figure Order
Order of outputs in the callback must match the order of Output(...) in the callback decorator and the order of graphs in the layout.

16. App Run Block
The if __name__ == "__main__": block to run the Dash app.


Summary Table:

Section	- Purpose
Data Import - Load and prepare data
Coordinate Extraction - Get lats/lons for polygons and points
Map Definition -	Build map with polygons and markers
App Layout -	Arrange UI, dropdown, scorecards, and graphs
Scorecard Calculations -	Compute metrics for display
Figure Creation -	Build bar, pie, scatter charts
Dash Callback -	Update figures/scorecards on filter change
Figure Order -	Ensure callback return order matches layout
App Run Block -	Start the Dash server
