"""Data processing -> from csv files """

import os, glob
import pandas as pd

# --Recettes apéritif ou buffet
aperitif_filename= "url_aperitif_*.csv"
df_aperitif_csv = "df_aperitif.csv"

# --Recettes entrée
entree_filename= "url_entree_*.csv"
df_entree_csv = "df_entree.csv"

# --Recettes plat principal
plat_filename= "url_plat_*.csv"
df_plat_csv = "df_plat.csv"

# --Recettes dessert
dessert_filename= "url_dessert_*.csv"
df_dessert_csv = "df_dessert.csv"

# --Recettes de boisson
boisson_filename= "url_boisson_*.csv"
df_boisson_csv = "df_boisson.csv"

def merge_csv(csv_filename, filename):
    """ Merge multiple CSV files """
    path = "/Users/ltaing/Documents/SIMPLON DATA IA/TITRE PRO/PROJET CD/data/"
    all_files = glob.glob(os.path.join(path, csv_filename))
    df_from_each_file = (pd.read_csv(f, sep=',') for f in all_files)
    df_merged = pd.concat(df_from_each_file, ignore_index=True)
    df_merged.to_csv(filename, index=False)
    return filename

def open_csv(filename):
    """ Open df and see shape (row, column)"""
    df = pd.read_csv(filename)
    print(df.head())
    print(df.shape)
    return df

def find_duplicate(df_list):
    """ Find a duplicate recipe"""
    # --Create a unique DataFrame object
    df_concat = pd.concat(df_list)
    df_concat.to_csv("df_allinfo.csv", index=False)

    print(df_concat.head())
    print("Complet dataframe:", df_concat.shape)

    # --Find a duplicate rows
    duplicateDFRow = df_concat[df_concat.duplicated(['titles'])]
    print(duplicateDFRow)
    print("Duplicate rows", duplicateDFRow)

    # --To remove duplicates on specific column(s)
    df = df_concat.drop_duplicates(subset=['titles'])
    df.to_csv("df_unique.csv", index=False)
    print(df.head())
    print("Complet dataframe without duplicates rows:", df.shape)
    return df

def delete_empty_row(df):
    """ Delete row where they are empty informations in columns """
    # --find rows with NaN values
    is_NaN = df.isnull()
    row_has_NaN = is_NaN.any(axis=1)
    rows_with_NaN = df[row_has_NaN]
    print(rows_with_NaN)

    # --drop empty rows
    # df = df.dropna(subset=["column2"], inplace=True)
    df = df.dropna()

    # Count NaN values under a single DataFrame column
    # print(df['ingredients'].isna().sum())
    # --Count NaN values under the entire DataFrame
    print(df.isnull().sum().sum())
    print(df.isna().sum().sum())
    return df

def full_recipe(df):
    df.to_json('marmiton.json', orient='index')  # 'records'


# --Merge all file and create df
# aperitif_merge_csv = merge_csv(aperitif_filename, df_aperitif_csv)
# df_aperitif = open_csv(df_aperitif_csv)

# entree_merge_csv = merge_csv(entree_filename, df_entree_csv)
# df_entree = open_csv(df_entree_csv)

# plat_merge_csv = merge_csv(plat_filename, df_plat_csv)
# df_plat = open_csv(df_plat_csv)

# dessert_merge_csv = merge_csv(dessert_filename, df_dessert_csv)
# df_dessert = open_csv(df_dessert_csv)

# boisson_merge_csv = merge_csv(boisson_filename, df_boisson_csv)
# df_boisson = open_csv(df_boisson_csv)

# df = pd.read_csv(df_aperitif_csv)
# print(df.head())

# df_list =[df_aperitif, df_entree, df_plat, df_dessert, df_boisson]
# df_concat, df = find_duplicate(df_list)
# print('done')

# df = open_csv("df_unique.csv")
# df = df.drop(["Unnamed: 0", "Unnamed: 0.1"], axis=1)
# df.to_csv("df_marmiton.csv", index=False)

df = open_csv("../dataset/marmiton/df_marmiton.csv")
# print(df.head())
print(df.columns)
# df = delete_empty_row(df)

# full_recipe(df)


