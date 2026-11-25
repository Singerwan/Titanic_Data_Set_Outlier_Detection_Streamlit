import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import seaborn as sns
from streamlit_option_menu import option_menu

import streamlit as st

st.title("Titanic Dataset") 


with st.sidebar:
    selected= option_menu(menu_title="Main"
                         ,options=["Outelier Detection"]
                         ,icons=["house",
                                ],menu_icon="cast",default_index=0)
if selected=="Outelier Detection":
    st.text("Outlier Detection")
    
df=sns.load_dataset("titanic")
df['age']=df['age'].fillna(0)

st.dataframe(df)

zscore = (df['age'] - df['age'].mean()) / df['age'].std()
z_abs  = np.abs(zscore)
df_filter = pd.DataFrame(data =df['age'])
df_filter["Zscore"] = zscore
df_filter["z_abs"]  = z_abs
df_filter['Outlier_Y|N_Zscr'] = np.where(df_filter['z_abs']>3, "Yes", "No")

Q1=np.percentile(df['age'],25)
Q3=np.percentile(df['age'],75)
IQR=Q3-Q1
Ulim=Q3+IQR*1.5
Llim=Q1-IQR*1.5
df_filter['Outliers_IQR']=np.where(~df['age'].between(Llim, Ulim),"Outlier","Normal")
st.title("Outlier Detection Table")
st.dataframe(df_filter)
fig_hist1 = px.histogram(data_frame=df,
                        x=df['age'],
                        text_auto=True,
                        title="Histogram of Titanic Passenger Age Distribution",
                        color="pclass")

fig_hist2 = px.histogram(
                        x=zscore,
                        text_auto=True,
                        title="Histogram of Titanic Passenger Age Distribution(Zscore)")
fig_hist2.add_vline(x=3, line_width=3, line_dash="dash", line_color="red")

st.title("Visualization")
st.plotly_chart(fig_hist1)
st.plotly_chart(fig_hist2)
fig_box = px.box(df, y='age', title='Outlier Detection of Titanic Passenger Age Distribution',
                color_discrete_sequence=["yellow","red","blue"])

fig_box.add_hline(df['age'].mean(), line_width=3, line_dash="dash", line_color="green")

fig_box.add_annotation(
    x=-1,y=65,
    font=dict( size=10,color="black", family="TimesNewRoman" ),align="left",valign="top",
    bgcolor="cyan",bordercolor="yellow",borderpad=0.1,borderwidth=4,
    showarrow=True,arrowhead=3,
    text=
"""Description: This boxplot displays the ages, in years,of Titanic passengers.<br>
Range：The ages range from 0.420 years to 80 yeasr.<br>
<span style="color:red;font-size:12px;font-weight:bold">Outliers :</span>
Any passenger <span style="color:red"><u>over the age of 65</u></span> appears to be an <br>
outlier within the data set.
<br>The distribution of the boxplot appears to be symmetric.
<br>Q1 25% of the Titanic passengers were younger(below) than 20 years old.
<br>Q2 50% of the Titanic passangers were younger than 28 years old.
<br>     Or the middle(median)is 28 years old. VS mean is :{}
<br>Q3 75% of the Titanic passengers were younger than 38 years old.
""".format(df['age'].mean().round(2) ),
    xanchor="center",)

st.plotly_chart(fig_box)