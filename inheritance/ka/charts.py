#%%

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

colors2 = ["maroon", "orange", "midnightblue", "dimgray"]


#%%
df1 = pd.read_csv("chart1.csv")
colors1 = ["midnightblue", "maroon", "teal", "dimgray"]

title = """
თქვენი აზრით, ვის საკუთრებაში უნდა გადავიდეს ბინა?<br>
პასუხების მიხედვით კითხვაზე, ვინ უნდა იზრუნოს<br>
მშობლებზე ვაჟმა თუ ქალიშვილმა? (%)<br>
(CRRC, კავკასიის ბარომეტრი 2019, საქართველო)
"""


y = df1["index"]
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
                    font=dict(family="sans-serif", size=12, color="rgb(248, 248, 255)"),
                    showarrow=False,
                )
            )
            space += xd[i]

fig.update_layout(
    title=dict(y=0.95, text=title),
    font=dict(family="sans-serif", size=12, color="#7f7f7f"),
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
fig.write_html(f"chart1.html")


#%%
title = """
ვის საკუთრებაში უნდა გადავიდეს ეს ბინა?<br>
მარჟინალური ეფექტები დამოკიდებულ ცვლადზე<br>
(CRRC, კავკასიის ბარომეტრი 2019, საქართველო)<br>

"""

df2 = pd.read_csv("chart2.csv")
df2[["value", "conf"]] = df2[["value", "conf"]] * 100

fig = px.scatter(
    df2, x="value", y="demographic", facet_col="outcome", error_x="conf", title=title
)
fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[1].title()))
fig.update_layout(
    {"titlefont": {"size": 16},},
    title={
        # 'text': "Plot Title",
        "y": 0.92,
        # 'x':0.5,
        # 'xanchor': 'center',
        "yanchor": "top",
    },
)

fig["layout"]["yaxis"]["title"]["text"] = ""
fig["layout"]["xaxis"]["title"]["text"] = ""
fig["layout"]["xaxis3"]["title"]["text"] = ""
fig["layout"]["xaxis2"]["title"]["text"] = ""

fig.update_layout(
    autosize=False, width=800, height=400, margin=dict(l=50, r=50, b=50, t=115, pad=1)
)


fig.show()
fig.write_html(f"chart2.html")

# %%
