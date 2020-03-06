import pandas as pd
import numpy as np
import re


def preprocess_missing(df):

    # drop NA for electrical variable
    df = df.loc[df["Electrical"].isna() == False,:]


    # Missing Values (NaN)
    ## Garage
    df.loc[df["GarageYrBlt"].isna(),"GarageYrBlt"] = 0
    df.loc[df["GarageType"].isna(), ["GarageType", "GarageFinish", "GarageQual", "GarageCond"]] = "NA"

    ## Basement
    falacy_1 = (df["BsmtQual"].isna() == False) & (df["BsmtExposure"].isna())
    falacy_2 = (df["BsmtQual"].isna() == False) & (df["BsmtFinType2"].isna())
    df = df.loc[(falacy_1 == False) & (falacy_2 == False), :] # remove NaN
    df.loc[df["BsmtQual"].isna(), ["BsmtQual", "BsmtCond", "BsmtExposure", "BsmtFinType1", "BsmtFinType2"]] = "NA"

    ## Other NA value's variable
    variable_na = ["Alley", "FireplaceQu", "PoolQC", "Fence", "MiscFeature"]
    for variab in variable_na:
        df.loc[df[variab].isna(),variab] = df.loc[df[variab].isna(),variab].fillna("NA")

    ## Last Part (Can change code here)
    df.loc[df["LotFrontage"].isna(), "LotFrontage"] = df["LotFrontage"].mean()
    df.loc[df["MasVnrArea"].isna(), "MasVnrArea"] = 0
    df.loc[df["MasVnrType"].isna(), "MasVnrType"] = "None"

    # MSZoning value C (all) change to C
    df.loc[df["MSZoning"] == "C (all)", "MSZoning"] = "C"
    
    # BldgType value Twnhs and 2fmCon change to TwnhsI and 2FmCon
    df.loc[df["BldgType"] == "Twnhs", "BldgType"] = "TwnhsI"
    df.loc[df["BldgType"] == "2fmCon", "BldgType"] = "2FmCon"
    
    # Exterior1st value Wd Sdng change to WdSdng
    df.loc[df["Exterior1st"] == "Wd Sdng", "Exterior1st"] = "WdSdng"

    type_cols = ["category", "category", "float64", "int64", "category", "category", "category", "category",  
    "category", "category", "category", "category", "category", "category", "category", "category",
    "category", "category", "int64", "int64", "category", "category", "category", "category",
    "category", "float64", "category", "category", "category", "category", "category", "category",
    "category", "int64", "category", "int64", "int64", "int64", "category", "category", "category",
    "category", "int64", "int64", "int64", "int64", "int64", "int64", "int64", "int64", "int64",
    "int64", "category", "int64", "category", "int64", "category", "category", "int64", "category",
    "int64", "int64", "category", "category", "category", "int64", "int64", "int64", "int64",
    "int64", "int64", "category", "category", "category", "int64", "int64", "int64", "category",
    "category", "int64"]
    
    type_cols = zip(df.columns, type_cols)


    for col, dtypee in type_cols:
        df[col] = df[col].astype(dtypee)
    
    

    return(df)

def get_instruction(label, output = True):
    df = pd.read_csv("_database/Input/train.csv")
    col_names = df.columns
    list_cat = []
    
    # input check
    if (not label in col_names) | (label == "SalePrice"):
        print("Error, column name not specified!")
        return 
    
    # specifying the next column name
    next_label = col_names[int([i+1 for i, val in enumerate(col_names) if val == label][0])]
    
    # compile using re
    label = re.compile("^{}:".format(label))
    next_label = re.compile("^{}:".format(next_label))
    cats = re.compile("\s+([A-Za-z0-9.,*&?$@^]+)\s+")

    # algorithm start
    with open("_database/Input/data_description.txt") as desc:
        finish = False
        while True:
            if finish:
                break
                
            line = desc.readline()

            if label.search(line):
                if output:
                    pass
                else:
                    print(line, end = "")
                

                while True:
                    line = desc.readline()
                    if next_label.search(line):
                        finish = True
                        break
                    elif line == "":
                        finish = True
                        break
                    else:
                        if output:
                            if cats.search(line):
#                                 print(line)
                                match = re.search(cats, line)
                                list_cat.append(match.group(1))
#                                 print(match.group(1))
                        else:
                            print(line, end = "")
                    
    return list_cat
