#%%#############################################################################
#                 PART 1: Module imports and object definition                 #
################################################################################

""" Assumes Python >= 3.7 & R == ??, and will require Linux to run properly.
    The code is dependent on pyromania, a wrapper for the rpy2 module I made
    so I can avoid learning R. I plan to get it up on github soon, but if
    you'd like to use it for replication in the meantime, please contact me
    on i.goodrich@crrccenters.org"""

# Import modules required for analysis
import pandas as pd
import numpy as np

# Plotting
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go

# Some weighted stats from statsmodels, because life is to short to work
# out grouped survey means in rpy2
from statsmodels.stats.weightstats import DescrStatsW

# Minmax normalizer
from sklearn.preprocessing import MinMaxScaler

scaler = MinMaxScaler()

# Getting R and Python to play nice
from pyromania.pyr import pyr, rpy, pyr_tab, freq, interpret

import rpy2.robjects as ro
from rpy2.robjects.packages import importr
import rpy2.robjects.lib.ggplot2 as ggplot2


# Defining R objects for later use
R = ro.r
survey = importr("survey")
gg = importr("ggeffects")

#%%#############################################################################
#                      PART 2: Data import and constants                       #
################################################################################

# Import data from STATA
PATH = "cb_time_series_w_passport.dta"
df = pd.read_stata(PATH)
var_labs = pd.read_stata(PATH, iterator=True).variable_labels()

# Setting analysis for Georgia only
df = df[df["COUNTRY"] == "Georgia"]

# Fixing PSUs for HH-level analysis
df["PSUHH"] = (df["PSU"] * 1000) + df["wave"]

# Final demographic variables
DEMS = ["RESPSEX", "AGE", "ETHNIC", "STRATUM", "RESPEDU"]
SURVEY_VARS = ["PSUHH", "HHWT", "SUBSTRATUM"]

# Non-response values
NON_RESPONSE = [
    "Don't know",
    "Refuse to answer",
    "Break-off",
    "Interviewer error",
    "Legal skip",
]

# Setting a set of variables for "Don't know" and "Refuse to answer"
DK_RA = ["Don't know", "Refuse to answer"]

# Creating dicts to map non-respone to NA where needed
NO_RESPONSE_NA = {i: np.nan for i in NON_RESPONSE}
DK_RA_NA = {i: np.nan for i in DK_RA}

# Setting dictionaries to recode Yes/no questions
BINARY = {"Yes": 1, "No": 0}  # Yes to 1, No to 0
BINARY.update(NO_RESPONSE_NA)  # Everything else to NA

#%%#############################################################################
#               PART 3: Independent variable transformations                   #
################################################################################

# Set a time column reflecting years since start of dataset, not since 2000
df["time"] = df["wave"] - 11

# Remove non-response from sex (n = 2 x break-off only)
df["RESPSEX"] = (
    df["RESPSEX"]
    .replace(NO_RESPONSE_NA)
    .astype("category")  # Not ordered factor, but preserves base category
    .cat.set_categories(["Male", "Female"], ordered=False)
)

# Make age groups from age column
AGES = ["18-34", "35-64", "65+"]
df["AGE"] = pd.cut(df["AGE"], [17, 34, 64, 150], labels=AGES).cat.set_categories(
    AGES, ordered=False  # Not ordered factor, but preserves base category
)

# Recode ethnicity from dict, implicit non-response and error (n=109) to NA
ETHNO_CODE = {
    "Georgian": "Georgian",
    "Armenian": "Armenian",
    "Azerbaijani": "Azerbaijani",
    "Other Caucasian": "Other",
    "Other ethnicity": "Other",
    "Russian": "Other",
}

# Recoding ethnicity
df["ETHNIC"] = (
    df["ETHNIC"]
    .str.strip()  # Deal with whitespace
    .map(ETHNO_CODE)  # Map recode
    .astype("category")  # Set as categorical
    .cat.set_categories(  # Cat accessor before ordering, below
        ETHNO_CODE, ordered=False  # Not ordered factor, but preserves base
    )
)

# Switiching 'STRATUM' to unordered, preserves base
CAT_STRATUM = df.STRATUM.cat.categories
df["STRATUM"] = df["STRATUM"].cat.set_categories(CAT_STRATUM, ordered=False)

# Recoding education
EDU_VARS = [i for i in df if "EDU" in i]
EDU_VARS_r = [i + "_r" for i in df if "EDU" in i]
EDU_RECODES = {
    "No primary education": "Secondary and below",
    "Primary education": "Secondary and below",
    "Incomplete secondary education": "Secondary and below",
    "Completed secondary education": "Technical education",
    "Secondary technical education": "Technical education",
    "Incomplete higher education": "Higher education",
    "Completed higher education": "Higher education",
    "Post-graduate degree": "Higher education",
}

EDU_NUM_LARGE = {i: n for n, i in enumerate(EDU_RECODES.keys())}

EDU_ORD = [
    "Secondary and below",
    "Technical education",
    "Higher education",
]

EDU_NUM = {i: n for n, i in enumerate(EDU_ORD)}  # Numerical equivalents of above

df[EDU_VARS_r] = (
    df[EDU_VARS]
    .stack()  # A bit of wrangling, allows easy transforms across multiple vars
    .map(EDU_RECODES)  # Map recodes, non-response & error <-NA
    .astype("category")  # Set categorical
    .cat.set_categories(EDU_ORD, ordered=False)  # Base preserved but unordered
    .unstack()  # Back to normal after the above wrangling
)

df["RESPEDU"] = (
    df["RESPEDU"]
    .map(EDU_RECODES)  # Map recodes
    .astype("category")  # Set to categorical
    .cat.set_categories(EDU_ORD, ordered=False)  # Not ordered, base preserved
)


#%%#############################################################################
#                PART 3: Dependent variable transformations                    #
################################################################################

# Ownership variables
# Excluding digital camera and landline, as no-longer indicator of wealth
OWN = [i for i in df if "OWN" in i and i not in ["OWNLNDP", "OWNDIGC"]]
OWN_r = [i + "_r" for i in OWN]
OWN_qs = OWN_r + ["OWN_SUM"]

# Recoding
df[OWN_r] = df[OWN].apply(  # Subset ownership vars
    lambda x: x.astype(str)  # To str, as some numeric errors
    .replace(BINARY)  # Replace using BINARY dict
    .astype(float)
)  # Return to float for summing

# Index of all ownership vars, non-response in any column will result in NA
df["OWN_SUM"] = df[OWN_r].sum(axis=1)

#%%#############################################################################
#                PART 4: Ownership by type, table                              #
################################################################################

# Building a single year-grouped dataframe with means for all item types
own_frame = (
    df.dropna(subset=OWN_qs, how="any")  # Drop NA
    .groupby("wave")  # Groupby wave, see readable.
    .apply(lambda x: DescrStatsW(x[OWN_qs], x["HHWT"]).mean)  # Apply mean (HHWT)
    .apply(pd.Series)  # Expand list to columns
    .rename(columns={n: i for (n, i) in enumerate(OWN_qs)})  # Name columns
    .T.assign(avg=lambda x: x.mean(axis=1))  # Add a sorting variable "avg"
    .T.sort_values(by="avg", axis=1)  # Sort by 'avg'
    .drop("avg", axis=0)  # Drop 'avg'
)

own_items = (
    own_frame.drop("OWN_SUM", axis=1)  # Not eventually needed, just each type
    .reset_index()
    .melt("wave")
)  # Wide to long transformation for plotting

own_items["wave"] = (own_items["wave"] + 2000).astype(int)  # e.g. 17.0 <- 2017


# This is a bit garbled, probably neater ways to do it, but what I'm doing is
# matching ownership variables in all variable labels, appending _r to key and splitting
# to give item only, not full question (e.g. "household owns - xbox")


OWN_RECODES = {
    k + "_r": v.split(" - ")[1].strip() for k, v in var_labs.items() if k in OWN
}

own_items["variable"] = (
    own_items["variable"]
    .map(OWN_RECODES)  # Mapping recodes
    .replace("Automatic washing machine", "Washing machine")  # Shortening label
)

own_items["value"] = own_items["value"].mul(100)  # Multiply by 100: 0.x <- x%

#%%#############################################################################
#                PART 5: Ownership by type, plots                              #
################################################################################


############################ 5.A By item plots #################################

fig, ax = plt.subplots(1, 1, figsize=(6, 6))  # Set up figure

sns.lineplot(
    data=own_items,  # data
    x="wave",
    y="value",
    hue="variable",  # vars
    ax=ax,
    legend=False,
)  # Ax and legend.

# Labeling lines (2019)
for item in own_items[own_items["wave"] == 2019].iterrows():  # Bounce thru table
    x = item[1]["wave"]  # Pull wave
    y, y_loc = item[1]["value"], item[1]["value"]  # Pull values
    label = item[1]["variable"]  # Pull label
    if label == "Refrigerator":  # Tweak the fridge, because it was overlapping
        y_loc -= 2
    ax.text(x, y_loc + 1, f"{int(y)}%     {label}")  # Label up

for item in own_items[own_items["wave"] == 2011].iterrows():  # Bounce thru table
    x = item[1]["wave"]  # Pull wave
    y, y_loc = item[1]["value"], item[1]["value"]  # Pull values
    label = item[1]["variable"]  # Pull label
    if label == "Personal computer":  # More tweaking
        y_loc -= 4
    ax.text(x, y_loc + 1, f"{int(y)}%")  # Add labels

plt.title(  # Title
    "Ownership of household items 2011-2019 (%)", fontdict={"fontsize": 16}, pad=20
)
plt.ylabel("Percentage reporting ownership of item")  # Label y
plt.xlabel("Year")  # Label x
sns.despine()  # Clear box edges
plt.savefig("per_item.png", bbox_inches="tight")  # Save

# Plotly version

thing_dict = dict(zip(own_items["variable"].unique()[::-1], px.colors.qualitative.Safe))

fig = px.line(
    own_items.loc[::-1],
    x="wave",
    y="value",
    color="variable",
    title="Ownership of household items 2011-2019 (%)",
    color_discrete_sequence=px.colors.qualitative.Safe,
    width=800,
    height=600,
)

annotations = []

for _, tup in own_items[["wave", "value", "variable"]].iterrows():
    x = tup[0]
    y = tup[1]
    lab = tup[2]
    if int(y) in [96, 40]:
        y_off = 2
    elif (int(y) in [92, 38]) and (lab != "Car"):
        y_off = -2
    else:
        y_off = 0

    # labeling the first percentage of each bar (x_axis)
    if x in [2011, 2019]:

        if x == 2019:
            x_off = 0.04
            x_anchor = "left"
            annotations.append(
                dict(
                    xref="x",
                    yref="y",
                    x=x + 0.35,
                    y=y + y_off,
                    text=lab,
                    font=dict(family="Calibri", size=14, color=thing_dict[lab]),
                    xanchor="left",
                    showarrow=False,
                )
            )
        else:
            x_off = -0.04
            x_anchor = "right"
        annotations.append(
            dict(
                xref="x",
                yref="y",
                x=x + x_off,
                y=y + y_off,
                xanchor=x_anchor,
                text=str(int(y)),
                font=dict(family="Calibri", size=14, color=thing_dict[lab]),
                showarrow=False,
            )
        )

fig.update_layout(annotations=annotations)
fig.update_layout(
    xaxis_title="", yaxis_title="", legend_title_text="", showlegend=False
)

fig.update_layout(
    xaxis=dict(
        tickmode="array",
        tickvals=list(range(2011, 2020)[::2]),
        # ticktext = ['One', 'Three', 'Five', 'Seven', 'Nine', 'Eleven']
    ),
    yaxis=dict(ticksuffix=" "),
)
fig.write_html('chart1.html')



#%%
############################### 5.B Total plot #################################

own_tot = own_frame["OWN_SUM"].reset_index()  # Just the one column this time
own_tot["wave"] = (own_tot["wave"] + 2000).astype(int)  # Fix wave as above

fig, ax = plt.subplots(1, 1, figsize=(6, 6))  # Set up fig
sns.lineplot(data=own_tot, x="wave", y="OWN_SUM", ax=ax)  # Base plot
ax.set_ylim([0, 8])  # Set y axis between 0-8 (min and max score)

for item in own_tot.iterrows():  # More labelling, ping through table
    x = item[1]["wave"]  # Get wave
    y = item[1]["OWN_SUM"]  # Get value
    ax.text(x, y + 0.2, f"{y:0.1f}")  # Plot on chart

plt.title(  # Title
    "Ownership of household items (mean owned)", fontdict={"fontsize": 16}, pad=20
)
plt.ylabel("Number of items owned")  # ylabel
plt.xlabel("Year")  # xlabel
sns.despine()  # More tidying
plt.savefig("own_sum.png", bbox_inches="tight")  # Save figure
own_items.to_csv("own_sum.csv")  # Save csv


# Plotly version
fig = px.line(
    own_tot,
    x="wave",
    y="OWN_SUM",
    text="OWN_SUM",
    title="Ownership of household items (mean owned)",
    color_discrete_sequence=px.colors.qualitative.Safe,
)
fig.update_yaxes(range=[0, 7])

fig.update_layout(
    xaxis=dict(
        tickmode="array",
        tickvals=list(range(2011, 2020)[::2]),
        # ticktext = ['One', 'Three', 'Five', 'Seven', 'Nine', 'Eleven']
    ),
    yaxis=dict(ticksuffix=" "),
)

fig.update_traces(texttemplate="%{text:.2s}", textposition="top center")
fig.update_layout(xaxis_title="", yaxis_title="", legend_title_text="")

fig.write_html('chart2.html')


#%%#############################################################################
#                PART 6: Conversion to R -- Here be dragons                    #
################################################################################

# Trim df to bare essentials
df_final = df[DEMS + SURVEY_VARS + ["OWN_SUM", "time"]]

# convert to R objects
data = pyr(df_final)
id, weights, strat = [pyr(df_final[i]) for i in SURVEY_VARS]

# Survey design object
svd = survey.svydesign(id=id, weights=weights, strat=strat, data=data)


#%%#############################################################################
#                  PART 7: No suggestion without regression                    #
################################################################################

# Define the regression formula. Time interactions for demographics and wealth
formula = """OWN_SUM ~ time +
                       RESPSEX * time +
                       AGE * time +
                       ETHNIC * time +
                       STRATUM * time +
                       RESPEDU * time
          """
# Or the posh way, if you like such things
formula_fun = "OWN_SUM ~ time + " + " + ".join([i + " * time" for i in DEMS])

# Model and summary
model = survey.svyglm(formula, design=svd)
summary = R.summary(model)

# Coefficients, brought back into the land of Python through helper functions
coeffs = pyr_tab(summary.rx2("coefficients"))
coeffs = interpret(coeffs)

# Use ggpredict to get predicted scores for education and stratum
predict = gg.ggpredict(model, terms=["time", "RESPEDU", "STRATUM"])
predict_py = rpy(predict)
predict_py["x"] = predict_py["x"] + 2011
#%%#############################################################################
#                  PART 8: Plotting predicted probabilities                    #
################################################################################

fig = px.line(
    predict_py,
    x="x",
    y="predicted",
    color="facet",
    facet_col="group",
    error_y="std.error",
    title="Predicted ownership index scores<br> by settlement type and education (2011-2019)",
    width=800,
    height=600,
    color_discrete_sequence=px.colors.qualitative.Safe

)
fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))

fig.update_yaxes(range=[0, 7])
fig.update_xaxes(title="", range=[2010, 2020], tickvals= [2011, 2013, 2015, 2017, 2019])

# fig.update_traces(texttemplate='%{text:.2s}', textposition='top center')
fig.update_layout(xaxis_title="", yaxis_title="Predicted ownership index", legend_orientation="h")
fig.update_xaxes(automargin=True)
fig.write_html('chart3.html')

#%%
df_wave = df[DEMS + SURVEY_VARS + ["OWN_SUM", "time", "wave"]]
# convert to R objects
data_11 = df_wave[df_wave["wave"] == 11]
data_11_r = pyr(data_11)

id, weights, strat = [pyr(data_11[i]) for i in SURVEY_VARS]

# Survey design object
svd = survey.svydesign(id=id, weights=weights, strat=strat, data=data_11_r)

# Model and summary

formula = "OWN_SUM ~ STRATUM"

model = survey.svyglm(formula, design=svd)
summary = R.summary(model)

# Coefficients, brought back into the land of Python through helper functions
coeffs = pyr_tab(summary.rx2("coefficients"))
coeffs = interpret(coeffs)
# 
# 
# %% Not sure what all the below was, it's so long since I did this. Will
# keep in case needed 

# data_19 = df_wave[df_wave["wave"] == 19]
# data_19_r = pyr(data_19)

# id, weights, strat = [pyr(data_19[i]) for i in SURVEY_VARS]

# # Survey design object
# svd = survey.svydesign(id=id, weights=weights, strat=strat, data=data_19_r)

# # Model and summary

# formula = "OWN_SUM ~ STRATUM"

# model = survey.svyglm(formula, design=svd)
# summary = R.summary(model)

# # Coefficients, brought back into the land of Python through helper functions
# coeffs = pyr_tab(summary.rx2("coefficients"))
# coeffs = interpret(coeffs)

# coeffs


# #%%
# descr = importr("descr")
# from pyromania.pyr import pyr_tab


# def crosstab(x, y, wt=None):
#     if len(wt) > 0:
#         weights = pyr(wt)
#     else:
#         weights = pd.Series([1 for i in range(len(x))])
#         weights = pyr(weights)
#     f = descr.crosstab(pyr(x), pyr(y), wt=pyr(weights))
#     return pyr_tab(f)


# # crosstab(df['wave'], df['RESPEDU'], df['INDWT'])
# from table import make_table

# bum = make_table(df, "wave", "RESPEDU", wt="INDWT")

# bum.div(bum.sum(axis=1), axis=0)


# #%%

# diff_tab = predict_py.groupby('group')['predicted'].mean().reset_index().assign(pct=lambda x: x['predicted'].pct_change()).assign(cumdif=lambda x: x['predicted'].sub(x['predicted'].shift()))

# diff_tab.loc[[0,2]]['predicted'].diff()