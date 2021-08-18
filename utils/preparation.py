import pandas as pd
from sklearn.model_selection import train_test_split
import numpy as np
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer 
import re


#nltk.download("punkt")
#nltk.download("wordnet")

lemmatizer = WordNetLemmatizer()

data = pd.read_json('/Users/Johanna/Documents/SIMPLON DATA IA/TITRE PRO/PROJET CD/data/marmiton_ner.json') # This is the original file from unpacked recipe1m
recipes = data.T
recipes.drop(['total_times','hosts', 'yields','links'], axis=1, inplace=True)

recipes.drop(recipes[recipes.titles.map(lambda x: len(x)<4)].index, inplace=True)
recipes.drop(recipes[recipes.ingredients.map(lambda x: len(x)<2)].index, inplace=True)
recipes.drop(recipes[recipes.instructions.map(lambda x: len(x) < 2 or len(''.join(x)) < 30)].index, inplace=True)
recipes.drop(recipes[recipes.instructions.map(lambda x: re.search('(step|mix all)', ''.join(str(x)), re.IGNORECASE)!=None)].index, inplace=True)

recipes.reset_index(drop=True, inplace=True)

def df_to_plaintext_file(input_df, output_file):
    print("Writing to", output_file)
    with open(output_file, 'w') as f:
        for index, row in input_df.iterrows():
            if index%5000==0:
                print(index)
            titles = row.titles
            instructions = row.instructions_list
            ingredients = row.ingredients
            ner = row.NER
            res = "<RECIPE_START> <INPUT_START> " + " <NEXT_INPUT> ".join(ner) + " <INPUT_END> <INGR_START> " + \
            " <NEXT_INGR> ".join(ingredients) + " <INGR_END> <INSTR_START> " + \
            " <NEXT_INSTR> ".join(instructions) + " <INSTR_END> <TITLE_START> " + titles + " <TITLE_END> <RECIPE_END>"
            f.write("{}\n".format(res))

#train, test = train_test_split(df, test_size=0.05) #use 5% for test set
#train.reset_index(drop=True, inplace=True)
#test.reset_index(drop=True, inplace=True)
#df_to_plaintext_file(train, 'unsupervised_train.txt')
#df_to_plaintext_file(test, 'unsupervised_test.txt')
