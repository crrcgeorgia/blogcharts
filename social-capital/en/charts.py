#%%

import pandas as pd
import plotly.express as px

#%%
c1 = pd.read_csv('chart1.csv')
c1['x'] = c1['x'].astype(str)
t1 = 'Index of structural social capital - frequency distribution<br>(Caucasus Barometer 2019)'

fig1 = px.bar(c1, x='x', y='y', text='y',title=t1, width=800, height=400)
fig1.update_traces(textposition='outside')
fig1.update_layout(xaxis={'tickvals': list(range(0,12)), 'title': None}, yaxis={'title': None, 'range':[0,50]})
fig1.write_html('chart1.html')
fig1
#%%

c2 = pd.read_csv('chart2.csv')
c2['x'] = c2['x'].astype(str)
t2 = 'Index of structural social capital - frequency distribution<br>(Caucasus Barometer 2019)'

fig2 = px.bar(c2, x='x', text='y', y='y', title=t2, width=800, height=400)
fig2.update_layout(xaxis={'title': None}, yaxis={'title': None, 'range':[0,50]})

fig2.update_traces(textposition='outside')
fig2.write_html('chart2.html')
fig2

#%%
c3 = pd.read_csv('chart3.csv')
title = 'Index of structural social capital<br>(Caucasus Barometer 2019)'
fig = px.line(c3, x='response', y='value', error_y='ci', facet_col='group', facet_col_wrap=2, height=700, width=800, title = title)
fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
fig.update_xaxes(matches=None)
fig.update_layout(xaxis={'title': None}, yaxis={'title': None, 'range': [0, 6]})
fig.update_xaxes(showticklabels=True)
fig.write_html('chart3.html')

