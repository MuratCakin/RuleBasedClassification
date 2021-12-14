import pandas as pd


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
df.groupby(by=["COUNTRY", 'SOURCE', "SEX", "AGE"]).agg({"PRICE": "mean"})


# Sort the output by PRICE
agg_df = df.groupby(by=["COUNTRY","SOURCE","SEX","AGE"]).\
            agg({"PRICE": "mean"}).\
            sort_values("PRICE",ascending=False)


#### Level based customers (COUNTRY_SOURCE_SEX_AGE_CAT) ####

agg_df.reset_index(inplace=True)

# Transform numeric variable to categorical variable
bins = [0, 18, 23, 30, 40, agg_df["AGE"].max()]
mylabels = ['0_18', '19_23', '24_30', '31_40', '41_' + str(agg_df["AGE"].max())]
agg_df["age_cat"] = pd.cut(agg_df["AGE"], bins, labels=mylabels)


agg_df["customer_level_based"] = [row[0].upper() + "_" +
                                  row[1].upper() + "_" +
                                  row[2].upper() + "_" +
                                  str(row[5]).upper()
                                  for row in agg_df.values]

# New DataFrame's structure (Index = customer_level_based, dependent variable = PRICE)
agg_df = agg_df[["customer_level_based", "PRICE"]]
agg_df = agg_df[["customer_level_based","PRICE"]].groupby(["customer_level_based"]).agg("mean")


# Prıce segments
agg_df["SEGMENT"] = pd.qcut(agg_df["PRICE"], 4, labels=["D","C","B","A"])
agg_df.groupby("SEGMENT").agg({"PRICE": "mean"})
agg_df = agg_df.reset_index()

# Predictions
new_user = "TUR_ANDROID_FEMALE_31_40"
agg_df[agg_df["customer_level_based"] == new_user]
new_user = "FR_IOS_FEMALE_31_40"
agg_df[agg_df["customer_level_based"] == new_user]

