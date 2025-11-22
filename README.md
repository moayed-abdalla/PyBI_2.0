📊 Dynamic KPI Dashboard Builder

This is a "full-stack" Python application built with Streamlit that allows business analysts and data engineers to quickly build and customize a KPI dashboard by uploading their own data.

The app uses pandas for data manipulation and plotly for interactive, modern data visualizations. The UI is customized with injected CSS to provide a clean, modern feel with rounded corners and shadows.

Features

Upload Your Data: Supports both .csv and .xlsx (Excel) files.

Add Multiple KPIs: Build a full dashboard by adding charts. and connecting it to the data set

Interactive Configuration:

Add KPIs via an intuitive space with a plus (+) sign on the top left of the page. it should be possible to resize graphs by dragging the side walls and adding a new graph beside or below it with the plus sign. 

Each graph should have an options pop up by click on the gear icon on the top right of each graph. this gear icon should only be visable if the user is hovering over the graph. the setting pop up should have the option to flip x and y, remove the graph and remove label and lines from the graph

when clicking on the plus sign to add a graph the user should select from multiple chart types (integer metric(just a number), Bar, Line, Scatter, Pie).

Toggle side bar that allows you to navigate between different dashboards 

Modern UI: Custom CSS provides a clean, web-app feel with rounded corners and shadows. 

Responsive Dark/Light Mode: The application and its charts automatically adapt to your system's setting. The charts should use pre-registered colors that have a light and dark version, and depending on the setting it will use the correct color library
