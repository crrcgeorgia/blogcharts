#%%

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

colors = ["#d7191c", "#fdae61", "#ffffbf", "#abd9e9", "#2c7bb6",][::-1]

#%%

ch1_title_en = "Attitudes towards democracy (%)"


def stacked_bar(lang, title, suffix, n, bar_type='group'):
    path = f"{lang}/chart{n}.csv"

    df = pd.read_csv(path).melt("label")[::-1]
    fig = px.bar(
        df,
        x="value",
        y="label",
        color="variable",
        barmode=bar_type,
        orientation="h",
        text="value",
        width=800,
        height=600,
        labels={"x": None, "y": None},
        title=title,
        color_discrete_sequence=colors,
    )


    fig.update_traces(
        texttemplate="%{text:.0f}", textfont_size=8, textposition="inside"
    )
    fig.update_layout(uniformtext_minsize=8, uniformtext_mode="hide")
    fig.update_layout(xaxis=dict(range=[0, 100], showticklabels=False),)
    fig.update_layout(
        legend=dict(
            orientation="h",
            yanchor="auto",
            y=-0.1,
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
    fig.show()
    fig.write_html(f"{lang}/chart_{suffix}_{n}.html")

ch2_title_en = "To what extent is it acceptable or unacceptable to (%)"

stacked_bar("en", ch1_title_en, None, "1")
stacked_bar("en", ch2_title_en, None, "2", bar_type='stack')

# %%

