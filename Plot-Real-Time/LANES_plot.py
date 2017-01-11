#ToDo - Import required libraries from Bokeh
import numpy as np
import pandas as pd
from bokeh.plotting import figure,output_file,show
from bokeh.embed import components

#Might be able to refactor a couple of lines if only process 3 is reported so no process filtering is required


#ToDo - Use pandas to (1) open csv, (2) parse dates from 'Timestamp' (3) get tail 60 data (4)

s_data = pd.read_csv('..\\test_data\s_192_168_1_4_2016-11-03-15_24_41_0296.csv',parse_dates=['Timestamp'])
source_id3 = s_data[s_data['ID'].isin([3])]
source_id3 = source_id3.tail(60)
source_id3['Timestamp'] = pd.to_datetime(source_id3['Timestamp'],format='%Y-%m-%d %H:%M:%s')
#print(type(source_id3['Timestamp']))  --->    <class 'pandas.core.series.Series'>
#print(type(source_id3['Throughput (bps)']))   ---->    <class 'pandas.core.series.Series'>

#print(source_id3)
#ToDo - plot line using bokeh xdata- Timestamp  ydata - BW

output_file('plot.html')

p = figure(width=1600, height=500, x_axis_type = "datetime")
p.line(source_id3['Timestamp'],source_id3['Throughput (bps)'],color='navy',alpha=0.5)

show(p)

script, div = components(p)
print(script)
print(div)

#ToDo - Cosmetics - update in while loop or via external process run every second