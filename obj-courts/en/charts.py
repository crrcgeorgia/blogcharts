#%%
import pandas as pd
import plotly.graph_objects as go

c1, c2, c3 = [pd.read_csv(f"chart{i}.csv") for i in [1, 2, 3]]


#%%
fig = go.Figure()
title = """
Court system favors some citizens VS treats all equally (%)
"""
if c1['y'].max() > 1:
    c1['y'] = c1['y'].div(100)

x = c1["x"].T

fig.add_bar(x=x, y=c1['y'], text=c1['y'])

fig.update_layout(
    title=title,
    width=800,
    height=600,
    legend_orientation="h",
    xaxis_title="",
    yaxis_title="",
    legend=dict(x=-0, y=-1.5),
)
fig["layout"]["yaxis1"].update(range=[0, 1], tickformat=".0%")
fig.update_traces(texttemplate="%{text:.0%}", textposition="outside")

fig.show()
fig.write_html("chart1.html")

#%%

fig = go.Figure()
title = """
Predicted probability of agreement that court system favors some citizens<br> 
by settlement type, ethnicity, and education (%)
"""

x = c2[["g", "x"]].T
for n, y_lab in enumerate(c2.columns[2:]):
    fig.add_bar(x=x, y=c2[y_lab], name=y_lab, text=c2[y_lab])

fig.update_layout(
    title=title,
    width=800,
    height=600,
    legend_orientation="h",
    xaxis_title="",
    yaxis_title="",
    legend=dict(x=-0, y=-1.5),
)
fig["layout"]["yaxis1"].update(range=[0, 1], tickformat=".0%")
fig.update_traces(texttemplate="%{text:.0%}", textposition="outside")

fig.show()
fig.write_html("chart2.html")

#%%
fig = go.Figure()
title = """
Predicted probability of agreement that court system favors some citizens<br>
by party support, institutional trust, and self-precevied treatment by government (%)

"""


x = c3[["g", "x"]].T
for n, y_lab in enumerate(c3.columns[2:]):
    fig.add_bar(x=x, y=c3[y_lab], name=y_lab, text=c3[y_lab])

fig.update_layout(
    title=title,
    width=800,
    height=600,
    legend_orientation="h",
    xaxis_title="",
    yaxis_title="",
    legend=dict(x=-0, y=-1.5),
)
fig["layout"]["yaxis1"].update(range=[0, 1], tickformat=".0%")
fig.update_traces(texttemplate="%{text:.0%}", textposition="outside")

fig.show()
fig.write_html("chart3.html")