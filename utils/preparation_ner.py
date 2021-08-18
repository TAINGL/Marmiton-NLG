import pandas as pd
import re

start_with = ['pincées de','cuillère à café de','rouleau de','cuillères à soupe de',
              'cuillère de','tasses de','paquet de',
              'verres de', 'tranches de','pincées de','petits pots de','®','boîtes de','boules de','branches de',
              'sachets de','de dés de','tranches de','bottes de','filets de','jus de',
              'égouttées et coupées en rondelles','en boîte bien égoutté et grossièrement émietté',
              '(ou bleu pour un goût moins prononcé)','(1 mesure=1 verre)','prendre une forme adaptée',
              'demandez conseil à votre boulanger','par personne','cubes de','briquettes de',
              'sachet de', 'pots de','cuillère à soupe de ','demis de ',
              'demi verre de ','fraîche avec ses tiges ','cuillères de ',"cuillères à soupe d'"
              'ou ml ', 'de cm de long', 'grillées','bouquets de ','non épluchées', 
              "cubes d'",'cuillère à soupe de ', 'etc', 'praires', ' fumé au poivre',
              ' à volonté', 'italiennes douces','à de cacao',
              'grosse cuillère à soupe de ', 'cuillères à café de', 'boule de',
              'entière', 'surgelé', 'corsé', 'demis de ', 'pincée de sesel', 'froid', 
              "de à cm d'épaisseur", 'rosé','pour gâteau','effilées et grillées',
              'de table',' pour',"belle branche d'",'que vous hacherez très finement ou que vous écraserez',
              'sans la peau','moyennes épluchées et coupées en','coupées en morceaux cuites préalablement à la vapeur',
              'au moins','frais','mille fleurs',' ou plus',' de savoie','eau avec ','en grains',
              'de g','cuillères à café de ','corsé type sidi brahim ou vins du sud ouest français qui vont bien',
              'tasse de','coupé en dés','pour la garniture','boîte de ','barquette de ',' de soja goût vanille',
              "petite boîte d'", 'de préférence',
              "ou confits",'la déco','le plat','séchées',' au sirop',' bien mûrs',
              "de préférence","ou boîte d'abricots au sirop",
              'demi secs','dénoyautés','en boite','en sirop','moelleux','en morceaux',
              'mûrs','s secs','très mûrs','bien murs et dénoyautés','de provence','en conserve',
              'pas trop mûrs','en poudre',' alimentaire en poudre',' coupé en morceaux','au moins',
              'en moulin','belle tranche de ', 'belle','belles','barquettes de','barquette de',
              'kg de','ml de','cl de', 'g de', 'cl de','de gr',"g d'","cl d'", "l d'",'l de',"ml d'"]

and_start_with = ["g d'","cl d'", "l d'",' ®',
              '(ou bleu pour un goût moins prononcé)','(1 mesure=1 verre)','prendre une forme adaptée',
              'demandez conseil à votre boulanger',"ml d'"]
def clean_line(line):
    '''
    Args:
        line: a string, such as food name, sentences...
    '''
    assert type(line) == str
    
    # all lowercase
    line = line.lower()
    line = line.replace(' .', '.')
    line = line.replace(' !', '!')
    line = line.replace('*', '')
    line = line.replace('..', '.')
    line = line.replace(' - ', '')
    
    # only reserve number and alphabets
    line = re.sub(r'[^a-z0-9\u00C0-\u00FF+()/?!.,]', ' ', line)
    
    # replace things in brace
    line = re.sub(r'\([^)]*\)', '', line)
    
    # remove extra spaces
    line = re.sub(' +',' ',line).strip()
    return line
    
def clean_prefix(ingr):
    
    assert type(ingr) == str
    
    # all lowercase
    ingr = ingr.lower()
    ingr = ingr.replace(' .', '.')
    ingr = ingr.replace(' !', '!')
    ingr = ingr.replace('*', '')
    ingr = ingr.replace('..', '.')
    ingr = ingr.replace(' - ', '')
    
    # only reserve number and alphabets
    ingr = re.sub(r'[^a-z0-9\u00C0-\u00FF+()/?!.,]', ' ', ingr)
    
    # replace things in brace
    ingr = re.sub(r'\([^)]*\)', ' ', ingr)

    # strip
    ingr = re.sub(' +',' ',ingr).strip()

    # remove number
    #ingr = re.sub(r'\d+', '', ingr)
    
    ingr = re.sub(r'/', ' ', ingr)
    ingr = re.sub(r'[0-9]+', ' ', ingr)
    ingr = re.sub(r' d ', " d'", ingr)
    

    # remove period
    ingr = ingr.replace('.', '')

    # remove prefixes
    ingr = re.sub("kg d'",' ', ingr)
    
    for prefix in and_start_with:
        ingr = re.sub(prefix,' ', ingr)
    
    for prefix in start_with:
        ingr = re.sub(prefix+'\s',' ', ingr)
        ingr = re.sub('^\s'+prefix+'\s',' ', ingr)
        
    ingr = ingr.replace(')', '')
    # strip again
    ingr = re.sub(' +',' ',ingr).strip()

    return ingr

def preparation(path_csv, menu):
    ingredients_list = []

    df = pd.read_csv(path_csv)

    for i in range(len(df)):
        ingredients_str = clean_line(df['ingredients'][i])
        ingredients_split = list(ingredients_str.split(","))
        ingredients_list.append(ingredients_split)
    
    df.insert(0, 'id', range(1, 1 + len(df)))
    df['instructions'].dropna(how ='all', inplace = True)
    instructions_list = [i.split('\n') for i in df['instructions']]
    df['categorie'] = menu
    df['NER'] = df['ingredients'].apply(clean_prefix)

    for i in range(len(df)):
        df['NER'][i] = df['NER'][i].split(",")

    df = df.drop(["Unnamed: 0", "Unnamed: 0.1", 'ingredients','instructions'], axis=1)
    df.insert(loc=3, column='ingredients', value=pd.Series(ingredients_list)) # value = can be a list, a Series, an array or a scalar
    df.insert(loc=4, column='instructions', value=pd.Series(instructions_list)) # value = can be a list, a Series, an array or a scalar
    return df

# --Recettes apéritif ou buffet
aperitif_path = "/Users/Johanna/Documents/SIMPLON DATA IA/TITRE PRO/PROJET CD/data/df_aperitif.csv"
aperitif_categ = "aperitif"

# --Recettes entrée
entree_path= "/Users/Johanna/Documents/SIMPLON DATA IA/TITRE PRO/PROJET CD/data/df_entree.csv"
entree_categ = "entree"

# --Recettes plat principal
plat_path= "/Users/Johanna/Documents/SIMPLON DATA IA/TITRE PRO/PROJET CD/data/df_plat.csv"
plat_categ = "plat"

# --Recettes dessert
dessert_path= "/Users/Johanna/Documents/SIMPLON DATA IA/TITRE PRO/PROJET CD/data/df_dessert.csv"
dessert_categ = "dessert"

# --Recettes de boisson
boisson_path= "/Users/Johanna/Documents/SIMPLON DATA IA/TITRE PRO/PROJET CD/data/df_boisson.csv"
boisson_categ = "boisson"


#marmiton = preparation(boisson_path, boisson_categ)
#print(marmiton.head())
#print(marmiton['instructions'][0])
#print(len(marmiton['instructions'][0]))
#marmiton.to_csv('/Users/Johanna/Documents/SIMPLON DATA IA/TITRE PRO/PROJET CD/data/ner_boisson.csv',index=False)