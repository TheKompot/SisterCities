
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
    page = requests.get(link)

    soup = BeautifulSoup(page.content, 'html.parser')

    states = soup.find_all("h2", class_="section-heading")

    states_names = []
    for state in states:
        state = state.text[:-4]
        if state != 'References':
            states_names.append(state)
    
    for index,state in enumerate(states_names):
        result = soup.find_all("section", class_="mf-section-"+str(index+1))
        for section in result:
            towns = []
            for town in section.find_all('p'):
                town = remove_brackets(town.text.strip())
                data[town] = {}
                towns.append(town)
   
            for index2,list_sc in enumerate(section.find_all('ul')):

                try:
                    data[towns[index2]]['sister_city'] = []
                    data[towns[index2]]['country_of_sc'] = []
                except IndexError:
                    print(index2)
                    break
                
                for sc in list_sc.find_all('li'):
                    
                    l = list(map(remove_brackets,sc.text.strip().split(',')))
                    if len(l) == 1:
                        city = l[0]
                        country = "NaN"
                    else:
                        city = l[0]
                        country = l[-1]

                    data[towns[index2]]['sister_city'].append(city)
                    data[towns[index2]]['country_of_sc'].append(country)
                    data[towns[index2]]['country'] = state
    return data

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
                    print(index)
                    break
                
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
                         "https://en.m.wikipedia.org/wiki/List_of_sister_cities_in_New_England"
                         ]
    other_american_links = ["https://en.m.wikipedia.org/wiki/List_of_sister_cities_in_Arizona",
                            "https://en.m.wikipedia.org/wiki/List_of_sister_cities_in_California",
                            "https://en.m.wikipedia.org/wiki/List_of_sister_cities_in_Colorado",
                            "https://en.m.wikipedia.org/wiki/List_of_sister_cities_in_Illinois",
                            "https://en.m.wikipedia.org/wiki/List_of_sister_cities_in_Michigan",
                            "https://en.m.wikipedia.org/wiki/List_of_sister_cities_in_New_York",
                            "https://en.m.wikipedia.org/wiki/List_of_sister_cities_in_North_Carolina",
                            "https://en.m.wikipedia.org/wiki/List_of_sister_cities_in_Ohio",
                            "https://en.m.wikipedia.org/wiki/List_of_sister_cities_in_Pennsylvania",
                            "https://en.m.wikipedia.org/wiki/List_of_sister_cities_in_Texas",
                            "https://en.m.wikipedia.org/wiki/List_of_sister_cities_in_Washington"
                            ]
    special_us_states_links = ["https://en.m.wikipedia.org/wiki/List_of_sister_cities_in_Maryland",
                               "https://en.m.wikipedia.org/wiki/List_of_sister_cities_in_Florida"]

    for link in links_for_regions:
        region = link
        while region.find('in_') != -1:
            region = region[region.find('in_')+3:]
        
        print(region)
        sc = sister_cities_for_regions(link)
        print()

        for town in sc:
            sc[town]['continent'] = region
            if region == 'New_England':
                sc[town]['country'] = 'the_United_States'
                sc[town]['continent'] = "North America"
        data.update(sc)

    for link, continent in links:
        country = link
        while country.find('in_') != -1:
            country = country[country.find('in_')+3:]

        if country in ["Kazakhstan", "the_United_Kingdom","the_Philippines","Thailand"]:
            continue # kazahstan does not have its own page, UK will be scrapped with regions
        
        print(country)
        sc = sister_cities(link)
        print()
        
        for town in sc:
            sc[town]['country'] = country
            sc[town]['continent'] = continent
        data.update(sc)

    for link in other_american_links:
        sc = sister_cities(link)
        for town in sc:
            sc[town]['country'] = 'the_United_States'
            sc[town]['continent'] = 'North America'
        data.update(sc)

    # Adding thailand
    data['Bangkok'] = {'sister_city':["Aichi Prefecture","Ankara","Astana","Beijing","Chaozhou","Chonqing",'Fukuoka Prefecture','Guangzhou','Hanoi','Ho Chi Minh City','Istanbul','Jakarta','Lausanne','Manila','Moscow','Penang Island','Phnom Penh','Saint Petersburg','Seoul','Shandong','Shanghai','Ulaanbaatar','Washington, D.C.','Wuhan'],
                    'country_of_sc':['Japan',"Turkey","Kazakhstan",'China','China','China','Japan','China','Vietnam','Vietnam','Turkey','Indonesia','Switzerland','Philippines','Russia','Malaysia','Cambodia','Russia','South Korea','China','China','Mongolia','United States','China'],
                    'country':'Thailand',
                    'continent':'Asia'}
    data['Chiang Rai'] = {'sister_city':["Union City"],
                        'country_of_sc':['United States'],
                        'country':'Thailand',
                        'continent':'Asia'}
    data['Udon Thani'] = {'sister_city':["Reno"],
                        'country_of_sc':['United States'],
                        'country':'Thailand',
                        'continent':'Asia'}


    print(data)