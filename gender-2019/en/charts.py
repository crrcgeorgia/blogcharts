# %%

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

config = {'displaylogo': False, 'scrollZoom': False, 'displayModeBar': False}
df2 = pd.read_csv('charts.csv')
df2['y'] = df2['y'].astype(str)

# %%
fig = go.Figure()
df = df2.groupby(['q', 'y'])['x'].mean().reset_index()

colors = ['#31859C', '#604A7B'] * 5

x = df[['q', 'y']].T
y = df['x']

fig.add_bar(x=x, y=y, text=y, marker_color=colors)

fig.update_layout(
    title="Never acceptable for a woman in Georgia to… (%)",
    width=800,
    height=600,
    barmode="group",
    legend_orientation="h",
    xaxis_title="",
    yaxis_title="",
    legend=dict(x=-0, y=-0.1, traceorder="normal"),
)
fig.update_yaxes(range=[0, 100])
fig.update_traces(texttemplate="%{text:.0f}", textposition="outside")
fig.update_layout(uniformtext_minsize=8, uniformtext_mode="hide")
fig.update_yaxes(automargin=True, title=None, tickfont={"size": 10})
fig.show(config=config)
fig.write_html('chart1.html', config=config)

# %%
fig = go.Figure()

df = df2.groupby(['q', 'y'])['x'].mean().reset_index()

for n, gender in enumerate(['Male', 'Female']):
    tab = df2[df2.g == gender]
    fig.add_bar(x=tab[['q', 'y']].T, y=tab['x'], text= tab['x'],
                name=gender, marker_color=colors[n])
fig.update_yaxes(range=[0, 100])
fig.update_layout(
    title="Never acceptable for a woman in Georgia to… (%)",
    width=800,
    height=600,
    barmode="group",
    # legend_orientation="h",
    xaxis_title="",
    yaxis_title="",
    # legend=dict(x=-0, y=-0.1, traceorder="normal"),
)

fig.update_traces(texttemplate="%{text:.0f}", textposition="outside")
fig.update_layout(uniformtext_minsize=8, uniformtext_mode="hide")
fig.update_yaxes(automargin=True, title=None, tickfont={"size": 10})
fig.show(config=config)
fig.write_html('chart2.html', config=config)

# %%
# df2['q'] = df2['q'].str.replace('<br>', ' ')
fig = px.scatter(df2, x='x', y=['q', 'g'],
                 facet_row='q', color='y', color_discrete_sequence=colors, width=800, height=600, title="Never acceptable for a woman in Georgia to… (%)", facet_row_spacing=0.05)

fig.update_xaxes(range=[0, 100])
fig.for_each_annotation(lambda a: a.update(
    text=f'<b>{a.text.split("=")[-1]}<b>', textangle=0, x=-0.4, align='left'))
fig.update_layout(
    margin=dict(l=250, r=20, t=80, b=20),
)
fig.update_traces(marker={'size':16, 'opacity':0.75})
for axis in fig.layout:
    if type(fig.layout[axis]) in [go.layout.XAxis, go.layout.YAxis]:
        fig.layout[axis].title.text = ''

fig.update_layout(legend=dict(
    orientation="h",
    yanchor="bottom",
    y=1,
    xanchor="right",
    x=1,
    title=''

))

fig.show()
fig.write_html('chart3.html')

# %%
# df2['q'] = df2['q'].str.replace('<br>', ' ')
fig = px.scatter(df2, x='x', y=['q', 'y'],
                 facet_row='q', color='g', color_discrete_sequence=colors, width=800, height=600, title="Never acceptable for a woman in Georgia to… (%)", facet_row_spacing=0.05)

fig.update_xaxes(range=[0, 100])
fig.for_each_annotation(lambda a: a.update(
    text=f'<b>{a.text.split("=")[-1]}<b>', textangle=0, x=-0.4, align='left'))
fig.update_layout(
    margin=dict(l=250, r=20, t=80, b=20),
)
fig.update_traces(marker={'size':16, 'opacity':0.75})
for axis in fig.layout:
    if type(fig.layout[axis]) in [go.layout.XAxis, go.layout.YAxis]:
        fig.layout[axis].title.text = ''
    if type(fig.layout[axis]) == go.layout.YAxis:
        fig.layout[axis].tickmode = 'array'
        fig.layout[axis].tickvals = [2019, 2010]
fig.update_layout(legend=dict(
    orientation="h",
    yanchor="bottom",
    y=1,
    xanchor="right",
    x=1,
    title=''

))


fig.show()
fig.write_html('chart4.html')
