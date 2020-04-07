#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np

from _lib.preprocess import preprocess_missing as prep
from _lib.preprocess import get_instruction as info


def preprocess_missing(df):

    train_data = pd.read_csv("_database/Input/train.csv", index_col = 0)
    train = prep(train_data)
    test = prep(df)

    numcol = pd.read_csv("_database/numcol.csv")


    # MSZoning
    year = pd.DataFrame(test[test["MSZoning"].isna()]["YearBuilt"])
    df = train[["MSZoning", "YearBuilt"]]
    by_mszoning = df.groupby("MSZoning")
    mean_std = by_mszoning.apply(lambda x : (np.mean(x), np.std(x)))

    for idx in mean_std.index:
        year[idx] = np.abs((year["YearBuilt"] - mean_std[idx][0].values[0]) / mean_std[idx][1].values[0])

    year["MIN"] = year.columns[1:][np.argmin(year.drop("YearBuilt", axis = 1).values, axis = 1)].values
    test.loc[test["MSZoning"].isna(), "MSZoning"] = year["MIN"]

    # Bsmt
    bsmt_nan = test.columns[(test.loc[test["BsmtFinSF1"].isna(),].isna()).values[0]]
    test.loc[test["BsmtFinSF1"].isna(), bsmt_nan.values] = 0
    test.loc[test["BsmtCond"].isna(), "BsmtCond"] = "TA"
    test.loc[test["BsmtHalfBath"].isna(), ["BsmtHalfBath", "BsmtFullBath"]] = 0

    # Exterior
    test.loc[test["Exterior1st"].isna(), ["Exterior1st", "Exterior2nd"]] = "VinylSd"

    # Garage
    vals = ["NA", 0, "NA", 0, 0, "NA", "NA", 1, 1]
    col_gar = ["Garage" in col for col in test.columns]
    test.loc[test["GarageFinish"].isna(), col_gar] = vals

    # Other
    features_na = ["KitchenQual", "SaleType", "Utilities", "Functional"]
    for col in features_na:
        val = train[col].value_counts().index[0]
        test.loc[test[col].isna(), col] = val

    return(test)
