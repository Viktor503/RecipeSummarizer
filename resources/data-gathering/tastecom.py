import requests
from bs4 import BeautifulSoup
import json

'''
https://www.taste.com.au/quick-easy/galleries/top-100-easy-dinner-recipes/biccuul7?page=100
https://www.taste.com.au/galleries/15-minute-meals-quick-dinner-ideas-top-rated-our-members/dm1703x6?page=50
https://www.taste.com.au/quick-easy/galleries/most-recent-quick-easy-recipes-day/kj1r4Zny?page=98
https://www.taste.com.au/quick-easy/galleries/easy-chicken-recipes-dinner-few-ingredients/s1h72hl9?page=48
https://www.taste.com.au/healthy/galleries/50-healthy-winter-dinner-recipes-make-temperature-drops/mrh8thxk?page=50
https://www.taste.com.au/healthy/galleries/healthy-slices/n7zfnze0?page=29
https://www.taste.com.au/galleries/ultimate-baileys-recipes/pc4io73u?page=50
https://www.taste.com.au/galleries/best-best-top-100-recipes-2020/hc4z4vlh?page=105
https://www.taste.com.au/baking/galleries/top-100-easy-baking-recipes/7t2ouzx8?page=100
https://www.taste.com.au/galleries/australias-top-100-best-dinners-time/bq1nra2u?page=100
'''

data = requests.get('https://www.taste.com.au/galleries/australias-top-100-best-dinners-time/bq1nra2u?page=100').text
soup = BeautifulSoup(data, 'html.parser')

#select all the recipe links
urls = []

headers = soup.find_all('h1')
headers.pop(0)

for i in headers:
    urls.append("https://www.taste.com.au/"+i.find('a')['href'])
print(len(urls))

out = open('resources\data-gathering\data.json', 'a')
rows = []
counter = 1
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
    ingredients = ["Ingredients:"]
    elements = soup.find("div", class_="recipe-ingredients-section")
    for element in elements.find_all("li"):
        if('class' in element.attrs):
            if('section-heading' in element.attrs['class']):
                ingredients.append('\n'+element.text.strip())        
        else:
            ingredients.append(element.text.strip())

    #get the recipe instructions
    instructions = []
    num = 1
    elements = soup.find("ul", class_="recipe-method-steps")
    for element in elements.find_all("li"):
        instructions.append([str(num)+"."])
        for inst in element.find("div", class_="recipe-method-step-content"):
            if(inst.name != None):
                if(inst.name == 'span'):
                    try:
                        instructions[num-1].append(inst.find("span", class_="descriptor").text.strip())
                    except:
                        instructions[num-1].append(inst.text.strip())
            else:
                instructions[num-1].append(inst.text.strip())
            
        #instructions.append(element.find("div", class_="recipe-method-step-content").text.strip())
        num += 1
    instructions = [' '.join(i) for i in instructions]
    

    #create correct answer
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

    print(counter)
    counter += 1

out.write(',\n'.join(rows))
    