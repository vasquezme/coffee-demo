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

## 4. App Layout<br>
Dash layout with html.Div, dcc.Dropdown for filtering, scorecard section, and multiple dcc.Graph components for map and charts.v
Scorecard section for key metrics (shops, revenue, customers, etc.).<br>

## 9. Scorecard Calculations<br>
Calculating totals and averages (number of shops, revenue, customers, donuts sold, average distance, average rating) from the filtered DataFrame.<br>

## 10. Figure Creation<br>
Creating charts (bar, pie, scatter) using Plotly Express, based on filtered data.<br>
Customizing chart labels, titles, and bubble sizes (e.g., using revenue for scatter size).<br>

## 12. Dash Callback<br>
Callback function to update all figures and scorecards when the dropdown filter changes.<br>
Filtering data based on dropdown selection.<br>
Returning figures and scorecard values in the correct order to match the layout.<br>

## 14. Figure Order<br>
Order of outputs in the callback must match the order of Output(...) in the callback decorator and the order of graphs in the layout.<br>

## 16. App Run Block<br>
The if __name__ == "__main__": block to run the Dash app.<br>


## Summary Table:<br>

Section	- Purpose<br>
Data Import - Load and prepare data<br>
Coordinate Extraction - Get lats/lons for polygons and points<br>
Map Definition -	Build map with polygons and markers<br>
App Layout -	Arrange UI, dropdown, scorecards, and graphs<br>
Scorecard Calculations -	Compute metrics for display<br>
Figure Creation -	Build bar, pie, scatter charts<br>
Dash Callback -	Update figures/scorecards on filter change<br>
Figure Order -	Ensure callback return order matches layout<br>
App Run Block -	Start the Dash server<br>


<!-- This is a hidden comment in the README
- clean up readme
- make summary section into table
-->
