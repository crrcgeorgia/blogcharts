# %%
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

c1, c2, c3 = [pd.read_csv(f'en/chart{i}.csv') for i in range(1, 4)]
config = {'displaylogo': False, 'scrollZoom': False, 'displayModeBar': False}
# %%
title = '''
<b>There is news circulating regarding 5G technologies and coronavirus<br>
Do you agree or disagree that 5G internet infrastructure is linked<br>
to the spread of coronavirus? (%)</b><br>CRRC/NDI Survey June 2020
'''
fig = px.bar(c1, 'x', 'y', text='y', title=title)
fig.update_layout(xaxis_title="", yaxis_title="%",
                  dragmode=False, title={'y': 0.95}, font={"size": 10})
fig.update_yaxes(range=[0, 50])
fig.show(config=config)
fig.write_html('en/chart1.html', config=config)
# %%
title = '<b>Do you think it is most likely that the coronavirus... ?</b><br>CRRC/NDI Survey June 2020'
fig = px.line(c2, x='x2', y='y', color='x1', title=title,
              facet_col='facet', error_y='err', )
fig.update_layout(xaxis_title="", yaxis_title="", legend_title_text='',
                  dragmode=False, title={'y': 0.93})
fig.update_layout(legend=dict(
    orientation="h",
    yanchor="top",
    y=-0.15,
    xanchor="right",
    x=1
))
fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[1]))

for axis in fig.layout:
    if type(fig.layout[axis]) == go.layout.XAxis:
        fig.layout[axis].title.text = ''

fig.show(config=config)
fig.write_html('en/chart2.html', config=config)

# %%
title = '''
<b>There is news circulating regarding 5G technologies and coronavirus<br>
Do you agree or disagree that 5G internet infrastructure is linked<br>
to the spread of coronavirus? (%)</b><br>CRRC/NDI Survey June 2020
'''
fig = px.line(c3, x='x', y='y', title=title,
              facet_col='facet', error_y='err', facet_col_spacing=0.05)
fig.update_layout(xaxis_title="", yaxis_title="", legend_title_text='',
                  dragmode=False, title={'y': 0.95,}, font={"size": 10})
fig.update_layout(legend=dict(
    orientation="h",
    yanchor="top",
    y=-0.15,
    xanchor="right",
    x=1
))
fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[1]))
fig.layout.xaxis2.update(matches=None)
for axis in fig.layout:
    if type(fig.layout[axis]) == go.layout.XAxis:
        fig.layout[axis].title.text = ''

fig.show(config=config)
fig.write_html('en/chart3.html', config=config)
# %%
