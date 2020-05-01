import pandas as pd
import plotly.graph_objects as go

colors1 = ["midnightblue", "maroon", "darkgrey", "dimgray"]
colors2 = ["maroon", "orange", "midnightblue", "dimgray"]
color_list = [colors1, colors2, colors2]
titles = [
    """To what degree do you trust or distrust the Prosecutor's<br>
office of Georgia? (%)""",
    """In your opinion, abuse of power by prosecutors in Georgia<br>
is a frequent case, a rare case, or never the case? (%)""",
    """In your opinion, prosecutors in Georgia making deals with judges<br>
in order to have decisions favourable for them is a frequent<br>
case, a rare case, or never the case? (%)""",
]

#%%

for colors, chart, title in zip(color_list, ["chart1", "chart2", "chart3"], titles):
    df = pd.read_csv(f"prosecutor_trust/{chart}.csv").T.reset_index()

    # Needs a quick transpose and some column faff. Next time fix in csv.
    df = df.rename(columns={k: v for (k, v) in zip(df.columns, df.iloc[0])}).iloc[1:]

    # fix percentages
    # Create total column
    df = df.set_index("label").assign(total=lambda x: x.sum(axis=1))

    # Divide the rest up by the total and drop total using iloc
    df = df[df.columns[:-1]].div(df["total"], axis=0).mul(100).reset_index().iloc[::-1]

    y = [str(i) for i in df["label"]]
    fig = go.Figure()

    annotations = []
    for n, x_lab in enumerate(df.columns[1:]):
        fig.add_trace(
            go.Bar(
                x=df[x_lab],
                y=y,
                name=x_lab,
                orientation="h",
                legendgroup=range(len(df.columns) - 1)[-n],
            )
        )
        fig["data"][n]["marker"].update({"color": colors[n]})

    for yd, xd in zip(y, df[df.columns[1:]].values):

        # labeling the first percentage of each bar (x_axis)
        annotations.append(
            dict(
                xref="x",
                yref="y",
                x=xd[0] / 2,
                y=yd,
                text=str(int(xd[0])),
                font=dict(family="sans serif", size=12, color="rgb(248, 248, 255)"),
                showarrow=False,
            )
        )

        space = xd[0]
        for i in range(1, len(xd)):
            # labeling the rest of percentages for each bar (x_axis)
            txt = str(int(xd[i]))
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
                            family="sans serif", size=12, color="rgb(248, 248, 255)"
                        ),
                        showarrow=False,
                    )
                )
                space += xd[i]

    fig.update_layout(
        title=title, font=dict(family="sans serif", size=12, color="#7f7f7f"),
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
    fig.write_html(f"{chart}.html")
