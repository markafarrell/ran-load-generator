Testing of application frontend for LANES demo visualsation

Using Bokeh plotting library for generating plotting web objects
    - Use type 'datetime' to create an x-axis
    - script and div created fro embedded plots


Use the following code snippet for embedding applications (http://bokeh.pydata.org/en/latest/docs/user_guide/embed.html):
This requires bokeh to be loaded using the <link>

!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="utf-8">
        <title>Bokeh Scatter Plots</title>

        <link rel="stylesheet" href="http://cdn.pydata.org/bokeh/release/bokeh-0.12.0.min.css" type="text/css" />
        <script type="text/javascript" src="http://cdn.pydata.org/bokeh/release/bokeh-0.12.0.min.js"></script>

        <!-- COPY/PASTE SCRIPT HERE -->

    </head>
    <body>
        <!-- INSERT DIVS HERE -->
    </body>
</html>



Using Pandas to read csv and only display the last 60 data points
    - Date parsing is also done via 'Timestamp' column
    - Created a custom formatter to help read_csv format data accurately

To Do
Web Framework to present web application
Investigate creation of a web server framework possibly using Bokeh itself as frontend for application