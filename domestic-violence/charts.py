#%%

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

colors = ["#d7191c", "#fdae61", "#ffffbf", "#abd9e9", "#2c7bb6",][::-1]

#%%

ch1_title_ka = "თქვენი აზრით, რა შეიძლება იყოს ოჯახური ძალადობის<br>შეუტყობინებლობის [თანამშრომელი ყოყმანებს] მიზეზი?"
ch1_title_en = "What do you think would be a reason [for a colleague being<br>hesitant] to report domestic violence?"


def stacked_bar(lang, title, suffix, n):
    path = f"{lang}/chart{n}.csv"

    df = pd.read_csv(path).melt("label")
    fig = px.bar(
        df,
        x="value",
        y="label",
        color="variable",
        barmode="stack",
        orientation="h",
        text="value",
        width=800 * 0.87,
        height=600 * 0.87,
        labels={"x": None, "y": None},
        title=title,
        color_discrete_sequence=colors,
    )
    fig.update_traces(
        texttemplate="%{text:.0f}", textfont_size=8, textposition="inside"
    )
    fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
    fig.update_layout(xaxis=dict(range=[0, 100], showticklabels=False),)
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
    fig.show()
    fig.write_html(f"{lang}/chart_{suffix}_{n}.html")


stacked_bar("ka", ch1_title_ka, None, "1")
stacked_bar("en", ch1_title_en, None, "1")
stacked_bar("ka", None, "no_title", "1")
stacked_bar("en", None, "no_title", "1")
# %%

ch2_title_ka = 'შედეგები ექსპერიმენტული ჯგუფების მიხედვით (%)'
ch2_title_en = 'Outcome by treatment group (%)'

def group_bar(lang, title, suffix):
    df = pd.read_csv(f'{lang}/chart2.csv')
    fig = go.Figure()
    x = df[["label", "group"]].T
    for n, y_lab in enumerate(df.columns[2:]):
        fig.add_bar(x=x, y=df[y_lab], name=y_lab, text=df[y_lab], textfont=dict(size=8,))
        fig["data"][n]["marker"].update({"color": colors[n]})
    fig.update_layout(
        title=None,
        width=800 * 0.87,
        height=600 * 0.87,
        legend_orientation="h",
        xaxis_title="",
        yaxis_title="",
        legend=dict(x=-0, y=-0.7, yanchor='bottom'),

    )
    fig["layout"]["yaxis1"].update(range=[0, 100])
    fig.update_traces(texttemplate="%{text:.0f}", textposition="outside")
    
    fig.show()
    fig.write_html(f"{lang}/chart{suffix}2.html")


group_bar("ka", ch2_title_ka, None)
group_bar("en", ch2_title_en, None)
group_bar("ka", None, "_no_title_")
group_bar("en", None, "_no_title_")



# %%
