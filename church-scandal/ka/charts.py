#%%
import pandas as pd
import plotly.express as px

df = pd.read_csv("church-scandal.csv")

six_colors = ["#ca0020", "#f4a582", "#f7f7f7", "#92c5de", "#0571b0", "grey"]
#%%
fig = px.bar(
    df.melt("label"),
    x="value",
    y="label",
    color="variable",
    orientation="h",
    text="value",
    width=800,
    height=400,
    color_discrete_sequence=six_colors,
)
fig.update_layout(
    title={
        "text": "რამდენად ენდობით ან არ ენდობით [საქართველოს მართლმადიდებლურ ეკლესიას]?<br>31 ოქტომბრამდე და შემდეგ (მართლმადიდებლების %)",
        "y": 0.94,
        "font": {"size": 14},
        # 'x':0,
        "xanchor": "left",
        "yanchor": "top",
    },
    barmode="stack",
    xaxis={"range": [0, 100], "title": None},
    legend_orientation="h",
    yaxis={"title": None},
)
fig.update_traces(texttemplate="%{text:0.0f}", insidetextanchor="middle")
fig.write_html('chart1.html')
# %%
df
