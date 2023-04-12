
# import required modules
from bs4 import BeautifulSoup
import requests
 

def links_from_mainpage() -> list:
    output_links = [] # [(link, continent)]
    # get URL
    page = requests.get("https://en.m.wikipedia.org/wiki/Lists_of_twin_towns_and_sister_cities")
    
    # scrape webpage
    soup = BeautifulSoup(page.content, 'html.parser')
    
    for i in range(6):
        section = soup.find_all("section", class_="mf-section-"+str(i+1))[0]
        links = section.find_all('a')
        continent = None
        for index,link in enumerate(links):
            if index == 0:
                continent = link.text.split()[-1]
                if continent == 'America': # find out if it is South or North America
                    continent = link.text.split()[-2:]
                    continent = ' '.join(continent)
                continue # first link in section is about the continent 
            link = link['href']
            link = "https://en.m.wikipedia.org" + link
            output_links.append((link,continent))

    return output_links[:-2] # last two links are from the "list of list" page and an arrow picture 

def remove_brackets(word:str) -> str:
    word = word.strip()

    if word.find('[') == -1:
        return word
    
    word = word[:word.find('[')]
    return word

def sister_cities_philippines() -> dict:
    pass

def sister_cities_for_regions(link:str) -> dict:
    data = {} # {city -> {sister_city -> [sister_cities], country_of_sc -> [country_of_sc]},
              #  country -> country}

def sister_cities(link:str) -> dict:
    data = {} # city -> {sister_city -> [sister_cities], country_of_sc -> [country_of_sc]}

    page = requests.get(link)

    soup = BeautifulSoup(page.content, 'html.parser')

    num = 1
    go_further = True

    while go_further:
        result = soup.find_all("section", class_="mf-section-"+str(num))

        go_further = False
        for section in result:
            towns = []
            for town in section.find_all('p'):
                town = remove_brackets(town.text.strip())
                data[town] = {}
                towns.append(town)
            
            for index,list_sc in enumerate(section.find_all('ul')):
                try:
                    data[towns[index]]['sister_city'] = []
                    data[towns[index]]['country_of_sc'] = []
                except IndexError:
                    print('error')
                    return {}

                for sc in list_sc.find_all('li'):
                    
                    l = list(map(remove_brackets,sc.text.strip().split(',')))
                    if len(l) == 1:
                        city = l[0]
                        country = "NaN"
                    else:
                        city = l[0]
                        country = l[-1]

                    data[towns[index]]['sister_city'].append(city)
                    data[towns[index]]['country_of_sc'].append(country)

            go_further = True
        
        num+=1
    return data
        

if __name__ == "__main__":
    data = {}
    links = links_from_mainpage()
    
    links_for_regions = ["https://en.m.wikipedia.org/wiki/List_of_twin_towns_and_sister_cities_in_Asia",
                         "https://en.m.wikipedia.org/wiki/List_of_twin_towns_and_sister_cities_in_Africa",
                         "https://en.m.wikipedia.org/wiki/List_of_twin_towns_and_sister_cities_in_Oceania",
                         "https://en.m.wikipedia.org/wiki/List_of_sister_cities_in_Europe",
                         "https://en.m.wikipedia.org/wiki/List_of_twin_towns_and_sister_cities_in_North_America",
                         "https://en.m.wikipedia.org/wiki/List_of_twin_towns_and_sister_cities_in_South_America",
                         "https://en.m.wikipedia.org/wiki/List_of_twin_towns_and_sister_cities_in_the_United_Kingdom",
                         ]

    for link, continent in links:
        country = link
        while country.find('in_') != -1:
            country = country[country.find('in_')+3:]

        if country in ["Kazakhstan", "the_United_Kingdom"]:
            continue # kazahstan does not have its own page, UK will be scrapped with regions

        if False:
            sc = sister_cities(link)
            sc['continent'] = continent
            sc['country'] =  country

        print(country)
        print(link)
        print()

        #data.update(sc)

#print(data)