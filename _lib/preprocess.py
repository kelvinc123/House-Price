import pandas as pd
import numpy as np
import re


def preprocess_missing(df):

    # drop NA for electrical variable
    df.loc[df["Electrical"].isna(), "Electrical"] = "SBrkr"


    # Missing Values (NaN)
    ## Garage
    df.loc[df["GarageYrBlt"].isna(),"GarageYrBlt"] = 0
    df.loc[df["GarageType"].isna(), ["GarageType", "GarageFinish", "GarageQual", "GarageCond"]] = "NA"

    ## Basement
    falacy_1 = (df["BsmtQual"].isna() == False) & (df["BsmtExposure"].isna())
    falacy_2 = (df["BsmtQual"].isna() == False) & (df["BsmtFinType2"].isna())
    df.loc[falacy_1, "BsmtExposure"] = "No"
    df.loc[falacy_2, "BsmtFinType2"] = "Unf"
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

    # Neighborhood value NAmes change to Names
    df.loc[df["Neighborhood"] == "NAmes", "Neighborhood"] = "Names"

    # BldgType value Duplex change to Duplx
    df.loc[df["BldgType"] == "Duplex", "BldgType"] = "Duplx"

    # Exterior2nd value Wd Sdng change to WdSdng
    df.loc[df["Exterior2nd"] == "Wd Sdng", "Exterior2nd"] = "WdSdng"

    # Exterior2nd value Brk Cmn change to BrkComm
    df.loc[df["Exterior2nd"] == "Brk Cmn", "Exterior2nd"] = "BrkComm"

    # Exterior2nd value Wd Shng change to WdShing
    df.loc[df["Exterior2nd"] == "Wd Shng", "Exterior2nd"] = "WdShing"

    # Exterior2nd value CmentBd change to CemntBd
    df.loc[df["Exterior2nd"] == "CmentBd", "Exterior2nd"] = "CemntBd"

    type_cols = ["category", "category", "float64", "int64", "category", "category", "category", "category",
    "category", "category", "category", "category", "category", "category", "category", "category",
    "category", "category", "int64", "int64", "category", "category", "category", "category",
    "category", "float64", "category", "category", "category", "category", "category", "category",
    "category", "float64", "category", "float64", "float64", "float64", "category", "category", "category",
    "category", "int64", "int64", "int64", "int64", "float64", "float64", "int64", "int64", "int64",
    "int64", "category", "int64", "category", "int64", "category", "category", "int64", "category",
    "float64", "float64", "category", "category", "category", "int64", "int64", "int64", "int64",
    "int64", "int64", "category", "category", "category", "int64", "int64", "int64", "category",
    "category", "int64"]

    type_cols = zip(df.columns, type_cols)


    for col, dtypee in type_cols:
#         print("Converting {} to {}\n".format(col, dtypee))
        df[col] = df[col].astype(dtypee)

    #df = df.drop([1299, 935, 186, 347, 1231, 1183, 692, 955])
    
    zero_var = ["WoodDeckSF", "ScreenPorch", "PoolArea", "OpenPorchSF", "MiscVal", "MasVnrArea",
            "LowQualFinSF", "GarageYrBlt", "GarageArea", "EnclosedPorch", "BsmtFinSF2",
            "BsmtFinSF1", "3SsnPorch", "2ndFlrSF"]
    
    for col in zero_var:
        df["has{}".format(col)] = df[col] == 0
    

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
    cats = re.compile("\s+([A-Za-z0-9.,&?]+)\s+")

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
                                match = re.search(cats, line)
                                list_cat.append(match.group(1))
                        else:
                            print(line, end = "")

    return list_cat
