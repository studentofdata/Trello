# -*- coding: utf-8 -*-
"""
Created on Fri Aug 19 15:10:48 2016

@author: Cloud User

TOOD: Move constants and/or inputs to a config file for a proper run through
 Comment code
 Clean up the plots of the report
 Generate a new section
 Perhaps a 'what's coming up next' type report
 Different Color Bar Charts
 
 
 Living Gantt Chart for Tasks



"""

import trello_transform
import os
from bokeh.charts import Bar, output_file, show

from bokeh.io import show

from bokeh.layouts import gridplot, widgetbox, layout

from bokeh.plotting import figure

from bokeh.models import ColumnDataSource, Row
from bokeh.models.widgets import DataTable, DateFormatter, TableColumn

import pandas as pd
import numpy as np




# Edit these!
start_date = '2016-08-22'
end_date   = '2016-08-26'




output_file("robert_wk2_breakdowns.html")

#data = trello_transform.generateData()
#data_bd = trello_transform.processData(data)

department_breakdown = data_bd.groupby('departments').aggregate(np.sum)
operations_breakdown = data_bd.groupby('operations').aggregate(np.sum)

department_breakdown = department_breakdown[['hrs']]
operations_breakdown = operations_breakdown[['hrs']]

plot_1 = Bar(department_breakdown, values = 'hrs', title = "Hrs by Department")
plot_2 = Bar(operations_breakdown, values = 'hrs', title = "Hrs by Operation")


data_v2 = trello_transform.outputData(data)
mask = (data_v2['date'] >= start_date) & (data_v2['date'] <= end_date)

data_thisweek = data_v2.loc[mask]

department_breakdown = data_thisweek.groupby('departments').aggregate(np.sum)
operations_breakdown = data_thisweek.groupby('operations').aggregate(np.sum)
task_breakdown       = data_thisweek.groupby('task_name').aggregate(np.sum)
task_breakdown       = task_breakdown.reset_index()


department_breakdown = department_breakdown[['hrs']]
operations_breakdown = operations_breakdown[['hrs']]
task_breakdown       = task_breakdown[['task_name','hrs']].sort('hrs', ascending = False)



source = ColumnDataSource(task_breakdown)
columns = [
        TableColumn(field="task_name", title="Tasks"),
        TableColumn(field="hrs", title = "Hours")
        ]
        
data_table = DataTable(source = source, columns = columns)


plot_1 = Bar(department_breakdown, values = 'hrs', title = "Hrs by Department")
plot_2 = Bar(operations_breakdown, values = 'hrs', title = "Hrs by Operation")

l = layout([
        [plot_1,plot_2],
        [data_table]], sizing_mode = 'scale_width')



show(l)