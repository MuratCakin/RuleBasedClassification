# Loading Libraries
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt


# Reading .csv file
def load_persona():
    df = pd.read_csv("2_HAFTA/Proje/persona.csv")
    return df

df = load_persona()


###################          First look at data          ###################

def check_df(dataframe):
    print("##################### Shape #####################")
    print(dataframe.shape)

    print("##################### Types #####################")
    print(dataframe.dtypes)

    print("##################### Head #####################")
    print(dataframe.head())

    print("##################### Tail #####################")
    print(dataframe.tail())

    print("##################### NA #####################")
    print(dataframe.isnull().sum())

    print("##################### Quantiles #####################")
    print(dataframe.quantile([0, 0.05, 0.50, 0.95, 0.99, 1]).T)

check_df(df)

# In COUNTRY, SOURCE, SEX, AGE breakdown average earnings
df[["PRICE","COUNTRY","SOURCE","SEX","AGE"]].groupby(["COUNTRY","SOURCE","SEX","AGE"]).agg("mean")


# Sort the output by PRICE
agg_df = df[["PRICE","COUNTRY","SOURCE","SEX","AGE"]].\
            groupby(["COUNTRY","SOURCE","SEX","AGE"]).\
            agg("mean").\
            sort_values("PRICE",ascending=False)


# Level based customers (COUNTRY_SOURCE_SEX_AGE_CAT)
agg_df.reset_index(inplace=True)

# Transform numeric variable to categorical variable
agg_df["AGE_CAT"] = pd.cut(agg_df["AGE"], [0, 19, 24, 31, 41, 70])

agg_df["customer_level_based"] = [row[0].upper() + "_" +
                                  row[1].upper() + "_" +
                                  row[2].upper() + "_" +
                                  str(row[5]).upper()
                                  for row in agg_df.values]

# New DataFrame's structure (Index = customer_level_based, dependent variable = PRICE)
drop_list = [col for col in agg_df.columns if col not in ["customer_level_based","PRICE"]]
agg_df.drop(drop_list, axis=1, inplace=True)
agg_df = agg_df[["customer_level_based","PRICE"]].groupby(["customer_level_based"]).agg("mean")


# Prıce segments
agg_df["SEGMENT"] = pd.qcut(agg_df["PRICE"], 4, labels=["D","C","B","A"])
agg_list = ["mean","max","sum"]
agg_df[["PRICE","SEGMENT"]].groupby("SEGMENT").agg(agg_list)
c_segment_df = pd.DataFrame([row for row in agg_df.values if str(row[1]) == "C"])

# Predictions
new_user = "TUR_ANDROID_FEMALE_31_40"
agg_df[agg_df["customer_level_based"] == new_user]
new_user = "FR_IOS_FEMALE_31_40"
agg_df[agg_df["customer_level_based"] == new_user]

