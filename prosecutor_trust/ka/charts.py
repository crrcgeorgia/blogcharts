import pandas as pd
import plotly.graph_objects as go

colors1 = ["midnightblue", "maroon", "darkgrey", "dimgray"]
colors2 = ["maroon", "orange", "midnightblue", "dimgray"]
color_list = [colors1, colors2, colors2]
titles = [
    """გთხოვთ, მითხრათ, რამდენად ენდობით ან არ ენდობით<br>
საქართველოს პროკურატურას? (%)""",
    """თქვენი აზრით, საქართველოში პროკურორების მიერ ძალაუფლების<br>
    ბოროტად გამოყენება კონკრეტულ საქმეზე მუშაობისას ხშირად ხდება,<br>
    იშვიათად ხდება, თუ არასდროს ხდება? (%)""",
    """თქვენი აზრით, საქართველოში პროკურორების გარიგება<br>
მოსამართლეებთან მათთვის სასარგებლო გადაწყვეტილების მისაღებად<br>
ხშირად ხდება, იშვიათად ხდება, თუ არასდროს ხდება? (%)""",
]

#%%

for colors, chart, title in zip(color_list, ["chart1", "chart2", "chart3"], titles):
    df = pd.read_csv(f"prosecutor_trust/ka/{chart}.csv").T.reset_index()

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
                text=str(int(round(xd[0], 0))),
                font=dict(family="sans serif", size=12, color="rgb(248, 248, 255)"),
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
    fig.write_html(f"prosecutor_trust\ka\{chart}.html")
