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
# Task 1 Question1
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

# Question 2
df["SOURCE"].nunique()
df["SOURCE"].value_counts()

# Question 3
df["PRICE"].nunique()

# Question 4
df["PRICE"].value_counts()

# Question 5
df["COUNTRY"].value_counts()

# Question 6
df[["PRICE","COUNTRY"]].groupby("COUNTRY").agg("sum")

# Question 7
df[["PRICE","SOURCE"]].groupby("SOURCE").agg("count")

# Question 8
df[["PRICE","COUNTRY"]].groupby("COUNTRY").agg("mean")

# Question 9
df[["PRICE","SOURCE"]].groupby("SOURCE").agg("mean")

# Question 10
df[["PRICE","SOURCE","COUNTRY"]].groupby(["COUNTRY","SOURCE"]).agg("mean")


# Task 2
df[["PRICE","COUNTRY","SOURCE","SEX","AGE"]].groupby(["COUNTRY","SOURCE","SEX","AGE"]).agg("mean")


# Task 3
agg_df = df[["PRICE","COUNTRY","SOURCE","SEX","AGE"]].\
            groupby(["COUNTRY","SOURCE","SEX","AGE"]).\
            agg("mean").\
            sort_values("PRICE",ascending=False)


# Task 4
agg_df.reset_index(inplace=True)


# Task 5
agg_df["AGE_CAT"] = pd.cut(agg_df["AGE"], [0, 19, 24, 31, 41, 70])


# Task 6
agg_df["customer_level_based"] = [str(row[0]) + "_" +
                                  str(row[1]) + "_" +
                                  str(row[2]) + "_" +
                                  str(row[5])
                                  for row in agg_df.values]

drop_list = [col for col in agg_df.columns if col not in ["customer_level_based","PRICE"]]
agg_df.drop(drop_list, axis=1, inplace=True)
agg_df = agg_df[["customer_level_based","PRICE"]].groupby(["customer_level_based"]).agg("mean")


# Task 7
agg_df["SEGMENT"] = pd.qcut(agg_df["PRICE"], 4, labels=["D","C","B","A"])
agg_list = ["mean","max","sum"]
agg_df[["PRICE","SEGMENT"]].groupby("SEGMENT").agg(agg_list)
c_segment_df = pd.DataFrame([row for row in agg_df.values if str(row[1]) == "C"])

# Task 8
new_user = "TUR_ANDROID_FEMALE_31_40"
new_user = agg_df[agg_df["customer_level_based"] == new_user]
new_user = "FR_IOS_FEMALE_31_40"
new_user = agg_df[agg_df["customer_level_based"] == new_user]

