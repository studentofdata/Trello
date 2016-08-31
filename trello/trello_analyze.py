# -*- coding: utf-8 -*-
"""
Created on Fri Aug 19 15:10:48 2016

@author: Cloud User

TOOD: Move constants and/or inputs to a config file for a proper run through
 Comment code
 

    Clean up the name, this is a report generating file, treat it as such. 
 

 Clean up the plots of the report

 Generate a new section

 Perhaps a 'what's coming up next' type report

 Different Color Bar Charts
  
 Living Gantt Chart for Tasks



"""
from bokeh.models import ColumnDataSource, Rowfrom bokeh.models.widgets import DataTable, DateFormatter, TableColumn
from bokeh.layouts import gridplot, widgetbox, layout
from bokeh.charts import Bar, output_file, show
from bokeh.plotting import figure
from bokeh.io import show
import trello_transform
import os
import pandas as pd
import numpy as np


# Setup Cron jobs for daily and weekly report breakdowns for email and to 
# place into weekly resources discussion

# Edit these!
start_date = '2016-08-30'
end_date   = '2016-08-31'
output_file("output.html")


# Grab the the most raw data frame
data = trello_transform.generateData()


###############################################################################
""" Transform data for Pie Charts in report """

# Transform the frame for pie charts
data_bd = trello_transform.processPieChartData(data)

# Aggregate the frame by departments, sum hours (only available float field to sum)
department_breakdown = data_bd.groupby('departments').aggregate(np.sum)
# Aggregate the frame by operations, sum hours (only available float field to sum)
operations_breakdown = data_bd.groupby('operations').aggregate(np.sum)

# Only need the type of label and hour for the bar chart
department_breakdown = department_breakdown[['hrs']]
operations_breakdown = operations_breakdown[['hrs']]

# Plot
plot_1 = Bar(department_breakdown, values = 'hrs', title = "Hrs by Department")
plot_2 = Bar(operations_breakdown, values = 'hrs', title = "Hrs by Operation")


###############################################################################
""" Transform data for Table in report """

data_v2 = trello_transform.processTableData(data)
mask = (data_v2['date'] >= start_date) & (data_v2['date'] <= end_date)

data_thisweek = data_v2.loc[mask]

task_breakdown       = data_thisweek.groupby('task_name').aggregate(np.sum)
task_breakdown       = task_breakdown.reset_index()
task_breakdown       = task_breakdown[['task_name','hrs']].sort('hrs', ascending = False)

source = ColumnDataSource(task_breakdown)
columns = [
        TableColumn(field="task_name", title="Tasks"),
        TableColumn(field="hrs", title = "Hours")
        ]
        
data_table = DataTable(source = source, columns = columns)


###############################################################################
""" Layout and display report """

l = layout([
        [plot_1,plot_2],
        [data_table]
        ], sizing_mode = 'scale_width')


show(l)