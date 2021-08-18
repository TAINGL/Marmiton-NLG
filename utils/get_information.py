"""Get information of recipe from url web -> df and csv files """

import os
import re
import pickle
import pandas as pd
from recipe_scrapers import scrape_me
import sys
sys.setrecursionlimit(10000)

path_url = "url_list.pkl"
titles = []
total_times = []
yields = []
ingredients = []
instructions = []
images = []
hosts = []
links = []
column_name = ['titles', 'total_times', 'yields', 'ingredients', 'instructions', 'images', 'hosts', 'links']

def merge_pickle_file(path_url_1, path_url_2):
    """ Merge two pickles files to one list """
    os.getcwd()
    os.chdir('data')
    cwd = os.getcwd()
    print(cwd)

    # --open pickle file
    url_list_1 = open_url_list(path_url_1)
    url_list_2 = open_url_list(path_url_2)

    # with open(path_url_1, 'rb') as f:
    #     url_list_1 = pickle.load(f)
    #     print(url_list_1)
    #     print(len(url_list_1))
    #
    # with open(path_url_2, 'rb') as f:
    #     url_list_2 = pickle.load(f)
    #     print(url_list_2)
    #     print(len(url_list_2))

    # --merge url list from pickle file
    webpage_list = []
    webpage_list = url_list_1 + url_list_2
    print("Length merged pickle list is:", len(webpage_list))

    open_file = open(path_url, "wb")
    pickle.dump(webpage_list, open_file)
    open_file.close()
    print('list saved')

    # --saving the dataframe
    df = pd.DataFrame(webpage_list)
    df.to_csv('url_list.csv')
    return webpage_list, df

def open_url_list(path_url):
    """ Read pickle url list """
    pickle_file = open(path_url, "rb")
    url_list = pickle.load(pickle_file)
    pickle_file.close()
    print("Length url list is:", len(url_list))
    print(url_list)

    return url_list

def rewrite_url(url_list):
    """ To write correctly all url link - Format : https://www.marmiton.org/recettes/[nameofrecipe] """
    rewrite_url = []
    for url in url_list:
        if not url.startswith("https:"):
            rewrite_url.append(url)
    return rewrite_url

def add_https(rewrite_url):
    """ Add https://www.marmiton.org for rewrite_url list """
    correct_url = []
    for url in rewrite_url:
        correct_url.append('https://www.marmiton.org'+url)
    return correct_url

def merge_url_list(correct_url, url_list):
    """ Create list with only correct_url """
    only_https_url = []

    for url in url_list:
        if url.startswith("https:"):
            only_https_url.append(url)
    # only_https_url = only_https_url + correct_url
    return only_https_url

def get_unique_value(only_https_url):
    """ Get unique value to list """
    mysetlist = set(only_https_url)
    my_list = list(mysetlist)
    print("Set list is:",mysetlist)
    return my_list

def slice_list(my_list, n = 100):
    """ Slice list to n list """
    mylist = [my_list[i:i + n] for i in range(0, len(my_list), n)]
    print("Sliced list is:", mylist)
    return mylist

def save_url_information(mylist):
    """ Save only correct_url to list """
    for url in mylist:
        try:
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

        except KeyError:
            titles.append(None)
            total_times.append(None)
            yields.append(None)
            ingredients.append(None)
            instructions.append(None)
            images.append(None)
            hosts.append(None)
            links.append(None)
            # print(f"{url} is not valid url")


    information_list = [titles, total_times, yields, ingredients, instructions, images, hosts, links]
    return information_list

def join_slide_list(mylist):
    """ Join info lis to one list """
    for nlist in mylist:
        # print("list 1", nlist)
        # for url in nlist:
            # print(url)
        information_list = save_url_information(nlist)

    # print("Information list is:",information_list)
    return information_list

def create_dataframe(information_list, column_name):
    """ Create df with only correct_url from two list """
    zipbObj = zip(column_name, information_list)
    dictOfWords = dict(zipbObj)
    df = pd.DataFrame(dictOfWords)
    return df

# path_url = 'webpage_list_pkl.pkl'

url_list = open_url_list(path_url)
rewrite_url = rewrite_url(url_list)
print("Length rewrite_url is:", len(rewrite_url))

correct_url = add_https(rewrite_url)
print("Length correct_url is:", len(correct_url))

only_https_url = merge_url_list(correct_url, url_list)
print("Length only_https_url is:", len(only_https_url))

mysetlist = get_unique_value(only_https_url)
print("Length mysetlist is:", len(mysetlist))

mylist = slice_list(mysetlist)
print("Length mylist is:", len(mylist))

information_list = join_slide_list(mylist)
print("Information_list is:",information_list)
print("Length information_list is:", len(information_list))

# --Save df to csv file
df = create_dataframe(information_list, column_name)
print(df.head())
print(df.shape)
df.to_csv('url_info.csv')