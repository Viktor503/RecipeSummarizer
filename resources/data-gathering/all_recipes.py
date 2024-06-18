import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import requests
from bs4 import BeautifulSoup
import json

browser = webdriver.Chrome()


'''
https://www.allrecipes.com/recipes/17057/everyday-cooking/more-meal-ideas/5-ingredients/main-dishes/
https://www.allrecipes.com/recipes/15436/everyday-cooking/one-pot-meals/
https://www.allrecipes.com/recipes/1947/everyday-cooking/quick-and-easy/
https://www.allrecipes.com/recipes/455/everyday-cooking/more-meal-ideas/30-minute-meals/
https://www.allrecipes.com/recipes/94/soups-stews-and-chili/
https://www.allrecipes.com/recipes/16099/everyday-cooking/comfort-food/
https://www.allrecipes.com/recipes/80/main-dish/
https://www.allrecipes.com/recipes/22992/everyday-cooking/sheet-pan-dinners/
https://www.allrecipes.com/recipes/78/breakfast-and-brunch/
https://www.allrecipes.com/recipes/17561/lunch/
https://www.allrecipes.com/recipes/84/healthy-recipes/
https://www.allrecipes.com/recipes/76/appetizers-and-snacks/
https://www.allrecipes.com/recipes/96/salad/
https://www.allrecipes.com/recipes/81/side-dish/
https://www.allrecipes.com/recipes/16369/soups-stews-and-chili/soup/
https://www.allrecipes.com/recipes/156/bread/
https://www.allrecipes.com/recipes/77/drinks/
https://www.allrecipes.com/recipes/79/desserts/
'''


containers = [
    "https://www.allrecipes.com/recipes/728/world-cuisine/latin-american/mexican/",
    "https://www.allrecipes.com/recipes/723/world-cuisine/european/italian/",
    "https://www.allrecipes.com/recipes/695/world-cuisine/asian/chinese/",
    "https://www.allrecipes.com/recipes/233/world-cuisine/asian/indian/",
    "https://www.allrecipes.com/recipes/722/world-cuisine/european/german/",
    "https://www.allrecipes.com/recipes/731/world-cuisine/european/greek/",
    "https://www.allrecipes.com/recipes/696/world-cuisine/asian/filipino/",
    "https://www.allrecipes.com/recipes/699/world-cuisine/asian/japanese/",
    "https://www.allrecipes.com/recipes/23070/everyday-cooking/cookware-and-equipment/air-fryer/",
    "https://www.allrecipes.com/recipes/253/everyday-cooking/slow-cooker/",
    "https://www.allrecipes.com/recipes/88/bbq-grilling/",
    "https://www.allrecipes.com/recipes/17583/everyday-cooking/cookware-and-equipment/",
    "https://www.allrecipes.com/recipes/22882/everyday-cooking/instant-pot/",
]


for container in containers:
    print("*******************************")
    print("new container: ", container)
    print("*******************************")
    browser.get(container)
    time.sleep(1)

    

    body = browser.find_element('tag name', 'body')

    for i in range(30):
        body.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.01)

    divs = [browser.find_element(By.ID,"tax-sc__recirc-list_"+str(i)+"-0") for i in range(1,6)]
    urls = []
    for div in divs:
        urls += div.find_elements(By.TAG_NAME, "a")
    urls = [link.get_attribute("href") for link in urls]

    num = 1
    rows = []
    out = open('resources\data-gathering\data.json', 'a')
    for url in urls:
        data = requests.get(url).content
        soup = BeautifulSoup(data, 'html.parser')

        #remove all the unnecessary elements from the page
        for s in soup.select('script'):
            s.extract()
        for s in soup.select('style'):
            s.extract()
        for s in soup.select('head'):
            s.extract()
        for s in soup.select('footer'):
            s.extract()
        for s in soup.select('nav'):
            s.extract()
        for s in soup.select('header'):
            s.extract()
        for s in soup.select('img'):
            s.extract()
        for s in soup.select('svg'):
            s.extract()
        for s in soup.select('button'):
            s.extract()

        #extract the ingredients from the page
        ingredients = []
        inglist = soup.find("div", id="mm-recipes-structured-ingredients_1-0")

        if inglist == None:
            continue

        inglist2 = inglist.text.strip().split('\n')
        ingredients += [i for i in inglist2 if (i != '' and i != ' ')]

        #get the recipe instructions
        instructions = []
        c = 1
        instructionslist = soup.find("div", id="mm-recipes-steps__content_1-0")
        for f in instructionslist.find_all("figure"):
            f.extract()
        steps = instructionslist.find_all("p")
        for step in steps:
            instructions.append(str(c)+". "+step.text.strip())
            c += 1
        
        ingredients = '\n'.join(ingredients)
        instructions = '\n\n'.join(instructions)
        answer = ingredients + '\n\n' + instructions


        #save text
        text = soup.get_text()
        while(text.find('\n') != -1):
            text = text.replace('\n', '\t')
        while(text.find('\t\t') != -1):
            text = text.replace('\t\t', '\t')
        
        with open('test.txt', 'w',encoding='utf-8') as f:
            f.write(text)

        row = {'text_input': text, 'output': answer}
        jsonrow = json.dumps(row,indent=4, sort_keys=True)
        rows.append(jsonrow)
        print()
        print(num)
        num+=1
        
        
    out.write(',\n')
    out.write(',\n'.join(rows))
    out.close()