# Pandas for data management
import pandas as pd

# os methods for manipulating paths
from os.path import dirname, join

# Bokeh basics 
from bokeh.io import curdoc
from bokeh.models.widgets import Tabs


# Each tab is drawn by one script

from scripts.age_hist import age_hist_tab
from scripts.gender_hist import gender_hist
from scripts.dialect_hist import dialect_hist
from scripts.combined_scatter import combined_scatter

from bokeh.sampledata.us_states import data as states

# Read data into dataframes
features = pd.read_csv(join(dirname(__file__), 'data', 'output.csv'), 
	                                          index_col=0).dropna()

label_mapping={"Male":1,"male":1,"Masculino":1,"Female":0,"female":0,"Weiblich":0}
df_selected=features.replace({'label':label_mapping})
df_selected=df_selected[(df_selected['label']==0)|(df_selected['label']==1)]
label_mapping={1:"Male",0:"Female"}
df_selected=df_selected.replace({'label':label_mapping})

df_selected[['dialect']]=df_selected[['dialect']].fillna("Other")
other_mapping={"other":"Other",'Please Select':"Other",'unknown':"Other",'non':"Other"}
df_selected=df_selected.replace({'dialect':other_mapping})

df_selected[['age_range']]=df_selected[['age_range']].fillna("Other")
age_range_mapping={"Please":"Other","unknown":"Other","youth":"Youth","Erwachsener":"Adult","Adulto":"Adult","adult":"Adult"}
df_selected=df_selected.replace({'age_range':age_range_mapping})





# Create each of the tabs
tab1 =  age_hist_tab(df_selected)
tab2 = gender_hist(df_selected)
tab3 = dialect_hist(df_selected)
tab4 = combined_scatter(df_selected)


tabs = Tabs(tabs=[tab1,tab2,tab3,tab4])

curdoc().add_root(tabs)

