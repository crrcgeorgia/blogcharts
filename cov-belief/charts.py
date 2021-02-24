# %%
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

c1, c2, c3 = [pd.read_csv(f"ru/chart{i}.csv") for i in range(1, 4)]
config = {"displaylogo": False, "scrollZoom": False, "displayModeBar": False}
# %%
title = """
<b>Распространяется информация о технологиях 5G и коронавирусе.
<br>Согласны ли вы или не согласны с тем, что интернет-инфраструктура<br>5G связана с распространением коронавируса? (%)</b>
<br>(Опрос CRRC / NDI, июнь 2020 г.)
"""
fig = px.bar(c1, "x", "y", text="y", title=title)
fig.update_layout(
    xaxis_title="",
    yaxis_title="%",
    dragmode=False,
    title={"y": 0.95},
    font={"size": 10},
)
fig.update_yaxes(range=[0, 100])
fig.update_traces(texttemplate="%{text:0.0f}")
fig.show(config=config)
fig.write_html("en/chart1.html", config=config)
# %%
title = "<b>Как вы думаете, что вероятнее, что коронавирус... ?</b><br>(Опрос CRRC / NDI, июнь 2020 г.)"
fig = px.line(
    c2, x="x2", y="y", color="x1", title=title, facet_col="facet", error_y="err",
)
fig.update_layout(
    xaxis_title="",
    yaxis_title="",
    legend_title_text="",
    dragmode=False,
    title={"y": 0.93},
)
fig.update_layout(
    legend=dict(orientation="h", yanchor="top", y=-0.15, xanchor="right", x=1)
)
fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[1]))

for axis in fig.layout:
    if type(fig.layout[axis]) == go.layout.XAxis:
        fig.layout[axis].title.text = ""

fig.show(config=config)
fig.write_html("en/chart2.html", config=config)

# %%
title = """
<b>Распространяется информация о технологиях 5G и коронавирусе.<br>
Согласны ли вы или не согласны с тем, что интернет-инфраструктура<br>
5G связана с распространением коронавируса? <i>Согласны</i> (%)</b><br>(Опрос CRRC / NDI, июнь 2020 г.)
"""
fig = px.line(
    c3,
    x="x",
    y="y",
    title=title,
    facet_col="facet",
    error_y="err",
    )
fig.update_layout(
    xaxis_title="",
    yaxis_title="",
    legend_title_text="",
    margin=dict(
        l=25,
        r=25,
        b=25,
        t=100,
        pad=0),
    dragmode=False,
    title={"y": 0.95,},
    font={"size": 10},
)
fig.update_layout(
    legend=dict(orientation="h", yanchor="top", y=-0.15, xanchor="right", x=1)
)
fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[1]))
fig.layout.xaxis2.update(matches=None)
for axis in fig.layout:
    if type(fig.layout[axis]) == go.layout.XAxis:
        fig.layout[axis].title.text = ""
fig.update_xaxes(automargin=True)
fig.show(config=config)
fig.write_html("en/chart3.html", config=config)
# %%
