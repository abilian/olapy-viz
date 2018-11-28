## OlaPy-Viz

The purpose of this tool which still on development is to let you explore your data quickly to extract 
the information they hold. You can only create simple plots.

This tool allows you to interactively explore your data by visualizing it with the olapy and bokeh packages. 
It allows you to draw bar graphs, circles, lines plots..., then export the graph.


How to use it
-------------

Start by importing your data (as csv files format right now), you can import either one file containing all your data, or
separated files dataset which follows [star schema model](http://datawarehouse4u.info/Data-warehouse-schema-architecture-star-schema.html)

<i>(you can use the two data sets demos in the [repository](https://github.com/abilian/olapy-web/tree/olapy-web2.0/demo_datasets) as example)</i>

![Import Data sets](https://raw.githubusercontent.com/abilian/olapy-web/olapy-web2.0/docs/img/import_files.gif)

Now lets construct some charts, to do so, drag and drop variables to x and y axis


Options-menus are available under the chart to modify some parameters:


![Circle chart](https://raw.githubusercontent.com/abilian/olapy-web/olapy-web2.0/docs/img/circle_hex_chart.gif)


Try it by yourself
------------------

First you need to clone the repository with:

    git clone https://github.com/abilian/olapy-web.git
    git ckeckout olapy-web2.0

install dependencies, ideally in a virtualenv  with:

    make install
    
run it with:

    make run
    
and then go to [http://localhost:5000/](http://localhost:5000/) 
    
