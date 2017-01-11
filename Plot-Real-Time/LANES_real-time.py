import pandas as pd
from bokeh.plotting import figure,output_file,show,curdoc
from bokeh.embed import components

output_file('plot.html')

p = figure(width=1600, height=500, x_axis_type = "datetime")
bw = p.line([],[],color='navy',alpha=0.5)

ds = bw.data_source

def update():
    s_data = pd.read_csv('..\\test_data\s_192_168_1_4_2016-11-03-15_24_41_0296.csv', parse_dates=['Timestamp'])
    source_id3 = s_data[s_data['ID'].isin([3])]
    source_id3 = source_id3.tail(60)
    source_id3['Timestamp'] = pd.to_datetime(source_id3['Timestamp'], format='%Y%m%d%H%M%S')
    ds.data["x"] = source_id3['Timestamp']
    ds.data["y"] = source_id3['Throughput (bps)']

curdoc().add_root(p)

#Periodic Callback
curdoc().add_periodic_callback(update,500)



