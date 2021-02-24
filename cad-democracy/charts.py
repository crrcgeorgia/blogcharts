#%%

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

colors = ["#d7191c", "#fdae61", "#ffffbf", "#abd9e9", "#2c7bb6",][::-1]

#%%
c3 = pd.read_csv("en/chart1.csv")
fig = go.Figure()
title = "Predicted probability of preferring democracy to any other kind of government<br>by settlement, ethincity and education (%)"

x = c3[["label", "group"]].T
for n, y_lab in enumerate(c3.columns[2:]):
    fig.add_bar(x=x, y=c3[y_lab], name=y_lab, text=c3[y_lab], textfont=dict(size=8,))
    fig["data"][n]["marker"].update({"color": colors[n]})
fig.update_layout(
    title=title,
    width=800,
    height=600,
    legend_orientation="h",
    xaxis_title="",
    yaxis_title="",
    legend=dict(x=-0, y=-1.5),
)
fig["layout"]["yaxis1"].update(range=[0, 100])
fig.update_traces(texttemplate="%{text:.0f}", textposition="outside")

fig.show()
fig.write_html("en/chart1.html")

# %%

