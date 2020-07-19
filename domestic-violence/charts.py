#%%

import pandas as pd
import plotly.express as px

colors = [
    "#d7191c",
    "#fdae61",
    "#ffffbf",
    "#abd9e9",
    "#2c7bb6",
][::-1]


#%%

path = "en/chart1.csv"
title = 'What do you think would be a reason [for a colleague being hesitant]<br>to report domestic violence?'
df = pd.read_csv(path).melt("label")
fig = px.bar(
    df,
    x="value",
    y="label",
    color="variable",
    barmode="stack",
    orientation="h",
    text="value",
    width=800,
    height=600,
    labels={"x": None, "y": None},
    title=title,
    color_discrete_sequence=colors,
)
fig.update_traces(texttemplate="%{text:.0f}", textfont_size=11, textposition="inside")
fig.update_layout(xaxis=dict(range=[0, 100]),)
fig.update_layout(
    legend=dict(
        orientation="h",
        yanchor="auto",
        y=-0.2,
        xanchor="auto",
        x=0,
        title="",
        font={"size": 10},
        tracegroupgap=0,
    ),
    margin={"autoexpand": True},
)
fig.update_yaxes(automargin=True, title=None, tickfont={"size": 10})
fig.update_xaxes(automargin=True, title=None)

fig.write_html('en/chart1.html')
# %%
