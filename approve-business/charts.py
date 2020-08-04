#%%

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# %%

title = "Approval of doing business with the following nationalities<br>Caucaus Barometer, Georgia and Armenia (2009 and 2019)"

chart1 = (
    pd.read_csv("en/charts.csv")
    .query('group == "Business"')
    .drop("group", axis=1)
    .melt(["label", "year"])
)
fig = px.bar(
    x="value",
    y="label",
    facet_col="year",
    color="variable",
    orientation="h",
    barmode="group",
    data_frame=chart1.loc[::-1],
    labels={"x": None, "y": None},
)
fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[1]))
for axis in fig.layout:
    if type(fig.layout[axis]) in [go.layout.XAxis, go.layout.YAxis]:
        fig.layout[axis].title.text = None

fig.update_layout(
    title=title,
    width=800,
    height=600,
    legend_orientation="h",
    legend=dict(x=-0, y=-0.05, traceorder="normal", title=""),
    margin=dict(l=50, r=50, b=20, t=100, pad=4),
)

fig.write_html('chart1.html')
#%%

title = "Approval of women of your nationality marrying the following nationalities<br>Caucaus Barometer, Georgia and Armenia (2009 and 2019)"

chart1 = (
    pd.read_csv("en/charts.csv")
    .query('group == "Marriage"')
    .drop("group", axis=1)
    .melt(["label", "year"])
)
fig = px.bar(
    x="value",
    y="label",
    facet_col="year",
    color="variable",
    orientation="h",
    barmode="group",
    data_frame=chart1.loc[::-1],
    labels={"x": None, "y": None},
)
fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[1]))
for axis in fig.layout:
    if type(fig.layout[axis]) in [go.layout.XAxis, go.layout.YAxis]:
        fig.layout[axis].title.text = None

fig.update_layout(
    title=title,
    width=800,
    height=600,
    legend_orientation="h",
    legend=dict(x=-0, y=-0.05, traceorder="normal", title=""),
    margin=dict(l=50, r=50, b=20, t=100, pad=4),
)

fig.write_html('en/chart2.html')
fig.show()
# %%
