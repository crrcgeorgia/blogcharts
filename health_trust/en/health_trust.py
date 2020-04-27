# -*- coding: utf-8 -*-
"""Untitled0.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1V9wrQgcQV19aftc1M8XvsXTTlWeuI7Bb
"""

import plotly.graph_objects as go
import pandas as pd

dems = pd.read_csv('trust_demographics.csv')

five_colours = ['#ca0020', '#f4a582', '#f7f7f7', '#92c5de', '#0571b0']
three_colours = ['#ef8a62', '#f7f7f7', '#67a9cf']

colors = three_colours[::-1]
fig = go.Figure()
x = dems[['cat', 'type']].T
for n, y_lab in enumerate(['Distrust', 'Neither trust nor distrust', 'Trust'][::-1]):
  fig.add_bar(x=x, y=dems[y_lab], name=y_lab)
  fig['data'][n]['marker'].update({'color': colors[n]})

fig.update_layout(
    title="Predicted probability of healthcare system trust<br>by settlement type, gender, minority status and internet usage (%)",
    font=dict(
        family="Calibri",
        size=18,
        color="#7f7f7f"
    ),
    yaxis = dict(range = [0,100]),
    plot_bgcolor='white'
)
fig.show()
fig.write_html("chart2.html")

ins = pd.read_csv('trust_institutions.csv')
ins = ins.set_index('Institution').assign(total=lambda x: x.sum(axis=1))
ins = ins[ins.columns[:-1]].div(ins['total'], axis=0).mul(100).reset_index().iloc[::-1]

# colors = ['#006400', '#228B22', 'yellow', '#FFA500', 'red', 'grey', 'black', 'red']
colors = five_colours[::-1] + ['darkgrey', 'darkslategrey']
y = ins['Institution']

fig = go.Figure()

annotations = []
for n, x_lab in enumerate(ins.columns[1:]):
  fig.add_trace(go.Bar(x=ins[x_lab], y=y, name=x_lab, orientation='h', legendgroup=range(len(ins.columns)-1)[-n]))
  fig['data'][n]['marker'].update({'color': colors[n]})


for yd, xd in zip(y, ins[ins.columns[1:]].values):

    # labeling the first percentage of each bar (x_axis)
    annotations.append(dict(xref='x', yref='y',
                            x=xd[0] / 2, y=yd,
                            text=str(int(xd[0])),
                            font=dict(family='Calibri', size=12,
                                      color='rgb(248, 248, 255)'),
                            showarrow=False))

    space = xd[0]
    for i in range(1, len(xd)):
      # labeling the rest of percentages for each bar (x_axis)
      txt = str(int(xd[i]))
      if i in [2]:
        color = 'black'
      else:
        color = 'white'
      annotations.append(dict(xref='x', yref='y',
                              x=space + (xd[i]/2), y=yd,
                              text=txt,
                              font=dict(family='Calibri', size=12,
                                        color=color),
                              showarrow=False))
      space += xd[i]

fig.update_layout(
    title="Trust towards social and political institutions (%)",
    font=dict(
        family="Calibri",
        size=18,
        color="#7f7f7f"
    )
)
fig.update_layout(barmode='stack', xaxis = dict(range = [0,100]), annotations=annotations, legend=dict(
                orientation="h"), plot_bgcolor='white')

fig.show()
fig.write_html("chart1.html")