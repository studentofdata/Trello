# -*- coding: utf-8 -*-
"""
Created on Fri Aug 19 15:10:48 2016

@author: Cloud User
"""

import trello_transform
import os
from bokeh.charts import Bar, output_file, show, hplot
from bokeh.plotting import figure
import pandas as pd



#Please add in documentation here
#Propse future amendments here
#
#
#
#


output_file("robert_wk1_breakdowns.html")

data = trello_transform.processData()

department_breakdown = data.groupby('departments').aggregate(np.sum)
operations_breakdown = data.groupby('operations').aggregate(np.sum)



department_breakdown = department_breakdown[['hrs']]
operations_breakdown = operations_breakdown[['hrs']]



plot_1 = Bar(department_breakdown, values = 'hrs', title = "Hrs by Department")
plot_2 = Bar(operations_breakdown, values = 'hrs', title = "Hrs by Operation")


p = hplot(plot_1, plot_2)

show(p)