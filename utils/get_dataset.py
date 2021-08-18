"""Save all url web of recipe page: Marmiton -> pickle file """

import pickle
import requests
import pandas as pd
from bs4 import BeautifulSoup
from recipe_scrapers import scrape_me

import sys, threading
sys.setrecursionlimit(10**8)  # max depth of recursion
threading.stack_size(2**27)  # new thread will get stack of such size


# --Recettes apéritif ou buffet
url_aperitif = 'https://www.marmiton.org/recettes/index/categorie/aperitif-ou-buffet/{}?rcp=0'
p_max_url_aperitif = 83
list_url_aperitif = []
url_aperitif_pkl = "url_aperitif.pkl"
url_aperitif_csv = "url_aperitif.csv"

# --Recettes entrée
url_entree = 'https://www.marmiton.org/recettes/index/categorie/entree/{}?rcp=0'
p_max_url_entree = 183
list_url_entree = []
url_entree_pkl = "url_entree.pkl"
url_entree_csv = "url_entree.csv"

# --Recettes plat principal
url_plat = 'https://www.marmiton.org/recettes/index/categorie/plat-principal/{}?rcp=0'
p_max_url_plat = 562
list_url_plat = []
url_plat_pkl = "url_plat.pkl"
url_plat_csv = "url_plat.csv"

# --Recettes dessert
url_dessert = 'https://www.marmiton.org/recettes/index/categorie/dessert/{}?rcp=0'
p_max_url_dessert = 423
list_url_dessert = []
url_dessert_pkl = "url_dessert.pkl"
url_dessert_csv = "url_dessert.csv"

# --Recettes de boisson
url_boisson = 'https://www.marmiton.org/recettes?type=boisson&page={}'
p_max_url_boisson = 56
list_url_boisson = []
url_boisson_pkl = "url_boisson.pkl"
url_boisson_csv = "url_boisson.csv"

# --Info sur les recettes
titles = []
total_times = []
yields = []
ingredients = []
instructions = []
images = []
hosts = []
links = []
column_name = ['titles', 'total_times', 'yields', 'ingredients', 'instructions', 'images', 'hosts', 'links']

def get_url(path, p_max, list_url, file_name):
    """Save url web of recipe page: Marmiton -> pickle file """

    page = 1

    while page <= p_max:
        url = path.format(page)
        html_text = requests.get(url).text
        soup = BeautifulSoup(html_text, 'lxml')
        url = [link.get('href') for link in soup.find_all('a', {"class": "recipe-card-link"})]
        # print(url)
        list_url = list_url + url
        # print(list_url)
        page += 1
        print(page)

        # --Save url web in pickle file
        open_file = open(file_name, "wb")
        pickle.dump(list_url, open_file)
        open_file.close()
        print('list saved')

    return list_url

def open_url_list(path_url):
    """ Read pickle url list """
    pickle_file = open(path_url, "rb")
    url_list = pickle.load(pickle_file)
    pickle_file.close()
    print("Length url list is:", len(url_list))
    print(url_list)

    return url_list

def get_unique_value(url_list):
    """ Get unique value to list """
    mysetlist = set(url_list)
    mylist = list(mysetlist)
    print("Set list is:", mysetlist)
    return mylist

def slice_list(my_list, n = 100):
    """ Slice list to n list """
    mylist = [my_list[i:i + n] for i in range(0, len(my_list), n)]
    print("Sliced list is:", mylist)
    return mylist

def save_url_information(mylist):
    """ Save only correct_url to list """
    for url in mylist:
        scraper = scrape_me(url)
        title = scraper.title()
        total_time = scraper.total_time()
        serving = scraper.yields()
        ingredient = scraper.ingredients()
        instruction = scraper.instructions()
        image = scraper.image()
        host = scraper.host()
        link = scraper.links()

        titles.append(title)
        total_times.append(total_time)
        yields.append(serving)
        ingredients.append(ingredient)
        instructions.append(instruction)
        images.append(image)
        hosts.append(host)
        links.append(link)

    information_list = [titles, total_times, yields, ingredients, instructions, images, hosts, links]
    return information_list

def create_dataframe(information_list, column_name, filenames):
    """ Create df and save to csv file """
    zipbObj = zip(column_name, information_list)
    dictOfWords = dict(zipbObj)
    df = pd.DataFrame(dictOfWords)

    # --Save df to csv file
    print(df.head())
    print(df.shape)
    df.to_csv(filenames)
    return df

# --Get url from Marmiton
# url_aperitif = get_url(url_aperitif, p_max_url_aperitif, list_url_aperitif, url_aperitif_pkl)
# print(len(url_aperitif))
# url_entree = get_url(url_entree, p_max_url_entree, list_url_entree, url_entree_pkl)
# print(len(url_entree))
# url_plat = get_url(url_plat, p_max_url_plat, list_url_plat, url_plat_pkl)
# print(len(url_plat))
# url_dessert = get_url(url_dessert, p_max_url_dessert, list_url_dessert, url_dessert_pkl)
# print(len(url_dessert))
# url_boisson = get_url(url_boisson, p_max_url_boisson, list_url_boisson, url_boisson_pkl)
# print(len(url_boisson))
# print('done')

# --Get information from url pickle file
path_url = url_boisson_pkl
url_list = open_url_list(path_url)
mylist = get_unique_value(url_list)
# print("Length my_list is:", len(mylist))

only_https_url = []

# --Error with some specific url
for url in mylist:
    if not url.endswith('recette_blanquette-vegetarienne_391745.aspx') \
            and not url.endswith('/recettes/recette_veloute-de-topinambours_35389.aspx'):
        only_https_url.append(url)

# mylist = slice_list(mylist)
mylist = slice_list(only_https_url)
# print("Length mylist is:", len(mylist))
# print("mylist is:", mylist[0])
# print("Length mylist is:", len(mylist[0]))

# --Error with quota requests
for nList in range(len(mylist[0:10])):
    # print(nList)
    information_list = save_url_information(mylist[nList])
    df = create_dataframe(information_list, column_name, url_boisson_csv)
print('done')
