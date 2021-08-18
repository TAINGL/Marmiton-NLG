"""Save random url web of recipe page: Marmiton -> pickle file """

import time
import pickle
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException

# --open Marmiton site web with Chromedriver
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")
# chrome_options.add_argument('--headless')
driver = webdriver.Chrome(options=chrome_options)

driver.get('https://www.marmiton.org/')
driver.maximize_window()
time.sleep(3)

webpage_list = []
file_name = "webpage_list_pkl.pkl"

def get_random_recipe():
    """ Find Random Recipe Button """
    try:
        time.sleep(3)
        random_recipe = driver.find_element_by_link_text('Recette au hasard').click()
        print('random recipe option 1')
    except NoSuchElementException:
        try:
            time.sleep(1)
            random_recipe = driver.find_element_by_class_name('NavBarstyle__ItemLink-gkm9mr-3 deaqEx').click()
            print('random recipe option 2')
        except NoSuchElementException:
            try:
                time.sleep(1)
                random_recipe = driver.find_element_by_xpath(
                    "//*[@id='header']/header/div[2]/nav/ul/li[5]/a").click()
                print('random recipe option 3')
            except NoSuchElementException:
                time.sleep(1)
                random_recipe = driver.find_element_by_xpath(
                    "//*[@id='header']/div/header/div[2]/nav/ul/li[5]/a").click()
                print('random recipe option 4')
    return random_recipe

def get_home_page():
    """Find Home Page Button """
    try:
        time.sleep(3)
        home_button = driver.find_element_by_xpath("//*[@id='header']/div/header/div[2]/div[1]/div[1]/a").click()
        print('home button option 1')
    except NoSuchElementException:
        try:
            time.sleep(1)
            home_button = driver.find_element_by_class_name('Headerstyle__BrandLogo-sc-11duill-7 jvWHLL').click()
            print('home button option 2')
        except NoSuchElementException:
            try:
                time.sleep(1)
                home_button = driver.find_element_by_xpath("//*[@id='header']/header/div[3]/div[1]/div[1]/a").click()
                print('home button option 3')
            except NoSuchElementException:
                time.sleep(1)
                home_button = driver.find_element_by_xpath("//*[@id='header']/header/div[2]/div[1]/div[1]/a").click()
                print('home button option 4')

    return home_button

page = 1

# --close pop-up cookies authorization Marmiton site web
cookies_button = driver.find_element_by_xpath('//*[@id="didomi-notice-agree-button"]').click()
time.sleep(3)

while page < 200000:
    # --Generate new recipe page
    try:
        random_recipe = get_random_recipe()
        print('ok random')
        # link_recipe = get_url_link
        # print(link_recipe)
        # print('ok link 1')
    except NoSuchElementException:
        #print('search homepage')
        home_button = get_home_page()
        print('find homepage')
        random_recipe = get_random_recipe()
        print('find recipe')
        # link_recipe = get_url_link
        # print(link_recipe)
        # print('ok link 2')

        # reload_button = driver.find_element_by_xpath('//*[@id="reload-button"]').click()

    # --Save url web of recipe page
    try:
        time.sleep(3)
        link_recipe = driver.find_element_by_xpath('//meta[@property="og:url"]').get_attribute('content')
        print(link_recipe)
    except StaleElementReferenceException:
        time.sleep(3)
        link_recipe = driver.find_element_by_xpath('/html/head/meta[12]').get_attribute('content')
        print(link_recipe)
    except NoSuchElementException:
        try:
            time.sleep(3)
            link_recipe = driver.find_element_by_xpath('/html/head/link[13]').get_attribute('href')
            print(link_recipe)
        except NoSuchElementException:
            print('No links found')

    # --Save url web in pickle file
    webpage_list.append(link_recipe)
    page += 1
    print(page)

    open_file = open(file_name, "wb")
    pickle.dump(webpage_list, open_file)
    open_file.close()
    print('list saved')