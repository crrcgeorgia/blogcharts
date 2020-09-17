#%%

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

df2 = pd.read_csv('charts.csv')
df2['y'] = df2['y'].astype(str)
#%%
fig = go.Figure()
df = df2.groupby(['q', 'y'])['x'].mean().reset_index()



x = df[['q', 'y']].T
y = df['x']

fig.add_bar(x=x, y=y, text=y)

fig.update_layout(
    title="Fuck off",
    width=800,
    height=600,
    barmode="group",
    legend_orientation="h",
    xaxis_title="",
    yaxis_title="",
    legend=dict(x=-0, y=-0.1, traceorder="normal"),
)

fig.update_traces(texttemplate="%{text:.0f}", textposition="outside")
fig.update_layout(uniformtext_minsize=8, uniformtext_mode="hide")
fig.update_yaxes(automargin=True, title=None, tickfont={"size": 10})
fig.show()
# %%
