#%%

import pandas as pd
import plotly.graph_objects as go


colors2 = ["maroon", "orange", "midnightblue", "dimgray"]
color_list = [colors1, colors2, colors2]
titles = [
    ,
    """In your opinion, abuse of power by prosecutors in Georgia<br>
is a frequent case, a rare case, or never the case? (%)""",
    """In your opinion, prosecutors in Georgia making deals with judges<br>
in order to have decisions favourable for them is a frequent<br>
case, a rare case, or never the case? (%)""",
]


df1 = pd.read_csv('chart1.csv')
df2 = pd.read_csv('chart2.csv')
df3 = pd.read_csv('chart3.csv')


# %%

#%%
colors1 = ["midnightblue", "maroon", "teal", "dimgray"]

title = """
In your opinion, who should take care of parents more a son or a daughter?<br>
By In your opinion, who should inherit the apartment? (%)
<br>(CRRC, Caucasus Barometer 2019, Georgia)
"""

y = df1['index']
fig = go.Figure()

annotations = []
for n, x_lab in enumerate(df1.columns[1:]):
    fig.add_trace(
        go.Bar(
            x=df1[x_lab],
            y=y,
            name=x_lab,
            orientation="h",
            legendgroup=range(len(df1.columns) - 1)[-n],
        )
    )
    fig["data"][n]["marker"].update({"color": colors1[n]})

for yd, xd in zip(y, df1[df1.columns[1:]].values):

    # labeling the first percentage of each bar (x_axis)
    annotations.append(
        dict(
            xref="x",
            yref="y",
            x=xd[0] / 2,
            y=yd,
            text=str(int(round(xd[0], 0))),
            font=dict(family="sans-serif", size=12, color="rgb(248, 248, 255)"),
            showarrow=False,
        )
    )

    space = xd[0]
    for i in range(1, len(xd)):
        # labeling the rest of percentages for each bar (x_axis)
        txt = str(int(round(xd[i], 0)))
        if int(txt) == 0:
            continue
        else:
            annotations.append(
                dict(
                    xref="x",
                    yref="y",
                    x=space + (xd[i] / 2),
                    y=yd,
                    text=txt,
                    font=dict(
                        family="sans-serif", size=12, color="rgb(248, 248, 255)"
                    ),
                    showarrow=False,
                )
            )
            space += xd[i]

fig.update_layout(
    title=title, font=dict(family="sans-serif", size=12, color="#7f7f7f"),
)
fig.update_layout(
    barmode="stack",
    xaxis=dict(range=[0, 100]),
    annotations=annotations,
    legend=dict(orientation="h"),
    plot_bgcolor="white",
)
fig.update_yaxes(tickvals=y)
fig.show()
fig.write_html(f"test.html")

# %%
df2
#%%

import plotly.express as px

fig = px.scatter(df2, x="value", y="demographic", facet_col="response", error_x='conf')
# fig.update_xaxes(range=[-0.5, 0.5], col=1)
fig.show()
