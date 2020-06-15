#%%

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

c1, c2, c3, c4, c5 = [
    pd.read_excel("charts.xlsx", sheet_name=f"c{i}") for i in range(1, 6)
]
colors = ["#ef8a62", "gold", "#67a9cf"]
two_colors = ["#ef8a62", "#67a9cf"]
#%%
title = "The first and the second most important issues <br>facing Georgia (%)"
fig = px.bar(
    c1.melt("x"),
    x="x",
    y="value",
    text="value",
    color="variable",
    color_discrete_sequence=two_colors,
    barmode="group",
    title=title,
)
fig.update_layout(
    legend_orientation="h", xaxis_title="", yaxis_title="", legend_title_text=""
)
fig["layout"]["yaxis1"].update(range=[0, 100])
fig.update_traces(texttemplate="%{text:0.0f}", textposition="outside")
fig.show()
fig.write_html("chart1.html")

#%%
title = "The first and the second most important issues <br>grouped by isssue type (%)"
fig = px.bar(
    c2.melt("x"),
    x="x",
    y="value",
    text="value",
    title=title,
    color_discrete_sequence=two_colors[::-1],
)
fig.update_layout(legend_orientation="h", xaxis_title="", yaxis_title="")
fig["layout"]["yaxis1"].update(range=[0, 100])
fig.update_traces(texttemplate="%{text:0.0f}", textposition="outside")
fig.show()
fig.write_html("chart2.html")

#%%
fig = go.Figure()
title = "Predicted probability of most important issues <br>by settlement type, gender, education, and internet usage (%)"

x = c3[["x", "g"]].T
for n, y_lab in enumerate(c3.columns[2:]):
    fig.add_bar(x=x, y=c3[y_lab], name=y_lab, text=c3[y_lab], textfont=dict(size=8,))
    fig["data"][n]["marker"].update({"color": colors[n]})
fig.update_layout(
    title=title,
    width=600,
    height=500,
    legend_orientation="h",
    xaxis_title="",
    yaxis_title="",
    legend=dict(x=-0, y=-1.5),
)
fig["layout"]["yaxis1"].update(range=[0, 100])
fig.update_traces(texttemplate="%{text:.0f}", textposition="outside")

fig.show()
fig.write_html("chart3.html")

#%%
title = "Predicted probability of most important issues<br>by party closest to you (%)"

fig = px.bar(
    c4.melt("x"),
    x="x",
    y="value",
    color="variable",
    text="value",
    color_discrete_sequence=colors,
    barmode="group",
    title=title,
)
fig.update_layout(
    legend_orientation="h", xaxis_title="", yaxis_title="", legend_title_text=""
)

fig["layout"]["yaxis1"].update(range=[0, 100])
fig.update_traces(texttemplate="%{text:0.0f}", textposition="outside")
fig.show()
fig.write_html("chart4.html")

#%%
title = "The first and the second most important issues grouped by <br>isssue type and year (%)"

fig = px.line(
    c5.melt("x"),
    x="variable",
    y="value",
    color="x",
<<<<<<< HEAD
    # text='value',
    title=title,
    color_discrete_sequence=colors,
)
fig.update_layout(
    legend_orientation="h", xaxis_title="", yaxis_title="", legend_title_text=""
)
fig.update_traces(texttemplate="%{text:.0f}")
fig["layout"]["yaxis1"].update(range=[0, 100])
fig.update_layout(
    xaxis=dict(
        tickmode="array",
        tickvals=[
            2008,
            2009,
            2010,
            2011,
            2012,
            2013,
            2014,
            2015,
            2016,
            2017,
            2018,
            2019,
        ],
        ticktext=[
            2008,
            2009,
            2010,
            2011,
            2012,
            2013,
            2014,
            2015,
            2016,
            2017,
            2018,
            2019,
        ],
    )
)

annotations = []

for _, tup in c5.melt("x")[["variable", "value"]].iterrows():
    x = tup[0]
    y = tup[1]

    # labeling the first percentage of each bar (x_axis)
    annotations.append(
        dict(
            xref="x",
            yref="y",
            x=x,
            y=y,
            text=str(int(y)),
            font=dict(family="Calibri", size=12, color="rgb(0, 0, 0)"),
            showarrow=False,
        )
    )

fig.update_layout(annotations=annotations)
=======
    text='value',
    title=title,
    color_discrete_sequence=colors,
)
fig.update_layout(legend_orientation="h", xaxis_title="", yaxis_title="", legend_title_text='')
fig.update_traces(texttemplate="%{text:.0f}")
fig["layout"]["yaxis1"].update(range=[0, 100])
fig.update_layout(

    xaxis = dict(
        tickmode = 'array',
        tickvals = [2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019],
        ticktext = [2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019]
    )
)

>>>>>>> 2d1dbb7900aeaa94042a342b2a87cdbe218ca735

fig.show()
fig.write_html("chart5.html")


# %%
