import requests
from bs4 import BeautifulSoup
import json

'''
https://streetkitchen.hu/category/vegetarianus-etelek/
https://streetkitchen.hu/category/instant/air-fryer-receptek/
https://streetkitchen.hu/category/instant/egytepsis-kajak/
https://streetkitchen.hu/category/instant/5-hozzavalos-kajak/
https://streetkitchen.hu/category/instant/egyszeru-levesek/
https://streetkitchen.hu/category/instant/egylabasos-egyserpenyos-kajak/
https://streetkitchen.hu/category/instant/tesztak/
https://streetkitchen.hu/category/instant/gyors-reggelik/
https://streetkitchen.hu/category/instant/konzervek-befottek/
https://streetkitchen.hu/category/instant/maradekmento-kajak/
https://streetkitchen.hu/category/instant/masnapos-kajak/
https://streetkitchen.hu/category/instant/mirelit-kajak/
https://streetkitchen.hu/category/instant/sutik/
https://streetkitchen.hu/category/instant/rizses-kajak/
https://streetkitchen.hu/category/instant/szendvicsek/
'''

data = requests.get('https://streetkitchen.hu/category/instant/szendvicsek/').text
soup = BeautifulSoup(data, 'html.parser')

#select all the recipe links
urls = []

for i in soup.select('a.article-link'):
    urls.append(i['href'])

f = open('streetkitchen.txt', 'w',encoding='utf-8')
out = open('resources\data-gathering\data.json', 'a')
rows = []
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
    elements = soup.find_all("div", class_="ingredient-group")
    ingredients = []
    for i in elements:
        a = i.text.strip().split('\n')
        b = a[0]
        for i in range(1,len(a)):
            if(a[i]==''):
                continue
            else:
                if(a[i-1]==''):
                    b += '\n'+a[i]
                else:
                    b += ' '+a[i]
        ingredients.append(b)

    #for some reason the ingredients are duplicated, so we only keep the first half
    ingredients = ingredients[0:len(ingredients)//2]

    #get the recipe instructions
    instructions = []
    content_div = soup.find("div", class_="the-content-div")
    
    formated = content_div.text.strip().split('\n')

    for i in range(len(formated)):
        if formated[i] != '':
            instructions.append(str(i+1)+". "+formated[i])
        else:
            break    
    
    #create correct answer
    ingredients = '\n\n'.join(ingredients)
    instructions = '\n\n'.join(instructions)
    answer = ingredients + '\n\n' + instructions

    print(answer)


    #save text
    text = soup.get_text()
    while(text.find('\n') != -1):
        text = text.replace('\n', '\t')
    while(text.find('\t\t') != -1):
        text = text.replace('\t\t', '\t')
    
    row = {'text_input': text, 'output': answer}
    jsonrow = json.dumps(row,indent=4, sort_keys=True)
    rows.append(jsonrow)

out.write(',\n'.join(rows))
    

