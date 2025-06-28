# coffee-demo

https://coffee-demo.onrender.com/


## 1. Data Import & Preparation<br>
Loading GeoJSON and other data files (coffee locations, polygons, office).<br> 
Flattening GeoJSON with pd.json_normalize.<br>
Converting columns to numeric for calculations and plotting.<br>

(Lines 7–28 in your code)<br>

## 2. Coordinate Extraction<br>
Extracting coordinates from GeoJSON features for both polygons (drive time areas) and point locations (coffee shops, office).<br>
Used for plotting polygons and markers on the map.<br>

(In your create_map function, lines 35–90)<br>

## 3. Map Definition<br>
Defining the map figure using Plotly Graph Objects (go.Figure).<br>
Adding polygons for drive time areas with different colors and opacities.<br>
Adding coffee shop and office markers with custom hover text.<br>

(In your create_map function, lines 33–110)

## 4. App Layout<br>
Dash layout with html.Div, dcc.Dropdown for filtering, scorecard section, and multiple dcc.Graph components for map and charts.v
Scorecard section for key metrics (shops, revenue, customers, etc.).<br>

(Your app.layout block, lines 113–184)

## 5. Scorecard Calculations<br>
Calculating totals and averages (number of shops, revenue, customers, donuts sold, average distance, average rating) from the filtered DataFrame.<br>

(In your callback, lines 191–205)

## 6. Figure Creation<br>
Creating charts (bar, pie, scatter) using Plotly Express, based on filtered data.<br>
Customizing chart labels, titles, and bubble sizes (e.g., using revenue for scatter size).<br>

(In your callback, lines 210–225)

## 7. Dash Callback<br>
Callback function to update all figures and scorecards when the dropdown filter changes.<br>
Filtering data based on dropdown selection.<br>
Returning figures and scorecard values in the correct order to match the layout.<br>

(Your @app.callback and update_dashboard function, lines 186–282)

## 8. Figure Order<br>
Order of outputs in the callback must match the order of Output(...) in the callback decorator and the order of graphs in the layout.<br>

(Return statement in your callback, lines 274–285)

## 9. App Run Block<br>
The if __name__ == "__main__": block to run the Dash app.<br>

(Lines 288–290)

## Summary Table:<br>

<div align="center">

| Section	| Purpose |
|-------- | ------- |
| Data Import | Load and prepare data
| Coordinate Extraction | Get lats/lons for polygons and points
| Map Definition |	Build map with polygons and markers
| App Layout | Arrange UI, dropdown, scorecards, and graphs
| Scorecard Calculations |	Compute metrics for display
| Figure Creation | Build bar, pie, scatter charts
| Dash Callback | Update figures/scorecards on filter change
| Figure Order |	Ensure callback return order matches layout
| App Run Block | Start the Dash server

</div>

<!-- This is a hidden comment in the README
- clean up readme
- make summary section into table
-->
